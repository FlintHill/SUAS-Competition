--[[
 Copyright (C) 2010-2014 <reyalp (at) gmail dot com>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License version 2 as
  published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
--]]
--[[
CLI commands for manipulating DNG images
]]
-- store info for DNG cli commands, global for easy script access
local m = {
	--selected = current selected dng, or nil
	list={},
}
-- current batch information, empty if not in batch
local batch={
	--current -- current dng object
	--relpath
	--src
	--pretend
}

m.get_index = function(to_find)
	for i,d in ipairs(m.list) do
		if d == to_find then
			return i
		end
	end
	return nil
end

--[[
get dng for command, using numeric index or defaulting to selected or batch current
]]
m.get_sel_batch = function(index_arg)
	if index_arg ~= nil then
		return m.list[tonumber(index_arg)] -- nil if invalid
	end
	if batch.current then
		return batch.current
	end
	return m.selected
end
m.get_sel_nobatch = function(index_arg)
	if index_arg ~= nil then
		return m.list[tonumber(index_arg)] -- nil if invalid
	end
	return m.selected
end

--[[
prepare output path for a file write
opts: {
	over:bool  -- overwrite existing
	sfx:string -- suffix to replace .dng
	pretend:bool -- don't make any changes
}
]]
local function prepare_dst_path(d,name,opts)
	opts=util.extend_table({},opts)
	local sfx = opts.sfx
	if type(name) == 'string' then
		if lfs.attributes(name,'mode') == 'directory' then
			name = fsutil.joinpath(name,fsutil.basename(d.filename))
		else
			sfx = nil -- if name specified, don't mess with suffix
		end
	else
		if batch.odir then
			name = fsutil.joinpath(batch.odir,batch.relpath)
		else
			name = d.filename
		end
	end
	if sfx then
		name = fsutil.remove_sfx(name,'.dng') .. sfx
	end


	local m = lfs.attributes(name,'mode')
	if m == 'file' then
		if not opts.over then
			return false, 'file exists, use -over to overwrite '..tostring(name)
		end
	elseif m then -- TODO might want to allow
		return false, "can't overwrite non-file "..tostring(filename)
	else
		-- doesn't exist, might need to create dir
		if not opts.pretend then
			local dstdir = fsutil.dirname(name)
			fsutil.mkdir_m(dstdir)
		end
	end
	return name
end

local function do_dump_thumb(d,args)
	local ext
	if args.tfmt == 'ppm' then
		ext = '.ppm'
	elseif args.tfmt then
		return false, 'invalid thumbnail format requested: '..tostring(args.tfmt)
	else
		ext = '.rgb'
	end

	local filename,err = prepare_dst_path(d,args.thm,{sfx='_thm'..ext,over=args.over,pretend=args.pretend})
	if not filename then
		return false, err
	end
	if args.pretend then
		printf("dump thumb: %s\n",tostring(filename))
		return true
	end
	if not args.tfmt then
		d.main_ifd:write_image_data(filename)
	elseif args.tfmt == 'ppm' then
		-- TODO should check that it's actually an RGB8 thumb
		local fh, err = io.open(filename,'wb')
		if not fh then
			return false,err
		end
		fh:write(string.format('P6\n%d\n%d\n%d\n',
			d.main_ifd.byname.ImageWidth:getel(),
			d.main_ifd.byname.ImageLength:getel(),255))
		d.main_ifd:write_image_data(fh)
		fh:close()
	end
	return true
end

local function do_dump_raw(d,args)
	local ext='.raw'
	local bpp,endian
	local fmt='asis'

	if args.rfmt then
		bpp,endian,fmt=string.match(args.rfmt,'(%d+)([lb]?)(%a*)')
		bpp = tonumber(bpp)
		if endian == '' then
			endian = nil -- use dump_image defaults
		elseif endian == 'l' then
			endian = 'little'
		elseif endian == 'b' then
			endian = 'big'
		else
			return false, 'invalid endian: '..tostring(endian)
		end
		if fmt == 'pgm' then
			ext = '.pgm'
		elseif fmt ~= '' then
			return false, 'invalid format: '..tostring(fmt)
		end
	end

	local filename,err = prepare_dst_path(d,args.raw,{sfx=ext,over=args.over,pretend=args.pretend})
	if not filename then
		return false, err
	end
	if args.pretend then
		printf("dump raw: %s\n",tostring(filename))
		return true
	end
	if fmt == 'asis' then
		d.raw_ifd:write_image_data(filename)
	elseif fmt == 'pgm' then
		return d:dump_image(filename,{bpp=bpp,pgm=true,endian=endian})
	else
		return d:dump_image(filename,{bpp=bpp,endian=endian})
	end
end


local dngbatch_cmds=util.flag_table{
	'info',
	'mod',
	'dump',
	'save',
}

local function dngbatch_docmd(cmd,dargs)
	if dargs.pretend or dargs.verbose then
		printf('%s %s\n',cmd.name,cmd.argstr)
		if dargs.pretend then
			-- these commands pretend at a lower level to output path names etc
			if cmd.name == 'dngsave' or cmd.name == 'dngdump' then
				cmd.args.pretend = true
			else
				return true
			end
		end
	end
	
	-- TODO based on cli.execute
	local cstatus,status,msg = xpcall(
		function()
			return cli.names[cmd.name]:func(cmd.args)
		end,
		errutil.format)
	if not cstatus then
		return false,status
	end
	if not status and not msg then
		msg = cmd.name .. ' failed'
	end
	return status,msg
end

--[[
findfiles callback
]]
local function dngbatch_callback(self,opts)
	local dargs = opts.dngbatch_args
	local cmds = opts.dngbatch_cmds
	local relpath
	local src=self.cur.full
	if #self.cur.path == 1 then
		relpath = self.cur.name
	else
		if #self.cur.path == 2 then
			relpath = self.cur.path[2]
		else
			relpath = fsutil.joinpath(unpack(self.cur.path,2))
		end
	end
	printf("load: %s\n",src)
	local d,err
	if dargs.pretend then
		d = {filename=src} -- dummy for pretend
	else
		d,err = dng.load(src)
		-- TODO warn and continue?
		if not d then 
			errlib.throw{etype='dng',msg=tostring(err)}
		end
	end
	batch = {
		current = d,
		src = src,
		relpath = relpath,
		odir = dargs.odir,
		pretend = dargs.pretend,
	}
	local status
	for i,cmd in ipairs(cmds) do
		status,err = dngbatch_docmd(cmd,dargs)
		if not status then
			errlib.throw{etype='dngcmd',msg=tostring(err)}
		end
	end
	-- ensure all batch vars are nil
	batch = {}
end

local dngbatch_ap=cli.argparser.create{
	patch=false,
	fmatch=false,
	rmatch=false,
	maxdepth=1,
	pretend=false,
	verbose=false,
	odir=false,
	ext='dng'
}
--[[
TODO there should be a generic framework for this in cli
]]
local function dngbatch_cmd(self,args)
	local err
	-- split of dngbatch args from rest, delimited by {}
	-- TODO input additional lines until }
	local args,rest = string.match(args,'^([^{]*){%s*([^}]*)}$')
	if not args then
		return false, 'parse error, missing {}?'
	end

	args,err = dngbatch_ap:parse(args)
	if not args then
		return false,err
	end

	if #args == 0  then
		return false,'no files specified'
	end

	local cmds={}
	local errors={}

	local cmdstrs = util.string_split(rest,'%s*;%s*',{empty=false})
	if #cmdstrs == 0 then
		return false, 'at least one command is required'
	end

	for i,v in ipairs(cmdstrs) do
		local cmd,largs = string.match(v,'^%s*(%a+)%s*(.*)')
		if not cmd then
			table.insert(errors,string.format('%d: failed to parse %s',i,tostring(v)))
		elseif not dngbatch_cmds[cmd] then
			table.insert(errors,string.format('%d: invalid command %s',i,tostring(cmd)))
		else
			cmd = 'dng'..cmd
			-- parse command args first to minimize errors during batch
			-- collect errors to display all at once
			local pargs, err = cli.names[cmd].args:parse(largs)
			if pargs then
				table.insert(cmds,{name=cmd,args=pargs,argstr=largs}) -- argstr is only for information with -pretend
			else
				table.insert(errors,string.format('%d: %s error %s',i,tostring(cmd),tostring(err)))
			end
		end
	end
	if #errors > 0 then
		return false,'\n'..table.concat(errors,'\n')
	end
	local sfx
	if args.ext ~= '*' and args.ext ~= true then
		sfx = '.'..args.ext
	end
	local opts={
		dirs=false, -- pass only files to callback
		fmatch=args.fmatch,
		rmatch=args.rmatch,
		pretend=args.pretend,
		maxdepth=tonumber(args.maxdepth),
		dngbatch_args=args,
		dngbatch_cmds=cmds,
		fsfx=sfx,
	}
	fsutil.find_files({unpack(args)},opts,dngbatch_callback)
	return true
end

m.init_cli = function()
	cli:add_commands{
	{
		names={'dngload'},
		help='load a dng file',
		arghelp="[options] <file>",
		args=cli.argparser.create({
			nosel=false,
		}),
		-- TODO options to reload or select/ignore if same file already loaded
		help_detail=[[
 file: file to load
   only DNGs generated by CHDK or chdkptp are supported
 options
   -nosel  do not automatically select loaded file
]],
		func=function(self,args) 
			if not args[1] then
				return false,'expected filename'
			end
			local d,err = dng.load(args[1])
			if not d then 
				return false,err
			end
			if not args.nosel then
				m.selected = d
			end
			table.insert(m.list,d)
			return true,'loaded '..d.filename
		end,
	},
	{
		-- backup or prompt for overwrite?
		names={'dngsave'},
		help='save a dng file',
		arghelp="[options] [image num] [file]",
		args=cli.argparser.create({
			over=false,
			keepmtime=false,
		}),
		help_detail=[[
 file:       file or directory to write to
   defaults to loaded name. if directory, appends original filename
 options:
   -over     overwrite existing files
   -keepmtime preserve existing modification time
]],
		func=function(self,args) 
			local filename
			local narg
			-- TODO this will prevent you from saving a file named '1' without explicit image number
			if tonumber(args[1]) then
				narg = table.remove(args,1)
			end
			local d = m.get_sel_batch(narg)
			if not d then
				return false, 'no file selected'
			end

			local filename,err = prepare_dst_path(d,args[1],{over=args.over,pretend=args.pretend})
			if not filename then
				return false, err
			end
			if args.pretend then
				printf("save: %s\n",filename)
				return true
			end

			local mtime

			if args.keepmtime then
				-- new file will return nil
				mtime = lfs.attributes(filename,'modification')
			end

			local fh,err = io.open(filename,'wb')
			if not fh then
				return false, err
			end

			local status, err = d._lb:fwrite(fh)
			fh:close()
			if status then
				printf('wrote %s\n',filename)
				if mtime then
					lfs.touch(filename,mtime)
				end
				return true
			end
			return false, err
		end,
	},
	{
		-- TODO unload all option, collect garbage?
		names={'dngunload'},
		help='unload dng file',
		arghelp="[image num]",
		args=cli.argparser.create({}),
		func=function(self,args) 
			if #args > 0 then
				narg = table.remove(args,1)
			end
			local d = m.get_sel_nobatch(narg)
			if not d then
				return false, 'no file selected'
			end
			local di = m.get_index(d)
			table.remove(m.list,di)
			if d == m.selected then
				m.selected = nil
			end
			return true, 'unloaded '..tostring(d.filename)
		end,
	},
	{
		-- TODO file output, histogram, ifd values, individual ifd values
		names={'dnginfo'},
		help='display information about a dng',
		arghelp="[options] [image num]",
		args=cli.argparser.create({
			s=false,
			ifd=false,
			h=false,
			r=false,
			vals=0,
		}),
		help_detail=[[
 options:
   -s   summary info, default if no other options given
   -h   tiff header
   -ifd[=<ifd>]
   	 raw, exif, main, or 0, 0.0 etc. default 0
   -r   recurse into sub-ifds
   -vals[=N]
     display up to N values for each IFD entry, default 20
]],
		func=function(self,args) 
			local d = m.get_sel_batch(args[1])
			if not d then
				return false, 'no file selected'
			end
			if not args.h and not args.ifd then
				args.s = true
			end
			printf("%s:\n",d.filename)
			if args.s then
				d:print_summary()
			end
			if args.h then
				d:print_header()
			end
			if args.ifd then
				local ifd
				if args.ifd == true then
					ifd = d.main_ifd
				elseif args.ifd == 'raw' then
					ifd = d.raw_ifd
				elseif args.ifd == 'main' then
					ifd = d.main_ifd
				elseif args.ifd == 'exif' then
					ifd = d.exif_ifd
				else
					local path={}
					util.string_split(args.ifd,'.',{
						plain=true,
						func=function(v)
							local n=tonumber(v)
							if n then
								table.insert(path,n)
							else
								table.insert(path,v)
							end
						end
					})
					ifd = d:get_ifd(path)
				end
				if args.vals == true then
					args.vals = 20
				else
					args.vals = tonumber(args.vals)
				end
				if not ifd then
					return false, 'could not find ifd ',tostring(args.ifd)
				end
				d:print_ifd(ifd,{recurse=args.r,maxvals=args.vals})
			end
			return true
		end,
	},
	{
		names={'dnghist'},
		help='generate a histogram',
		arghelp="[options] [image num]",
		args=cli.argparser.create({
			min=false,
			max=false,
--			out=false,
			reg='active',
			fmt='count',
--			coords='abs',
			bin=1,
		}),
		-- TODO arbitrary rect
		-- text or netpbm file output
		--[[
  -out=<file> 
  	<file> is name of output file
	]]
		
		help_detail=[[
 options:
  -min=N   list pixels with value >= N
  -max=N   list pixels with value <= N
  -reg=<active|all>
  	region of image to search, either active area (default) or all
  -bin=<n>
    number of values in histogram bin
  -fmt=<count|%>
    format for output
]],
		func=function(self,args) 
			local d = m.get_sel_batch(args[1])
			if not d then
				return false, 'no file selected'
			end

			local ifd=d.raw_ifd

			local vmin = 0 
			local vmax = ifd.byname.WhiteLevel:getel()

			if args.min then
				vmin = tonumber(args.min)
			end
			if args.max then
				vmax = tonumber(args.max)
			end

			local top,left,bottom,right
			if args.reg == 'all' then
				top = 0
				left = 0
				bottom = ifd.byname.ImageLength:getel()
				right = ifd.byname.ImageWidth:getel()
			elseif args.reg == 'active' then
				top=ifd.byname.ActiveArea:getel(0)
				left=ifd.byname.ActiveArea:getel(1)
				bottom=ifd.byname.ActiveArea:getel(2)
				right=ifd.byname.ActiveArea:getel(3)
			else
				return false, 'invalid region'
			end

			if args.fmt ~= '%' and args.fmt ~= 'count' then
				return false, 'invalid format'
			end

			local h = d:build_histogram({top=top,left=left,bottom=bottom,right=right})
			local binsize = tonumber(args.bin)
			
			local fmt_range
			local fmt_count
			if args.fmt == '%' then
				fmt_count = function(count)
					return string.format('%f',(count / h.total) * 100)
				end
			else
				fmt_count = function(count)
					return tostring(count)
				end
			end
			if binsize == 1 then
				fmt_range = function(v1)
					return tostring(v1)
				end
			else
				fmt_range = function(v1,v2)
					return string.format('%d-%d',v1,v2)
				end
			end

			local outfn=function(count,v1,v2)
				printf("%s %s\n",fmt_range(v1,v2),fmt_count(count))
			end

			local v = vmin

			while v <= vmax do
				local count = 0
				for i=0,binsize - 1 do
					-- bin size may not evenly divide range
					if v+i <= vmax then
						count = count + h[v+i]
					end
				end
				outfn(count,v,v+binsize-1)
				v = v + binsize
			end
			return true
		end,
	},

	{
		names={'dnglistpixels'},
		help='generate a list of pixel coordinates',
		arghelp="[options] [image num]",
		args=cli.argparser.create({
			min=false,
			max=false,
			out=false,
			reg='active',
			coords='abs',
			fmt='chdk',
		}),
		-- TODO add default crop as region, badpixel.bin format
		help_detail=[[
 options:
  -min=N   list pixels with value >= N
  -max=N   list pixels with value <= N
  -out=<file> 
  	<file> is name of output file
  -fmt=<chdk|rt|dcraw|count>
  	format badpixel list for chdk badpixel.txt, raw therapee, dcraw, or just count them
  -reg=<active|all>
  	region of image to search, either active area (default) or all
  -coords=<abs|rel>
    output coordinates relative to region, or absolute
    use rel for raw therapee and dcraw
]],
		func=function(self,args) 
			local d = m.get_sel_batch(args[1])
			if not d then
				return false, 'no file selected'
			end
			local vmin = tonumber(args.min)
			local vmax = tonumber(args.max)
			if not vmin and not args.max then
				return false, 'must specify min or max'
			end

			local ifd=d.raw_ifd

			if not vmax then
				vmax = ifd.byname.WhiteLevel:getel()
			end
			if not vmin then
				vmin = 0
			end
			local top,left,bottom,right
			if args.reg == 'all' then
				top = 0
				left = 0
				bottom = ifd.byname.ImageLength:getel()
				right = ifd.byname.ImageWidth:getel()
			elseif args.reg == 'active' then
				top=ifd.byname.ActiveArea:getel(0)
				left=ifd.byname.ActiveArea:getel(1)
				bottom=ifd.byname.ActiveArea:getel(2)
				right=ifd.byname.ActiveArea:getel(3)
			else
				return false, 'invalid region'
			end

			local xoff = 0
			local yoff = 0
			if args.coords == 'rel' then
				xoff = left
				yoff = top
			elseif args.coords ~= 'abs' then
				return false, 'invalid coords'
			end
			local fmt
			if args.fmt == 'chdk' then
				fmtstr = '%d,%d\n'
			elseif args.fmt == 'rt' then
				fmtstr = '%d %d\n'
			elseif args.fmt == 'dcraw' then
				fmtstr = '%d %d 0\n' -- TODO final value can be timestamp for dcraw
			elseif args.fmt == 'count' then
				fmtstr = nil
			else
				return false, 'invalid format'
			end

			local fh
			local outfn
			if args.fmt == 'count' then
				outfn = function() end
			elseif args.out then
				local err
				fh,err = io.open(args.out,'wb')
				if not fh then return
					false, err
				end

				outfn = function(fmt,x,y)
					fh:write(string.format(fmt,x,y))
				end
			else
				outfn = printf
			end
			local total = 0
			for y = top, bottom-1 do
				for x = left, right-1 do
					local v = d.img:get_pixel(x,y)
					if v >= vmin and v <= vmax then
						outfn(fmtstr,x-xoff,y-yoff)
						total = total+1
					end
				end
			end
			printf("%d matching pixels\n",total)
			if fh then
				fh:close()
			end
			return true
		end,
	},
	{
		names={'dnglist'},
		help='list loaded dng files',
		func=function(self,args) 
			local r=''
			for i, d in ipairs(m.list) do
				if d == m.selected then
					r = r .. '*'
				else
					r = r .. ' '
				end
				r = r .. string.format('%-3d: %s\n',i,d.filename)
			end
			return true, r
		end,
	},
	{
		names={'dngsel'},
		help='select dng',
		arghelp="<number>",
		args=cli.argparser.create({
			ifds=false,
		}),
		help_detail=[[
 number:
   dng number from dnglist to select
]],
		func=function(self,args) 
			local n = tonumber(args[1])
			if m.list[n] then
				m.selected = m.list[n]
				return true, string.format('selected %d: %s',n,m.selected.filename)
			end
			return false, 'invalid selection'
		end,
	},
	{
		names={'dngmod'},
		help='modify dng',
		arghelp="[options] [files]",
		args=cli.argparser.create({
			patch=false,
			over=false,
		}),
		--TODO opcode based patch, other rawops
		help_detail=[[
 options:
   -patch[=n]   interpolate over pixels with value less than n (default 0)
]],
		func=function(self,args) 
			local d = m.get_sel_batch(args[1])
			if not d then
				return false, 'no file selected'
			end
			if args.patch then
				if args.patch == true then
					args.patch = 0
				else
					args.patch = tonumber(args.patch)
				end
				local count = d.img:patch_pixels(args.patch)
				printf('patched %d pixels\n',count)
			end
			return true
		end,
	},
	{
		names={'dngdump'},
		help='extract data from dng',
		arghelp="[options] [image num]",
		-- TODO scale options
		args=cli.argparser.create({
			thm=false,
			raw=false,
			rfmt=false,
			tfmt=false,
			over=false,
		}),
		help_detail=[[
 options:
   -thm[=name]   extract thumbnail to name, default dngname_thm.(rgb|ppm)
   -raw[=name]   extract raw data to name, default dngname.(raw|pgm)
   -over         overwrite existing file
   -rfmt=fmt raw format (default: unmodified from DNG)
     format is <bpp>[endian][pgm], e.g. 8pgm or 12l
	 pgm is only valid for 8 and 16 bpp
	 endian is l or b and defaults to little, except for 16 bit pgm
   -tfmt=fmt thumb format (default, unmodified rgb)
     ppm   8 bit rgb ppm
]],
		func=function(self,args) 
			local d = m.get_sel_batch(args[1])
			if not d then
				return false, 'no file selected'
			end
			if args.thm then
				local status, err = do_dump_thumb(d, args)
				if not status then
					return false, err
				end
			end
			if args.raw then
				local status, err = do_dump_raw(d, args)
				if not status then
					return false, err
				end
			end
			return true
		end,
	},
	{
		names={'dngbatch'},
		help='manipulate multiple files',
		arghelp="[options] [files] { command ; command ... }",
		-- TODO should allow filename substitutions for commands, e.g. dump -raw=$whatever
		help_detail=[[
 options:
   -odir             output directory, if no name specified in file commands
   -pretend          print actions instead of doing them
   -verbose[=n]      print detail about actions
 file selection
   -fmatch=<pattern> only file with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -maxdepth=n       only recurse into N levels of directory (default 1, only those specified in command)
   -ext=string       only files with specified extension, default dng, * for all. Not a pattern
 commands:
   mod dump save info listpixels
  take the same options as the corresponding standalone commands
  load and unload are implicitly called for each file
]],
		func=dngbatch_cmd,
	},
}
end

return m
