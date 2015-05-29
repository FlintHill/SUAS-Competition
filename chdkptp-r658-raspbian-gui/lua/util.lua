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
common generic lua utilities
utilities that depend on the chdkptp api go in chdku
]]
local util={}

--[[
to allow overriding, e.g. for gui
--]]
util.util_stderr = io.stderr
util.util_stdout = io.stdout

-- return version components as numbers
-- _VERSION does not usally contain final (release) number
function util.lua_version()
	if type(_VERSION) ~= 'string' then
		error('missing _VERSION')
	end
	local major,minor = string.match(_VERSION,'(%d+)%.(%d+)')
	return tonumber(major),tonumber(minor)
end

util.lua_ver_major,util.lua_ver_minor = util.lua_version()

function util.is_lua_ver(major,minor)
	return (major == util.lua_ver_major and minor == util.lua_ver_minor)
end

function util.fprintf(f,...)
	local args={...}
	if #args == 0 or type(args[1]) ~= 'string' then
		args[1]=''
	end
	f:write(string.format(unpack(args)))
end

function util.printf(...)
	fprintf(util.util_stdout,...)
end

function util.warnf(format,...)
	fprintf(util.util_stderr,"WARNING: " .. format,...)
end

function util.errf(format,...)
	fprintf(util.util_stderr,"ERROR: " .. format,...)
end

--[[
force reload a module
]]
function util.forcerequire(modname,...)
	package.loaded[modname] = nil
	return require(modname,...)
end
--[[
log2(n) = log(n)/log(2)
]]
function util.log2(n)
	return math.log(n)/0.693147180559945
end
--[[
round to nearest int, away from 0
]]
function util.round(n)
	local f=math.floor(n)
	if n > 0 then
		if n-f < 0.5 then
			return f
		end
		return math.ceil(n)
	else
		if n-f > 0.5 then
			return math.ceil(n)
		end
		return f
	end
end

--[[
return a function that prints if result of curlevel_fn is greater than vlevel
for making different areas of code have different verbosity
]]
function util.make_msgf(curlevel_fn,fixed_level)
	if type(curlevel_fn) ~= 'function' then
		error('expected function')
	end
	if type(fixed_level) == 'nil' then
		-- return a function that expects a verbosity level as the first arg, e.g.
		-- myprint(1,"foo")
		return function(vlevel,format,...)
			if curlevel_fn() >= vlevel then
				util.printf(format,...)
			end
		end
	elseif tonumber(fixed_level) then
		-- return a function that only prints at fixed level, e.g
		-- myprint("foo")
		return function(format,...)
			if curlevel_fn() >= fixed_level then
				util.printf(format,...)
			end
		end
	else
		error('invalid type')
	end
end

function util.err_traceback(err)
	return debug.traceback(err,2)
end

util.extend_table_max_depth = 10
local extend_table_r
extend_table_r = function(target,source,seen,depth) 
	if not seen then
		seen = {}
	end
	if not depth then
		depth = 1
	end
	if depth > util.extend_table_max_depth then
		error('extend_table: max depth');
	end
	-- a source could have references to the target, don't want to do that
	seen[target]=true
	if seen[source] then
		error('extend_table: cycles');
	end
	seen[source]=true
	for k,v in pairs(source) do
		if type(v) == 'table' then
			if type(target[k]) ~= 'table' then
				target[k] = {}
			end
			extend_table_r(target[k],v,seen,depth+1)
		else
			target[k]=v
		end
	end
	return target
end

--[[ 
copy members of source into target
by default, not deep so any tables will be copied as references
returns target so you can do x=extend_table({},...)
opts
	deep=bool - copy recursively
	keys={key,key...} - copy only specified subset of keys, if key in source is unset, target is unchanged
if deep, cycles result in an error
deep does not copy keys which are themselves tables (the key will be a reference to the original key table)
]]
function util.extend_table(target,source,opts)
	if not opts then
		opts={}
	end
	if type(target) ~= 'table' then
		error('extend_table: target not table')
	end
	if source == nil then -- easier handling of default options
		return target
	end
	if type(source) ~= 'table' then 
		error('extend_table: source not table')
	end
	if source == target then
		error('extend_table: source == target')
	end
	if opts.deep then
		return extend_table_r(target, source)
	elseif opts.keys then -- copy only specific keys
		for i,k in ipairs(opts.keys) do
			if type(source[k]) == 'table' and opts.deep then
				if type(target[k]) ~= 'table' then
					target[k]={}
				end
				extend_table_r(target[k],source[k])
			elseif source[k] ~= nil then
				target[k] = source[k]
			end
		end
	else
		for k,v in pairs(source) do
			target[k]=v
		end
	end
	return target
end

--[[
swap keys and values
dupe values will be lost
]]
function util.flip_table(t)
	local r={}
	for k,v in pairs(t) do
		r[v]=k
	end
	return r
end
--[[
compare v1 and v2
table values are compared recursively, returning true if all key/values in v2 exist in v1
]]
util.compare_values_subset_defaults = {
	maxdepth=10
}
function util.compare_values_subset(v1,v2,opts,seen,depth)
	if not depth then
		depth=1
		opts = util.extend_table(util.extend_table({},util.compare_values_subset_defaults),opts)
	elseif depth > opts.maxdepth then
		error('compare_values_subset: maxdepth exceeded')
	end

	if v1 == v2 then
		return true
	end
	-- if not exactly equal, check table
	if type(v2) ~= 'table' or type(v1) ~= 'table' then
		return false
	end

	if not seen then
		seen={}
	elseif seen[v2] then
		error('compare_values_subset: cycle')
	end
	-- TODO this is restrictive, t={}, t2={t,t} will be treated as cycle
	seen[v2] = true

	for k,v in pairs(v2) do
		if not util.compare_values_subset(v,v1[k],opts,seen,depth+1) then
			return false
		end
	end
	return true
end
--[[
compare v1 and v2
tables are recursively checked for identical keys and values
]]
function util.compare_values(v1,v2,opts)
	if util.compare_values_subset(v1,v2,opts) then
		return util.compare_values_subset(v2,v1,opts)
	end
	return false
end

--[[
does table have value in it ?
]]
function util.in_table(table,value)
	if table == nil then
		return false
	end
	for k,v in pairs(table) do
		if v == value then
			return true
		end
	end
end

function util.table_amean(table)
	if #table == 0 then
		return nil
	end
	local sum = 0
	for i=1,#table do
		sum = sum + table[i]
	end
	return sum/#table
end

--[[
return table with sum, min, max, mean and standard deviation of values in table
all values are nil if table is empty
]]
function util.table_stats(table)
	if #table == 0 then
		return {}
	end
	local sum = 0
	local min = table[1]
	local max = table[1]
	for i=1,#table do
		sum = sum + table[i]
		if table[i] < min then
			min = table[i]
		end
		if table[i] > max then
			max = table[i]
		end
	end
	local mean = sum/#table
	local vsum = 0
	for i=1,#table do
		vsum = vsum + (table[i] - mean)^2
	end
	return {
		min=min,
		max=max,
		sum=sum,
		mean=mean,
		sd=math.sqrt(vsum/#table)
	}
end

--[[
--turn an integer into a zero based array of bits
--]]
function util.bit_unpack(n,limit)
	if not limit then
		limit = 31
	end
	local t={}
	n=math.floor(n)
	for i=0,limit do
		t[i]=n%2
		n=math.floor(n/2)
	end
	return t
end

function util.bit_packu(bits)
	local r=0
	local limit = #bits
	if limit > 31 then
		limit = 31
	end
	for i=0,limit do
		r = r + bits[i]*2^i
	end
	return r
end
--[[
--pack a 0 based array of bits into a string
--]]
function util.bit_packstr(bits)
	local bpos = 0
	local bitval = 1
	local byte = 0
	local i = 0
	local out = {}
	while bits[i] do
		if bits[i] == 1 then
			byte = byte + bitval
		end
		if bpos < 7 then
			bpos = bpos + 1
			bitval = bitval*2
		else
			table.insert(out,string.char(byte))
			bpos = 0
			bitval = 1
			byte = 0
		end
		i = i + 1
	end
	-- final incomplete value, will be padded with 0s
	if bpos ~= 0 then
		table.insert(out,string.char(byte))
	end
	return table.concat(out)
end

function util.bit_unpackstr(str)
	local bytes = {string.byte(str,1,-1)}
	local r = {}
	local o = 0
	for _,b in ipairs(bytes) do
		bits = util.bit_unpack(b,7)
		for j=0,7 do
			r[o]=bits[j]
			o = o + 1
		end
	end
	return r
end

function util.bit_unpacked_fmt(t)
	local b = {}
	local r = {}
	local bi=0
	for i=0,#t do
		table.insert(b,t[i])
		bi = bi + 1
		if bi==8 then
			table.insert(r,string.reverse(table.concat(b)))
			b={}
			bi=0
		end
	end
	if #b ~= 0 then
		for i=#b,7 do
			table.insert(b,'-')
		end
		table.insert(r,string.reverse(table.concat(b)))
	end
	return table.concat(r,' ')
end

--[[
concatinate numeric indexed elements of dst onto the end of src
]]
function util.array_cat(dst,src,opts)
	opts = util.extend_table({
		start=1,
		last=#src,
		dststart=#dst+1,
	},opts)
	local di = opts.dststart
	for i=opts.start,opts.last do
		dst[di] = src[i]
		di = di+1
	end
	return dst
end

--[[
return a slice of numeric indexed elements of an array
]]
function util.array_slice(t,opts)
	opts = util.extend_table({
		start=1,
		last=#t,
		rstart=1,
	},opts)
	local r={}
	local ri = opts.rstart
	for i=opts.start,opts.last do
		r[ri] = t[i]
		ri = ri+1
	end
	return r
end

--[[
convert values of an array to table of value=true
]]
function util.flag_table(t)
	local r={}
	for i,v in ipairs(t) do
		r[v]=true
	end
	return r
end

--[[
return a (sub)table value with path indicated by arrray, e.g. 
table_path_get(t,'a','b','c') returns t.a.b.c
missing subtables in path return nil, like a missing value
]]
function util.table_path_get(t,...)
	return util.table_pathtable_get(t,{...})
end
function util.table_pathtable_get(t,keys)
	local sub=t
	for i,key in ipairs(keys) do
		local v = sub[key]
		if i == #keys then
			return v
		end
		-- missing subtables are treated as nil
		if type(v) == 'nil' then
			return v
		end
		if type(v) ~= 'table' then
			error('expected table for '..table.concat(keys,'.',1,i))
		end
		sub = v
	end
end
--[[
return a (sub)table value indexed by a string like foo.bar
note numbers will be treated as string indexes
]]
function util.table_pathstr_get(t,keystr)
	return util.table_pathtable_get(t,util.string_split(keystr,'.',{plain=true}))
end

--[[
sort a table by nested subtable values
cmp is a function, or one of 'asc', 'des' or nil (=asc)
]]
function util.table_path_sort(t,path,cmp)
	-- default, low to high like lua default
	if not cmp or cmp == 'asc' then
		cmp = function(a,b)
			return a < b
		end
	elseif cmp == 'des' then
		cmp = function(a,b)
			return a > b
		end
	end
	table.sort(t,function(a,b)
		return cmp(util.table_pathtable_get(a,path),util.table_pathtable_get(b,path))
	end)
end
--[[
split str delimited by pattern pat, or plain text if opts.plain
empty pat splits chars
trailing delimiters generate empty strings
with func, iterate over split strings
]]
function util.string_split(str,pat,opts)
	opts = util.extend_table({
		plain=false,
		start=1,
		empty=true, -- include empty strings from multiple / trailing delimiters (default func only)
	},opts)
	local r = {}
	local pos = opts.start
	local s,e 
	if not opts.func then
		opts.func = function(v)
			if string.len(v) > 0 or opts.empty then
				table.insert(r,v)
			end
		end
	end
	if string.len(pat) == 0 then
		while true do
			local c = string.sub(str,pos,pos)
			if string.len(c) == 0 then
				return r
			end
			pos = pos+1
			opts.func(c)
		end
	end

	while true do
		s, e = string.find(str,pat,pos,opts.plain)
		if not s then
			opts.func(string.sub(str,pos,-1))
			break
		end
		opts.func(string.sub(str,pos,s-1))
		pos = e + 1
	end

	return r
end

--[[
very simple meta-table inheritance
]]
function util.mt_inherit(t,base)
	local mt={
		__index=function(table, key)
			return base[key]
		end
	}
	setmetatable(t,mt)
	return t
end

function util.hexdump(str,offset)
	local c, result, byte
	if not offset then
		offset = 0
	end
	c = 0
	result = ''
	for i=1,#str do
		if c == 0 then
			result = result .. string.format("%8x: ",offset)
		end
		result = result .. string.format("%02x ",string.byte(str,i))
		c = c + 1
		if c == 16 then
			c = 0
			offset = offset + 16
			result = result .. "| " .. string.gsub(string.sub(str,i-15,i),'[%c%z%s\128-\255]','.') .. '\n'
		end
	end
	if c ~= 0 then
		for i=1,16-c do
			result = result .. "-- "
		end
		result = result .. "| " .. string.gsub(string.sub(str,-c),'[%c%z%s\128-\255]','.')
	end
	return result
end

-- requires lbuf
function util.hexdump_words(str,offset,fmt)
	if not offset then
		offset = 0
	end
	if not fmt then
		fmt = '0x%08x'
	end
	local lb = lbuf.new(str)
	local s = ''
	for i=0,string.len(str)-4,4 do 
		if i%16 == 0 then
			if i > 1 then
				s = s .. '\n'
			end
			s = s .. string.format('0x%08x:',offset+i)
		end
		s = s..string.format(' '..fmt,lb:get_u32(i))
	end
	return s..'\n'
end

local serialize_r
serialize_r = function(v,opts,r,seen,depth)
	local vt = type(v)
	if vt == 'nil' or  vt == 'boolean' then 
		table.insert(r,tostring(v))
		return
	end
	if vt == 'number' then
		-- camera has problems with decimal constants that would be negative
		if opts.fix_bignum and v > 0x7FFFFFFF then
			table.insert(r,string.format("0x%x",v))
		-- camera numbers are ints
		elseif opts.forceint then
			table.insert(r,string.format("%d",v))
		else
			table.insert(r,tostring(v))
		end
		return
	end
	if vt == 'string' then
		table.insert(r,string.format('%q',v))
		return 
	end
	if vt == 'table' then
		if not depth then
			depth = 1
		end
		if depth >= opts.maxdepth then
			error('serialize: max depth')
		end
		if not seen then
			seen={}
		elseif seen[v] then 
			if opts.err_cycle then
				error('serialize: cycle')
			else
				table.insert(r,'"cycle:'..tostring(v)..'"')
				return 
			end
		end
		-- TODO this is restrictive, t={}, t2={t,t} will be treated as cycle
		seen[v] = true;
		table.insert(r,'{')
		for k,v1 in pairs(v) do
			if opts.pretty then
				table.insert(r,'\n'..string.rep(' ',depth))
			end
			-- more compact/friendly format simple string keys
			-- TODO we could make integers more compact by doing array part first
			if type(k) == 'string' and string.match(k,'^[_%a][%a%d_]*$') then
				table.insert(r,k)
			else
				table.insert(r,'[')
				serialize_r(k,opts,r,seen,depth+1)
				table.insert(r,']')
			end
			table.insert(r,'=')
			serialize_r(v1,opts,r,seen,depth+1)
			table.insert(r,',')
		end
		if opts.pretty then
			table.insert(r,'\n'..string.rep(' ',depth-1))
		end
		table.insert(r,'}')
		return
	end
	if opts.err_type then
		error('serialize: unsupported type ' .. vt, 2)
	else
		table.insert(r,'"'..tostring(v)..'"')
	end
end

util.serialize_defaults = {
	-- maximum nested depth
	maxdepth=10,
	-- ignore or error on various conditions
	err_type=true, -- bad type, e.g. function, userdata
	err_cycle=true, -- cyclic references
	pretty=true, -- indents and newlines
	fix_bignum=true, -- send values > 2^31 as hex, to avoid problems with camera conversion from decimal
	forceint=true, -- convert numbers to integer
}

--[[
serialize lua values
options as documented above
]]
function util.serialize(v,opts)
	local r={}
	serialize_r(v,util.extend_table(util.extend_table({},util.serialize_defaults),opts),r)
	return table.concat(r)
end

--[[
turn string back into lua data by executing it and returning the value
the value is sandboxed in an empty function environment
returns the resulting value, or false + an error message on failure
check the message, since the serialized value might be false or nil!
]]
-- lua 5.1
if type(setfenv) == 'function' then
function util.unserialize(s)
	local f,err=loadstring('return ' .. s)
	if not f then
		return false, err
	end
	setfenv(f,{}) -- empty fenv
	local status,r=pcall(f)
	if status then
		return r
	end
	return false,r
end
else
-- lua 5.2
function util.unserialize(s)
	local f,err=load('return ' .. s,nil,'t',{})
	if not f then
		return false, err
	end
	local status,r=pcall(f)
	if status then
		return r
	end
	return false,r
end
end

--[[
hacky hacky
"import" values from a table into globals
]]
function util.import(t,names)
	if names == nil then
		for name,val in pairs(t) do
			_G[name] = val
		end
		return
	end
	for i,name in ipairs(names) do
		if t[name] ~= nil then
			_G[name] = t[name]
		end
	end
end
return util
