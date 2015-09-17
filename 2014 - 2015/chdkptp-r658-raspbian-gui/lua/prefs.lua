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
simple system for handling prefrences
]]
local m={}
-- preference objects
local prefs={}
-- array to order them
local order={}
-- unregistered pref values to be picked up on later _add calls
local unreg={}
-- accept unregistered or error?
local allow_unreg

local vtypes={
	boolean={
		-- allow "true" "false", 0,1
		parse=function(val)
			val = val:lower()
			if val == 'true' or tonumber(val) == 1 then
				return true,true
			end
			if val == 'false' or tonumber(val) == 0 then
				return true,false
			end
			return false,"invalid value"
		end,
	},
	string={
		parse=function(val)
			return true,val
		end,
	},
	number={
		parse=function(val)
			local v = tonumber(val)
			if v then
				return true,v
			end
			return false,"invalid value"
		end,
	},
}
local function read_val(vtype,val)
	if not vtypes[vtype] then 
		return false,'unknown vtype: '..tostring(vtype)
	end
	if type(val) == vtype then
		return true,val
	end
	if type(val) ~= 'string' then
		return false,'invalid type '..type(val)
	end
	return vtypes[vtype].parse(val)
end

function m._add(name,vtype,desc,default,get_fn,set_fn)
	if type(name) ~= 'string' then 
		error('pref name must be string')
	end
	if m[name] then
		error('pref name conflicts with method: '..tostring(name))
	end
	if not desc then
		desc = ''
	end
	if default==nil then
		default=false
	end
	if unreg[name] then
		default=unreg[name]
		unreg[name]=nil
	end
	local status,val = read_val(vtype,default)
	if not status then
		error(val)
	end
	table.insert(order,name)
	local p={
		vtype=vtype,
		desc=desc,
		default=val,
		set=set_fn,
		get=get_fn,
	}
	if p.set==nil then
		p.set = function(self,val)
			self.value=val
		end
	end
	if p.get==nil then
		p.get = function(self)
			return self.value
		end
	end
	prefs[name]=p
	p:set(val)
end
function m._each()
	local i=0
	return function()
		i = i + 1
		return order[i],prefs[order[i]]
	end
end

function m._describe(name,mode)
	if not prefs[name] then
		return false,'invalid pref: '..tostring(name)
	end
	local r=string.format('%s=%s',name,tostring(prefs[name]:get()))
	if mode == 'full' then
		r=string.format('%-20s - %s: %s',r,prefs[name].vtype,prefs[name].desc)
	elseif mode == 'cmd' then
		r='set '..r
	end
	return true,r
end
function m._set(name,value)
	if value == nil then
		value = false
	end
	local p = prefs[name]
	if p then
		local status,value = read_val(p.vtype,value)
		if status then
			local status,msg=p:set(value)
			-- nil is treated as OK, so setters don't have to return a value
			-- only explicit false returns error
			if status or status == nil then
				return true
			end
			return false,msg
		end
		return false,value
	end
	if allow_unreg then
		unreg[name] = value
		return true
	end
	return false,'invalid pref: ' .. tostring(name)
end
function m._allow_unreg(allow)
	allow_unreg = allow
end
function m._get(name)
	if prefs[name] then
		return true,prefs[name]:get()
	end
	return false,'invalid pref: ' .. tostring(name)
end

local mt={
	__index=function(t,k)
		-- methods
		if m[k] then
			return m[k]
		end
		local status,val = m._get(k)
		if status then
			return val
		end
		error(val)
	end,
	__newindex=function(t,k,v)
		local status,err = m._set(k,v)
		if not status then
			error(err)
		end
	end
}
local proxy = {}
setmetatable(proxy,mt)
return proxy
