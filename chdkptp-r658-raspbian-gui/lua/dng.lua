--[[
 Copyright (C) 2010-2011 <reyalp (at) gmail dot com>

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
utilities for dealing with CHDK DNG images and headers
this is not a fully featured TIFF/TIFF-EP/DNG reader
]]
local m={}
local lbu=require'lbufutil'
--[[
bind the tiff header
--]]
m.header_fields = {
	'byte_order',
	'id',
	'ifd0_off'
}
-- "interesting" tags, i.e. those used in a CHDK dng
m.tags = {
}
m.tags_map = {
	NewSubfileType				=0xfe,
	SubfileType					=0xff,
	ImageWidth					=0x100,
	ImageLength					=0x101,
	BitsPerSample				=0x102,
	Compression					=0x103,
	PhotometricInterpretation	=0x106,
	ImageDescription			=0x10e,
	Make						=0x10f,
	Model						=0x110,
	StripOffsets				=0x111,
	Orientation					=0x112,
	SamplesPerPixel				=0x115,
	RowsPerStrip				=0x116,
	StripByteCounts				=0x117,
	XResolution					=0x11a,
	YResolution					=0x11b,
	PlanarConfiguration			=0x11c,
	ResolutionUnit				=0x128,
	Software					=0x131,
	DateTime					=0x132,
	Artist						=0x13b,

	SubIFDs						=0x14a,

	CFARepeatPatternDim			=0x828d,
	CFAPattern					=0x828e,
	Copyright					=0x8298,

	ExposureTime				=0x829a,
	FNumber						=0x829d,

	ExifIFD						=0x8769,

	ExposureProgram				=0x8822,
	ISOSpeedRatings				=0x8827,
	ExifVersion					=0x9000,
	DateTimeOriginal			=0x9003,
	ShutterSpeedValue			=0x9201,
	ApertureValue				=0x9202,
	ExposureBiasValue			=0x9204,
	MaxApertureValue			=0x9205,
	SubjectDistance				=0x9206,
	MeteringMode				=0x9207,
	Flash						=0x9209,
	FocalLength					=0x920A,

	TIFFEPStandardID			=0x9216,

	SubsecTime					=0x9290,
	SubsecTimeOriginal			=0x9291,
	FocalLengthIn35mmFilm		=0xa405,

	-- DNG
	DNGVersion					=0xc612,
	DNGBackwardVersion			=0xc613,
	UniqueCameraModel			=0xc614,
	BlackLevel					=0xc61a,
	WhiteLevel					=0xc61d,
	DefaultCropOrigin			=0xc61f,
	DefaultCropSize				=0xc620,
	ColorMatrix1				=0xc621,
	ColorMatrix2				=0xc622,
	CameraCalibration1			=0xc623,
	CameraCalibration4			=0xc624,
	AnalogBalance				=0xc627,
	AsShotNeutral				=0xc628,
	BaselineExposure			=0xc62a,
	BaselineNoise				=0xc62b,
	BaselineSharpness			=0xc62c,
	LinearResponseLimit			=0xc62e,
	LenseInfo					=0xc630,
	CalibrationIlluminant1		=0xc65a,
	CalibrationIlluminant2		=0xc65b,
	ActiveArea					=0xc68d,
	ForwardMatrix1				=0xc714,
	ForwardMatrix2				=0xc715,
	OpcodeList1					=0xc740,

}

for k,v in pairs(m.tags_map) do
	m.tags[v] = k
end

m.tag_types = {
	{name='BYTE',size=1},
	{name='ASCII',size=1,string=true},
	{name='SHORT',size=2},
	{name='LONG',size=4},
	{name='RATIONAL',size=8,elsize=4,rational=true},
	{name='SBYTE',size=1,signed=true},
	{name='UNDEFINED',size=1},
	{name='SSHORT',size=2,signed=true},
	{name='SSLONG',size=4,signed=true},
	{name='SRATIONAL',size=8,elsize=4,signed=true,rational=true},
	{name='FLOAT',size=4,float=true},
	{name='DOUBLE',size=8,float=true},
}

local function init_tag_types()
	for i,t in pairs(m.tag_types) do
		-- element size for rational
		if not t.elsize then
			t.elsize = t.size
		end
		-- lbuf functions to get / set values
		local sfx = tostring(t.elsize*8)
		if t.signed then
			sfx = 'i'..sfx
		elseif t.float then -- TODO not actually implemented in lbuf
			sfx = 'f'..sfx
		else
			sfx = 'u'..sfx
		end
		-- will be nil if not supported in lbuf
		t.lb_get = lbuf['get_'..sfx]
		t.lb_set = lbuf['set_'..sfx]
	end
end
init_tag_types()

function m.bind_tiff_header(d)
	d:bind_u16('byte_order')
	d:bind_u16('id')
	d:bind_u32('ifd0_off')
end

local ifd_entry_methods = {
	tagname = function(self)
		local n = m.tags[self.tag]
		if n then
			return n
		end
		return string.format('unk_0x%04x',self.tag)
	end,
	type = function(self)
		local t = m.tag_types[self.type_id]
		if t then
			return t
		end
		return {name='unk',size=0} -- size is actually unknown
	end,
	is_inline = function(self)
		return (self.count * self:type().size <= 4)
	end,
	--[[
	return a formatted text description of the tag (name, number, type, count, offset/value)
	]]
	describe = function(self)
		local vdesc
		if self:is_inline() then
			vdesc = ' value'
		else 
			vdesc = 'offset'
		end
		return string.format('%-30s tag=0x%04x type=%-10s count=%07d %s=0x%08x',
					self:tagname(),
					self.tag,
					self:type().name,
					self.count,
					vdesc,
					self.valoff)
	end,
	--[[
	return the offset of the data within the lbuf, either inline in the ifd entry or in body
	]]
	get_data_off = function(self) 
		if self:is_inline() then
			return self.off + 8 -- short tag + short type + long count
		else
			return self.valoff
		end
	end,
	--[[
	get a numeric elements of a value
	for ASCII, bytes are returned
	for rational, numerator and denominator are retuned in an array
	--]]
	getel = function(self,index)
		if not index then
			index = 0
		end
		if index >= self.count then
			return nil
		end
		local t = self:type()
		-- if type is unknown, can't know size, just return nil
		-- calling code could inspect valoff if desired
		if t.name == 'unk' then
			return nil
		end
		local v_off = self:get_data_off() + t.size*index
		if not t.lb_get then
			return nil
		end
		if t.rational then
			return {t.lb_get(self._lb,v_off,2)}
		end
		return t.lb_get(self._lb,v_off)
	end,
	getel_array = function(self,start,count)
		local r = {}
		if not start then
			start = 0
		elseif start >= self.count then
			return r
		end
		if not count then
			count = self.count
		elseif count > self.count then
			count = self.count
		end
		for i = start,count do
			table.insert(r,self:getel(i))
		end
		return r
	end,
	-- get bytes as a lua string
	get_byte_str = function(self)
		local v_off = self:get_data_off()
		return self._lb:string(v_off+1,v_off+self:type().size*self.count)
	end,
	-- get ascii string field as array of strings
	get_ascii_array = function(self,start,max)
		if not self:type().string then
			return nil
		end
		if not start then
			start = 0
		end

		local bytes = self:get_byte_str()
		local strings = {} -- every ascii field can theoretically contain multiple null terminated strings
		local n = 0
		for s in string.gmatch(bytes,'[^%z]+') do
			if max and #strings >= max then
				break
			end
			if n >= start then
				table.insert(strings,s)
			end
			n = n + 1
		end
		return strings
	end,
	get_ascii = function(self,index)
		if not index then
			index = 0
		end
		return (self:get_ascii_array())[index+1]
	end,
	getval_array = function(self,start,max)
		if self:type().string then
			return self:get_ascii_array(start,max)
		else
			return self:getel_array(start,max)
		end
	end,
}
function m.bind_ifd_entry(d,ifd,i)
	local off = ifd.off + 2 + i*12 -- offset + entry count + index*sizeof(entry)
	local e=lbu.wrap(d._lb)
	util.extend_table(e,ifd_entry_methods)
	e.off = off
	e:bind_seek(off)
	e:bind_u16('tag')
	e:bind_u16('type_id')
	e:bind_u32('count')
	e:bind_u32('valoff')
	return e
end

local ifd_methods = {}

--[[
write image data, either to a file handle or name
]]
function ifd_methods.has_image(self)
	if self.byname.StripOffsets == nil or self.byname.StripByteCounts == nil then
		return false
	end
	return true
end

function ifd_methods.write_image_data(self,dst)
	local fh
	-- some ifds (e.g. exif) don't have image data
	if not self:has_image() then
		error('ifd does not contain image data')
	end

	if type(dst) == 'string' then
		local err
		fh, err = io.open(dst,'wb')
		if not fh then
			error('open failed '..tostring(err))
		end
	elseif type(dst) == 'userdata' and type(dst.read) == 'function' then
		fh = dst
	else
		error('expected string or file')
	end
	for i=0,self.byname.StripOffsets.count - 1 do
		self.dng._lb:fwrite(fh,self.byname.StripOffsets:getel(i),self.byname.StripByteCounts:getel(i))
	end
	if fh ~= dst then
		fh:close()
	end
end

-- ifds
function m.bind_ifds(d,ifd_off,ifd_list,parent)
	-- for sub, we may be appending
	if not ifd_list then
		ifd_list={}
	end
	repeat
		if ifd_off >= d._lb:len() then
			error('ifd outside of data')
		end
		local n_entries = d._lb:get_u16(ifd_off)
		local ifd = {
			dng=d, -- DNG object this ifd belongs to
			index=#ifd_list,
			off=ifd_off,
			n_entries=n_entries,
			entries={},
			bytag={},
			byname={},
			parent=parent, -- parent ifd, if any
		}
		for i=0, n_entries-1 do
			local e = m.bind_ifd_entry(d,ifd,i)
			table.insert(ifd.entries,e)
			if e.tag == m.tags_map.SubIFDs then
				ifd.sub={}
				-- sub ifds could point to a list of offsets, which could in turn each be chained (???)
				for i=1,e.count do
					m.bind_ifds(d,e.valoff+(i-1)*e:type().elsize,ifd.sub,ifd)
				end
			elseif e.tag == m.tags_map.ExifIFD then
				ifd.exif={ }
				-- assume there is only one
				if e.count == 1 then
					m.bind_ifds(d,e.valoff,ifd.exif,ifd)
					ifd.exif[1].is_exif=true
				else
					util.warnf('multiple exif IFDs per IFD not supported')
				end
			end
			ifd.bytag[e.tag] = e
			-- avoid including unk_xxx names
			if m.tags[e.tag] then
				ifd.byname[e:tagname()] = e
			end
		end
		util.extend_table(ifd,ifd_methods)
		table.insert(ifd_list,ifd)
		ifd_off = d._lb:get_u32(ifd_off + n_entries * 12 + 2)
	until ifd_off == 0
	return ifd_list
end

local dng_methods={}

function dng_methods.print_ifd(self,ifd,opts)
	opts=util.extend_table({
		depth=0,
		maxvals=20,
		recurse=false,
		inlinevals=true,
	},opts)

	local indent = string.rep(' ',opts.depth)
	opts.depth = opts.depth+1
	local pathstr
	if ifd.is_exif then
		pathstr = 'exif'
	else
		pathstr = ifd.index
	end
	local p = ifd.parent
	while p do
		pathstr = p.index .. '.' .. pathstr
		p = p.parent
	end

	printf('%sifd%s offset=0x%x entries=%d\n',indent,pathstr,ifd.off,ifd.n_entries)
	for j, e in ipairs(ifd.entries) do
		printf('%s %s\n',indent,e:describe())
		-- TODO undefined we know about should be sub-classed in a way that allows displaying
		if opts.maxvals > 0 and e:type().name ~= 'UNDEFINED' and (not e:is_inline() or e.count > 1) then
			local i = 0
			local vals = e:getval_array(0,opts.maxvals)
			for i,v in ipairs(vals) do
				local str
				if e:type().string then
					str = string.format('"%s"',v)
				elseif e:type().rational then
					if e:type().signed then
						str = string.format('%d/%d',v[1],v[2])
					else
						str = string.format('%u/%u',v[1],v[2])
					end
					if v[2] ~= 0 then
						str = string.format('%23s %12f',str,v[1]/v[2])
					end
				else
					str = string.format('%12d 0x%08x',v,v)
				end
				printf("%s %4d: %s\n",indent,i-1,str)
			end
			-- TODO inidicate if full count not reach (problematic for strings)
		end
	end
	if opts.recurse then
		if ifd.sub then
			for i, subifd in ipairs(ifd.sub) do
				self:print_ifd(subifd,opts)
			end
		end
		if ifd.exif then
			for i, subifd in ipairs(ifd.exif) do
				self:print_ifd(subifd,opts)
			end
		end
	end
	opts.depth = opts.depth-1
end

function m.cfa_bytes_to_str(cfa_bytes) 
	local cfa={cfa_bytes:byte(1,-1)}
	local r = ''
	for i,v in ipairs(cfa) do
		r= r.. tostring(({[0]='R','G','B'})[v])
	end
	return r
end

function m.dng_version_to_str(ver_bytes)
	return string.format('%d.%d.%d.%d',ver_bytes:byte(1,-1))
end

function dng_methods.cfa_str(self)
	return m.cfa_bytes_to_str(self.raw_ifd.byname.CFAPattern:get_byte_str())
end

function dng_methods.print_summary(self)
	printf("%dx%dx%d, %s, DNG %s / %s, %s, %s\n",
		self.raw_ifd.byname.ImageWidth:getel(),
		self.raw_ifd.byname.ImageLength:getel(),
		self.raw_ifd.byname.BitsPerSample:getel(),
		self:cfa_str(),
		m.dng_version_to_str(self.main_ifd.byname.DNGVersion:get_byte_str()),
		m.dng_version_to_str(self.main_ifd.byname.DNGBackwardVersion:get_byte_str()),
		self.main_ifd.byname.Software:get_ascii(),
		self.main_ifd.byname.Model:get_ascii()
	)
end
function dng_methods.print_header(self)
	for i,fname in ipairs(m.header_fields) do
		printf('%s 0x%x\n',fname,self[fname])
	end
end
function dng_methods.print_info(self)
	self:print_header()
	for i, ifd in ipairs(self.ifds) do 
		self:print_ifd(ifd,{recurse=true})
	end
end

--[[
convenience function
maximum value for bit depth
probably the same as white level
]]
function dng_methods.max_value(self)
	return 2^self.img:bpp() - 1
end
--[[
build a histogram from a rectangle of the image, default active area
not bayer aware
]]
function dng_methods.build_histogram(self,opts)
	local ifd=self.raw_ifd
	opts = util.extend_table({
		top=ifd.byname.ActiveArea:getel(0),
		left=ifd.byname.ActiveArea:getel(1),
		bottom=ifd.byname.ActiveArea:getel(2),
		right=ifd.byname.ActiveArea:getel(3),
	},opts);
	local h={}
	for i=0,self:max_value() do
		h[i]=0
	end
	local total = 0
	for y = opts.top, opts.bottom-1 do
		for x = opts.left, opts.right-1 do
			local v = self.img:get_pixel(x,y)
			h[v] = h[v] + 1
			total = total+1
		end
	end
	h.total = total
	return h
end

-- for testing rawimg
function dng_methods.print_img_info(self)
	local img = self.img
	if not img then
		printf("no image\n")
		return
	end
	printf("%dx%dx%d %s endian %s\n",
		img:width(),
		img:height(),
		img:bpp(),
		img:endian(),
		m.cfa_bytes_to_str(img:cfa_pattern())
	)
end

--[[
function to dump image data converted to various bit depths and byte orders
note: use ifd:write_image_data() for unconverted
]]
function dng_methods.dump_image(self,dst,opts)
	local img = self.img
	opts=util.extend_table({
		bpp=8,
	},opts)
	-- hack to default 16 bit pgm to big endian if not specified
	-- per http://netpbm.sourceforge.net/doc/pamendian.html is the correct format,
	-- but allow little endian to be forced if someone wants it
	if not opts.endian then 
		if opts.pgm and opts.bpp == 16 then
			opts.endian = 'big'
		else
			opts.endian = 'little'
		end
	end

	if not img then
		return false, 'image data not set'
	end
	if opts.pgm and opts.bpp ~= 8  and opts.bpp ~= 16 then
		return false, 'only 8 and 16 bpp supported for pgm'
	end
	local outimg,outlb = img:convert(opts)

	local fh,err = io.open(dst,'wb')
	if not fh then
		return false, 'open failed '..tostring(err)
	end

	if opts.pgm then
		-- set max value to max value that should appear
		local maxval
		if img:bpp() > outimg:bpp() then -- down converting max value will be full range of ouput
			maxval = (2^outimg:bpp())-1
		else
			if opts.upvalmod == 'shift' then -- up converting, with multiply
				maxval = (2^outimg:bpp())-1
			else -- up converting, unchanged values
				maxval = (2^img:bpp())-1
			end
		end
		fh:write(string.format('P5\n%d\n%d\n%d\n',outimg:width(),outimg:height(),maxval))
	end
	outlb:fwrite(fh)
	fh:close()
	return true
end

local function do_set_pixel_test(img)
	local bad = 0
	local bad_b = 0
	local bad_a = 0
	for y=200,400 do
		for x=200,1200 do
			-- assumes get has already been validated
			-- check neighbors since packing set can affect both
			local v={
				img:get_pixel(x-2,y),
				img:get_pixel(x-1,y),
				img:get_pixel(x,y),
				img:get_pixel(x+1,y),
				img:get_pixel(x+2,y),
			}
			img:set_pixel(x,y,v[3])
			if v[3] ~= img:get_pixel(x,y) then
				bad = bad + 1
			end
			if v[1] ~= img:get_pixel(x-2,y) or v[2] ~= img:get_pixel(x-1,y) then
				bad_b = bad_b + 1
			end
			if v[4] ~= img:get_pixel(x+1,y) or v[5] ~= img:get_pixel(x+2,y)then
				bad_a = bad_a + 1
			end
		end
	end
	if bad > 0 or bad_b > 0 or bad_a > 0 then
		printf("mismatched %d before %d after %d\n",bad, bad_b, bad_a)
	else
		printf("ok\n",bad)
	end
end

function dng_methods.test_set_pixel(self)
	local img = self.img
	if not img then
		return false, 'image data not set'
	end
	local width=img:width()
	local height=img:height()
	local bpp=img:bpp()

	printf('testing big endian\n')
	do_set_pixel_test(img)

	local ifd=self.raw_ifd
	local offset = ifd.byname.StripOffsets:getel()
	local ldata = self._lb:sub(offset+1,offset+ifd.byname.StripByteCounts:getel())
	ldata:reverse_bytes()
	self:set_data(ldata,0,'little')
	img = self.img

	printf('testing little endian\n')
	do_set_pixel_test(img)

	self:set_data() -- restore default data
end

--[[
set image data, either to internal data or an external lbuf
initializes dng.img
order is only for testing external data in little endian format
]]
function dng_methods.set_data(self,data,offset,order)
	-- TODO makes assumptions about header layout
	local ifd=self.raw_ifd
	if not ifd then 
		error('ifd 0.0 not found')
	end

	if not order then
		order = 'big'
	end

	if not offset then
		offset = 0
	end

	-- no data, use internal
	if not data then
		data = self._lb
		offset = ifd.byname.StripOffsets:getel() -- TODO in theory could be more than one
		-- order should always be big for embedded data
	end

	local active_area = {
		top=ifd.byname.ActiveArea:getel(0),
		left=ifd.byname.ActiveArea:getel(1),
		bottom=ifd.byname.ActiveArea:getel(2),
		right=ifd.byname.ActiveArea:getel(3),
	}
	-- clamp invalid active area for easier DNG debugging
	if active_area.bottom > ifd.byname.ImageLength:getel() then
		util.warnf("invalid active area bottom %d > %d\n",active_area.bottom,ifd.byname.ImageLength:getel())
		active_area.bottom = ifd.byname.ImageLength:getel()
	end
	if active_area.left > ifd.byname.ImageWidth:getel() then
		util.warnf("warning invalid active area left %d > %d\n",active_area.left,ifd.byname.ImageWidth:getel())
		active_area.left = ifd.byname.ImageWidth:getel()
	end
	local img = rawimg.bind_lbuf{
		data=data,
		data_offset=offset,
		width=ifd.byname.ImageWidth:getel(),
		height=ifd.byname.ImageLength:getel(),
		bpp=ifd.byname.BitsPerSample:getel(),
		endian=order,
		black_level=ifd.byname.BlackLevel:getel(),
		cfa_pattern=ifd.byname.CFAPattern:get_byte_str(),
		active_area=active_area,
	}
	self.img = img
	return true
end

--[[
return ifd specified by "path", or nil
path: table of 0 based ifd numbers
{0,0}
]]
function dng_methods.get_ifd(self,path)
	local cur_list = self.ifds
	local cur
	for _,index in ipairs(path) do
		if not cur_list then
			return nil
		end
		if type(index) == 'number' then
			if not cur_list[index+1] then
				return
			end
			cur = cur_list[index+1]
			cur_list = cur.sub
		elseif index == 'exif' then
			if not cur.exif then
				return nil
			end
			-- assume only one exif
			cur = cur.exif[1]
			cur_list = nil
		else
			error('invalid path')
		end
	end
	return cur
end

function m.bind_header(lb)
	local d=lbu.wrap(lb)
	util.extend_table(d,dng_methods)
	m.bind_tiff_header(d)
	if d.byte_order ~= 0x4949 then
		if d.byte_order == 0x4d4d then
			return false, 'big endian unsupported'
		end
		return false, string.format('invalid byte order 0x%x',d.byte_order)
	end
	if d.id ~= 42 then
		return false, string.format('invalid id %d, expected 42',d.id)
	end
	d.ifds = m.bind_ifds(d,d.ifd0_off)
	-- shortcuts to main IFDs of interest, could be smarter about finding them
	d.main_ifd = d:get_ifd{0} -- thumb an overall information
	d.raw_ifd = d:get_ifd{0,0} -- raw data
	d.exif_ifd = d:get_ifd{0,'exif'} -- exif
	return d
end

function m.load(filename)
	local lb,err=lbu.loadfile(filename)
	if not lb then
		return false, err
	end
	local d,err = m.bind_header(lb)
	if not d then
		return false, err
	end
	d.filename = filename
	-- TODO this will fail loading dngs that aren't in a format supported by rawimg
	-- TODO also will prevent loading standalone headers
	local status, err = d:set_data()
	if not status then
		return false, err
	end
	return d
end
return m
