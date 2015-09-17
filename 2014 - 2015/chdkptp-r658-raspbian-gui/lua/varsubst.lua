--[[
 Copyright (C) 2014 <reyalp (at) gmail dot com>

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
utility for substitution strings

substitution strings are of the form
${name} or ${name,args}
]]
local m={}

local methods={}

--[[
expend a single ${} expression
]]
function methods.process_var(self,str)
	-- discard {}
	str=str:sub(2,-2)
	-- extract func name
	local s,e,func=str:find('^([%w]+)')
	-- no match, try args (format is arbitrary)
	local argstr
	if e ~= str:len() then
		s,e,argstr=str:find(',%s*(.*)$')
	end
	if not s then
		error('parse failed '..tostring(str))
	end
	-- recursively expand args, so ${foo, ${bar}} gets expanded
	-- TODO there is no way to prevent any {} from being counted in the %b{}
	if argstr then
		argstr=self:run(argstr)
	end
	if self.funcs[func] then
		return self.funcs[func](argstr,self)
	end
	error('unknown substitution function '..tostring(func))
end

--[[
process a string
--]]
methods.run=function(obj,str)
	local r=str:gsub('$(%b{})',
		function(s)
			return obj:process_var(s)
		end)
	return r
end

--[[
return a function that passes the named value from state through string.format, 
using the first arg as the format string, or default_fmt if not specified
]]
m.format_state_val=function(name,default_fmt)
	return function(argstr,obj)
		if not argstr then 
			argstr=default_fmt
		end
		return string.format(argstr,obj.state[name])
	end
end
--[[
return a function that passes the named value from state through os.date
using the first arg as the date format, or default_fmt if not specified
]]
m.format_state_date=function(name,default_fmt)
	return function(argstr,obj)
		if not argstr then 
			argstr=default_fmt
		end
		return os.date(argstr,obj.state[name])
	end
end

--[[
general purpose ${sprintf,format,arg....}
TODO doesn't have quoting, so format better not contain , or {} or leading spaces
]]
m.sprintf=function(argstr,obj)
	local args=util.string_split(argstr,',%s*')
	return string.format(unpack(args))
end
--[[
funcs={
	name,f(str,obj)
}
state=table containing any state to be used by funcs, keying by func name recommended
--]]
m.new=function(funcs,state)
	local t={
		funcs=funcs,
		state=state,
		run=m.run,
	}
	if not t.state then
		t.state={}
	end
	util.extend_table(t,methods)
	return t
end
return m
