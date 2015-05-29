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
a script for stressing the usb layer and message system

usage:
!m=require'extras/msgtest'
!m.test(options)
opions:{
	size=number     -- initial message size
	sizemax=number  -- end message size
	sizestep=number -- increment size by N
	count=number    -- number of messages
	verbose=number  -- level of verbosity, 2 = print a line for each message
	checkmem=bool   -- check free memory and lua allocated memory for each message
	memverbose=bool -- print memory stats for each message
	gc=string|nil   -- garbage collection mode, 'step', 'collect' or nil
}
example
!m.test{size=100,sizeinc=10,sizemax=200,verbose=0,memverbose=true,checkmem=true,gc='step'}
]]
local m={}

local default_opts = {
	verbose = 2,
	checkmem = false,
	memverbose = false,
	gc = nil,
}

m.opts = {}

m.detailmsg = util.make_msgf( function() return m.opts.verbose end, 2)

function m.init_test()
	m.fail_count = 0
	m.run_count = 0
	if m.opts.checkmem then
		m.memstats = {
			free={},
			count={}
		}
	end
	m.load()
	m.set_gc(m.opts.gc)
	m.t0=ustime.new()
	return true
end

function m.fmt_memstats(stats)
	local min=1000000000
	local max=0 
	local total = 0
	if #stats == 0 then
		return "no stats"
	end

	for i,v in ipairs(stats) do
		if v > max then
			max = v
		end
		if v < min then
			min = v
		end
		total = total + v
	end
	return string.format("min %d max %d avg %d",min, max, total/#stats)
end

function m.finish_test()
	m.quit()
	printf("ran %d fail %d time %.4f\n",m.run_count,m.fail_count,ustime.diff(m.t0)/1000000)
	if m.opts.checkmem then
		printf("free   (bytes): %s\n",m.fmt_memstats(m.memstats.free))
		printf("lua alloc (kb): %s\n",m.fmt_memstats(m.memstats.count))
	end
	return (m.fail_count == 0)
end

function m.load()
	con:exec('msg_shell:run()',{libs={'msg_shell','serialize'}})
	con:write_msg([[exec
msg_shell.read_msg_timeout = nil
msg_shell.default_cmd=function(msg)
	if msgtest_gc then
		collectgarbage(msgtest_gc)
	end
	write_usb_msg(msg)
end
msg_shell.cmds.memstats=function()
	write_usb_msg(serialize({mem=get_meminfo().free_size,lmem=collectgarbage('count')}))
end
]])
end

function m.quit()
	con:write_msg('quit')
end

function m.test_msg(len)
	m.run_count = m.run_count + 1
	local s=string.rep('x',len)
	con:write_msg(s)
	local r = con:wait_msg({mtype='user'})
	if s == r.value then 
		m.detailmsg('ok\n')
	else
		m.fail_count = m.fail_count + 1
		printf('failed\nmsg %d len %d not equal\n',m.run_count,len)
	end
	if m.opts.checkmem then
		con:write_msg('memstats')
		r = con:wait_msg({mtype='user',munserialize=true})
		table.insert(m.memstats.free,r.mem)
		table.insert(m.memstats.count,r.lmem)
		if m.opts.memverbose then
			printf('free:%d lua alloc:%d kb\n',r.mem,r.lmem)
		end
	end
end

function m.test(opts)
	opts = util.extend_table(util.extend_table({},default_opts),opts)
	
	m.opts = opts

	if not opts.size then 
		error("missing size")
	end

	if not opts.count then
		if opts.sizeinc and opts.sizemax then
			opts.count = math.floor((opts.sizemax - opts.size )/opts.sizeinc)
		else
			error("missing count")
		end
	end
	if opts.sizeinc == 0 then
		opts.sizeinc = nil
	end

	if opts.sizeinc and not opts.sizemax then
		opts.sizemax = opts.size + opts.count * opts.sizeinc
	end

	local size = opts.size

	printf("testing %d messages size %d",opts.count,size)
	if opts.sizeinc and opts.sizeinc > 0 then
		printf("-%d, inc %d",opts.sizemax,opts.sizeinc)
	end
	printf("\n")
	m.init_test()
	for i=1,opts.count do
		m.detailmsg("send %d...",i)
		local status,err=pcall(m.test_msg,size)
		if not status then
			printf("%s\n",tostring(err))
			printf("aborted, communication error\n")
			m.finish_test()
			return false
		end
		if opts.sizeinc and size < opts.sizemax then
			size = size + opts.sizeinc
		end
	end 
	return m.finish_test()
end

function m.set_gc(mode)
	if not mode then
		mode='nil'
	else
		mode = '"'..mode..'"'
	end
	con:write_msg('exec msgtest_gc='..mode)
end
return m
