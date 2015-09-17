--[[
usage
!vlog=require'extras/vxromlog'
!l=vlog.load('ROMLOG.LOG)
!l:print()

or
require'extras/vxromlog'.load('ROMLOG.LOG'):print_all()

]]
--[[
forum thread: http://chdk.setepontos.com/index.php?topic=5394.0
a540-ptp-raw-1.1.0.2597.LOG
assert(I think)
3470 bytes
8E 0D 00 00 = 3470

date (looks like fixed length)
2013:03:02 13:23:07\0
01 00 00 00 = (type 1?)
00 00 00 00 = ?
26 01 00 00 = (line number?)
FsIoNotify.c + nulls through offset 67?
2C 2E 1C 0B = task id? at offset 68
tFsIoNotif = task name at offset 72
prio offset 124

stack offset 556 ? (not clear if full dump, but includes debug assert address)

total header 668

a540-invalidmem-romlog.log
exception
size 2,474 bytes
AA 09 00 0B
2013:03:02 19:29:54\0
02 00 00 00
00 00 00 00 = ?
10 00 00 00 = exception type 0x10 data abort
nulls instead of file name
task id at 68?
task name at offset 72
registers start offset 516
stack start 588
size  = 128 = 32 words

total header 716
--]]
local m = {}
local lbu=require'lbufutil'

function m.load(name)
	local lb = lbu.loadfile(name)
	local d=lbu.wrap(lb)
	d:bind_u32('size')
	d:bind_sz('time',20)
	d:bind_u32('type')
	d:bind_u32('unk0')
	if d.type == 1 then -- assert
		d:bind_u32('line') -- line number for assert, exception code for exception
		d:bind_sz('file',32) -- nulls for exception
		d.log_start = 668
		d.stack_start = 556
		d.stack_words = 28
		d.fmt_desc = function(self)
			return string.format('Assert %s line %d\n',self.file,self.line)
		end
	elseif d.type == 2 then -- exception
		d:bind_u32('code') -- exception code
		local enames = {
			[0]='Reset',
			[4]='Undefined instruction',
			[8]='Software interrupt',
			[0xC]='Prefetch abort',
			[0x10]='Data abort',
			[0x18]='IRQ',
			[0x1c]='FIQ',
		}
		local rnames = {
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
		d.reg_start = 516
		local o = d.reg_start
		for i,name in ipairs(rnames) do
			d:bind_u32(name,o)
			o = o + 4
		end
		d.log_start = 716
		d.stack_start = 588
		d.stack_words = 32
		d.fmt_code = function(self)
			if enames[self.code] then
				return enames[self.code]
			end
			return 'Unknown'
		end
		d.fmt_desc = function(self)
			return string.format('Exception vector 0x%x (%s)\n',self.code,self:fmt_code())
		end
		d.fmt_regs = function(self) 
			local o = self.reg_start
			local r = 'Registers:\n'
			for i,name in ipairs(rnames) do
				r = r .. string.format('%-4s 0x%08x %12i\n',name,d[name],d._lb:get_i32(o)) -- TODO direct lbuf to get int
				o = o + 4
			end
			return r
		end
	else
		self.fmt_desc = function(self)
			return string.format('Unknown type %d\n')
		end
	end
	d:bind_u32('task_id',68)
	d:bind_sz('task_name',10)
	d.fmt_stack = function(self)
		if not self.stack_start then
			return string.format('no stack defined\n')
		end
		local o
		local r = ''
		for o = self.stack_start,self.stack_start + 4*(self.stack_words-1),4 do
			r = r..string.format('0x%08x %12d\n',self._lb:get_u32(o),self._lb:get_i32(o))
		end
		return r
	end
	d.fmt_log = function(self)
		if not self.log_start then
			return 'no log defined\n'
		end
		local s = self._lb:string(self.log_start+1) -- :string is 1 based
		s = string.gsub(s,'\r','') -- logs r \r\n
		return s
	end
	d.print = function(self)
		printf(self:fmt_desc())
		printf('Occured at %s\n',self.time)
		printf('Task ID: %d\n',self.task_id)
		printf('Task Name: %s\n',self.task_name)
		if self.fmt_regs then
			printf(self:fmt_regs())
		end
		printf('Stack:\n')
		printf(self:fmt_stack())
	end
	d.print_all = function(self)
		self:print()
		printf('Camera log:\n')
		printf(self:fmt_log())
	end
	return d
end

return m
