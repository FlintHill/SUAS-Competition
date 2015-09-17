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

local cli = {
	cmds={},
	names={},
	finished = false,
	source_level = 0, -- number of nested execfile calls
}
--[[
info printf - message to be printed at normal verbosity
]]
cli.infomsg = util.make_msgf( function() return prefs.cli_verbose end, 1)
cli.dbgmsg = util.make_msgf( function() return prefs.cli_verbose end, 2)

--[[
get command args of the form -a[=value] -bar[=value] .. [wordarg1] [wordarg2] [wordarg...]
--]]
local argparser = { }
cli.argparser = argparser

-- trim leading spaces
function argparser:trimspace(str)
	local s, e = string.find(str,'^[%c%s]*')
	return string.sub(str,e+1)
end
--[[
get a 'word' argument, either a sequence of non-white space characters, or a quoted string
inside " \ is treated as an escape character
return word, end position on success or false, error message
]]
function argparser:get_word(str)
	local result = ''
	local esc = false
	local qchar = false
	local pos = 1
	while pos <= string.len(str) do
		local c = string.sub(str,pos,pos)
		-- in escape, append next character unconditionally
		if esc then
			result = result .. c
			esc = false
		-- inside double quote, start escape and discard backslash
		elseif qchar == '"' and c == '\\' then
			esc = true
		-- character is the current quote char, close quote and discard
		elseif c == qchar then
			qchar = false
		-- not hit a space and not inside a quote, end
		elseif not qchar and string.match(c,"[%c%s]") then
			break
		-- hit a quote and not inside a quote, enter quote and discard
		elseif not qchar and c == '"' or c == "'" then
			qchar = c
		-- anything else, copy
		else
			result = result .. c
		end
		pos = pos + 1
	end
	if esc then
		return false,"unexpected \\"
	end
	if qchar then
		return false,"unclosed " .. qchar
	end
	return result,pos
end

function argparser:parse_words(str)
	local words={}
	str = self:trimspace(str)
	while string.len(str) > 0 do
		local w,pos = self:get_word(str)
		if not w then
			return false,pos -- pos is error string
		end
		table.insert(words,w)
		str = string.sub(str,pos)
		str = self:trimspace(str)
	end
	return words
end

--[[
parse a command string into switches and word arguments
switches are in the form -swname[=value]
word arguments are anything else
any portion of the string may be quoted with '' or ""
inside "", \ is treated as an escape
on success returns table with args as array elements and switches as named elements
on failure returns false, error
defs defines the valid switches and their default values. Can also define default values of numeric args
TODO enforce switch values, number of args, integrate with help
]]
function argparser:parse(str)
	-- default values
	local results=util.extend_table({},self.defs)
	local words,errmsg=self:parse_words(str)
	if not words then
		return false,errmsg
	end
	for i, w in ipairs(words) do
		-- look for -name
		local s,e,swname=string.find(w,'^-(%a[%w_-]*)')
		-- found a switch
		if s then		
			if type(self.defs[swname]) == 'nil' then
				return false,'unknown switch '..swname
			end
			local swval
			-- no value
			if e == string.len(w) then
				swval = true
			elseif string.sub(w,e+1,e+1) == '=' then
				-- note, may be empty string but that's ok
				swval = string.sub(w,e+2)
			else
				return false,"invalid switch value "..string.sub(w,e+1)
			end
			results[swname]=swval
		else
			table.insert(results,w)
		end
	end
	return results
end

-- a default for comands that want the raw string
argparser.nop = {
	parse =function(self,str)
		return str
	end
}

function argparser.create(defs)
	local r={ defs=defs }
	return util.mt_inherit(r,argparser)
end

cli.cmd_proto = {
	get_help = function(self)
		local namestr = self.names[1]
		if #self.names > 1 then
			namestr = namestr .. " (" .. self.names[2]
			for i=3,#self.names do
				namestr = namestr .. "," .. self.names[i]
			end
			namestr = namestr .. ")"
		end
		return string.format("%-12s %-12s: - %s\n",namestr,self.arghelp,self.help)
	end,
	get_help_detail = function(self)
		local msg=self:get_help()
		if self.help_detail then
			msg = msg..self.help_detail..'\n'
		end
		return msg
	end,
}

cli.cmd_meta = {
	__index = function(cmd, key)
		return cli.cmd_proto[key]
	end,
}

function cli:add_commands(cmds)
	for i = 1, #cmds do
		cmd = cmds[i]
		table.insert(self.cmds,cmd)
		if not cmd.arghelp then
			cmd.arghelp = ''
		end
		if not cmd.args then
			cmd.args = argparser.nop
		end
		for _,name in ipairs(cmd.names) do
			if self.names[name] then
				warnf("duplicate command name %s\n",name)
			else
				self.names[name] = cmd
			end
		end
		setmetatable(cmd,cli.cmd_meta)
	end
end

function cli:get_prompt()
	if con:is_connected() then
		local script_id = con:get_script_id()
		if script_id then
			return string.format("con %d> ",script_id)
		else
			return "con> "
		end
	else
		return "___> "
	end
end

function cli:prompt()
	printf("%s",self:get_prompt())
end

-- execute command given by a single line
-- returns status,message
-- message is an error message or printable value
function cli:execute(line)
	-- single char shortcuts
	local s,e,cmd = string.find(line,'^[%c%s]*([!.#=])[%c%s]*')
	if not cmd then
		s,e,cmd = string.find(line,'^[%c%s]*([%w_]+)[%c%s]*')
	end
	if s then
		local args = string.sub(line,e+1)
		if self.names[cmd] then
			local status,msg
			args,msg = self.names[cmd].args:parse(args)
			if not args then
				return false,msg
			end
			local cstatus
			local t0=ustime.new()
			con:reset_counters()
			if self.names[cmd].noxpcall then
				cstatus = true
				status,msg = self.names[cmd]:func(args)
			else
				cstatus,status,msg = xpcall(
					function()
						return self.names[cmd]:func(args)
					end,
					errutil.format)
			end
			local tdiff = ustime.diff(t0)/1000000;
			if prefs.cli_time then
				printf("time %.4f\n",tdiff)
			end
			if prefs.cli_xferstats then
				local xferstats = con:get_counters();
				local rbps,wbps
				if tdiff == 0 then
					rbps = "-"
					wbps = "-"
				else
					-- note these are based on total command execution time, not just transfer
					rbps = string.format("%d",xferstats.read/tdiff)
					wbps = string.format("%d",xferstats.write/tdiff)
				end
				printf("r %d %s/s w %d %s/s\n",xferstats.read,rbps,xferstats.write,wbps)
			end
			if not cstatus then
				return false,status
			end
			if not status and not msg then
				msg=cmd .. " failed"
			end
			return status,msg
		else 
			return false,string.format("unknown command '%s'\n",cmd)
		end
	elseif string.find(line,'[^%c%s]') then
		return false, string.format("bad input '%s'\n",line)
	end
	-- blank input is OK
	return true,""
end

function cli:execfile(filename) 
	if cli.source_level == prefs.cli_source_max then
		return false, 'too many nested source calls'
	end
	cli.source_level = cli.source_level + 1
	local fh, err = io.open(filename,'rb')
	if not fh then 
		return false, 'failed to open file: '..tostring(err)
	end
	-- empty file is OK
	local status = true
	local lnum = 1
	for line in fh:lines() do
		local msg
		status, msg = self:execute(line)
		self:print_status(status,msg)
		-- TODO pref to continue on errors
		if self.finished or not status then
			break
		end
		lnum = lnum + 1
	end
	fh:close()
	cli.source_level = cli.source_level - 1
	if not status then
		return false, string.format('error on line %d',lnum)
	end
	return true
end

function cli:print_status(status,msg) 
	if not status then
		errf("%s\n",tostring(msg))
	elseif msg then
		msg = tostring(msg) -- ensure error object is converted
		if string.len(msg) ~= 0 then
			printf("%s",msg)
			if string.sub(msg,-1,-1) ~= '\n' then
				printf("\n")
			end
		end
	end
	return status,msg
end

if readline then
	cli.readline = readline.line
	cli.add_history = readline.add_history
else
	function cli.readline(prompt)
		printf("%s",prompt)
		return io.read()
	end
-- noop
	function cli.add_history(line)
	end
end

function cli:run()
	while true do
		line = cli.readline(self:get_prompt())
		if not line then
			break
		end
		if line:len() > 0 then
			cli.add_history(line)
		end
		self:print_status(self:execute(line))
		if self.finished then
			break
		end
	end
end

-- update gui for cli commands
-- TODO should be a generic event system
function cli:connection_status_change()
	if gui then
		gui.update_connection_status()
	end
end

function cli:mode_change()
	if gui then
		gui.update_mode_list()
	end
end

--[[
process options common to shoot and remoteshoot
]]
function cli:get_shoot_common_opts(args)
	if not con:is_connected() then
		return false, 'not connected'
	end
	if not util.in_table({'s','a','96'},args.u) then
		return false,"invalid units"
	end
	if args.sv and args.svm then
		return false, "both sv and svm given"
	end
	local opts={}
	if args.u == 's' then
		if args.av then
			opts.av=exp.f_to_av96(args.av)
		end
		if args.sv then
			opts.sv=exp.iso_to_sv96(args.sv)
		end
		if args.svm then
			opts.svm=exp.iso_to_sv96(args.svm)
		end
		if args.tv then
			local n,d = string.match(args.tv,'^([%d]+)/([%d.]+)$')
			if n then
				n = tonumber(n)
				d = tonumber(d)
				if not n or not d or n == 0 or d == 0 then
					return false, 'invalid tv fraction'
				end
				opts.tv = exp.shutter_to_tv96(n/d)
			else
				n = tonumber(args.tv)
				if not n then
					return false, 'invalid tv value'
				end
				opts.tv = exp.shutter_to_tv96(n)
			end
		end
	elseif args.u == 'a' then
		if args.av then
			opts.av = util.round(args.av*96)
		end
		if args.sv then
			opts.sv = util.round(args.sv*96)
		end
		if args.svm then
			opts.svm = util.round(args.svm*96)
		end
		if args.tv then
			opts.tv = util.round(args.tv*96)
		end
	else
		if args.av then
			opts.av=tonumber(args.av)
		end
		if args.sv then
			opts.sv=tonumber(args.sv)
		end
		if args.svm then
			opts.svm=tonumber(args.svm)
		end
		if args.tv then
			opts.tv=tonumber(args.tv)
		end
	end
	if args.isomode then
		if opts.sv or opts.svm then
			return false,'set only one of sv, svm or isomode!'
		end
		opts.isomode = tonumber(args.isomode)
	end
	if args.nd then
		local val = ({['in']=1,out=2})[args.nd]
		if not val then
			return false,'invalid ND state '..tostring(args.nd)
		end
		opts.nd = val
	end
	if args.sd then
		local sd,units=string.match(args.sd,'(%d+)(%a*)')

		local convert={
			mm=1,
			cm=100,
			m=1000,
			ft=304.8,
			['in']=25.4,
		}
		if units == '' then
			units = 'm'
		end
		if not convert[units] then
			return false,string.format('invalid sd units %s',tostring(units))
		end
		opts.sd = util.round(sd*convert[units])
	end

	-- hack for CHDK override bug that ignores APEX 0
	-- only used for CHDK 1.1 (API 2.4 and earlier)
	if  opts.tv == 0 and not con:is_ver_compatible(2,5) then
		opts.tv = 1
	end
	return opts
end

--[[
return a single character status,formatted text listing for a single device specified by desc, or throw an error

]]
function cli.list_dev_single(desc)
	local lcon = chdku.connection(desc)
	local tempcon = false
	local con_status = "+"
	if not lcon:is_connected() then
		tempcon = true
		con_status = "-"
		lcon:connect()
	else
		-- existing con wrapped in new object won't have info set
		lcon.update_connection_info(lcon)
	end

	if con_status == '+' and lcon._con == con._con then
		con_status = "*"
	end

	local msg=string.format("%s b=%s d=%s v=0x%x p=0x%x s=%s",
									tostring(lcon.ptpdev.model),
									lcon.condev.bus, lcon.condev.dev,
									tostring(lcon.condev.vendor_id),
									tostring(lcon.condev.product_id),
									tostring(lcon.ptpdev.serial_number))
	if tempcon then
		lcon:disconnect()
	end
	return con_status,msg
end

--[[
helper function to setup lvdumpimg files
]]
function cli.init_lvdumpimg_file_opts(which,args,subst)
	local opts={}
	local pipeopt, ext, write_fn
	if which == 'vp' then
		pipeopt = 'pipevp'
		ext='ppm'
		write_fn = chdku.live_dump_vp_pbm
	elseif which == 'bm' then
		pipeopt = 'pipebm'
		ext='pam'
		write_fn = chdku.live_dump_bm_pam
	else
		errlib.throw{etype='bad_arg',msg='invalid type '..tostring(which)}
	end
	local filespec
	if args[which] == true then
		if args[pipeopt] then
			errlib.throw{etype='bad_arg',msg='must specify command with '..tostring(pipeopt)}
		end
		filespec = which..'_${time,%014.3f}.'..ext
	else
		filespec = args[which]
	end

	if args[pipeopt] then
		opts.pipe = true
		if args[pipeopt] == 'oneproc' then
			opts.pipe_oneproc = true
		end
	end

	opts.write = function(frame)
		if not args.nosubst then
			opts.filename = subst:run(filespec)
		else
			opts.filename = filespec
		end
		write_fn(frame,opts)
		if not args.quiet then
			if opts.pipe_oneproc then
				cli.infomsg('frame %d\n',subst.state.frame)
			else
				cli.infomsg('%s\n',opts.filename)
			end
		end
	end

	return opts
end

cli.download_overwrite_opts={
	n=false,
	y=true,
	old=function(lcon,lopts,finfo,st,src,dst)
		return chdku.ts_cam2pc(finfo.st.mtime) > st.modification
	end,
	ask=function(lcon,lopts,finfo,st,src,dst)
		while true do
			printf("existing: %s %d bytes modified %s\n",dst,st.size,os.date('%c',st.modification))
			printf("new: %s %d bytes modified %s\n",src,finfo.st.size,os.date('%c',chdku.ts_cam2pc(finfo.st.mtime)))
			local line = cli.readline('overwrite y / n / a (abort)? ')
			if line == 'y' then
				return true
			end
			if line == 'n' then
				return false
			end
			if line == 'a' then
				errlib.throw{etype='user_abort',msg='aborted by user'}
			end
		end
	end,
}

function cli.get_download_overwrite_opt(val)
	if type(val) == 'string' then
		local ow = cli.download_overwrite_opts[val]
		if ow == nil then
			errlib.throw{etype='bad_arg',msg='unrecognized overwrite option '..val}
		end
		return ow
	else
		errlib.throw{etype='bad_arg',msg='unrecognized overwrite option '..tostring(val)}
	end
end
-- TODO should have a system to split up command code
local rsint=require'rsint'
rsint.register_rlib()

cli:add_commands{
	{
		names={'help','h'},
		arghelp='[cmd]|[-v]',
		args=argparser.create{v=false},
		help='help on [cmd] or all commands',
		help_detail=[[
 help -v gives full help on all commands, otherwise as summary is printed
]],
		func=function(self,args) 
			cmd = args[1]
			if cmd and cli.names[cmd] then
				return true, cli.names[cmd]:get_help_detail()
			end
			if cmd then
				return false, string.format("unknown command '%s'\n",cmd)
			end
			msg = ""
			for i,c in ipairs(cli.cmds) do
				if args.v then
					msg = msg .. c:get_help_detail()
				else
					msg = msg .. c:get_help()
				end
			end
			return true, msg
		end,
	},
	{
		names={'#'},
		help='comment',
		func=function(self,args) 
			return true
		end,
	},
	{
		names={'exec','!'},
		help='execute local lua',
		arghelp='<lua code>',
		help_detail=[[
 Execute lua in chdkptp. 
 The global variable con accesses the current CLI connection.
 Return values are printed in the console.
]],
		func=function(self,args) 
			local f,r = loadstring(args)
			if not f then
				return false, string.format("compile failed:%s\n",r)
			end
			r={xpcall(f,errutil.format)} -- TODO would be nice to be able to force backtrace or not per call
			if not r[1] then 
				return false, string.format("call failed:%s\n",r[2])
			end
			local s
			local sopts={pretty=true,err_type=false,err_cycle=false,forceint=false,fix_bignum=false}
			if #r > 1 then
				s='=' .. serialize(r[2],sopts)
				for i = 3, #r do
					s = s .. ',' .. serialize(r[i],sopts)
				end
			end
			return true, s
		end,
	},
	{
		names={'set'},
		help='show or set option',
		arghelp='[-v|-c] [option[=value]]',
		args=argparser.create{
			v=false,
			c=false,
		},

		help_detail=[[
 Use set with no options to see a list
  -v show desciption when showing value
  -c output as set command
]],
		func=function(self,args) 
			local mode
			if args.v then
				mode='full'
			end
			if args.c then
				mode='cmd'
			end
			if #args == 0 then	
				local r={}
				for name,pref in prefs._each() do
					local status, desc = prefs._describe(name,mode)
					-- desc will be error if we somehow get invalid in here
					table.insert(r,desc)
				end
				return true,table.concat(r,'\n')
			end
			if #args > 1 then
				return false, 'unexpected args'
			end
			local name,value = string.match(args[1],'^([%a_][%w%a_]+)=(.*)$')
			if not name then
				return prefs._describe(args[1],mode)
			end
			return prefs._set(name,value)
		end,
	},
	{
		names={'quit','q'},
		help='quit program',
		func=function() 
			cli.finished = true
			return true
		end,
	},
	{
		names={'source'},
		help='execute cli commands from file',
		arghelp='<file>',
		args=argparser.create{ },
		func=function(self,args) 
			return cli:execfile(args[1])
		end,
	},
	{
		names={'lua','.'},
		help='execute remote lua',
		arghelp='<lua code>',
		help_detail=[[
 Execute Lua code on the camera.
 Returns immediately after the script is started.
 Return values or error messages can be retrieved with getm after the script is completed.
]],
		func=function(self,args) 
			con:exec(args)
			return true
		end,
	},
	{
		names={'getm'},
		help='get messages',
		func=function(self,args) 
			local msgs=''
			local msg,err
			while true do
				msg=con:read_msg()
				if msg.type == 'none' then
					return true,msgs
				end
				msgs = msgs .. chdku.format_script_msg(msg) .. "\n"
			end
		end,
	},
	{
		names={'putm'},
		help='send message',
		arghelp='<msg string>',
		func=function(self,args) 
			con:write_msg(args)
			return true
		end,
	},
	{
		names={'luar','='},
		help='execute remote lua, wait for result',
		arghelp='<lua code>',
		help_detail=[[
 Execute Lua code on the camera, waiting for the script to end.
 Return values or error messages are printed after the script completes.
]],
		func=function(self,args) 
			local rets={}
			local msgs={}
			con:execwait(args,{rets=rets,msgs=msgs})
			local r=''
			for i=1,#msgs do
				r=r .. chdku.format_script_msg(msgs[i]) .. '\n'
			end
			for i=1,table.maxn(rets) do
				r=r .. chdku.format_script_msg(rets[i]) .. '\n'
			end
			return true,r
		end,
	},
	{
		names={'killscript'},
		help='kill running remote script',
		args=argparser.create{
			noflush=false,
			force=false,
		},
		arghelp='[-noflush][-force][-nowait]',
		help_detail=[[
 Terminate any running script on the camera
   -noflush: don't discard script messages
   -force: force kill even if camera does not support (crash / memory leaks likely!)
]],
		func=function(self,args) 
			if not con:is_ver_compatible(2,6) then
				if not args.force then
					return false,'camera does not support clean kill, use -force if you are sure'
				end
				warnf("camera does not support clean kill, crashes likely\n")
			end
			-- execute an empty script with kill options set
			-- wait ensures it will be all done
			local flushmsgs = not args.noflush;
			con:exec("",{
					flush_cam_msgs=flushmsgs,
					flush_host_msgs=flushmsgs,
					clobber=true})
			-- use standalone wait_status because we don't want execwait message handling
			con:wait_status{run=false}
			return true
		end,
	},
	{
		names={'rmem'},
		help='read memory',
		args=argparser.create{i32=false}, -- word
		arghelp='<address> [count] [-i32[=fmt]]',
		help_detail=[[
 Dump <count> bytes or words starting at <address>
  -i32 display as 32 bit words rather than byte oriented hex dump
  -i32=<fmt> use printf format string fmt to display
]],
		func=function(self,args) 
			local addr = tonumber(args[1])
			local count = tonumber(args[2])
			if not addr then
				return false, "bad args"
			end
			if not count then
				count = 1
			end
			if args.i32 then
				count = count * 4
			end

			local r = con:getmem(addr,count)

			if args.i32 then
				local fmt
				if type(args.i32) == 'string' then
					fmt = args.i32
				end
				r=util.hexdump_words(r,addr,fmt)
			else
				r=util.hexdump(r,addr)
			end
			return true, string.format("0x%08x %u\n",addr,count)..r
		end,
	},
	{
		names={'list'},
		help='list USB devices',
		help_detail=[[
 Lists all recognized PTP devices in the following format on success
  <status><num>:<modelname> b=<bus> d=<device> v=<usb vendor> p=<usb pid> s=<serial number>
 or on error
  <status><num> b=<bus> d=<device> ERROR: <error message>
 status values
  * connected, current target for CLI commands (con global variable)
  + connected, not CLI target
  - not connected
  ! error querying status
 serial numbers are not available from all models, nil will be shown if not available
]],
		func=function() 
			local msg = ''
			-- TODO usb only, will not show connected PTP/IP
			local devs = chdk.list_usb_devices()
			for i,desc in ipairs(devs) do
				local status,con_status,str = pcall(cli.list_dev_single,desc)
				if status then
					msg = msg .. string.format("%s%d:%s\n",con_status,i,str)
				else
					-- use the requested dev/bus here, since the lcon data may not be set
					msg = msg .. string.format('!%d: b=%s d=%s ERROR: %s\n',i,desc.bus, desc.dev,tostring(con_status))
				end
			end
			return true,msg
		end,
	},
	{
		names={'upload','u'},
		help='upload a file to the camera',
		arghelp="[-nolua] <local> [remote]",
		args=argparser.create{nolua=false},
		help_detail=[[
 <local>  file to upload
 [remote] destination
   If not specified, file is uploaded to A/
   If remote is a directory or ends in / uploaded to remote/<local file name>
 -nolua   skip lua based checks on remote
   Allows upload while running script
   Prevents detecting if remote is a directory
 Some cameras have problems with paths > 32 characters
 Dryos cameras do not handle non 8.3 filenames well
]],
		func=function(self,args) 
			local src = args[1]
			if not src then
				return false, "missing source"
			end
			if lfs.attributes(src,'mode') ~= 'file' then
				return false, 'src is not a file: '..src
			end

			local dst_dir
			local dst = args[2]
			-- no dst, use filename of source
			if dst then
				dst = fsutil.make_camera_path(dst)
				if string.find(dst,'[\\/]$') then
					-- trailing slash, append filename of source
					dst = string.sub(dst,1,-2)
					if not args.nolua then
						local st,err = con:stat(dst)
						if not st then
							return false, 'stat dest '..dst..' failed: ' .. err
						end
						if not st.is_dir then
							return false, 'not a directory: '..dst
						end
					end
					dst = fsutil.joinpath(dst,fsutil.basename(src))
				else
					if not args.nolua then
						local st = con:stat(dst)
						if st and st.is_dir then
							dst = fsutil.joinpath(dst,fsutil.basename(src))
						end
					end
				end
			else
				dst = fsutil.make_camera_path(fsutil.basename(src))
			end

			local msg=string.format("%s->%s\n",src,dst)
			con:upload(src,dst)
			return true, msg
		end,
	},
	{
		names={'download','d'},
		help='download a file from the camera',
		arghelp="[-nolua] <remote> [local]",
		args=argparser.create{nolua=false},
		help_detail=[[
 <remote> file to download
 	A/ is prepended if not present
 [local]  destination
   If not specified, the file will be downloaded to the current directory
   If a directory, the file will be downloaded into it
 -nolua   skip lua based checks on remote
   Allows download while running script
]],

		func=function(self,args) 
			local src = args[1]
			if not src then
				return false, "missing source"
			end
			local dst = args[2]
			if not dst then
				-- no dest, use final component of source path
				dst = fsutil.basename(src)
			-- if target is a directory or has explicit trailing / download into it
			elseif lfs.attributes(dst,'mode') == 'directory' or fsutil.is_dir_sep(string.sub(dst,-1,-1)) then
				dst = fsutil.joinpath(dst,fsutil.basename(src))
			end

			-- ensure target dir exists
			fsutil.mkdir_parent(dst)

			src = fsutil.make_camera_path(src)
			if not args.nolua then
				local src_st,err = con:stat(src)
				if not src_st then
					return false, 'stat source '..src..' failed: ' .. err
				end
				if not src_st.is_file then
					return false, src..' is not a file'
				end
			end
			local msg=string.format("%s->%s\n",src,dst)
			con:download(src,dst)
			return true, msg
		end,
	},
	{
		names={'imdl'},
		help='download images from the camera',
		arghelp="[options] [src ...]",
		args=argparser.create{
			d='${subdir}/${name}',
			ddir=false,
			last=false,
			imin=false,
			imax=false,
			dmin=false,
			dmax=false,
			fmatch='%a%a%a_%d%d%d%d%.%w%w%w',
			rmatch=false,
			maxdepth=2, -- dcim/subdir
			pretend=false,
			nomtime=false,
			batchsize=20,
			dbgmem=false,
			overwrite='ask',
			quiet=false,
			rm=false,
		},
		help_detail=[[
 [src] source directories, default A/DCIM.
  Specifying directories which do not follow normal image directory naming will
  limit available substitution patterns.
 options:
   -d=<dest spec>    destination spec, using substitutions described below
                     default ${subdir}/${name} which mirrors the DCIM image
                     subdirectories into current working directory or ddir
   -ddir=<path>      directory path to prepend to dest, default none
   -last=n           download last N images based on file counter
   -imin=n           download images number n or greater
   -imax=n           download images number n or less
   -dmin=n           download images from directory number n or greater
   -dmax=n           download images from directory number n or less
   -fmatch=<pattern> download only file with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -maxdepth=n       only recurse into N levels of directory, default 2
   -pretend          print actions instead of doing them
   -nomtime          don't preserve modification time of remote files
   -batchsize=n      lower = slower, less memory used
   -dbgmem           print memory usage info
   -overwrite=<str>  overwrite existing files (y|n|old|ask), default ask
   -quiet            don't display actions
   -rm               delete files after downloading
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG

Substitutions
${serial,strfmt}  camera serial number, or empty if not available, default format %s
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

Unavailable values (e.g. ${dirday} without daily folders) result in an empty string
PC clock times are set to the start of download, not per image
]],

		func=function(self,args) 
			-- some names need translating
			local opts={
				dst=args.d,
				dstdir=args.ddir,
				lastimg=args.last,
				imgnum_min=args.imin,
				imgnum_max=args.imax,
				dirnum_min=args.dmin,
				dirnum_max=args.dmax,
				fmatch=args.fmatch,
				rmatch=args.rmatch,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				mtime=not args.nomtime,
				batchsize=tonumber(args.batchsize),
				dbgmem=args.dbgmem,
				verbose=not args.quiet,
				overwrite=cli.get_download_overwrite_opt(args.overwrite),
			}
			if #args > 0 then
				opts.start_paths={}
				for i,v in ipairs(args) do
					opts.start_paths[i]=fsutil.make_camera_path(v)
				end
			end

			local files=con:imglist(opts)
			con:imglist_download(files,opts)
			if args.rm then
				con:imglist_delete(files,opts)
			end
			return true
		end,
	},
	{
		names={'imrm'},
		help='delete images from the camera',
		arghelp="[options] [path ...]",
		args=argparser.create{
			last=false,
			imin=false,
			imax=false,
			dmin=false,
			dmax=false,
			fmatch='%a%a%a_%d%d%d%d%.%w%w%w',
			rmatch=false,
			maxdepth=2, -- dcim/subdir
			pretend=false,
			batchsize=20,
			dbgmem=false,
			quiet=false,
		},
		help_detail=[[
 [path] directories to delete from, default A/DCIM.
 options:
   -last=n           delete last N images based on file counter
   -imin=n           delete images number n or greater
   -imax=n           delete images number n or less
   -dmin=n           delete images from directory number n or greater
   -dmax=n           delete images from directory number n or less
   -fmatch=<pattern> delete only file with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -maxdepth=n       only recurse into N levels of directory, default 2
   -pretend          print actions instead of doing them
   -batchsize=n      lower = slower, less memory used
   -dbgmem           print memory usage info
   -quiet            don't display actions
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG

 file selection options are equivalent to imdl
]],

		func=function(self,args) 
			-- some names need translating
			local opts={
				lastimg=args.last,
				imgnum_min=args.imin,
				imgnum_max=args.imax,
				dirnum_min=args.dmin,
				dirnum_max=args.dmax,
				fmatch=args.fmatch,
				rmatch=args.rmatch,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				mtime=not args.nomtime,
				batchsize=tonumber(args.batchsize),
				dbgmem=args.dbgmem,
				verbose=not args.quiet
			}
			if #args > 0 then
				opts.start_paths={}
				for i,v in ipairs(args) do
					opts.start_paths[i]=fsutil.make_camera_path(v)
				end
			end

			local files=con:imglist(opts)
			con:imglist_delete(files,opts)
			return true
		end,
	},
	{
		names={'imls'},
		help='list images on the camera',
		arghelp="[options] [path ...]",
		args=argparser.create{
			last=false,
			imin=false,
			imax=false,
			dmin=false,
			dmax=false,
			fmatch='%a%a%a_%d%d%d%d%.%w%w%w',
			rmatch=false,
			maxdepth=2, -- dcim/subdir
			sort='path',
			r=false,
			batchsize=20,
			dbgmem=false,
			quiet=false,
		},
		help_detail=[[
 [path] directories to list from, default A/DCIM.
 options:
   -last=n           list last N images based on file counter
   -imin=n           list images number n or greater
   -imax=n           list images number n or less
   -dmin=n           list images from directory number n or greater
   -dmax=n           list images from directory number n or less
   -fmatch=<pattern> list only files with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -maxdepth=n       only recurse into N levels of directory, default 2
   -sort=order       where order is one of 'path','name','date','size' default 'path'
   -r                sort descending instead of ascending
   -batchsize=n      lower = slower, less memory used
   -dbgmem           print memory usage info
   -quiet            don't display actions
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG

 file selection options are equivalent to imdl
]],

		func=function(self,args) 
			-- some names need translating
			local opts={
				lastimg=args.last,
				imgnum_min=args.imin,
				imgnum_max=args.imax,
				dirnum_min=args.dmin,
				dirnum_max=args.dmax,
				fmatch=args.fmatch,
				rmatch=args.rmatch,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				mtime=not args.nomtime,
				batchsize=tonumber(args.batchsize),
				dbgmem=args.dbgmem,
				verbose=not args.quiet
			}
			local sortopts={
				path={'full'},
				name={'name'},
				date={'st','mtime'},
				size={'st','size'},
			}
			local sortpath = sortopts[args.sort]
			if not sortpath then
				return false,'invalid sort '..tostring(args.sort)
			end
			if #args > 0 then
				opts.start_paths={}
				for i,v in ipairs(args) do
					opts.start_paths[i]=fsutil.make_camera_path(v)
				end
			end

			local files=con:imglist(opts)
			if args.r then
				util.table_path_sort(files,sortpath,'des')
			else
				util.table_path_sort(files,sortpath,'asc')
			end
			local r=''
			for i,finfo in ipairs(files) do
					local size = finfo.st.size
					r = r .. string.format("%s %10s %s\n",
							os.date('%c',chdku.ts_cam2pc(finfo.st.mtime)),
							tostring(finfo.st.size),
							finfo.full)
			end
			return true, r
		end,
	},
	{
		names={'mdownload','mdl'},
		help='download file/directories from the camera',
		arghelp="[options] <remote, remote, ...> <target dir>",
		args=argparser.create{
			fmatch=false,
			dmatch=false,
			rmatch=false,
			nodirs=false,
			maxdepth=100,
			pretend=false,
			nomtime=false,
			batchsize=20,
			dbgmem=false,
			overwrite='ask',
		},
		help_detail=[[
 <remote...> files/directories to download
 <target dir> directory to download into
 options:
   -fmatch=<pattern> download only file with path/name matching <pattern>
   -dmatch=<pattern> only create directories with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -nodirs           only create directories needed to download file  
   -maxdepth=n       only recurse into N levels of directory
   -pretend          print actions instead of doing them
   -nomtime          don't preserve modification time of remote files
   -batchsize=n      lower = slower, less memory used
   -dbgmem           print memory usage info
   -overwrite=<str>  overwrite existing files (y|n|old|ask), default ask
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG
]],

		func=function(self,args) 
			if #args < 2 then
				return false,'expected source(s) and destination'
			end
			local dst=table.remove(args)
			local srcs={}
			for i,v in ipairs(args) do
				srcs[i]=fsutil.make_camera_path(v)
			end
			-- TODO some of these need translating, so can't pass direct
			local opts={
				fmatch=args.fmatch,
				dmatch=args.dmatch,
				rmatch=args.rmatch,
				dirs=not args.nodirs,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				mtime=not args.nomtime,
				batchsize=tonumber(args.batchsize),
				dbgmem=args.dbgmem,
				overwrite=cli.get_download_overwrite_opt(args.overwrite),
			}
			con:mdownload(srcs,dst,opts)
			return true
		end,
	},
	{
		names={'mupload','mup'},
		help='upload file/directories to the camera',
		arghelp="[options] <local, local, ...> <target dir>",
		args=argparser.create{
			fmatch=false,
			dmatch=false,
			rmatch=false,
			nodirs=false,
			maxdepth=100,
			pretend=false,
			nomtime=false,
		},
		help_detail=[[
 <local...> files/directories to upload
 <target dir> directory to upload into
 options:
   -fmatch=<pattern> upload only file with path/name matching <pattern>
   -dmatch=<pattern> only create directories with path/name matching <pattern>
   -rmatch=<pattern> only recurse into directories with path/name matching <pattern>
   -nodirs           only create directories needed to upload file 
   -maxdepth=n       only recurse into N levels of directory
   -pretend          print actions instead of doing them
   -nomtime          don't preserve local modification time
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG
]],

		func=function(self,args) 
			if #args < 2 then
				return false,'expected source(s) and destination'
			end
			local dst=fsutil.make_camera_path(table.remove(args))
			local srcs={}
			-- args has other stuff in it, copy array parts
			srcs={unpack(args)}
			-- TODO some of these need translating, so can't pass direct
			local opts={
				fmatch=args.fmatch,
				dmatch=args.dmatch,
				rmatch=args.rmatch,
				dirs=not args.nodirs,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				mtime=not args.nomtime,
			}
			con:mupload(srcs,dst,opts)
			return true
		end,
	},
	{
		names={'delete','rm'},
		help='delete file/directories from the camera',
		arghelp="[options] <target, target,...>",
		args=argparser.create{
			fmatch=false,
			dmatch=false,
			rmatch=false,
			nodirs=false,
			maxdepth=100,
			pretend=false,
			ignore_errors=false,
			skip_topdirs=false,
		},
		help_detail=[[
 <target...> files/directories to remote
 options:
   -fmatch=<pattern> upload only file with names matching <pattern>
   -dmatch=<pattern> only delete directories with names matching <pattern>
   -rmatch=<pattern> only recurse into directories with names matching <pattern>
   -nodirs           don't delete drictories recursed into, only files
   -maxdepth=n       only recurse into N levels of directory
   -pretend          print actions instead of doing them
   -ignore_errors    don't abort if delete fails, continue to next item
   -skip_topdirs     don't delete directories given in command line, only contents
 note <pattern> is a lua pattern, not a filesystem glob like *.JPG
]],

		func=function(self,args) 
			if #args < 1 then
				return false,'expected at least one target'
			end
			-- args has other stuff in it, copy array parts
			local tgts={}
			for i,v in ipairs(args) do
				tgts[i]=fsutil.make_camera_path(v)
			end
			-- TODO some of these need translating, so can't pass direct
			local opts={
				fmatch=args.fmatch,
				dmatch=args.dmatch,
				rmatch=args.rmatch,
				dirs=not args.nodirs,
				maxdepth=tonumber(args.maxdepth),
				pretend=args.pretend,
				ignore_errors=args.ignore_errors,
				skip_topdirs=args.skip_topdirs,
			}
			-- TODO use msg_handler to print as they are deleted instead of all at the end
			local results = con:mdelete(tgts,opts)
			for i,v in ipairs(results) do
				-- TODO success should not be displayed at low verbosity
				printf("%s: ",v.file)
				if v.status then
					printf('OK')
				else
					printf('FAILED')
				end
				if v.msg then
					printf(": %s",v.msg)
				end
				printf('\n')
			end
			return true
		end,
	},
	{
		names={'mkdir'},
		help='create directories on camera',
		arghelp="<directory>",
		args=argparser.create{ },
		help_detail=[[
 <directory> directory to create. Intermediate directories will be created as needed
]],
		func=function(self,args)
			if #args ~= 1 then
				return false,'expected exactly one arg'
			end
			return con:mkdir_m(fsutil.make_camera_path(args[1]))
		end
	},
	{
		names={'version','ver'},
		help='print API and program versions',
		args=argparser.create{ 
			p=false,
			l=false,
		},
		arghelp="[-p][-l]",
		help_detail=[[
 -p print program version
 -l print library versions
]],
		func=function(self,args) 
			local host_ver = string.format("host:%d.%d cam:",chdku.apiver.MAJOR,chdku.apiver.MINOR)
			local status = true
			local r
			if con:is_connected() then
				-- TODO could just use con cached versions
				local cam_major, cam_minor = con:camera_api_version()
				if cam_major then
					r = host_ver .. string.format("%d.%d",cam_major,cam_minor)
				else
					status = false
					r =  host_ver .. string.format("error %s",cam_minor)
				end 
			else
				r = host_ver .. "not connected"
			end
			if args.p then
				r = string.format('chdkptp %d.%d.%d-%s built %s %s\n%s',
									chdku.ver.MAJOR,chdku.ver.MINOR,chdku.ver.BUILD,chdku.ver.DESC,
									chdku.ver.DATE,chdku.ver.TIME,r)
			end
			if args.l then
				r = r .. '\n'.._VERSION -- Lua version
				-- note these will only show up if actually running gui
				if iup then
					r = r .. '\nIUP '..iup._VERSION
				end
				if cd then
					r = r .. '\nCD '..cd._VERSION
				end
			end
			return status,r
		end,
	},
	{
		names={'connect','c'},
		help='connect to device',
		arghelp="[-nodis] [USB dev spec] | -h=host [-p=port]",
		args=argparser.create{
			b=false,
			d=false,
			p=false,
			s=false,
			h=false,
			nodis=false,
			nopat=false,
		},
		
		help_detail=[[
 If no options are given, connects to the first available USB device.
 USB dev spec:
  -b=<bus>
  -d=<dev> 
  -p=<pid>
  -s=<serial> 
  model 
 <pid> is the USB product ID, as a decimal or hexadecimal number.
 All other values are treated as a Lua pattern, unless -nopat is given.
 If the serial or model are specified, a temporary connection will be made to each device
 If <model> includes spaces, it must be quoted.
 If multiple devices match, the first matching device will be connected.
 other options:
  -nodis do not close current connection
  -nopat use plain substring matches instead of patterns
]],
		func=function(self,args) 
			local match = {}
			local opt_map = {
				b='bus',
				d='dev',
				p='product_id',
				s='serial_number',
				[1]='model',
			}
			for k,v in pairs(opt_map) do
				-- TODO matches expect nil
				if type(args[k]) == 'string' then
					match[v] = args[k]
				end
--				printf('%s=%s\n',v,tostring(args[k]))
			end
			match.plain = args.nopat

			if not args.nodis and con:is_connected() then
				con:disconnect()
			end

			-- ptp/ip ignore other options
			-- TODO should warn
			local lcon
			if args.h then
				if not args.p then
					args.p = nil
				end
				lcon = chdku.connection({host=args.h,port=args.p})
			else
				if match.product_id and not tonumber(match.product_id) then
					return false,"expected number for product id"
				end
				local devices = chdk.list_usb_devices()
				for i, devinfo in ipairs(devices) do
					lcon = nil
					if chdku.match_device(devinfo,match) then
						lcon = chdku.connection(devinfo)
						-- if we are looking for model or serial, need to connect to the dev to check
						if match.model or match.serial_number then
							local tempcon = false
							cli.dbgmsg('model check %s %s\n',tostring(match.model),tostring(match.serial_number))
							if not lcon:is_connected() then
								lcon:connect()
								tempcon = true
							else
								lcon:update_connection_info()
							end
							if not lcon:match_ptp_info(match) then
								if tempcon then
									lcon:disconnect()
								end
								lcon = nil
							end
						end
						if lcon then
							break
						end
					end
				end
			end
			local status, err
			if lcon then
				con = lcon
				if not con:is_connected() then
					con:connect()
				end
				if con:is_connected() then
					cli.infomsg('connected: %s, max packet size %d\n',con.ptpdev.model,con.ptpdev.max_packet_size)
					-- TODO should have a min API version check
					if con.apiver.MAJOR < 0 then
						util.warnf('CHDK extension not detected\n')
					end
					status = true
				end
			else 
				status = false
				err = "no matching devices found"
			end
			cli:connection_status_change()
			return status,err
		end,
	},
	{
		names={'reconnect','r'},
		help='reconnect to current device',
		-- NOTE camera may connect to a different device,
		-- will detect and fail if serial, model or pid don't match
		func=function(self,args) 
			con:reconnect()
			cli:connection_status_change()
			return true
		end,
	},
	{
		names={'disconnect','dis'},
		help='disconnect from device',
		func=function(self,args) 
			con:disconnect()
			cli:connection_status_change()
			return true
		end,
	},
	{
		names={'ls'},
		help='list files/directories on camera',
		args=argparser.create{l=false},
		arghelp="[-l] [path]",
		func=function(self,args) 
			local listops
			local path=args[1]
			path = fsutil.make_camera_path(path)
			if args.l then
				listopts = { stat='*' }
			else
				listopts = { stat='/' }
			end
			listopts.dirsonly=false
			local list = con:listdir(path,listopts)
			local r = ''
			if args.l then
				-- alphabetic sort TODO sorting/grouping options
				chdku.sortdir_stat(list)
				for i,st in ipairs(list) do
					local name = st.name
					local size = st.size
					if st.is_dir then
						name = name..'/'
						size = '<dir>'
					else
					end
					r = r .. string.format("%s %10s %s\n",os.date('%c',chdku.ts_cam2pc(st.mtime)),tostring(size),name)
				end
			else
				table.sort(list)
				for i,name in ipairs(list) do
					r = r .. name .. '\n'
				end
			end

			return true,r
		end,
	},
	{
		names={'reboot'},
		help='reboot the camera',
		arghelp="[options] [file]",
		args=argparser.create({
			wait=3500,
			norecon=false,
		}),
		help_detail=[[
 file: Optional file to boot.
  Must be an unencoded binary or for DryOS only, an encoded .FI2
  Format is assumed based on extension
  If not set, firmware boots normally, loading diskboot.bin if configured
 options:
   -norecon  don't try to reconnect
   -wait=<N> wait N ms before attempting to reconnect, default 3500
]],
		func=function(self,args) 
			local bootfile=args[1]
			if bootfile then
				bootfile = fsutil.make_camera_path(bootfile)
				bootfile = string.format("'%s'",bootfile)
			else
				bootfile = ''
			end
			-- sleep and disconnect to avoid later connection problems on some cameras
			-- clobber because we don't care about memory leaks
			con:exec('sleep(1000);reboot('..bootfile..')',{clobber=true})
			if args.norecon then
				return true
			end
			con:reconnect({wait=args.wait})
			return true
		end,
	},
	{
		names={'lvdump','dumpframes'},
		help='dump camera display frames to file',
		arghelp="[options] [file]",
		args=argparser.create({
			count=5,
			wait=100,
			novp=false,
			nobm=false,
			nopal=false,
			quiet=false,
			pbm=false,
		}),
		help_detail=[[
 file:
 	optional output file name, defaults to chdk_<pid>_<date>_<time>.lvdump
 options:
   -count=<N> number of frames to dump
   -wait=<N>  wait N ms between frames
   -novp      don't get viewfinder data
   -nobm      don't get ui overlay data
   -nopal     don't get palette for ui overlay
   -quiet     don't print progress
]],
		func=function(self,args) 
			local dumpfile=args[1]
			local what = 0
			if not args.novp then
				what = 1
			end
			if not args.nobm then
				what = what + 4
				if not args.nopal then
					what = what + 8
				end
			end
			if what == 0 then
				return false,'nothing selected'
			end
			if args.wait then
				args.wait = tonumber(args.wait)
			end
			if args.count then
				args.count = tonumber(args.count)
			end
			local status,err
			if not con:live_is_api_compatible() then
				return false,'incompatible api'
			end
			status, err = con:live_dump_start(dumpfile)
			if not status then
				return false,err
			end
			for i=1,args.count do
				if not args.quiet then
					printf('grabbing frame %d\n',i)
				end
				status, err = con:live_get_frame(what)
				if not status then
					break
				end
				status, err = con:live_dump_frame()
				if not status then
					break
				end
				if args.wait and i < args.count then
					sys.sleep(args.wait)
				end
			end
			con:live_dump_end()
			if status then
				err = string.format('%d bytes recorded to %s\n',tonumber(con.live.dump_size),tostring(con.live.dump_fn))
			end
			return status,err
		end,
	},
	{
		names={'lvdumpimg'},
		help='dump camera display frames to netpbm images',
		arghelp="[options]",
		args=argparser.create({
--			infile=false,
			count=1,
			wait=false,
			fps=10,
			vp=false,
			bm=false,
			pipevp=false,
			pipebm=false,
			nopal=false,
			quiet=false,
			nosubst=false,
		}),
-- TODO
--   -infile=<file> lvdump file to use as source instead of camera
		help_detail=[[
 options:
   -count=<N> number of frames to dump, default 1
   -wait=<N>  wait N ms between frames
   -fps=<N>   specify wait as a frame rate, default 10
   -vp[=dest] get viewfinder in ppm format
   -bm[=dest] get ui overlay in pam format
   -pipevp[=oneproc]
   -pipebm[=oneproc]
      treat vp or bm 'dest' as a command to pipe to. With =oneproc a single process
      receives all frames. Otherwise, a new process is spawned for each frame
   -nopal     don't get palette for ui overlay
   -quiet     don't print progress
   -nosubst   don't do pattern substitution on file names
  vp and bm 'dest' may include substitution patterns
   ${date,datefmt} current time formatted with os.date()
   ${frame,strfmt} current frame number formatted with string.format
   ${time,strfmt}  current time in seconds, as float, formatted with string.format
   default vp_${time,%014.3f}.ppm bm_${time,%014.3f}.pam for viewfinder and ui respectively
   if piping with oneproc, time will be the start of the first frame and frame will be 1
]],
		func=function(self,args) 
			local what = 0
			if args.vp then
				what = 1
			end
			if args.bm then
				what = what + 4
				if not args.nopal then
					what = what + 8
				end
			end
			if what == 0 then
				return false,'nothing selected'
			end
			if args.wait then
				args.wait = tonumber(args.wait)
			end
			if args.fps then
				if args.wait then
					return false,'specify wait or fps, not both'
				end
				args.wait = 1000/tonumber(args.fps)
			end
			if args.count then
				args.count = tonumber(args.count)
			end

			if not con:is_connected() then
				return false,'not connected'
			end

			local status,err
			if not con:live_is_api_compatible() then
				return false,'incompatible api'
			end

			-- state for substitutions
			local subst=varsubst.new({
				frame=varsubst.format_state_val('frame','%06d'),
				time=varsubst.format_state_val('time','%d'),
				date=varsubst.format_state_date('date','%Y%m%d_%H%M%S'),
			})

			local vp_opts = cli.init_lvdumpimg_file_opts('vp',args,subst)
			local bm_opts = cli.init_lvdumpimg_file_opts('bm',args,subst)

			local t0=ustime.new()
			local t_frame_start=ustime.new()

			-- TODO frame source should be split out to allow dumping from existing lvdump file
			for i=1,args.count do
				t_frame_start:get()
				-- TODO should use wrapped frame, maybe con:live_get_frame
				frame = con:get_live_data(frame,what)

				subst.state.frame = i
				-- set time state once per frame to avoid varying between viewport and bitmap
				subst.state.date = os.time()
				subst.state.time = ustime.new():float()

				if args.vp then
					vp_opts.write(frame)
				end
				if args.bm then
					bm_opts.write(frame)
				end
				if args.wait and i < args.count and t_frame_start:diffms() < args.wait then
					sys.sleep(args.wait - t_frame_start:diffms())
				end
			end
			-- if using oneproc pipe, need to close
			if vp_opts.filehandle then
				vp_opts.filehandle:close()
			end
			if bm_opts.filehandle then
				bm_opts.filehandle:close()
			end
			if subst.state.frame and not args.quiet then
				local t_total = t0:diffms()/1000
				-- fudge to handle the final sleep being skipped
				if args.wait and t_frame_start:diffms() < args.wait then
					t_total = t_total + (args.wait - t_frame_start:diffms())/1000
				end
				cli.dbgmsg('frames:%d time:%f fps:%f\n',subst.state.frame,t_total,subst.state.frame/t_total)
			end
			return true
		end,
	},
	{
		names={'shoot'},
		help='shoot a picture with specified exposure',
		arghelp="[options]",
		args=argparser.create({
			u='s',
			tv=false,
			sv=false,
			svm=false,
			av=false,
			isomode=false,
			nd=false,
			sd=false,
			raw=false,
			dng=false,
			pretend=false,
			nowait=false,
			dl=false,
			rm=false,
		}),
		-- TODO allow setting destinations and filetypes for -dl
		help_detail=[[
 options:
   -u=<s|a|96>
      s   standard units (default)
      a   APEX
      96  APEX*96
   -tv=<v>    shutter speed. In standard units both decimal and X/Y accepted
   -sv=<v>    ISO value, Canon "real" ISO
   -svm=<v>   ISO value, Canon "Market" ISO (requires CHDK 1.3)
   -av=<v>    Aperture value. In standard units, f number
   -isomode=<v> ISO mode, must be ISO value in Canon UI, shooting mode must have manual ISO
   -nd=<in|out> set ND filter state
   -sd=<v>[units]  subject distance, units one of m, mm, in, ft default m
   -raw[=1|0] Force raw on or off, defaults to current camera setting
   -dng[=1|0] Force DNG on or off, implies raw if on, default current camera setting
   -pretend   print actions instead of running them
   -nowait    don't wait for shot to complete
   -dl        download shot file(s)
   -rm        remove file after shooting
  Any exposure parameters not set use camera defaults
]],
		func=function(self,args) 
			local opts,err = cli:get_shoot_common_opts(args)
			if not opts then
				return false,err
			end
			-- allow -dng
			if args.dng == true then
				args.dng = 1
			end
			if args.dng then
				opts.dng = tonumber(args.dng)
				if opts.dng == 1 then
					-- force raw on if dng. TODO complain if raw/dng mismatch?
					args.raw = 1
				end
			end
			-- allow -raw to turn raw on
			if args.raw == true then
				args.raw=1
			end
			if args.raw then
				opts.raw=tonumber(args.raw)
			end
			if args.rm or args.dl then
				if args.nowait then
					return false, "can't download or remove with nowait"
				end
				opts.info=true
			end
			local cmd=string.format('rlib_shoot(%s)',util.serialize(opts))
			if args.pretend then
				return true,cmd
			end
			if args.nowait then
				con:exec(cmd,{libs={'rlib_shoot'}})
				return
			end

			local rstatus,rerr = con:execwait('return '..cmd,{libs={'serialize_msgs','rlib_shoot'}})

			if not rstatus then
				return false, rerr
			end
			if not (args.dl or args.rm) then
				return true
			end

			local info = rstatus

			local jpg_path = string.format('%s/IMG_%04d.JPG',info.dir,info.exp)
			local raw_path

			if info.raw then
				-- TODO
				-- get_config_value only returns indexes
				-- chdk versions might change these
				local pfx_list = {[0]="IMG", "CRW", "SND"}
				local ext_list = {[0]="JPG", "CRW", "CR2", "THM", "WAV"}
				local raw_dir
				local raw_ext
				local raw_pfx
				if info.raw_in_dir then
					raw_dir = info.dir
				else
					raw_dir = 'A/DCIM/100CANON'
				end
				if info.dng and info.use_dng_ext then
					raw_ext = 'DNG'
				else
					raw_ext = ext_list[info.raw_ext]
					if not raw_ext then
						raw_ext = 'RAW'
					end
				end
				raw_pfx = pfx_list[info.raw_pfx]
				if not raw_pfx then
					raw_pfx = 'RAW_'
				end
				raw_path = string.format('%s/%s_%04d.%s',raw_dir,raw_pfx,info.exp,raw_ext)
			end
			-- TODO some delay may be required between shot and dl start
			if args.dl then
				cli:print_status(cli:execute('download '..jpg_path))
				if raw_path then
					cli:print_status(cli:execute('download '..raw_path))
				end
			end
			if args.rm then
				cli:print_status(cli:execute('rm -maxdepth=0 '..jpg_path))
				if raw_path then
					cli:print_status(cli:execute('rm -maxdepth=0 '..raw_path))
				end
			end
			return true
		end,
	},
	-- TODO this should be combined with the shoot command,
	-- or at least make the syntax / options consistent
	{
		names={'remoteshoot','rs'},
		help='shoot and download without saving to SD (requires CHDK 1.2)',
		arghelp="[local] [options]",
		args=argparser.create{
			u='s',
			tv=false,
			sv=false,
			svm=false,
			av=false,
			isomode=false,
			nd=false,
			sd=false,
			jpg=false,
			raw=false,
			dng=false,
			dnghdr=false,
			s=false,
			c=false,
			cont=false,
			quick=false,
			shots=false,
			int=false,
			badpix=false,
		},
		help_detail=[[
 [local]       local destination directory or filename (w/o extension!)
 options:
   -u=<s|a|96>
      s   standard units (default)
      a   APEX
      96  APEX*96
   -tv=<v>    shutter speed. In standard units both decimal and X/Y accepted
   -sv=<v>    ISO value, Canon "real" ISO
   -svm=<v>   ISO value, Canon "Market" ISO (requires CHDK 1.3)
   -av=<v>    Aperture value. In standard units, f number
   -isomode=<v> ISO mode, must be ISO value in Canon UI, shooting mode must have manual ISO
   -nd=<in|out> set ND filter state
   -sd=<v>[units]  subject distance, units one of m, mm, in, ft default m
   -jpg         jpeg, default if no other options (not supported on all cams)
   -raw         framebuffer dump raw
   -dng         DNG format raw
   -dnghdr      save DNG header to a separate file, ignored with -dng
   -s=<start>   first line of for subimage raw
   -c=<count>   number of lines for subimage
   -cont[=n]    shoot in continuous mode, optionally specifying number of shots
   -quick[=n]   shoot by holding halfshoot and repeatedly clicking full
   -shots=<n>   shoot n shots
   -int=<n.m>   interval for multiple shots, in seconds
   -badpix[=n]  interpolate over pixels with value <= n, default 0, (dng only)
]],
		func=function(self,args)
			local dst = args[1]
			local dst_dir
			if dst then
				if string.match(dst,'[\\/]+$') then
					-- explicit / treat it as a directory
					-- and check if it is
					dst_dir = string.sub(dst,1,-2)
					if lfs.attributes(dst_dir,'mode') ~= 'directory' then
						cli.dbgmsg('mkdir %s\n',dst_dir)
						fsutil.mkdir_m(dst_dir)
					end
					dst = nil
				elseif lfs.attributes(dst,'mode') == 'directory' then
					dst_dir = dst
					dst = nil
				end
			end

			local opts,err = cli:get_shoot_common_opts(args)
			if not opts then
				return false,err
			end

			util.extend_table(opts,{
				fformat=0,
				lstart=0,
				lcount=0,
			})
			-- fformat required for init
			if args.jpg then
				opts.fformat = opts.fformat + 1
			end
			if args.dng then
				opts.fformat = opts.fformat + 6
			else
				if args.raw then
					opts.fformat = opts.fformat + 2
				end
				if args.dnghdr then
					opts.fformat = opts.fformat + 4
				end
			end
			-- default to jpeg TODO won't be supported on cams without raw hook
			if opts.fformat == 0 then
				opts.fformat = 1
				args.jpg = true
			end

			if args.badpix and not args.dng then
				util.warnf('badpix without dng ignored\n')
			end

			if args.s or args.c then
				if args.dng or args.raw then
					if args.s then
						opts.lstart = tonumber(args.s)
					end
					if args.c then
						opts.lcount = tonumber(args.c)
					end
				else
					util.warnf('subimage without raw ignored\n')
				end
			end
			if args.cont then
				if type(args.cont) == 'string' then
					opts.shots = tonumber(args.cont)
				end
				opts.cont = true
			end
			if args.quick then
				if type(args.quick) == 'string' then
					opts.shots = tonumber(args.quick)
				end
				opts.quick = true
			end
			if opts.shots and args.shots then
				util.warnf("shot count specified with -quick or -cont, ignoring -shots")
			else
				if args.shots then
					opts.shots = tonumber(args.shots)
				elseif not opts.shots then
					opts.shots = 1
				end
			end

			-- convert to integer ms
			if args.int then
				opts.int = util.round(tonumber(args.int)*1000)
			end

			local opts_s = serialize(opts)
			cli.dbgmsg('rs_init\n')
			local rstatus,rerr = con:execwait('return rs_init('..opts_s..')',{libs={'rs_shoot_init'}})
			if not rstatus then
				return false,rerr
			end

			cli.dbgmsg('rs_shoot\n')
			-- TODO script errors will not get picked up here
			con:exec('rs_shoot('..opts_s..')',{libs={'rs_shoot'}})

			local rcopts={}
			if args.jpg then
				rcopts.jpg=chdku.rc_handler_file(dst_dir,dst)
			end
			if args.dng then
				if args.badpix == true then
					args.badpix = 0
				end
				local dng_info = {
					lstart=opts.lstart,
					lcount=opts.lcount,
					badpix=args.badpix,
				}
				rcopts.dng_hdr = chdku.rc_handler_store(function(chunk) dng_info.hdr=chunk.data end)
				rcopts.raw = chdku.rc_handler_raw_dng_file(dst_dir,dst,'dng',dng_info)
			else
				if args.raw then
					rcopts.raw=chdku.rc_handler_file(dst_dir,dst)
				end
				if args.dnghdr then
					rcopts.dng_hdr=chdku.rc_handler_file(dst_dir,dst)
				end
			end

			local status,err
			local shot = 1
			repeat 
				cli.dbgmsg('get data %d\n',shot)
				status,err = con:capture_get_data_pcall(rcopts)
				if not status then
					warnf('capture_get_data error %s\n',tostring(err))
					cli.dbgmsg('sending stop message\n')
					con:write_msg_pcall('stop')
					break
				end
				shot = shot + 1
			until shot > opts.shots

			local t0=ustime.new()
			-- wait for shot script to end or timeout
			local wpstatus,wstatus=con:wait_status_pcall{
				run=false,
				timeout=30000,
			}
			if not wpstatus then
				warnf('error waiting for shot script %s\n',tostring(werr))
			else
				if wstatus.timeout then
					warnf('timed out waiting for shot script\n')
				end
				-- TODO should allow passing a message handler to capture_get_data
				-- stop immediately on script error
				if wstatus.msg then
					con:read_all_msgs({
						['return']=function(msg,opts)
							warnf("unexpected script return %s\n",tostring(msg.value))
						end,
						user=function(msg,opts)
							warnf("unexpected script msg %s\n",tostring(msg.value))
						end,
						error=function(msg,opts)
							warnf("script error %s\n",tostring(msg.value))
						end,
					})
				end
			end
			cli.dbgmsg("script wait time %.4f\n",ustime.diff(t0)/1000000)

			local ustatus, uerr = con:execwait_pcall('init_usb_capture(0)') -- try to uninit
			-- if uninit failed, combine with previous status
			if not ustatus then
				uerr = 'uninit '..tostring(uerr)
				status = false
				if err then
					err = err .. ' ' .. uerr
				else 
					err = uerr
				end
			end
			if not status then
				return false,err
			end
			return true
		end,
	},
	{
		names={'rsint'},
		help='shoot and download with interactive control',
		arghelp="[local] [options]",
		args=cli.argparser.create{
			u='s',
			tv=false,
			sv=false,
			svm=false,
			av=false,
			isomode=false,
			nd=false,
			sd=false,
			jpg=false,
			raw=false,
			dng=false,
			dnghdr=false,
			s=false,
			c=false,
			badpix=false,
			cmdwait=60,
			cont=false,
		},
		help_detail=[[
 [local]       local destination directory or filename (w/o extension!)
 options:
   -u=<s|a|96>
      s   standard units (default)
      a   APEX
      96  APEX*96
   -tv=<v>    shutter speed. In standard units both decimal and X/Y accepted
   -sv=<v>    ISO value, Canon "real" ISO
   -svm=<v>   ISO value, Canon "Market" ISO (requires CHDK 1.3)
   -av=<v>    Aperture value. In standard units, f number
   -isomode=<v> ISO mode, must be ISO value in Canon UI, shooting mode must have manual ISO
   -nd=<in|out> set ND filter state
   -sd=<v>[units]  subject distance, units one of m, mm, in, ft default m
   -jpg         jpeg, default if no other options (not supported on all cams)
   -raw         framebuffer dump raw
   -dng         DNG format raw
   -dnghdr      save DNG header to a seperate file, ignored with -dng
   -s=<start>   first line of for subimage raw
   -c=<count>   number of lines for subimage
   -badpix[=n]  interpolate over pixels with value <= n, default 0, (dng only)
   -cmdwait=n   wait n seconds for command, default 60
   -cont        use continuous mode


 The following commands are available at the rsint> prompt
  s    shoot
  l    shoot and then quit rsint
  q    quit (not available in continuous mode, use l)
  exec <lua code>   execute code on the camera
  pcall <lua code>  execute code on the camera in pcall
  path[=path] change download destination, equivalent to [local] in the initial command

 In -cont mode, the following restrictions apply:
 The camera must be set to continuous mode in the Canon UI
 CHDK 1.3 shoot hooks must be available
 The l command must be used to exit
]],
		func=rsint.cli_cmd_func,
	},
	{
		names={'rec'},
		help='switch camera to shooting mode',
		func=function(self,args) 
			local rstatus,rerr = con:execwait([[
if not get_mode() then
	switch_mode_usb(1)
	local i=0
	while not get_mode() and i < 300 do
		sleep(10)
		i=i+1
	end
	if not get_mode() then
		return false, 'switch failed'
	end
	return true
end
return false,'already in rec'
]])
			cli:mode_change()
			return rstatus,rerr
		end,
	},
	{
		names={'play'},
		help='switch camera to playback mode',
		func=function(self,args) 
			local rstatus,rerr = con:execwait([[
if get_mode() then
	switch_mode_usb(0)
	local i=0
	while get_mode() and i < 300 do
		sleep(10)
		i=i+1
	end
	if get_mode() then
		return false, 'switch failed'
	end
	return true
end
return false,'already in play'
]])
			cli:mode_change()
			return rstatus,rerr
		end,
	},
}


prefs._add('cli_time','boolean','show cli execution times')
prefs._add('cli_xferstats','boolean','show cli data transfer stats')
prefs._add('cli_verbose','number','control verbosity of cli',1)
prefs._add('cli_source_max','number','max nested source calls',10)
return cli
