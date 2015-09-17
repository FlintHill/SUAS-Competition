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
local path and filesystem related utilities
depends on sys.ostype, errlib and lfs
]]
local fsutil={}
--[[
valid separator characters
]]
-- default function for ostype, can override for testing
fsutil.ostype = sys.ostype

function fsutil.dir_sep_chars()
	if fsutil.ostype() == 'Windows' then
		return '\\/'
	end
	return '/'
end

function fsutil.is_dir_sep(c)
	if c == '/' then
		return true
	end
	if fsutil.ostype() == 'Windows' then
		return c == '\\'
	end
	return false
end

--[[
remove suffix from a path if found
opts {
	ignorecase=bool -- is suffix case sensitive? default true
}
]]
function fsutil.remove_sfx(path,sfx,opts)
	opts = util.extend_table({ignorecase=true},opts)
	if string.len(sfx) <= string.len(path) then
		if (opts.ignorecase and string.lower(string.sub(path,-string.len(sfx))) == string.lower(sfx))
				or string.sub(path,-string.len(sfx)) == sfx then
			return string.sub(path,1,string.len(path) - string.len(sfx))
		end
	end
	return path
end
--[[
similar to unix basename
]]
function fsutil.basename(path,sfx,opts)
	if not path then
		return nil
	end
	local drive
	-- drive is discarded, like leading /
	drive,path = fsutil.splitdrive(path)
	local s,e,bn=string.find(path,'([^'..fsutil.dir_sep_chars()..']+)['..fsutil.dir_sep_chars()..']?$')
	if not s then
		return nil
	end
	-- unix basename returns full name if suffix is equal to original
	if sfx and string.len(sfx) < string.len(bn) then
		bn = fsutil.remove_sfx(bn,sfx,opts)
	end
	return bn
end

function fsutil.splitdrive(path)
	if fsutil.ostype() ~= 'Windows' then
		return '',path
	end
	local s,e,drive,rest=string.find(path,'^(%a:)(.*)')
	if not drive then
		drive = ''
		rest = path
	end
	if not rest then
		rest = ''
	end
	return drive,rest
end
--[[
note A/=>nil
]]
function fsutil.basename_cam(path,sfx,opts)
	if not path then
		return nil
	end
	if path == 'A/' then
		return nil
	end
	local s,e,bn=string.find(path,'([^/]+)/?$')
	if not s then
		return nil
	end
	-- unix basename returns full name if suffix is equal to original
	if sfx and string.len(sfx) < string.len(bn) then
		bn = fsutil.remove_sfx(bn,sfx,opts)
	end
	return bn
end

--[[
similar to unix dirname, with some workarounds to make it more useful on windows
UNC paths are not supported
]]
function fsutil.dirname(path)
	if not path then
		return nil
	end
	local drive=''
	-- windows - save the drive, if present, and perform dirname on the rest of the path
	drive,path=fsutil.splitdrive(path)
	-- remove trailing blah/?
	local dn=string.gsub(path,'[^'..fsutil.dir_sep_chars()..']+['..fsutil.dir_sep_chars()..']*$','')
	if dn == '' then
		if drive == '' then
			return '.'
		else
			return drive
		end
	end
	-- remove any trailing /
	dn = string.gsub(dn,'['..fsutil.dir_sep_chars()..']*$','')
	-- all /
	if dn == '' then
		return drive..'/'
	end
	return drive..dn
end

--[[
dirname variant for camera paths
note, A/ is ambiguous if used on relative paths, treated specially
has trailing directory removed, except for A/ (camera functions trailing / on A/ and reject on subdirs) 
A/ must be uppercase (as required by dryos)
]]
function fsutil.dirname_cam(path)
	if not path then
		return nil
	end
	if path == 'A/' then
		return path
	end
	-- remove trailing blah/?
	dn=string.gsub(path,'[^/]+/*$','')
	-- invalid, 
	if dn == '' then
		return nil
	end
	-- remove any trailing /
	dn = string.gsub(dn,'/*$','')
	if dn == 'A' then
		return 'A/'
	end
	-- all /, invalid
	if dn == '' then
		return nil
	end
	return dn
end

--[[ 
add / between components, only if needed.
accepts / or \ as a separator on windows
TODO joinpath('c:','foo') becomes c:/foo
]]
function fsutil.joinpath(...)
	local parts={...}
	-- TODO might be more useful to handle empty/missing parts
	if #parts < 2 then
		error('joinpath requires at least 2 parts',2)
	end
	local r=parts[1]
	for i = 2, #parts do
		local v = string.gsub(parts[i],'^['..fsutil.dir_sep_chars()..']','')
		if not string.match(r,'['..fsutil.dir_sep_chars()..']$') then
			r=r..'/'
		end
		r=r..v
	end
	return r
end

function fsutil.joinpath_cam(...)
	local parts={...}
	-- TODO might be more useful to handle empty/missing parts
	if #parts < 2 then
		error('joinpath requires at least 2 parts',2)
	end
	local r=parts[1]
	for i = 2, #parts do
		local v = string.gsub(parts[i],'^/','')
		if not string.match(r,'/$') then
			r=r..'/'
		end
		r=r..v
	end
	return r
end

--[[
split a path into an array of components
the leading component will may have a /, drive or .
]]
function fsutil.splitpath(path)
	local parts={}
	while true do
		local part=fsutil.basename(path)
		path = fsutil.dirname(path)
		table.insert(parts,1,part)
		if path == '.' or path == '/' or (fsutil.ostype() == 'Windows' and string.match(path,'^%a:/?$')) then
			table.insert(parts,1,path)
			return parts
		end
	end
end

function fsutil.splitpath_cam(path)
	local parts={}
	while true do
		local part=fsutil.basename_cam(path)
		path = fsutil.dirname_cam(path)
		table.insert(parts,1,part)
		if path == 'A/' then
			table.insert(parts,1,path)
			return parts
		end
		if path == nil then
			return parts
		end
	end
end

--[[
return final .chars or empty string
.foo is not considered an extension
]]
function fsutil.get_ext(path)
	local ext=string.match(path,'[^.].*(%.[^.'..fsutil.dir_sep_chars()..']*)$')
	if not ext then
		return ''
	end
	return ext
end

--[[
return name, ext
]]
function fsutil.split_ext(path)
	local ext=fsutil.get_ext(path)
	return fsutil.remove_sfx(path,ext),ext
end
--[[
ensure path starts with A/, replace \ with / 
]]
function fsutil.make_camera_path(path)
	if not path then
		return 'A/'
	end
	-- fix slashes
	path = string.gsub(path,'\\','/')
	local pfx = string.sub(path,1,2)
	if pfx == 'A/' then
		return path
	end
	if pfx == 'a/' then
		return 'A' .. string.sub(path,2,-1)
	end
	return 'A/' .. path
end

--[[
make multiple subdirectories
throws on error
]]
function fsutil.mkdir_m(path)
	local mode = lfs.attributes(path,'mode')
	if mode == 'directory' then
		return
	end
	if mode then
		errlib.throw{etype='exists', msg='path exists, not directory'}
	end
	local parts = fsutil.splitpath(path)
	-- never try to create the initial . or /
	local p=parts[1]
	for i=2, #parts do
		p = fsutil.joinpath(p,parts[i])
		local mode = lfs.attributes(p,'mode')
		if not mode then
			local status,err = lfs.mkdir(p)
			if not status then
				errlib.throw{etype='lfs', msg=tostring(err)}
			end
		elseif mode ~= 'directory' then
			errlib.throw{etype='exists', msg='path exists, not directory'}
		end
	end
end

--[[
make a directory containing the target path
]]
function fsutil.mkdir_parent(path)
	fsutil.mkdir_m(fsutil.dirname(path))
end

--[[
iterate over files/directories, borrowed from rlib
TODO there's probably better ways to do this
]]
local fs_iter={}

function fs_iter:depth()
	return #self.rpath
end

function fs_iter:can_recurse()
	if self.cur.st.mode ~= 'directory' or self.cur.name == '..' then
		return false
	end
	-- need to be able to recurse into . if it's the initial directory
	if #self.rpath ~= 0 and self.cur.name == '.' then
		return false
	end
	return true
end

function fs_iter:recurse()
	if not self:can_recurse() then
		error("tried to recurse into invalid target")
	end
	table.insert(self.rpath,self.cur.path[#self.cur.path])
	local save_cur = self.cur
	self:singledir()
	self.cur = save_cur
	table.remove(self.rpath)
end

function fs_iter:singleitem(path)
	local st,err=lfs.attributes(path)
	if not st then
		errlib.throw{etype='lfs',msg=tostring(err)}
	end
	self.cur={st=st,full=path,name=fsutil.basename(path)}
	-- root directory (or bare drive on win) returns nil
	if not self.cur.name then
		self.cur.name = path
	end

	if #self.rpath == 0 then
		self.cur.path = {path}
	else
		self.cur.path = {unpack(self.rpath)}
		table.insert(self.cur.path,self.cur.name)
	end
	self:callback()
end

function fs_iter:singledir()
	local cur_dir = self.cur.full
	for name in lfs.dir(cur_dir) do
		self:singleitem(fsutil.joinpath(cur_dir,name))
	end
end

function fs_iter.run(paths,opts)
	local t=extend_table({},opts)
	util.mt_inherit(t,fs_iter)

	for i,path in ipairs(paths) do
		t.rpath={}
		t:singleitem(path)
	end
	if t.result_callback() then
		return t:result_callback()
	end
end

fsutil.fs_iter = fs_iter

function fsutil.find_files_all_fn(self,opts)
	self:ff_store(self.cur)
end

function fsutil.find_files_fullname_fn(self,opts)
	--print(di.cur.full)
	self:ff_store(self.cur.full)
end

--[[
process directory tree with matching
[results]=find_files(paths,opts,func)
paths=<array of paths to process>
opts={
	fmatch='<pattern>', -- match on full path of files, default any (NOTE can match on filename with /<match>$)
	dmatch='<pattern>', -- match on names of directories, default any 
	rmatch='<pattern>', -- recurse into directories matching, default any 
	fsfx='string',      -- compare (not pattern) suffix of file, can be used for extension
	fsfx_ic=bool,       -- should suffix be case sensitive (default false)
	dirs=true, -- pass directories to func. otherwise only files sent to func, but dirs are still recursed
	dirsfirst=false, -- process directories before contained files
	maxdepth=100, -- maxium depth of directories to recurse into, 0=just process paths passed in, don't recurse
	martians=bool, -- process non-file, not directory items (devices etc) default false
}
]]

function fsutil.find_files(paths,opts,func)
	if not func then
		func=fsutil.find_files_fullname_fn
	end
	opts=util.extend_table({
		dirs=true,
		dirsfirst=false,
		maxdepth=100,
		fsfx_ic=true,
	},opts)

	-- optional place to store callback data
	local results

	return fs_iter.run(paths,{
		-- check file suffix (usually extension, but doesn't have to be)
		ff_check_fsfx=function(self,opts)
			if not opts.fsfx then
				return true -- option not set, all match
			end
			local len=string.len(opts.fsfx)
			if opts.fsfx_ic then
				return self.cur.full:lower():sub(-len,-1) == opts.fsfx:lower()
			end
			return self.cur.full:sub(-len,-1) == opts.fsfx
		end,
		ff_check_match=function(self,opts)
			if self.cur.st.mode == 'file' then
				if opts.fmatch then
					return string.match(self.cur.full,opts.fmatch) and self:ff_check_fsfx(opts)
				end
				return self:ff_check_fsfx(opts)
			end
			if self.cur.st.mode == 'directory' then
				return not opts.dmatch or string.match(self.cur.full,opts.dmatch)
			end
			if opts.martians then
				return true
			end
			return false
		end,
		ff_func=func,
		ff_item=function(self,opts)
			if self:ff_check_match(opts) then
				self:ff_func(opts)
			end
		end,
		ff_store=function(self,data)
			if not results then
				results={data}
			else
				table.insert(results,data)
			end
		end,
		callback=function(self)
			if self.cur.st.mode == 'directory' then
				if opts.dirs and opts.dirsfirst then
					self:ff_item(opts)
				end
				if self:depth() < opts.maxdepth and self:can_recurse() then
					if not opts.rmatch or string.match(self.cur.full,opts.rmatch) then
						self:recurse()
					end
				end
				if opts.dirs and not opts.dirsfirst then
					self:ff_item(opts)
				end
			else
				self:ff_item(opts)
			end
		end,
		result_callback=function()
			return results
		end,
	})
end

--[[
simple delete tree
note lists ALL into memory, not recommended for huge trees
in_paths
	path as string, or array of paths
opts:{
	pretend=bool
	verbose=bool
}
--]]
function fsutil.rm_r(in_paths,opts)
	opts = util.extend_table({},opts)
	if type(in_paths) == 'string' then
		in_paths={in_paths}
	end
	-- get full subdirectory path for each file, with files before containing dir
	local paths=fsutil.find_files(in_paths,{dirsfirst=false})
	for i,p in ipairs(paths) do
		if string.sub(p,-2) ~= '/.' and string.sub(p,-3) ~= '/..' then
			local mode = lfs.attributes(p,'mode')
			if opts.pretend or opts.verbose then
				if mode == 'directory' then
					printf("lfs.rmdir('%s')\n",p)
				else
					printf("os.remove('%s')\n",p)
				end
			end
			if not opts.pretend then
				-- on windows, os.remove does not remove directories, even if empty
				local status, err
				if mode == 'directory' then
					status,err=lfs.rmdir(p)
				else
					status,err=os.remove(p)
				end
				if not status then
					error(tostring(err))
				end
			end
		end
	end
end

--[[
handle windows file mode on popen in a portable way
accept b or a suffix on all platforms, default to binary on windows
]]
function fsutil.popen(prog,mode)
	if not mode then
		mode = 'r'
	end
	-- windows - add a b if mode is one char, othewise leave alone
	if fsutil.ostype() == 'Windows' then
		if string.len(mode) == 1 then
			mode = mode .. 'b'
		end
	elseif string.len(mode) == 2 then
		-- other os - if mode is two chars, truncate to 1
		mode = string.sub(mode,1,1)
	end
	return io.popen(prog,mode)
end
return fsutil
