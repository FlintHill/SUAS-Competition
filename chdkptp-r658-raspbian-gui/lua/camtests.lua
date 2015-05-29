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
some tests to run against the camera
--]]
local m={}

function m.make_stats(stats)
	local r={
		total=0
	}

	if #stats == 0 then
		return r
	end

	for i,v in ipairs(stats) do
		if not r.max or v > r.max then
			r.max = v
		end
		if not r.min or v < r.min then
			r.min = v
		end
		r.total = r.total + v
	end
	r.mean = r.total/#stats
	return r
end


--[[
repeatedly start scripts, measuring time
opts:{
	count=number -- number of iterations
	code=string  -- code to run
}
]]
function m.exectime(opts)
	opts = util.extend_table({count=100, code="dummy=1"},opts)
	if not con:is_connected() then
		error('not connected')
	end
	local times={}
	local tstart = ustime.new()
	for i=1,opts.count do
		local t0 = ustime.new()
		con:exec(opts.code,{nodefaultlib=true})
		table.insert(times,ustime.diff(t0)/1000000)
		-- wait for the script to be done
		con:wait_status{run=false}
	end
	local wall_time = ustime.diff(tstart)/1000000
	local stats = m.make_stats(times)
	printf("exec %d mean %.4f min %.4f max %.4f total %.4f (%.4f/sec) wall %.4f (%.4f/sec)\n",
		opts.count,
		stats.mean,
		stats.min,
		stats.max,
		stats.total, opts.count / stats.total, 
		wall_time, opts.count / wall_time)
end

--[[
repeatedly exec code and wait for return, checking that returned value = retval
opts:{
	count=number -- number of iterations
	code=string  -- code to run, should return something
	retval=value -- value code is expected to return
}
--]]
function m.execwaittime(opts)
	opts = util.extend_table({count=100, code="return 1",retval=1},opts)
	if not con:is_connected() then
		error('not connected')
	end
	local times={}
	local tstart = ustime.new()
	for i=1,opts.count do
		local t0 = ustime.new()
		local r = con:execwait(opts.code,{nodefaultlib=true,poll=50})
		if r ~= opts.retval then
			error('bad retval '..tostring(r) .. ' ~= '..tostring(opts.retval))
		end
		table.insert(times,ustime.diff(t0)/1000000)
	end
	local wall_time = ustime.diff(tstart)/1000000
	local stats = m.make_stats(times)
	printf("execw %d mean %.4f min %.4f max %.4f total %.4f (%.4f/sec) wall %.4f (%.4f/sec)\n",
		opts.count,
		stats.mean,
		stats.min,
		stats.max,
		stats.total, opts.count / stats.total, 
		wall_time, opts.count / wall_time)
end

--[[
repeatedly time memory transfers from cam
opts:{
	count=number -- number of iterations
	size=number  -- size to transfer
	addr=number  -- address to transfer from (default 0x1900)
}
]]
function m.xfermem(opts)
	opts = util.extend_table({count=100, size=1024*1024,addr=0x1900},opts)
	if not con:is_connected() then
		error('not connected')
	end
	local times={}
	local tstart = ustime.new()
	for i=1,opts.count do
		local t0 = ustime.new()
		local v=con:getmem(opts.addr,opts.size)
		table.insert(times,ustime.diff(t0)/1000000)
	end
	local wall_time = ustime.diff(tstart)/1000000
	local stats = m.make_stats(times)
	printf("%d x %d bytes mean %.4f min %.4f max %.4f total %.4f (%d byte/sec) wall %.4f (%d byte/sec)\n",
		opts.count,
		opts.size,
		stats.mean,
		stats.min,
		stats.max,
		stats.total, opts.count*opts.size / stats.total, 
		wall_time, opts.count*opts.size / wall_time)
end
local tests = {}

function m.cliexec(cmd)
	local status,err=cli:execute(cmd)
	if not status then
		error(err,2)
	end
	cli:print_status(true,err)
end

-- return output on success instead of printing
function m.cliexec_ret_ok(cmd)
	local status,err=cli:execute(cmd)
	if not status then
		error(err,2)
	end
	return err
end

-- return output on on fail, assert on success
function m.cliexec_ret_fail(cmd)
	local status,err=cli:execute(cmd)
	if not status then
		return err
	end
	assert('command succeeded when expected to fail')
end

function m.makelocalfile(path,content)
	fsutil.mkdir_m(fsutil.dirname(path))
	local fh,err=io.open(path,'wb')
	if not fh then
		error(err)
	end
	local status=true
	if content:len() > 0 then
		status,err = fh:write(content)
	end
	fh:close()
	assert(status,err)
end

function m.readlocalfile(path)
	assert(lfs.attributes(path,'mode') == 'file')
	local fh,err=io.open(path,'rb')
	if not fh then
		error(err)
	end
	local content=fh:read('*a')
	fh:close()
	assert(content)
	return content
end

function m.comparefiles(path1,path2)
	local mode=lfs.attributes(path1,'mode')
	assert(mode == lfs.attributes(path2,'mode'))
	if mode ~= 'file' then
		return
	end
	assert(m.readlocalfile(path1)==m.readlocalfile(path2))
end

function tests.xfer()
	m.xfermem({count=50})
end

function tests.exectimes()
	m.execwaittime({count=50})
	m.exectime({count=50})
end

function tests.exec_errors()
	con:exec('sleep(500)')
	local status,err=con:exec_pcall('print"test"')
	assert((not status) and err.etype == 'execlua_scriptrun')
	-- test killscript if compatible
	if con:is_ver_compatible(2,6) then
		con:execwait('print"kill"',{clobber=true})
	else
		-- otherwise just wait
		sys.sleep(600)
	end
	status,err=con:exec_pcall('bogus(')
	assert((not status) and err.etype == 'execlua_compile')
end
function tests.not_connected()
	if con:is_connected() then
		error('already connected')
	end
	local status,err=con:script_status_pcall()
	assert((not status) and err.ptp_rc == ptp.ERROR_NOT_CONNECTED)
end

-- prepare for connected tests by connecting
-- devspec is a string for connect
function tests.connect(devspec)
	local devs=chdk.list_usb_devices()
	if #devs == 0 then
		error('no usb devices available')
	end
	if con:is_connected() then
		error('already connected')
	end
	local cmd = 'c'
	if devspec then
		cmd = cmd .. ' ' .. devspec
	else
		printf('using default device\n')
	end
	m.cliexec(cmd)
	assert(con:is_connected())
end
function tests.list_connected()
	local list=m.cliexec_ret_ok('list')
	local lines=util.string_split(list,'\n',{plain=true,empty=false})
	for i,l in ipairs(lines) do
		-- match the current (marked *) device, grab bus and dev name
		local bus,dev=string.match(lines[1],'^%*%d+:.*b=([%S]+) d=([%S]+)')
		if bus then
			assert(bus==con.condev.bus and dev==con.condev.dev)
			return true
		end
	end
	error('current dev not found')
end
function tests.wait_status()
	local status=con:wait_status{msg=true,timeout=100}
	assert(status.timeout)
	local pstatus,status=con:wait_status_pcall{msg=true,timeout=100,timeout_error=true}
	assert(status.etype=='timeout')
end
function tests.msgfuncs()
	-- test script not running
	local status,err=con:write_msg_pcall("test")
	assert((not status) and err.etype == 'msg_notrun')
	-- test flushmsgs
	con:exec('write_usb_msg("msg1") return 2,3')
	con:wait_status{run=false}
	status = con:script_status()
	assert(status.msg == true)
	con:flushmsgs()
	status = con:script_status()
	assert(status.msg == false)
	con:exec('write_usb_msg("msg2") return 1')
	local m=con:wait_msg({mtype='user'})
	assert(m.type=='user' and m.value == 'msg2')
	m=con:wait_msg({mtype='return'})
	assert(m.type=='return' and m.value == 1)
	status,err=pcall(con.wait_msg,con,{mtype='return',timeout=100})
	assert(err.etype=='timeout',tostring(err))
	con:exec('return 1')
	status,err=pcall(con.wait_msg,con,{mtype='user'})
	assert(err.etype=='wrongmsg',tostring(err))
end
function tests.filexfer()
	local ldir='camtest'
	for i,size in ipairs({511,512,4096}) do
		local fn=string.format('test%d.dat',size)
		local lfn=string.format('%s/%s',ldir,fn)
		local dfn=string.format('%s/d_%s',ldir,fn)
		local s1=string.rep('x',size)
		m.makelocalfile(lfn,s1)
		m.cliexec('u '..lfn)
		m.cliexec('d '..fn .. ' ' .. dfn)
		local s2=m.readlocalfile(dfn)
		assert(s1==s2)
		m.cliexec('rm '..fn)
	end
	fsutil.rm_r(ldir)
end

function tests.mfilexfer()
	local ldir='camtest'
	-- names are in caps since cam may change, client may be case sensitive
	m.makelocalfile(ldir..'/up/EMPTY.TXT','')
	m.makelocalfile(ldir..'/up/ONE.TXT','one')
	m.makelocalfile(ldir..'/up/SUB1/SUB.TXT',string.rep('subtext',1000))
	fsutil.mkdir_m(ldir..'/up/EMPTYSUB')
	m.cliexec('mup '..ldir..'/up muptest')
	m.cliexec('mdl muptest '..ldir..'/dn')
	m.comparefiles(ldir..'/up/EMPTY.TXT',ldir..'/dn/EMPTY.TXT')
	m.comparefiles(ldir..'/up/ONE.TXT',ldir..'/dn/ONE.TXT')
	m.comparefiles(ldir..'/up/SUB1/SUB.TXT',ldir..'/dn/SUB1/SUB.TXT')
	m.comparefiles(ldir..'/up/EMPTYSUB',ldir..'/dn/EMPTYSUB')
	m.cliexec('rm muptest')
	-- test on non-existing dir
	local s=m.cliexec_ret_fail('mdl muptest '..ldir)
	assert(string.sub(s,1,10) == 'A/muptest:') -- exact message varies by cam
	fsutil.rm_r(ldir)
end

function tests.msgs()
	local mt=require'extras/msgtest'
	assert(mt.test({size=1,sizeinc=1,count=100,verbose=0}))
	assert(con:wait_status{run=false})
	assert(mt.test({size=10,sizeinc=10,count=100,verbose=0}))
end

function tests.reconnect()
	assert(con:is_connected())
	m.cliexec('reconnect')
	assert(con:is_connected())
end

function tests.disconnect()
	m.cliexec('dis')
	assert(not con:is_connected())
end

function m.run(name,...)
	printf('%s:start\n',name)
	status,msg = xpcall(tests[name],errutil.format_traceback,...)
	printf('%s:',name)
	if status then
		m.passed = m.passed + 1
		printf('ok\n')
		return true
	else
		m.failed = m.failed + 1
		printf('failed %s\n',msg)
		return false
	end
end

--[[
opts:{
	devspec=<usb device spec> -- specify which device to use, default to first available
	bench=bool -- run "benchmark" tests
	filexfer=bool -- run file transfer tests
}
NOTE
filexfer creates and deletes various hard coded paths, both locally and on the camera
]]
function m.runbatch(opts)
	opts = util.extend_table({},opts)
	-- if connect fails, don't try to run anything else
	m.passed = 0
	m.failed = 0
	if not m.run('connect',opts.devspec) then
		printf('aborted\n')
		return false
	end
	m.run('list_connected')
	m.run('wait_status')
	m.run('exec_errors')
	m.run('msgfuncs')
	if opts.bench then
		m.run('exectimes')
		m.run('xfer')
		m.run('msgs')
	end
	if opts.filexfer then
		m.run('filexfer')
		m.run('mfilexfer')
	end
	m.run('reconnect')
	m.run('disconnect')
	m.run('not_connected')
	printf("passed %d\nfailed %d\n",m.passed,m.failed)
	return m.failed == 0
end

return m
