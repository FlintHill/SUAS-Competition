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
error handling utilities
]]

local m={
	last_traceback='',
 	-- when to include a traceback 'always', 'never', 'critical'
	-- crit means string errors (thrown with error(...) rather than throw)
	-- or error objects with crit set
	do_traceback='critical',
}
--[[
handler for xpcall
formats the error message with or without a traceback depending on settings
if thrown error object includes traceback, uses it, otherwise attempts to get a new one
--]]
function m.format(err)
	return m.format_f(err,m.do_traceback)
end
function m.format_traceback(err)
	return m.format_f(err,'always')
end
function m.format_f(err,do_traceback)
	-- not an error object, try to backtrace
	if do_traceback == 'never' then
		return tostring(err)
	end
	if type(err) == 'string' then
		m.last_traceback = debug.traceback('',3)
		return err ..  m.last_traceback
	end
	if type(err) ~= 'table' then
		err = string.format('unexpected error type %s [%s]',type(err),tostring(err))
		m.last_traceback = debug.traceback('',3)
		return err .. m.last_traceback
	end
	if not err.traceback or type(err.traceback) ~= 'string' then
		err.traceback = debug.traceback('',3)
	end
	m.last_traceback = err.traceback
	if do_traceback == 'always' or err.critical then
		return tostring(err) .. err.traceback
	end
	return tostring(err)
end
--[[
wrap in function that calls with xpcall and prints errors, or returns values
opts:{
	err_default:value - value other than nil to return on error
	output:function - receives formatted error messages, default util.errf("%s\n",err)
	handler:function - handles/formats error, default m.format
]]
function m.default_err_output(err)
	util.errf('%s\n',tostring(err))
end
function m.wrap(f,opts)
	opts=util.extend_table({
		output=m.default_err_output,
		handler=m.format,
	},opts)
-- in 5.1, xpcall can't pass args
	if util.is_lua_ver(5,1) then
		return function(...)
			local args = {...}
			local r={xpcall(function() return f(unpack(args,1,table.maxn(args))) end,opts.handler)}
			if not r[1] then
				if opts.output then
					opts.output(tostring(r[2]))
				end
				if type(opts.err_default) ~= 'nil' then
					return opts.err_default
				end
				return
			end
			if table.maxn(r) > 1 then
				return unpack(r,2,table.maxn(r))
			end
		end
	else
		return function(...)
			local r={xpcall(f,opts.handler,...)}
			if not r[1] then
				if opts.output then
					opts.output(tostring(r[2]))
				end
				if type(opts.err_default) ~= 'nil' then
					return opts.err_default
				end
				return
			end
			if table.maxn(r) > 1 then
				return unpack(r,2,table.maxn(r))
			end
		end
	end
end
return m
