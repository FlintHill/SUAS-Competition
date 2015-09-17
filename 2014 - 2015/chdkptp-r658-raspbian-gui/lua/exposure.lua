--[[
 Copyright (C) 2010-2012 <reyalp (at) gmail dot com>
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
functions to convert traditional exposure values to and from apex and apex96
for information about APEX see http://dougkerr.net/Pumpkin/#APEX
]]


local m={}

--[[
shutter value in seconds to APEX Tv
]]
function m.shutter_to_tv(sec)
	return -util.log2(sec)
end

function m.tv_to_shutter(tv)
	return 1/(2^tv)
end

function m.tv_to_shutter_str(tv)
	if tv > 0 then
		return string.format("1/%.2f",(2^tv))
	else
		return string.format("%.2f",2^-tv)
	end
end
--[[
ISO (real) value APEX Sv
]]
function m.iso_to_sv(iso)
	return util.log2(iso/3.125)
end

function m.sv_to_iso(sv)
	return (2^sv)*3.125
end

--[[
f/n to APEX Av
]]
function m.f_to_av(f)
	return util.log2(f^2)
end

function m.av_to_f(av)
	return math.sqrt(2^av)
end

local function wrap_to_96(f)
	return function(v)
		return util.round(96*f(v))
	end
end

local function wrap_from_96(f)
	return function(v)
		return f(v/96)
	end
end

m.shutter_to_tv96 = wrap_to_96(m.shutter_to_tv)
m.iso_to_sv96 = wrap_to_96(m.iso_to_sv)
m.f_to_av96 = wrap_to_96(m.f_to_av)

m.tv96_to_shutter = wrap_from_96(m.tv_to_shutter)
m.tv96_to_shutter_str = wrap_from_96(m.tv_to_shutter_str)
m.sv96_to_iso = wrap_from_96(m.sv_to_iso)
m.av96_to_f = wrap_from_96(m.av_to_f)

function m.print_av_table()
	printf("%5s %4s (%4s) f/n\n","Av","Av96","rev");
	for av96=0,960,32 do
		local f=m.av96_to_f(av96)
		local av=m.f_to_av(f)
		local av96x=m.f_to_av96(f)
		printf("%5.2f %4d (%4d) f/%.1f\n",av,av96,av96x,f)
	end
end

function m.print_tv_table()
	printf("%5s %4s (%4s) sec\n","Tv","Tv96","rev");
	for tv96=-576,960,32 do
		local sec=m.tv96_to_shutter(tv96)
		local sec_str=m.tv96_to_shutter_str(tv96)
		local tv=m.shutter_to_tv(sec)
		local tv96x=m.shutter_to_tv96(sec)
		printf("%5.2f %4d (%4d) %8s %12.9f\n",tv,tv96,tv96x,sec_str,sec)
	end
end

function m.print_sv_table()
	printf("%5s %4s (%4s) ISO\n","Sv","Sv96","rev");
	for sv96=384,960,32 do
		local iso=m.sv96_to_iso(sv96)
		local sv=m.iso_to_sv(iso)
		local sv96x=m.iso_to_sv96(iso)
		printf("%5.2f %4d (%4d) %8.2f\n",sv,sv96,sv96x,iso)
	end
end

function m.print_tables()
	m.print_av_table();
	m.print_tv_table();
	m.print_sv_table();
end
return m
