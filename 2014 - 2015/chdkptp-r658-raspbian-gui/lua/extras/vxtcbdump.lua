--[[
 Copyright (C) 2012-2013 <reyalp (at) gmail dot com>

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
module for displaying vxworks tcb dumps
format is
char taskname[10]
tcb
]]

local lbu=require'lbufutil'

local m = {}
m.tcb_size = 400 -- as defined in chdk vxworks.h
-- original version
-- m.rec_size = 10 + m.tcb_size -- name
m.rec_size = 16 + m.tcb_size -- task id, name + 2 struct alignment padding

m.regs = {
	'r0',
	'r1',
	'r2',
	'r3',
	'r4',
	'r5',
	'r6',
	'r7',
	'r8',
	'r9',
	'r10',
	'r11',
	'r12',
	'sp',
	'lr',
	'pc',
	'cpsr',
}

m.task_states = {
	[0]='ready',
	'suspend',
	'pending',
	'delay',
	'dead'
}
local tcb_methods = {}
function tcb_methods.print_regs(self)
	for _,rname in ipairs(m.regs) do
		printf('%4s: 0x%08x %u\n',rname,self[rname],self[rname])
	end
end

function tcb_methods.describe_state(self)
	local sbits = util.bit_unpack(self.state)
	local r={}
	for i=0,#m.task_states-1 do 
		if sbits[i] == 1 then
			table.insert(r,m.task_states[i])
		end
	end
	return table.concat(r,', ')
end
function tcb_methods.print(self)
	printf('%s:\n',self.namestr)
	printf('state: 0x%x %s\n',self.state,self:describe_state())
	for _, fname in ipairs({'options','priority','entry','stack_base','stack_limit','stack_end','error_num','exit_code'}) do
		printf('%12s: 0x%08x %u\n',fname,self[fname],self[fname])
	end
	printf('context:\n')
	self:print_regs()
end
function m.bind_tcb(d,index)
	local off = (index-1)*m.rec_size
	local ti = lbu.wrap(d._lb)
	ti.offset = off
	ti:bind_seek('set',off)
	ti:bind_u32('task_id')
	ti:bind_sz('namestr',10)
	ti:bind_seek('cur',2) -- padding in struct
 	-- unknown1
	ti:bind_seek('cur',13*4)
	ti:bind_u32('name')
	ti:bind_u32('options')
	ti:bind_u32('state')
	ti:bind_u32('priority')
 	-- unknown2
	ti:bind_seek('cur',12*4)
	ti:bind_u32('entry')
	ti:bind_u32('stack_base')
	ti:bind_u32('stack_limit')
	ti:bind_u32('stack_end')
	ti:bind_u32('error_num')
	ti:bind_u32('exit_code')
 	-- unknown3
	ti:bind_seek('cur',7*4)
	-- file descriptors
	ti:bind_seek('cur',6*4)
 	-- unknown3
	ti:bind_seek('cur',24*4)
	for i, rname in ipairs(m.regs) do
		ti:bind_u32(rname)
	end
	d.byname[ti.namestr] = ti
	d.tasks[index] = ti
	util.extend_table(ti,tcb_methods)
end

local dump_methods = {}
function dump_methods.list_tasks(self)
	for i,tcb in ipairs(self.tasks) do
		printf('%3d: 0x%08x %-10s opt:0x%08x s:0x%08x %s\n',i,tcb.task_id,tcb.namestr,tcb.options,tcb.state,tcb:describe_state())
	end
end
function m.load(name)
	local lb,err=lbu.loadfile(name)
	if not lb then
		return false, err
	end
	local d=lbu.wrap(lb)
	local n = lb:len()/m.rec_size
	local n_tcbs = math.floor(n)
	if n ~= n_tcbs then
		util.warnf("size %f > %d records\n",n,n_tcbs)
	end
	d.byname = {}
	d.tasks = {}
	util.extend_table(d,dump_methods)
	for i=1,n_tcbs do
		local tcb = m.bind_tcb(d,i)
	end
	return d
end

return m
