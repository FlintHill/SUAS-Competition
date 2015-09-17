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
stats collector for live view
]]
local counter_proto = {
	hist_size=10,
}
function counter_proto.new(init)
	local t=util.extend_table({},counter_proto)
	util.extend_table(t,init)
	t.t_start=ustime.new()
	t:reset()
	return t
end
function counter_proto:reset()
	self.times={}
	self.r_times={} -- repeat times = time between starts 
	self.count=0
end
function counter_proto:start()
	if self.count > 0 then
		self.r_times[self.cur_index] = self.t_start:diffms()
	end
	self.t_start:get()
	self.count = self.count + 1
	self.cur_index = math.floor(self.count%self.hist_size)
end

function counter_proto:finish()
	self.times[self.cur_index] = self.t_start:diffms()
end

function counter_proto:last_time()
	return self.times[self.cur_index]
end

function counter_proto:last_r_time()
	return self.r_times[self.cur_index]
end

-- ensure a usable value is returned
function counter_proto.avg(t)
	local m=util.table_amean(t)
	if not m or m == 0 then
		return 0.1
	end
	return m
end

function counter_proto:avg_time()
	return self.avg(self.times)
end

function counter_proto:avg_r_time()
	return self.avg(self.r_times)
end

local stats={
	frames=counter_proto.new(),
	xfer=counter_proto.new({
		reset=function(self)
			counter_proto.reset(self)
			self.bytes={}
		end,
		finish=function(self,bytes)
			counter_proto.finish(self)
			self.bytes[self.cur_index] = bytes
		end,
		avg_bytes=function(self)
			return self.avg(self.bytes)
		end,
		last_bytes=function(self)
			return self.bytes[self.cur_index]
		end,
	}),
}


function stats:init_counters()
	self.frames:reset()
	self.xfer:reset()
end

stats:init_counters()

function stats:start()
	if self.run then
		return
	end
	self:init_counters()
	self.run = true
end
function stats:stop()
	if not self.run then
		return
	end
	self.run = false
end

function stats:start_frame()
	self.frames:start()
end

function stats:end_frame()
	self.frames:finish()
end
function stats:start_xfer()
	self.xfer:start()
end
function stats:end_xfer(bytes)
	self.xfer:finish(bytes)
end

function stats:get_last_total_ms()
	return self.frames:last_time() + self.xfer:last_time() 
end

function stats:get()
	local run

	if self.run then
		run = "yes"
	else
		run = "no"
	end
	
	local fps_avg = 0
	local frame_time = 0
	local tp_bps_avg = 0
	local bps_avg = 0
	local xfer_avg = 0
	local xfer_time = 0
	local xfer_bytes = 0
	if self.frames.count > 1 then
		fps_avg = 1000/self.frames:avg_r_time()
		frame_time = self.frames:last_time()
	end

	if self.xfer.count > 1 then
		local avg_bytes = self.xfer:avg_bytes()
		-- total throughput (against wall time)
		tp_bps_avg = 1000*avg_bytes/self.xfer:avg_r_time()
		-- actual transfer bps
		bps_avg = 1000*avg_bytes/self.xfer:avg_time()
		xfer_time = self.xfer:last_time()
		xfer_bytes = self.xfer:last_bytes()
	end

	-- TODO this rapidly spams lua with lots of unique strings
	return string.format(
[[Running: %s
FPS: %0.2f
Frame last ms: %d
T/P kb/s: %d
Xfer last ms: %d
Xfer kb: %d
Xfer kb/s: %d]],
		run,
		fps_avg,
		frame_time,
		tp_bps_avg/1024,
		xfer_time,
		xfer_bytes/1024,
		bps_avg/1024)
end

return stats
