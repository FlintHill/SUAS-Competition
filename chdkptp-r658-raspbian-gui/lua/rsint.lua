--[[
 Copyright (C) 2013-2014 <reyalp (at) gmail dot com>
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
interactive remote shoot
--]]
local m={}

--[[
initializer remotecap handlers and path
]]
function init_handlers(args,opts)
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
	m.rcopts={}
	if args.jpg then
		m.rcopts.jpg=chdku.rc_handler_file(dst_dir,dst)
	end
	if args.dng then
		local badpix = args.badpix
		if badpix == true then
			badpix = 0
		end
		local dng_info = {
			lstart=opts.lstart,
			lcount=opts.lcount,
			badpix=badpix,
		}
		m.rcopts.dng_hdr = chdku.rc_handler_store(function(chunk) dng_info.hdr=chunk.data end)
		m.rcopts.raw = chdku.rc_handler_raw_dng_file(dst_dir,dst,'dng',dng_info)
	else
		if args.raw then
			m.rcopts.raw=chdku.rc_handler_file(dst_dir,dst)
		end
		if args.dnghdr then
			m.rcopts.dng_hdr=chdku.rc_handler_file(dst_dir,dst)
		end
	end
end

--[[
do a single iteration of rsint
returns true if done
errors are thrown
]]
m.rsint_once = function(args,opts)
	local line = cli.readline('rsint> ')
	if not line then
		-- TODO maybe this should just be done
		error('cli.readline failed / eof')
	end
	local status = con:script_status()
	local returned
	if status.msg then
		con:read_all_msgs({
			['return']=function(msg,opts)
				printf("script return %s\n",tostring(msg.value))
				returned = true
			end,
			user=function(msg,opts)
				printf("script msg %s\n",tostring(msg.value))
			end,
			error=function(msg,opts)
				printf("script error %s\n",tostring(msg.value))
				returned = true
			end,
		})
	end
	-- script ended with return, bail out
	if returned then
		return true
	end
	if not status.run then 
		error('script not running\n')
	end
	local s,e,cmd = string.find(line,'^[%c%s]*([%w_]+)[%c%s]*')
	local rest = string.sub(line,e+1)
	-- printf("cmd [%s] rest [%s]\n",cmd,rest);
	if cmd == 'path' then
		if rest == '' then
			rest = nil
		end
		args[1] = rest
		-- TODO could catch errors, send l to script
		init_handlers(args,opts)
	else
		-- remaining commands assumed to be cam side
		-- TODO could check if remotecap has timed out here
		con:write_msg(cmd..' '..rest)
		if cmd == 's' or cmd == 'l' then
			-- throws on error
			con:capture_get_data(m.rcopts)
			if cmd == 'l' then
				return true
			end
		end
		if cmd == 'q' and not opts.cont then
			return true 
		end
	end
	return false
end

m.cli_cmd_func = function(self,args)
	local opts,err = cli:get_shoot_common_opts(args)
	if not opts then
		return false,err
	end

	if args.cont then
		opts.cont=1
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

	init_handlers(args,opts)

	-- wait time for remotecap
	opts.cap_timeout=30000
	-- wait time for shoot hook
	opts.shoot_hook_timeout=args.cmdwait * 1000

	local opts_s = serialize(opts)
	cli.dbgmsg('rs_init\n')
	local rstatus,rerr = con:execwait('return rsint_init('..opts_s..')',{libs={'rsint'}})
	if not rstatus then
		return false,rerr
	end

	-- throws on error, rs_shoot should not initialize remotecap if there's an error, so no need to uninit
	con:exec('return rsint_run('..opts_s..')',{libs={'rsint'}})

	local status
	repeat
		local r
		status,r = xpcall(m.rsint_once,errutil.format,args,opts)
		if not status then
			warnf("%s",tostring(r))
		end
	until r

	local t0=ustime.new()
	-- wait for shot script to end or timeout
	local pstatus,wstatus=con:wait_status_pcall{
		run=false,
		timeout=30000,
	}
	if not pstatus then
		warnf('error waiting for shot script %s\n',tostring(wstatus))
	elseif wstatus.timeout then
		warnf('timed out waiting for shot script\n')
	end
	cli.dbgmsg("script wait time %.4f\n",ustime.diff(t0)/1000000)
	-- TODO check messages

	-- TODO remote script should try to uninit when done
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
	return status, err
end

function m.register_rlib() 
	chdku.rlibs:register{
		name='rsint',
		depend={'extend_table','serialize_msgs','rlib_shoot_common','rs_shoot_init'},
		code=[[
function wait_shooting(state, timeout)
	if not timeout then
		timeout = 2000
	end
	local timeout_tick = get_tick_count() + timeout
 	while get_shooting() ~= state do
		sleep(10)
		if get_tick_count() >= timeout_tick then
			return false, 'get_shooting timed out'
		end
	end
	return true
end

function rsint_init(opts)
	if opts.cont and type(hook_shoot) ~= 'table' then
		return false, 'build does not support shoot hook'
	end

	return rs_init(opts)
end

-- from msg_shell
cmds={
	echo=function(msg)
		if write_usb_msg(msg) then
			print("ok")
		else 
			print("fail")
		end
	end,
	exec=function(msg)
		local f,err=loadstring(string.sub(msg,5));
		if f then 
			local r={f()} -- pcall would be safer but anything that yields will fail
			for i, v in ipairs(r) do
				write_usb_msg(v)
			end
		else
			write_usb_msg(err)
			print("loadstring:"..err)
		end
	end,
	pcall=function(msg)
		local f,err=loadstring(string.sub(msg,6));
		if f then 
			local r={pcall(f)}
			for i, v in ipairs(r) do
				write_usb_msg(v)
			end
		else
			write_usb_msg(err)
			print("loadstring:"..err)
		end
	end,
}

function rsint_run_cont(opts)
	local errmsg

	hook_shoot.set(opts.shoot_hook_timeout)
	local shoot_count = hook_shoot.count()
	press('shoot_full')
	while true do
		local next_shot
		local msg=read_usb_msg(10)

		if type(get_usb_capture_target) == 'function' and get_usb_capture_target() == 0 then
			errmsg = 'remote capture cancelled'
			break
		end

		local cmd=nil
		if msg then
			cmd = string.match(msg,'^%w+')
		end
		if cmd == 's' or cmd == 'l' then
			next_shot = true
		elseif msg then
			if type(cmds[cmd]) == 'function' then
				cmds[cmd](msg)
			else
				write_usb_msg('unknown command '..tostring(cmd))
			end
		end
		if next_shot then
 			if hook_shoot.is_ready() then
				shoot_count = hook_shoot.count()
				hook_shoot.continue()
				next_shot = false
			end
		else
			if hook_shoot.count() > shoot_count and not hook_shoot.is_ready() then
				errmsg = 'timeout waiting for command'
				break
			end
		end
		if cmd == 'l' then
			break
		end
	end
	hook_shoot.set(0)
	release('shoot_full')
	if errmsg then
		return false, errmsg
	end
end

function rsint_run_single(opts)
	local errmsg

	local last_msg=get_tick_count()
	while true do
		local next_shot
		local msg=read_usb_msg(10)

		if type(get_usb_capture_target) == 'function' and get_usb_capture_target() == 0 then
			errmsg = 'remote capture cancelled'
			break
		end

		local cmd=nil
		if msg then
			cmd = string.match(msg,'^%w+')
			last_msg=get_tick_count()
		end
		if cmd == 's' or cmd == 'l' then
			click('shoot_full_only')
			if cmd == 'l' then
				break
			end
		elseif cmd == 'q' then
			break
		elseif msg then
			if type(cmds[cmd]) == 'function' then
				cmds[cmd](msg)
			else
				write_usb_msg('unknown command '..tostring(cmd))
			end
		end
		if get_tick_count() - last_msg > opts.shoot_hook_timeout then
			errmsg = 'timeout waiting for command'
		end
	end
	release('shoot_half')
	if errmsg then
		return false, errmsg
	end
end

function rsint_run(opts)
	rlib_shoot_init_exp(opts)

	press('shoot_half')

	local status, err = wait_shooting(true)
	if not status then
		return false, err
	end

	if opts.cont then
		return rsint_run_cont(opts)
	else
		return rsint_run_single(opts)
	end
end
]]}
end
return m
