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
module for gui timer/scheduler
]]
local m={
	now=ustime.new(),
	pending={},
	repeating={},
}
function m.ensure_timer_running()
	if not m.timer then
		error('gui_sched timer not initialized')
	end
	if m.timer.run ~= 'YES' then
		m.timer.run = 'YES'
	end
end
--[[
call scheduled function after time ms
]]
function m.run_after(time,fn,data)
	local t=ustime.new()
	t:addms(time)
	table.insert(m.pending,{time=t,fn=fn,data=data})
	m.ensure_timer_running()
end
function m.run_repeat(time,fn,data)
	t = {
		last=ustime.new(),
		time=time,
		fn=fn,
		data=data,
	}
	t.cancel=function(self)
		m.repeating[t]=nil
	end
	m.repeating[t] = t
	m.ensure_timer_running()
	return t
end

m.tick=errutil.wrap(function()
	m.now:get()
	local num_pending = 0
	for k,v in pairs(m.pending) do
--		printf('check %f %f\n',v.time:float(),m.now:float())
		if v.time:float() < m.now:float() then
--			printf('run\n')
			m.pending[k]=nil
			v:fn()
		else
			num_pending = num_pending + 1
		end
	end
	local num_repeating = 0
	for k,v in pairs(m.repeating) do
		if v.last:diffms(now) > v.time then
			v.last:get() -- TODO might want to check for run time > interval to avoid pile-up
						-- could update after run
			v:fn()
		end
		num_repeating = num_repeating + 1
	end
	-- stop running timer if no jobs
	if num_pending == 0 and num_repeating == 0 then
		m.timer.run = "NO"
	end
end)

function m.init_timer(time)
	if not time then
		time = 50
	end 
	if m.timer then
		iup.Destroy(m.timer)
	end
	m.timer = iup.timer{ 
		time = tostring(time),
		action_cb = m.tick,
		run = "NO", -- first scheduled action will start
		-- note for some reason, creating with YES fails occasionally, setting after seems OK
	}
end
return m
