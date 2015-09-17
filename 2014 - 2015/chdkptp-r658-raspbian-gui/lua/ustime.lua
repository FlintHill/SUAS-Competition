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
utilities for working with microsecond time provided by sys.gettimeofday
depends on chdkpt sys
in some windows variants, sys.gettimeofday will return much lower precision, ~15ms
]]

local proto={}

local mt={
	__index=function(t,key)
		return proto[key];
	end,
	-- TODO can add some more methods so regular operators work
}
local ustime={}
--[[
create a new ustime, defaulting to current time
]]
function ustime.new(sec,usec)
-- TODO user values are not normalized
	local t={sec=sec,usec=usec}
	setmetatable(t,mt)
	if not sec then
		t:get()
	elseif not usec then
		t.usec=0
	end
	return t;
end
--[[
return difference as number of microseconds
if only one time is given, subtract from current time
no provision is made for overflow
]]
function ustime.diff(t1,t0)
	local t1_sec, t1_usec
	if t0 then
		t1_sec,t1_usec = t1.sec,t1.usec
	else
		t0 = t1
		-- get times directly rather than creating a new ustime object
		t1_sec,t1_usec = sys.gettimeofday()
	end
	return (t1_sec - t0.sec)*1000000 + t1_usec - t0.usec
end

--[[
difference in ms
]]
function ustime.diffms(t1,t0)
	return ustime.diff(t1,t0)/1000
end

--[[
formate with os.date with additional formats
%_m = milliseconds part
%_u = microseconds part
]]
function ustime.format(t,fmt)
	if fmt then
		fmt = fmt:gsub('%%_([um])',function(c)
			if c == 'u' then
				return string.format('%06d',t.usec)
			end
			if c == 'm' then
				return string.format('%03d',t.usec/1000)
			end
		end)
	end
	return os.date(fmt,t.sec)
end

function proto:get()
	self.sec,self.usec = sys.gettimeofday()
end

-- assumes number is double
-- TODO why didn't I just do the whole thing in floating point ?
function proto:normalize()
	local v = (self.sec + self.usec/1000000)
	self.sec = math.floor(v)
	self.usec = (v - self.sec)*1000000
end

function proto:addus(us)
	self.usec = self.usec + us
	self:normalize()
end

function proto:addms(ms)
	self:addus(1000*ms)
end

function proto:float()
	return (self.sec + self.usec/1000000)
end

proto.diff = ustime.diff
proto.diffms = ustime.diffms
proto.format = ustime.format

return ustime
