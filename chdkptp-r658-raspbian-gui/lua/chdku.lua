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

]]
--[[
lua helper functions for working with the chdk.* c api
]]

local chdku={}
chdku.rlibs = require('rlibs')
chdku.sleep = sys.sleep -- to allow override
-- format a script message in a human readable way
function chdku.format_script_msg(msg)
	if msg.type == 'none' then
		return ''
	end
	local r=string.format("%d:%s:",msg.script_id,msg.type)
	-- for user messages, type is clear from value, strings quoted, others not
	if msg.type == 'user' or msg.type == 'return' then
		if msg.subtype == 'boolean' or msg.subtype == 'integer' or msg.subtype == 'nil' then
			r = r .. tostring(msg.value)
		elseif msg.subtype == 'string' then
			r = r .. string.format("'%s'",msg.value)
		else
			r = r .. msg.subtype .. ':' .. tostring(msg.value)
		end
	elseif msg.type == 'error' then
		r = r .. msg.subtype .. ':' .. tostring(msg.value)
	end
	return r
end

--[[
Camera timestamps are in seconds since Jan 1, 1970 in current camera time
PC timestamps (linux, windows) are since Jan 1, 1970 UTC
return offset of current PC time from UTC time, in seconds
]]
function chdku.ts_get_offset()
	-- local timestamp, assumed to be seconds since unix epoch
	local tslocal=os.time()
	-- !*t returns a table of hours, minutes etc in UTC (without a timezone spec)
	-- the dst flag is overridden using the local value
	-- os.time turns this into a timestamp, treating as local time
	local ttmp = os.date('!*t',tslocal)
	ttmp.isdst  = os.date('*t',tslocal).isdst
	return tslocal - os.time(ttmp)
end

--[[
covert a timestamp from the camera to the equivalent local time on the pc
]]
function chdku.ts_cam2pc(tscam)
	local tspc = tscam - chdku.ts_get_offset()
	-- TODO
	-- on windows, a time < 0 causes os.date to return nil 
	-- these can appear from the cam if you set 0 with utime and have a negative utc offset
	-- since this is a bogus date anyway, just force it to zero to avoid runtime errors
	if tspc > 0 then
		return tspc
	end
	return 0
end

--[[
covert a timestamp from the pc to the equivalent on the camera
default to current time if none given
]]
function chdku.ts_pc2cam(tspc)
	if not tspc then
		tspc = os.time()
	end
	local tscam = tspc + chdku.ts_get_offset()
	-- TODO
	-- cameras handle < 0 times inconsistently (vxworks > 2100, dryos < 1970)
	if tscam > 0 then
		return tscam
	end
	return 0
end

--[[ 
connection methods, added to the connection object
]]
local con_methods = {}
--[[
check whether this cameras model and serial number match those given
assumes self.ptpdev is up to date
bool = con:match_ptp_info(match)
{
	model='model pattern'
	serial='serial number pattern'
	plain=bool -- plain text match
}
empty / false model or serial matches any
]]
function con_methods:match_ptp_info(match) 
	if match.model and not string.find(self.ptpdev.model,match.model,1,match.plain) then
		return false
	end
	-- older cams don't have serial
	local serial = ''
	if self.ptpdev.serial_number then
		serial = self.ptpdev.serial_number
	end
	if match.serial_number and not string.find(serial,match.serial_number,1,match.plain) then
		return false
	end
	return true
end

--[[
check if connection API is major and >= minor
todo might want to allow major >= in some cases
]]
function con_methods:is_ver_compatible(major,minor)
	-- API ver not initialized
	-- TODO maybe it should just be an error to call without connecting?
	if not self.apiver then
		return false
	end
	if self.apiver.MAJOR ~= major or self.apiver.MINOR < minor then
		return false
	end
	return true
end
--[[
return a list of remote directory contents
dirlist=con:listdir(path,opts)
path should be directory, without a trailing slash (except in the case of A/...)
opts may be a table, or a string containing lua code for a table
returns directory listing as table, throws on local or remote error
note may return an empty table if target is not a directory
]]
function con_methods:listdir(path,opts) 
	if type(opts) == 'table' then
		opts = serialize(opts)
	elseif type(opts) ~= 'string' and type(opts) ~= 'nil' then
		return false, "invalid options"
	end
	if opts then
		opts = ','..opts
	else
		opts = ''
	end
	local results={}
	local i=1
	local rstatus,err=self:execwait("return ls('"..path.."'"..opts..")",{
		libs='ls',
		msgs=chdku.msg_unbatcher(results),
	})
	if not rstatus then
		errlib.throw{etype='remote',msg=err}
	end

	return results
end

--[[
download using a table returned by find_files
]]
function con_methods:download_file_ff(finfo,dst,opts)
	local src=finfo.full

	-- TODO info_fn should be a msgf function that accepts verbosity
	if opts.verbose then
		opts.info_fn('%s->%s\n',src,dst)
	end

	local st=lfs.attributes(dst)

	if st then
		local skip
		if not opts.overwrite then
			skip=true
		elseif type(opts.overwrite) == 'function' then
			skip = not opts.overwrite(self,opts,finfo,st,src,dst)
		elseif opts.overwrite == true then
			skip = false
		else
			error("invalid overwrite option")
		end
		if skip then
			opts.info_fn("skip existing: %s\n",dst)
			return
		else
			opts.info_fn("overwrite: %s\n",dst)
		end
	end

	if opts.pretend then
		return
	end

	-- ensure parent exists
	fsutil.mkdir_parent(dst)

	-- ptp download fails on zero byte files (zero size data phase, possibly other problems)
	if finfo.st.size > 0 then
		self:download(src,dst)
	else
		local f,err=io.open(dst,"wb")
		if not f then
			error(err)
		end
		f:close()
	end
	if opts.mtime then
		status,err = lfs.touch(dst,chdku.ts_cam2pc(finfo.st.mtime));
		if not status then
			error(err)
		end
	end
end

--[[
download files and directories
con:mdownload(srcpaths,dstpath,opts)
opts:
	mtime=bool -- keep (default) or discard remote mtime NOTE files only for now
	overwrite=bool|function -- overwrite if existing found
	info_fn=function -- printf like function to receive status messages
	pretend=bool
	verbose=bool
other opts are passed to find_files
throws on error
]]
function con_methods:mdownload(srcpaths,dstpath,opts)
	if not dstpath then
		dstpath = '.'
	end
	local lopts=extend_table({
		mtime=true,
		overwrite=true,
		info_fn=util.printf,
		verbose=true,
	},opts)
	if lopts.pretend then
		lopts.verbose=true
	end
	local ropts=extend_table({},opts)
	ropts.dirsfirst=true
	-- unset options that don't apply to remote
	ropts.mtime=nil
	ropts.overwrite=nil
	local dstmode = lfs.attributes(dstpath,'mode')
	if dstmode and dstmode ~= 'directory' then
		errlib.throw{etype='bad_arg',msg='mdownload: dest must be a directory'}
	end
	local files={}
	if lopts.dbgmem then
		files._dbg_fn=chdku.msg_unbatcher_dbgstr
	end
	local rstatus,rerr = self:execwait('return ff_mdownload('..serialize(srcpaths)..','..serialize(ropts)..')',
										{libs={'ff_mdownload'},msgs=chdku.msg_unbatcher(files)})

	if not rstatus then
		errlib.throw{etype='remote',msg=rerr}
	end

	if #files == 0 then
		util.warnf("no matching files\n");
		return true
	end

	local mkdir=function(path)
		if lopts.verbose then
			lopts.info_fn('mkdir %s\n',tostring(path))
		end
		if not lopts.pretend then
			fsutil.mkdir_m(path)
		end
	end

	for i,finfo in ipairs(files) do
		local relpath
		local src,dst
		src = finfo.full
		if #finfo.path == 1 then
			relpath = finfo.name
		else
			if #finfo.path == 2 then
				relpath = finfo.path[2]
			else
				relpath = fsutil.joinpath(unpack(finfo.path,2))
			end
		end
		dst=fsutil.joinpath(dstpath,relpath)
		if finfo.st.is_dir then
			mkdir(dst)
		else
			self:download_file_ff(finfo,dst,lopts)
		end
	end
end

--[[
standard imglist varsubst
${serial,strfmt}  camera serial number, or '' if not available, default format %s
${pid,strfmt}     camera platform ID, default format %x
${ldate,datefmt}  PC clock date, os.date format, default %Y%m%d_%H%M%S
${lts,strfmt}     PC clock date as unix timestamp + microseconds, default format %f
${lms,strfmt}     PC clock milliseconds part, default format %03d
${mdate,datefmt}  Camera file modified date, converted to PC time, os.date format, default %Y%m%d_%H%M%S
${mts,strfmt}     Camera file modified date, as unix timestamp converted to PC time, default format %d
${name}           Image full name, like IMG_1234.JPG
${basename}       Image name without extension, like IMG_1234
${ext}            Image extension, like .JPG
${subdir}         Image DCIM subdirectory, like 100CANON or 100___01 or 100_0101
${imgnum}         Image number like 1234
${dirnum}         Image directory number like 101
${dirmonth}       Image DCIM subdirectory month, like 01, date folder naming cameras only
${dirday}         Image DCIM subdirectory day, like 01, date folder naming cameras only
]]

--[[
default subst func
]]
chdku.imglist_subst_funcs={
	serial=varsubst.format_state_val('serial','%s'),
	pid=varsubst.format_state_val('pid','%x'),
	ldate=varsubst.format_state_date('ldate','%Y%m%d_%H%M%S'),
	lts=varsubst.format_state_val('lts','%f'),
	lms=varsubst.format_state_val('lms','%03d'),
	mdate=varsubst.format_state_date('mdate','%Y%m%d_%H%M%S'),
	mts=varsubst.format_state_val('mts','%d'),
	name=varsubst.format_state_val('name','%s'),
	basename=varsubst.format_state_val('basename','%s'),
	ext=varsubst.format_state_val('ext','%s'),
	subdir=varsubst.format_state_val('subdir','%s'),
	imgnum=varsubst.format_state_val('imgnum','%s'),
	dirnum=varsubst.format_state_val('dirnum','%s'),
	dirmonth=varsubst.format_state_val('dirmonth','%s'),
	dirday=varsubst.format_state_val('dirday','%s'),
}

--[[
per connection state
]]
function con_methods:imglist_set_subst_con_state(state)
	if self.ptpdev.serial_number then
		state.serial = self.ptpdev.serial_number
	else
		state.serial = ''
	end
	state.pid=self.condev.product_id
end

--[[
local PC time related state
callers may want this to apply to an entire batch, or each file
]]
function chdku.imglist_set_subst_time_state(state)
	state.ldate = os.time() -- local time as a timestamp
	local t=ustime.new()
	state.lts = t:float() -- local unix timestamp + microseconds
	state.lms = t.usec/1000 -- ms only
end

--[[
per file state
]]
function chdku.imglist_set_subst_finfo_state(state,finfo)
	state.mdate = chdku.ts_cam2pc(finfo.st.mtime)
	state.mts = chdku.ts_cam2pc(finfo.st.mtime)
	state.name = finfo.name
	state.basename,state.ext = fsutil.split_ext(finfo.name)
	state.subdir = fsutil.basename_cam(fsutil.dirname_cam(finfo.full))
	state.imgnum = string.match(state.basename,'(%d%d%d%d)$')
	if not state.imgnum then
		state.imgnum = ''
	end
	-- 100CANON or 100_xxxx or 100___xx
	state.dirnum = string.match(state.subdir,'^(%d%d%d)')
	if not state.dirnum then
		state.dirnum = ''
	end

	-- try date folder, daily naming
	local dirmonth,dirday string.match(state.subdir,'_(%d%d)(%d%d)$')
	if dirmonth then
		state.dirmonth = dirmonth
		state.dirday = dirday
	else
		-- try date folder, monthly naming
		local dirmonth = string.match(state.subdir,'_(%d%d)$')
		if dirmonth then
			state.dirmonth = dirmonth
			state.dirday = ''
		else
			state.dirmonth = ''
			state.dirday = ''
		end
	end
end
--[[
names of option to pass to remote code
]]
chdku.imglist_remote_opts={
	'lastimg',
	'imgnum_min',
	'imgnum_max',
	'dirnum_min',
	'dirnum_max',
	'start_paths',
	'fmatch',
	'dmatch',
	'rmatch',
	'maxdepth',
	'batchsize',
	'dbgmem',
}
--[[
get a list of image files with ff_imglist
]]
function con_methods:imglist(opts)
	local ropts=util.extend_table({
		dirs=false,
		fmatch='%a%a%a_%d%d%d%d%.%w%w%w',
	},opts,{
		keys=chdku.imglist_remote_opts,
	})

	-- coerce numeric options to numbers
	for i,name in ipairs{'lastimg','imgnum_min','imgnum_max','dirnum_min','dirnum_max'} do
		if type(ropts[name]) == 'string' then
			ropts[name] = tonumber(ropts[name])
		end
	end

	local files={}

	if opts.dbgmem then
		files._dbg_fn=chdku.msg_unbatcher_dbgstr
	end

	local rstatus,rerr = self:execwait('return ff_imglist('..serialize(ropts)..')',
										{libs={'ff_imglist'},msgs=chdku.msg_unbatcher(files)})

	if not rstatus then
		errlib.throw{etype='remote',msg=rerr}
	end
	return files
end

--[[
download files returned by imglist, using varsubst to generate output names
]]
function con_methods:imglist_download(files,opts)
	opts=util.extend_table({
		dst='${subdir}/${name}',
		dstdir=false,
		mtime=true,
		info_fn=util.printf,
	},opts)
	if opts.pretend then
		opts.verbose = true
	end
	local subst=varsubst.new(chdku.imglist_subst_funcs)
	chdku.imglist_set_subst_time_state(subst.state)
	self:imglist_set_subst_con_state(subst.state)
	for i,finfo in ipairs(files) do
		chdku.imglist_set_subst_finfo_state(subst.state,finfo)
		local dst = subst:run(opts.dst)
		if opts.dstdir then
			dst=fsutil.joinpath(opts.dstdir,dst)
		end
		self:download_file_ff(finfo,dst,opts)
	end
end

--[[
delete files from imglist
]]
function con_methods:imglist_delete(files,opts)
	opts=util.extend_table({
		info_fn=util.printf,
	},opts)
	if opts.pretend then
		opts.verbose = true
	end
	for i,f in ipairs(files) do
		if opts.verbose then
			opts.info_fn('delete %s\n',f.full)
		end
		if not opts.pretend then
			-- TODO would be much faster to send a bunch of names over at once
			local status, err = self:remove(f.full)
			-- TODO maybe this should abort with error?
			if not status then
				util.warnf("failed %s\n",tostring(err))
			end
		end
	end
end

--[[
upload files and directories
status[,err]=con:mupload(srcpaths,dstpath,opts)
opts are as for find_files, plus
	pretend: just print what would be done
	mtime: preserve mtime of local files
]]
local function mupload_fn(self,opts)
	local con=opts.con
	if #self.rpath == 0 and self.cur.st.mode == 'directory' then
		return
	end
	if self.cur.name == '.' or self.cur.name == '..' then
		return
	end
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
	local dst=fsutil.joinpath_cam(opts.mu_dst,relpath)
	if self.cur.st.mode == 'directory' then
		if opts.pretend then
			printf('remote mkdir_m(%s)\n',dst)
		else
			local status,err=con:mkdir_m(dst)
			if not status then
				errlib.throw{etype='remote',msg=tostring(err)}
			end
		end
		opts.lastdir = dst
	else
		local dst_dir=fsutil.dirname_cam(dst)
		-- cache target directory so we don't have an extra stat call for every file in that dir
		if opts.lastdir ~= dst_dir then
			local st,err=con:stat(dst_dir)
			if st then
				if not st.is_dir then
					errlib.throw{etype='remote',msg='not a directory: '..tostring(dst_dir)}
				end
			else
				if opts.pretend then
					printf('remote mkdir_m(%s)\n',dst_dir)
				else
					local status,err=con:mkdir_m(dst_dir)
					if not status then
						errlib.throw{etype='remote',msg=tostring(err)}
					end
				end
			end
			opts.lastdir = dst_dir
		end
		-- TODO stat'ing in batches would be faster
		local st,err=con:stat(dst)
		if st and not st.is_file then
			errlib.throw{etype='remote',msg='not a file: '..tostring(dst)}
		end
		-- TODO timestamp comparison
		printf('%s->%s\n',src,dst)
		if not opts.pretend then
			con:upload(src,dst)
			if opts.mtime then
				-- TODO updating times in batches would be faster
				local status,err = con:utime(dst,chdku.ts_pc2cam(self.cur.st.modification))
				if not status then
					errlib.throw{etype='remote',msg=tostring(err)}
				end
			end
		end
	end
end

function con_methods:mupload(srcpaths,dstpath,opts)
	opts = util.extend_table({mtime=true},opts)
	opts.dirsfirst=true
	opts.mu_dst=dstpath
	opts.con=self
	fsutil.find_files(srcpaths,opts,mupload_fn)
end

--[[
delete files and directories
opts are as for find_files, plus
	pretend:only return file name and action, don't delete
	skip_topdirs: top level directories passed in paths will not be removed 
		e.g. mdelete({'A/FOO'},{skip_topdirs=true}) will delete everything in FOO, but not foo itself
	ignore_errors: ignore failed deletes
]]
function con_methods:mdelete(paths,opts)
	opts=extend_table({},opts)
	opts.dirsfirst=false -- delete directories only after recursing into
	local results
	local msg_handler
	if opts.msg_handler then
		msg_handler = opts.msg_handler
		opts.msg_handler = nil -- don't pass to remote
	else
		results={}
		msg_handler = chdku.msg_unbatcher(results)
	end
	local status,err = self:call_remote('ff_mdelete',{libs={'ff_mdelete'},msgs=msg_handler},paths,opts)

	if not status then
		errlib.throw{etype='remote',msg=tostring(err)}
	end
	if results then
		return results
	end
end

--[[
wrapper for remote functions, serialize args, combine remote and local error status 
func must be a string that evaluates to a function on the camera
returns remote function return values on success, throws on error
]]
function con_methods:call_remote(func,opts,...)
	local args = {...}
	local argstrs = {}
	-- preserve nils between values (not trailing ones but shouldn't matter in most cases)
	for i = 1,table.maxn(args) do
		argstrs[i] = serialize(args[i])
	end

	local code = "return "..func.."("..table.concat(argstrs,',')..")"
--	printf("%s\n",code)
	local results = {self:execwait(code,opts)}
	return unpack(results,1,table.maxn(results)) -- maxn expression preserves nils
end

function con_methods:stat(path)
	return self:call_remote('os.stat',nil,path)
end

function con_methods:utime(path,mtime,atime)
	return self:call_remote('os.utime',nil,path,mtime,atime)
end

function con_methods:mdkir(path)
	return self:call_remote('os.mkdir',nil,path)
end

function con_methods:remove(path)
	return self:call_remote('os.remove',nil,path)
end

function con_methods:mkdir_m(path)
	return self:call_remote('mkdir_m',{libs='mkdir_m'},path)
end

--[[
sort an array of stat+name by directory status, name
]]
function chdku.sortdir_stat(list)
	table.sort(list,function(a,b) 
			if a.is_dir and not b.is_dir then
				return true
			end
			if not a.is_dir and b.is_dir then
				return false
			end
			return a.name < b.name
		end)
end

--[[
read pending messages and return error from current script, if available
]]
function con_methods:get_error_msg()
	while true do
		local msg = self:read_msg()
		if msg.type == 'none' then
			return false
		end
		if msg.type == 'error' and msg.script_id == self:get_script_id() then
			return msg
		end
		util.warnf("chdku.get_error_msg: ignoring message %s\n",chdku.format_script_msg(msg))
	end
end

--[[
format a remote lua error from chdku.exec using line number information
]]
local function format_exec_error(libs,code,msg)
	local errmsg = msg.value
	local lnum=tonumber(string.match(errmsg,'^%s*:(%d+):'))
	if not lnum then
		print('no match '..errmsg)
		return errmsg
	end
	local l = 0
	local lprev, errlib, errlnum
	for i,lib in ipairs(libs.list) do
		lprev = l
		l = l + lib.lines + 1 -- TODO we add \n after each lib when building code
		if l >= lnum then
			errlib = lib
			errlnum = lnum - lprev
			break
		end
	end
	if errlib then
		return string.format("%s\nrlib %s:%d\n",errmsg,errlib.name,errlnum)
	else
		return string.format("%s\nuser code: %d\n",errmsg,lnum - l)
	end
end

--[[
read and discard all pending messages.
throws on error
]]
function con_methods:flushmsgs()
	repeat
		local msg=self:read_msg()
	until msg.type == 'none' 
end

--[[
read all pending messages, processing as specified by opts
opts {
	default=handler -- for all not matched by a specific handler
	user=handler
	return=handler
	error=handler
}
handler = table or function(msg,opts)
throws on error
returns true unless aborted by handler
handler function may abort by returning false or throwing
]]
function con_methods:read_all_msgs(opts)
	opts = util.extend_table({},opts)
	-- if an 'all' handler is given, use it for any that don't have a specific handler
	if opts.default then
		for i,mtype in ipairs({'user','return','error'}) do
			if not opts[mtype] then
				opts[mtype] = opts.default
			end
		end
	end
	while true do
		msg=self:read_msg()
		if msg.type == 'none' then
			break
		end
		local handler = opts[msg.type]
		if type(handler) == 'table' then
			table.insert(handler,msg)
		elseif type(handler) == 'function' then
			local status, err = handler(msg,opts)
			-- nil / no return value is NOT treated as an error
			if status == false then
				return false, err
			end
		elseif handler then -- nil or false = ignore
			error('invalid handler')
		end
	end
	return true
end

function chdku.msg_unbatcher_dbgstr(self,chunk) 
	if chunk._dbg then
		printf("dbg: %s\n",tostring(chunk._dbg))
	end
end
--[[
return a closure to be used with as a chdku.exec msgs function, which unbatches messages msg_batcher into t
]]
function chdku.msg_unbatcher(t)
	local i=1
	return function(msg)
		if msg.subtype ~= 'table' then
			errlib.throw{etype='wrongmsg_sub',msg='wrong message subtype: ' ..tostring(msg.subtype)}
		end
		local chunk,err=unserialize(msg.value)
		if err then
			errlib.throw{etype='unserialize',msg=tostring(err)}
		end
		for j,v in ipairs(chunk) do
			t[i]=v
			i=i+1
		end
		if type(t._dbg_fn) == 'function' then
			t:_dbg_fn(chunk)
		end
		return true
	end
end
--[[ 
wrapper for chdk.execlua, using optional code from rlibs
[remote results]=con:exec("code",opts)
opts {
	libs={"rlib name1","rlib name2"...} -- rlib code to be prepended to "code"
	wait=bool -- wait for script to complete, return values will be returned after status if true
	nodefaultlib=bool -- don't automatically include default rlibs
	clobber=bool -- if false, will check script-status and refuse to execute if script is already running
				-- clobbering is likely to result in crashes / memory leaks in chdk prior to 1.3
	flush_cam_msgs=bool -- if true (default) read and silently discard any pending messages from previous script before running script
					-- Prior to 1.3, ignored if clobber is true, since the running script could just spew messages indefinitely
	flush_host_msgs=bool -- Only supported in 1.3 and later, flush any message from the host unread by previous script
	-- below only apply if with wait
	msgs={table|callback} -- table or function to receive user script messages
	rets={table|callback} -- table or function to receive script return values, instead of returning them
	fdata={any lua value} -- data to be passed as second argument to callbacks
	initwait={ms|false} -- passed to wait_status, wait before first poll
	poll={ms} -- passed to wait_status, poll interval after ramp up
	pollstart={ms|false} -- passed to wait_status, initial poll interval, ramps up to poll
}
callbacks
	f(message,fdata)
	callbacks should throw an error to abort processing
	return value is ignored

returns
	if wait is set and rets is not, returns values returned by remote code
	otherwise returns nothing

throws on error
]]
-- use serialize by default
chdku.default_libs={
	'serialize_msgs',
}

-- script execute flags, for proto 2.6 and later
chdku.execflags={
	nokill=0x100,
	flush_cam_msgs=0x200,
	flush_host_msgs=0x400,
}

--[[
convenience, defaults wait=true
]]
function con_methods:execwait(code,opts_in)
	return self:exec(code,extend_table({wait=true,initwait=5},opts_in))
end

function con_methods:exec(code,opts_in)
	-- setup the options
	local opts = extend_table({flush_cam_msgs=true,flush_host_msgs=true},opts_in)
	local liblist={}
	-- add default libs, unless disabled
	-- TODO default libs should be per connection
	if not opts.nodefaultlib then
		extend_table(liblist,chdku.default_libs)
	end
	-- allow a single lib to be given as by name
	if type(opts.libs) == 'string' then
		liblist={opts.libs}
	else
		extend_table(liblist,opts.libs)
	end

	local execflags = 0
	-- in protocol 2.6 and later, handle kill and message flush in script exec call
	if self:is_ver_compatible(2,6) then
		if not opts.clobber then
			execflags = chdku.execflags.nokill
		end
		-- TODO this doesn't behave the same as flushmsgs in pre 2.6
		-- works whether or not clobber is set, flushes both inbound and outbound
		if opts.flush_cam_msgs then
			execflags = execflags + chdku.execflags.flush_cam_msgs
		end
		if opts.flush_host_msgs then
			execflags = execflags + chdku.execflags.flush_host_msgs
		end
	else
		-- check for already running script and flush messages
		if not opts.clobber then
			-- this requires an extra PTP round trip per exec call
			local status = self:script_status()
			if status.run then
				errlib.throw({etype='execlua_scriptrun',msg='a script is already running'})
			end
			if opts.flush_cam_msgs and status.msg then
				self:flushmsgs()
			end
		end
	end

	-- build the complete script from user code and rlibs
	local libs = chdku.rlibs:build(liblist)
	code = libs:code() .. code

	-- try to start the script
	-- catch errors so we can handle compile errors
	local status,err=self:execlua_pcall(code,execflags)
	if not status then
		-- syntax error, try to fetch the error message
		if err.etype == 'execlua_compile' then
			local msg = self:get_error_msg()
			if msg then
				-- add full details to message
				-- TODO could just add to a new field and let caller deal with it
				-- but would need lib code
				err.msg = format_exec_error(libs,code,msg)
			end
		end
		--  other unspecified error, or fetching syntax/compile error message failed
		error(err)
	end

	-- if not waiting, we're done
	if not opts.wait then
		return
	end

	-- to collect return values
	local results={}
	local i=1

	-- process messages and wait for script to end
	while true do
		status=self:wait_status{
			msg=true,
			run=false,
			initwait=opts.initwait,
			poll=opts.poll,
			pollstart=opts.pollstart
		}
		if status.msg then
			local msg=self:read_msg()
			if msg.script_id ~= self:get_script_id() then
				util.warnf("chdku.exec: message from unexpected script %d %s\n",msg.script_id,chdku.format_script_msg(msg))
			elseif msg.type == 'user' then
				if type(opts.msgs) == 'function' then
					opts.msgs(msg,opts.fdata)
				elseif type(opts.msgs) == 'table' then
					table.insert(opts.msgs,msg)
				else
					util.warnf("chdku.exec: unexpected user message %s\n",chdku.format_script_msg(msg))
				end
			elseif msg.type == 'return' then
				if type(opts.rets) == 'function' then
					opts.rets(msg,opts.fdata)
				elseif type(opts.rets) == 'table' then
					table.insert(opts.rets,msg)
				else
					-- if serialize_msgs is not selected, table return values will be strings
					if msg.subtype == 'table' and libs.map['serialize_msgs'] then
						results[i] = unserialize(msg.value)
					else
						results[i] = msg.value
					end
					i=i+1
				end
			elseif msg.type == 'error' then
				errlib.throw{etype='exec_runtime',msg=format_exec_error(libs,code,msg)}
			else
				errlib.throw({etype='wrongmsg',msg='unexpected msg type: '..tostring(msg.type)})
			end
		-- script is completed and all messages have been processed
		elseif status.run == false then
			-- returns were handled by callback or table
			if opts.rets then
				return
			else
				return unpack(results,1,table.maxn(results)) -- maxn expression preserves nils
			end
		end
	end
end

--[[
convenience method, get a message of a specific type
mtype=<string> - expected message type
msubtype=<string|nil> - expected subtype, or nil for any
munserialize=<bool> - unserialize and return the message value, only valid for user/return

returns
message|msg value
]]
function con_methods:read_msg_strict(opts)
	opts=extend_table({},opts)
	local msg=self:read_msg()
	if msg.type == 'none' then
		errlib.throw({etype='nomsg',msg='read_msg_strict no message'})
	end
	if msg.script_id ~= self:get_script_id() then
		errlib.throw({etype='bad_script_id',msg='msg from unexpected script id'})
	end
	if msg.type ~= opts.mtype then
		if msg.type == 'error' then
			errlib.throw({etype='wrongmsg_error',msg='unexpected error: '..msg.value})
		end
		errlib.throw({etype='wrongmsg',msg='unexpected msg type: '..tostring(msg.type)})
	end
	if opts.msubtype and msg.subtype ~= opts.msubtype then
		errlib.throw({etype='wrongmsg_sub',msg='wrong message subtype: ' ..msg.subtype})
	end
	if opts.munserialize then
		local v = util.unserialize(msg.value)
		if opts.msubtype and type(v) ~= opts.msubtype then
			errlib.throw({etype='unserialize',msg='unserialize error'})
		end
		return v
	end
	return msg
end
--[[
convenience method, wait for a single message and return it
throws if matching message is not available within timeout
opts passed wait_status, and read_msg_strict
]]
function con_methods:wait_msg(opts)
	opts=extend_table({},opts)
	opts.msg=true
	opts.run=nil
	local status=self:wait_status(opts)
	if status.timeout then
		errlib.throw({etype='timeout',msg='wait_msg timed out'})
	end
	if not status.msg then
		errlib.throw({etype='nomsg',msg='wait_msg no message'})
	end
	return self:read_msg_strict(opts)
end

-- bit number to ext + id mapping
chdku.remotecap_dtypes={
	[0]={
		ext='jpg',
		id=1,
-- actual limit isn't clear, sanity check so bad hook won't fill up disk
-- MAX_CHUNKS_FOR_JPEG is per session, dryos > r50 can have multiple sessions
		max_chunks=100, 
	},
	{ 
		ext='raw',
		id=2,
		max_chunks=1,
	},
	{ 
		ext='dng_hdr', -- header only
		id=4,
		max_chunks=1,
	},
}

--[[
return a handler that stores collected chunks into an array or using a function
]]
function chdku.rc_handler_store(store)
	return function(lcon,hdata) 
		local store_fn
		if not store then
			store_fn = hdata.store_return
		elseif type(store) == 'function' then
			store_fn = store
		elseif type(store) == 'table' then
			store_fn = function(val)
				table.insert(store,val)
			end
		else
			return false,'invalid store target'
		end
		local chunk
		local n_chunks = 0
		repeat
			local status,err
			cli.dbgmsg('rc chunk get %d %d\n',hdata.id,n_chunks)
			status,chunk=lcon:capture_get_chunk_pcall(hdata.id)	
			if not status then
				return false,chunk
			end
			cli.dbgmsg('rc chunk size:%d offset:%s last:%s\n',
						chunk.size,
						tostring(chunk.offset),
						tostring(chunk.last))

			chunk.imgnum = hdata.imgnum -- for convenience, store image number in chunk
			status,err = store_fn(chunk)
			if status==false then -- allow nil so simple functions don't need to return a value
				return false,err
			end
			n_chunks = n_chunks + 1
		until chunk.last or n_chunks > hdata.max_chunks
		if n_chunks > hdata.max_chunks then
			return false, 'exceeded max_chunks'
		end
		return true
	end
end

function chdku.rc_build_path(hdata,dir,filename,ext)
	if not filename then
		filename = string.format('IMG_%04d',hdata.imgnum)
	end

	if ext then
		filename = filename..'.'..ext
	else
		filename = filename..'.'..hdata.ext
	end

	if dir then
		filename = fsutil.joinpath(dir,filename)
	end
	return filename
end

function chdku.rc_process_dng(dng_info,raw)
	local hdr,err=dng.bind_header(dng_info.hdr)
	if not hdr then
		return false, err
	end
	-- TODO makes assumptions about header layout
	local ifd=hdr:get_ifd{0,0} -- assume main image is first subifd of first ifd
	if not ifd then 
		return false, 'ifd 0.0 not found'
	end
	local ifd0=hdr:get_ifd{0} -- assume thumb is first ifd
	if not ifd0 then 
		return false, 'ifd 0 not found'
	end

	raw.data:reverse_bytes()

	local bpp = ifd.byname.BitsPerSample:getel()
	local width = ifd.byname.ImageWidth:getel()
	local height = ifd.byname.ImageLength:getel()

	cli.dbgmsg('dng %dx%dx%d\n',width,height,bpp)
	
	-- values are assumed to be valid
	-- sub-image, pad
	if dng_info.lstart ~= 0 or dng_info.lcount ~= 0 then
		-- TODO assume a single strip with full data
		local fullraw = lbuf.new(ifd.byname.StripByteCounts:getel())
		local offset = (width * dng_info.lstart * bpp)/8;
		--local blacklevel = ifd.byname.BlackLevel:getel()
		-- filling with blacklevel would be nicer but max doesn't care about byte order
		fullraw:fill(string.char(0xff),0,offset) -- fill up to data
		-- copy 
		fullraw:fill(raw.data,offset,1)
		fullraw:fill(string.char(0xff),offset+raw.data:len()) -- fill remainder
		-- replace original data
		raw.data=fullraw
	end


	local twidth = ifd0.byname.ImageWidth:getel()
	local theight = ifd0.byname.ImageLength:getel()

	local status, err = pcall(hdr.set_data,hdr,raw.data)
	if not status then
		cli.dbgmsg('not creating thumb: %s\n',tostring(err))
		dng_info.thumb = lbuf.new(twidth*theight*3)
		return true -- thumb failure isn't fatal
	end
	if dng_info.badpix then
		cli.dbgmsg('patching badpixels: ')
		local bcount=hdr.img:patch_pixels(dng_info.badpix) -- TODO should use values from opcodes
		cli.dbgmsg('%d\n',bcount)
	end

	cli.dbgmsg('creating thumb: %dx%d\n',twidth,theight)
	-- TODO assumes header is set up for RGB uncompressed
	-- TODO could make a better / larger thumb than default and adjust entries
	dng_info.thumb = hdr.img:make_rgb_thumb(twidth,theight)
	return true
end
--[[
return a raw handler that will take a previously received dng header and build a DNG file
dng_info:
	lstart=<number> sub image start
	lcount=<number> sub image lines
	hdr=<lbuf> dng header lbuf

]]
function chdku.rc_handler_raw_dng_file(dir,filename_base,ext,dng_info)
	return function(lcon,hdata)
		local filename,err = chdku.rc_build_path(hdata,dir,filename_base,'dng')
		if not filename then
			return false, err
		end
		if not dng_info then
			return false, 'missing dng_info'
		end
		if not dng_info.hdr then
			return false, 'missing dng_hdr'
		end

		cli.dbgmsg('rc file %s %d\n',filename,hdata.id)
		
		local fh,err=io.open(filename,'wb')
		if not fh then
			return false, err
		end

		cli.dbgmsg('rc chunk get %s %d\n',filename,hdata.id)
		local status,raw=lcon:capture_get_chunk_pcall(hdata.id)	
		if not status then
			return false, raw
		end
		cli.dbgmsg('rc chunk size:%d offset:%s last:%s\n',
						raw.size,
						tostring(raw.offset),
						tostring(raw.last))
		dng_info.hdr:fwrite(fh)
		--fh:write(string.rep('\0',128*96*3)) -- TODO fake thumb
		local status, err = chdku.rc_process_dng(dng_info,raw)
		if status then
			dng_info.thumb:fwrite(fh)
			raw.data:fwrite(fh)
		end
		fh:close()
		return status,err
	end
end
--[[
return a handler function that just downloads the data to a file
TODO should stream to disk in C code like download
]]
function chdku.rc_handler_file(dir,filename_base,ext)
	return function(lcon,hdata)
		local filename,err = chdku.rc_build_path(hdata,dir,filename_base,ext)
		if not filename then
			return false, err
		end
		cli.dbgmsg('rc file %s %d\n',filename,hdata.id)
		
		local fh,err = io.open(filename,'wb')
		if not fh then
			return false, err
		end

		local chunk
		local n_chunks = 0
		-- note only jpeg has multiple chunks
		repeat
			cli.dbgmsg('rc chunk get %s %d %d\n',filename,hdata.id,n_chunks)
			local status
			status,chunk=lcon:capture_get_chunk_pcall(hdata.id)	
			if not status then
				fh:close()
				return false,chunk
			end
			cli.dbgmsg('rc chunk size:%d offset:%s last:%s\n',
						chunk.size,
						tostring(chunk.offset),
						tostring(chunk.last))

			if chunk.offset then
				fh:seek('set',chunk.offset)
			end
			if chunk.size ~= 0 then
				chunk.data:fwrite(fh)
			else
				-- TODO zero size chunk could be valid but doesn't appear to show up in normal operation
				util.warnf('ignoring zero size chunk\n')
			end
			n_chunks = n_chunks + 1
		until chunk.last or n_chunks > hdata.max_chunks
		fh:close()
		if n_chunks > hdata.max_chunks then
			return false, 'exceeded max_chunks'
		end
		return true
	end
end
function con_methods:capture_is_api_compatible()
	return self:is_ver_compatible(2,5)
end
--
--[[
fetch remote capture data
rets,errmsg=con:capture_get_data(opts)
opts:
	timeout, initwait, poll, pollstart -- passed to wait_status
	jpg=handler,
	raw=handler,
	dng_hdr=handler,
handler:
	f(lcon,handler_data)
handler_data:
	ext -- extension from remotecap dtypes
	id  -- data type number
	opts -- options passed to capture_get_data
	imgnum -- image number
	store_return() -- a function that can be used to store values for the return value of capture_get_data
rets
	true or array of store_return[bitnum][value] values on success
	throws on error
]]
function con_methods:capture_get_data(opts)
	opts=util.extend_table({
		timeout=20000,
	},opts)
	local wait_opts=util.extend_table({rsdata=true},opts,{keys={'timeout','initwait','poll','pollstart'}})

	local toget = {}
	local handlers = {}
	
	if not self:capture_is_api_compatible() then
		error("camera does not support remote capture")
	end


	-- TODO can probably combine these
	if opts.jpg then
		toget[0] = true
		handlers[0] = opts.jpg
	end
	if opts.raw then
		toget[1] = true
		handlers[1] = opts.raw
	end
	if opts.dng_hdr then
		toget[2] = true
		handlers[2] = opts.dng_hdr
	end

	-- table to return chunks (or other values) sent by hdata.store_return
	local rets = {}

	local done
	while not done do
		local status = con:wait_status(wait_opts)
		if status.timeout then
			error('timed out')
		end
		if status.rsdata == 0x10000000 then
			error('remote shoot error')
		end
		local avail = util.bit_unpack(status.rsdata)
		local n_toget = 0
		for i=0,2 do
			if avail[i] == 1 then
				if not toget[i] then
					-- TODO could have a nop handler
					error(string.format('unexpected type %d',i))
				end
				local hdata = util.extend_table({
					opts=opts,
					imgnum=status.rsimgnum,
					store_return=function(val)
						if rets[i] then
							table.insert(rets,val)
						else
							rets[i] = {val}
						end
					end,
				},chdku.remotecap_dtypes[i])

				local status, err = handlers[i](self,hdata)
				if not status then
					error(tostring(err))
				end
				toget[i] = nil
			end
			if toget[i] then
				n_toget = n_toget + 1
			end
		end
		if n_toget == 0 then
			done = true
		end
	end
	if #rets > 0 then
		return rets
	end
	return true
end
--[[
sleep until specified status is matched
status=con:wait_status(opts)
opts:
{
	-- msg/run bool values cause the function to return when the status matches the given value
	-- if not set, status of that item is ignored
	msg=bool
	run=bool
	rsdata=bool -- if true, return when remote capture data available, data in status.rsdata
	timeout=<number> -- timeout in ms
	timeout_error=bool -- if true, an error is thrown on timeout instead of returning it in status
	poll=<number> -- polling interval in ms
	pollstart=<number> -- if not false, start polling at pollstart, double interval each iteration until poll is reached
	initwait=<number> -- wait N ms before first poll. If this is long enough for call to finish, saves round trip
}
-- TODO should allow passing in a custom sleep in opts
status:
{
	msg:bool -- message status
	run:bool -- script status
	rsdata:number -- available remote capture data format
	rsimgnum:number -- remote capture image number
	timeout:bool -- true if timed out
}
rs values are only set if rsdata is requested in opts
throws on error
]]
function con_methods:wait_status(opts)
	opts = util.extend_table({
		poll=250,
		pollstart=4,
		timeout=86400000 -- 1 day
	},opts)
	local timeleft = opts.timeout
	local sleeptime
	if opts.poll < 50 then
		opts.poll = 50
	end
	if opts.pollstart then
		sleeptime = opts.pollstart
	else
		sleeptime = opts.poll
	end
	if opts.initwait then
		chdku.sleep(opts.initwait)
		timeleft = timeleft - opts.initwait
	end
	-- if waiting on remotecap state, make sure it's supported
	if opts.rsdata then
		if not self:capture_is_api_compatible() then
			error('camera does not support remote capture')
		end
		if type(self.capture_ready) ~= 'function' then
			error('client does not support remote capture')
		end
	end

	-- TODO timeout should be based on time, not adding up sleep times
	-- local t0=ustime.new()
	while true do
		-- TODO shouldn't poll script status if only waiting on rsdata
		local status = self:script_status()
		if opts.rsdata then
			local imgnum
			status.rsdata,imgnum = self:capture_ready()
			-- TODO may want to handle PTP_CHDK_CAPTURE_NOTSET differently
			if status.rsdata ~= 0 then
				status.rsimgnum = imgnum
				return status
			end
		end
		if status.run == opts.run or status.msg == opts.msg then
			return status
		end
		if timeleft > 0 then
			if opts.pollstart and sleeptime < opts.poll then
				sleeptime = sleeptime * 2
				if sleeptime > opts.poll then
					sleeptime = opts.poll
				end
			end
			if timeleft < sleeptime then
				sleeptime = timeleft
			end
			chdku.sleep(sleeptime)
			timeleft = timeleft - sleeptime
		else
			if opts.timeout_error then
				errlib.throw{etype='timeout',msg='timed out'}
			end
			status.timeout=true
			return status
		end
	end
end

--[[
set condev, ptpdev apiver for current connection
throws on error
if CHDK extension not present, apiver is set to -1,-1 but no error is thrown
]]
function con_methods:update_connection_info()
	-- this currently can't fail, devinfo is always stored in connection object
	self.condev=self:get_con_devinfo()
	self.ptpdev=self:get_ptp_devinfo()
	local status,major,minor=self:camera_api_version_pcall()
	if not status then
		local err = major
		-- device connected doesn't support PTP_OC_CHDK
		if err.ptp_rc == ptp.RC_OperationNotSupported then
			self.apiver={MAJOR=-1,MINOR=-1}
			return
		end
		error(err) -- re-throw
	end
	self.apiver={MAJOR=major,MINOR=minor}
end
--[[
override low level connect to gather some useful information that shouldn't change over life of connection
opts{
	raw:bool -- just call the low level connect (saves ~40ms)
}
]]
function con_methods:connect(opts)
	opts = util.extend_table({},opts)
	self.live = nil
	chdk_connection.connect(self._con)
	if opts.raw then
		return
	end
	self:update_connection_info()
end

--[[
attempt to reconnect to the device
opts{
	wait=<ms> -- amount of time to wait, default 2 sec to avoid probs with dev numbers changing
	strict=bool -- fail if model, pid or serial number changes
}
if strict is not set, reconnect to different device returns true, <message>
]]
function con_methods:reconnect(opts)
	opts=util.extend_table({
		wait=2000,
		strict=true,
	},opts)
	if self:is_connected() then
		self:disconnect()
	end
	local ptpdev = self.ptpdev
	local condev = self.condev
	-- appears to be needed to avoid device numbers changing (reset too soon ?)
	chdku.sleep(opts.wait)
	self:connect()
	if ptpdev.model ~= self.ptpdev.model
			or ptpdev.serial_number ~= self.ptpdev.serial_number
			or condev.product_id ~= self.condev.product_id then
		if opts.strict then
			self:disconnect()
			error('reconnected to a different device')
		else
			util.warnf('reconnected to a different device')
		end
	end
end

--[[
all assumed to be 32 bit signed ints for the moment
]]

chdku.live_fields={
	'version_major',
	'version_minor',
	'lcd_aspect_ratio',
	'palette_type',
	'palette_data_start',
	'vp_desc_start',
	'bm_desc_start',
}

chdku.live_fb_desc_fields={
	'fb_type',
	'data_start',
	'buffer_width',

	'visible_width',
	'visible_height',

	'margin_left',
	'margin_top',
	'margin_right',
	'margin_bot',
}

chdku.live_frame_map={}
chdku.live_fb_desc_map={}

--[[
init name->offset mapping
]]
local function live_init_maps()
	for i,name in ipairs(chdku.live_fields) do
		chdku.live_frame_map[name] = (i-1)*4
	end
	for i,name in ipairs(chdku.live_fb_desc_fields) do
		chdku.live_fb_desc_map[name] = (i-1)*4
	end
end
live_init_maps()

function chdku.live_get_frame_field(frame,field)
	if not frame then
		return nil
	end
	return frame:get_i32(chdku.live_frame_map[field])
end
local live_info_meta={
	__index=function(t,key)
		local frame = rawget(t,'_frame')
		if frame and chdku.live_frame_map[key] then
			return chdku.live_get_frame_field(frame,key)
		end
	end
}
local live_fb_desc_meta={
	__index=function(t,key)
		local frame = t._lv._frame
		if frame and chdku.live_fb_desc_map[key] then
			return frame:get_i32(t:offset()+chdku.live_fb_desc_map[key])
		end
	end
}

local live_fb_desc_methods={
	get_screen_width = function(self) 
		return self.margin_left + self.visible_width + self.margin_right;
	end,
	get_screen_height = function(self) 
		return self.margin_top + self.visible_height + self.margin_bot;
	end,
	offset = function(self) 
		return chdku.live_get_frame_field(self._lv._frame,self._offset_name)
	end,
}
function chdku.live_fb_desc_wrap(lv,fb_pfx)
	local t=util.extend_table({
		_offset_name = fb_pfx .. '_desc_start',
		_lv = lv,
	},live_fb_desc_methods);
	setmetatable(t,live_fb_desc_meta)
	return t
end

function chdku.live_wrap(frame)
	local t={_frame = frame}
	t.vp = chdku.live_fb_desc_wrap(t,'vp')
	t.bm = chdku.live_fb_desc_wrap(t,'bm')
	setmetatable(t,live_info_meta)
	return t
end


--[[
helper functions for live image dump
open file or pipe for pbm / pam dump
opts are from chdku.live_dump_*
TODO this isn't really live dump specific
]]
local function live_dump_img_open(opts)
	if opts.filehandle then
		return opts.filehandle
	end
	if not opts.filename then
		error('no filename or filehandle')
	end

	local fh, err
	if opts.pipe then
		fh,err = fsutil.popen(opts.filename,'wb')
		if opts.pipe_oneproc then
			opts.filehandle = fh
		end
	else
		-- ensure parent dir exists
		fsutil.mkdir_parent(opts.filename)
		fh, err = io.open(opts.filename,'wb')
	end
	if not fh then
		error(err)
	end
	return fh
end
local function live_dump_img_close(fh,opts)
	-- open was passed a handle, don't mess with it
	if opts.filehandle then
		return
	end
	fh:close()
end

--[[
write viewport data to an unscaled pbm image
frame: live view frame
opts:{
	filename=string -- filename or pipe command
	pipe=bool -- filename is a command to pipe to
	pipe_oneproc=bool -- start pipe process once and use for all subsequent writes,
						caller must close opts.filehandle when done
	filehandle=handle -- already open handle to write to, filename ignored
	lb=lbuf -- lbuf for image to re-use, created and set if not given
	pimg=pimg -- pimg to re-use, created if and set if not given
	skip=bool -- downsample image width 50% in X (faster, rough aspect correction for some cams)
}
]]
function chdku.live_dump_vp_pbm(frame,opts)
	opts.pimg = liveimg.get_viewport_pimg(opts.pimg,frame,opts.skip)
	-- TODO may be null if video selected on startup
	if not opts.pimg then
		error('no viewport data')
	end
	opts.lb = opts.pimg:to_lbuf_packed_rgb(opts.lb)
	local width = opts.pimg:width()
	if opts.skip then
		width = width/2
	end

	local fh = live_dump_img_open(opts)
	fh:write(string.format('P6\n%d\n%d\n%d\n',
		width,
		opts.pimg:height(),255))
	opts.lb:fwrite(fh)
	live_dump_img_close(fh,opts)
end
--[[
write viewport data to an unscaled RGBA pam image
opts as above
]]
function chdku.live_dump_bm_pam(frame,opts)
	opts.pimg = liveimg.get_bitmap_pimg(opts.pimg,frame,opts.skip)
	opts.lb = opts.pimg:to_lbuf_packed_rgba(opts.lb)

	local width = opts.pimg:width()
	if opts.skip then
		width = width/2
	end

	local fh = live_dump_img_open(opts)

	fh:write(string.format(
		'P7\nWIDTH %d\nHEIGHT %d\nDEPTH %d\nMAXVAL %d\nTUPLTYPE RGB_ALPHA\nENDHDR\n',
		width,
		opts.pimg:height(),
		4,255))
	opts.lb:fwrite(fh)
	live_dump_img_close(fh,opts)
end

--[[
NOTE this only tells if the CHDK protocol supports live view
the live sub-protocol might not be fully compatible
]]
function con_methods:live_is_api_compatible()
	return self:is_ver_compatible(2,3)
end

function con_methods:live_get_frame(what)
	if not self.live then
		self.live = chdku.live_wrap()
	end
	self.live._frame = self:get_live_data(self.live._frame,what)
	return true
end

function con_methods:live_dump_start(filename)
	if not self:is_connected() then
		return false,'not connected'
	end
	if not self:live_is_api_compatible() then
		return false,'api not compatible'
	end
	-- TODO
	if not self.live then
		self.live = chdku.live_wrap()
	end
	if not filename then
		filename = string.format('chdk_%x_%s.lvdump',tostring(con.condev.product_id),os.date('%Y%m%d_%H%M%S'))
	end
	--printf('recording to %s\n',dumpname)
	self.live.dump_fh = io.open(filename,"wb")
	if not self.live.dump_fh then
		return false, 'failed to open dumpfile'
	end

	-- used to write the size field of each frame
	self.live.dump_sz_buf = lbuf.new(4)

	-- header (magic, size of following data, version major, version minor)
	-- TODO this is ugly
	self.live.dump_fh:write('chlv') -- magic
	self.live.dump_sz_buf:set_u32(0,8) -- header size (version major, minor)
	self.live.dump_sz_buf:fwrite(self.live.dump_fh)
	self.live.dump_sz_buf:set_u32(0,1) -- version major
	self.live.dump_sz_buf:fwrite(self.live.dump_fh)
	self.live.dump_sz_buf:set_u32(0,0) -- version minor
	self.live.dump_sz_buf:fwrite(self.live.dump_fh)

	self.live.dump_size = 16;

	self.live.dump_fn = filename
	return true
end

function con_methods:live_dump_frame()
	if not self.live or not self.live.dump_fh then
		return false,'not initialized'
	end
	if not self.live._frame then
		return false,'no frame'
	end

	self.live.dump_sz_buf:set_u32(0,self.live._frame:len())
	self.live.dump_sz_buf:fwrite(self.live.dump_fh)
	self.live._frame:fwrite(self.live.dump_fh)
	self.live.dump_size = self.live.dump_size + self.live._frame:len() + 4
	return true
end

-- TODO should ensure this is automatically called when connection is closed, or re-connected
function con_methods:live_dump_end()
	if self.live.dump_fh then
		self.live.dump_fh:close()
		self.live.dump_fh=nil
	end
end

--[[
meta table for wrapped connection object
]]
local con_meta = {
	__index = function(t,key)
		return con_methods[key]
	end
}

--[[
proxy connection methods from low level object to chdku
]]
local function init_connection_methods()
	for name,func in pairs(chdk_connection) do
		if con_methods[name] == nil and type(func) == 'function' then
			con_methods[name] = function(self,...)
				return chdk_connection[name](self._con,...)
			end
			-- pcall variants for things that want to catch errors
			con_methods[name..'_pcall'] = function(self,...)
				return pcall(chdk_connection[name],self._con,...)
			end
		end
	end
end

init_connection_methods()

-- methods with pcall wrappers
-- generally stuff you would expect to want to examine the error rather than just throwing
-- or for direct use with cli:print_status
local con_pcall_methods={
	'connect',
	'exec',
	'execwait',
	'wait_status',
	'capture_get_data',
}
local function init_pcall_wrappers()
	for i,name in ipairs(con_pcall_methods) do
		if type(con_methods[name]) ~= 'function' then
			error('tried to wrap non-function '..tostring(name))
		end
		-- pcall variants for things that want to catch errors
		con_methods[name..'_pcall'] = function(self,...)
			return pcall(con_methods[name],self,...)
		end
	end
end
init_pcall_wrappers()

-- host api version
chdku.apiver = chdk.host_api_version()
-- host progam version
chdku.ver = chdk.program_version()

--[[
bool = chdku.match_device(devinfo,match)
attempt to find a device specified by the match table 
{
	bus='bus pattern'
	dev='device pattern'
	product_id = number
	plain = bool -- plain text match
}
empty / false dev or bus matches any
]]
function chdku.match_device(devinfo,match) 
--[[
	printf('try bus:%s (%s) dev:%s (%s) pid:%s (%s)\n',
		devinfo.bus, tostring(match.bus),
		devinfo.dev, tostring(match.dev),
		devinfo.product_id, tostring(match.product_id))
--]]
	if match.bus and not string.find(devinfo.bus,match.bus,1,match.plain) then
		return false
	end
	if match.dev and not string.find(devinfo.dev,match.dev,1,match.plain) then
		return false
	end
	return (match.product_id == nil or tonumber(match.product_id)==devinfo.product_id)
end
--[[
return a connection object wrapped with chdku methods
devspec is a table specifying the bus and device name to connect to
no checking is done on the existence of the device
if devspec is null, a dummy connection is returned

TODO this returns a *new* wrapper object, even
if one already exist for the underlying object
not clear if this is desirable, could cache a table of them
]]
function chdku.connection(devspec)
	local con = {}
	setmetatable(con,con_meta)
	con._con = chdk.connection(devspec)
	return con
end

return chdku
