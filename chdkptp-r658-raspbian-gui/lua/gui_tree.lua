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
module for gui tree view
]]
local m={}
local itree=iup.tree{}
itree.name="Camera"
itree.state="collapsed"
itree.addexpanded="NO"
-- itree.addroot="YES"

function itree:get_data(id)
	return iup.TreeGetUserId(self,id)
end

-- TODO we could keep a map somewhere
function itree:get_id_from_path(fullpath)
	local id = 0
	while true do
		local data = self:get_data(id)
		if data then
			if not data.dummy then
				if data:fullpath() == fullpath then
					return id
				end
			end
		else
			return
		end
		id = id + 1
	end
end

-- TODO
local filetreedata_getfullpath = function(self)
	-- root is special special, we don't want to add slashes
	if self.name == 'A/' then
		return 'A/'
	end
	if self.path == 'A/' then
		return self.path .. self.name
	end
	return self.path .. '/' .. self.name
end

local function get_all_files_filter()
	if sys.ostype() == 'Windows' then
		return "*.*"
	end
	return "*"
end
function itree:set_data(id,data)
	data.fullpath = filetreedata_getfullpath
	iup.TreeSetUserId(self,id,data)
end

local function do_download_dialog(data)
	local remotepath = data:fullpath()
	local filedlg = iup.filedlg{
		dialogtype = "SAVE",
		title = "Download "..remotepath, 
		filter = get_all_files_filter(), 
		filterinfo = "all files",
		file = fsutil.basename(remotepath)
	} 

-- Shows file dialog in the center of the screen
	gui.dbgmsg('download dialog %s\n',remotepath)
	filedlg:popup (iup.ANYWHERE, iup.ANYWHERE)

-- Gets file dialog status
	local status = filedlg.status

-- new or overwrite (windows native dialog already prompts for overwrite)
	if status == "1" or status == "0" then 
		gui.dbgmsg("d %s->%s\n",remotepath,filedlg.value)
		-- can't use mdownload here because local name might be different than remote basename
		add_status(con:download_pcall(remotepath,filedlg.value))
		add_status(lfs.touch(filedlg.value,chdku.ts_cam2pc(data.stat.mtime)))
-- canceled
--	elseif status == "-1" then 
	end
end

local function do_dir_download_dialog(data)
	local remotepath = data:fullpath()
	local filedlg = iup.filedlg{
		dialogtype = "DIR",
		title = "Download contents of "..remotepath, 
	} 

-- Shows dialog in the center of the screen
	gui.dbgmsg('dir download dialog %s\n',remotepath)
	filedlg:popup (iup.ANYWHERE, iup.ANYWHERE)

-- Gets dialog status
	local status = filedlg.status

	if status == "0" then 
		gui.dbgmsg("d %s->%s",remotepath,filedlg.value)
		con:mdownload({remotepath},filedlg.value)
	end
end

local function do_dir_upload_dialog(data)
	local remotepath = data:fullpath()
	local filedlg = iup.filedlg{
		dialogtype = "DIR",
		title = "Upload contents to "..remotepath, 
	} 
-- Shows dialog in the center of the screen
	gui.dbgmsg('dir upload dialog %s\n',remotepath)
	filedlg:popup (iup.ANYWHERE, iup.ANYWHERE)

-- Gets dialog status
	local status = filedlg.status

	if status == "0" then 
		gui.dbgmsg("d %s->%s\n",remotepath,filedlg.value)
		con:mupload({filedlg.value},remotepath)
		itree:refresh_tree_by_path(remotepath)
	end
end


local function do_upload_dialog(remotepath)
	local filedlg = iup.filedlg{
		dialogtype = "OPEN",
		title = "Upload to: "..remotepath, 
		filter = get_all_files_filter(), 
		filterinfo = "all files",
		multiplefiles = "yes",
	} 
	gui.dbgmsg('upload dialog %s\n',remotepath)
	filedlg:popup (iup.ANYWHERE, iup.ANYWHERE)

-- Gets file dialog status
	local status = filedlg.status
	local value = filedlg.value
-- new or overwrite (windows native dialog already prompts for overwrite
	if status ~= "0" then
		gui.dbgmsg('upload canceled status %s\n',status)
		return
	end
	gui.dbgmsg('upload value %s\n',tostring(value))
	local paths = {}
	local e=1
	local dir
	while true do
		local s,sub
		s,e,sub=string.find(value,'([^|]+)|',e)
		if s then
			if not dir then
				dir = sub
			else
				table.insert(paths,fsutil.joinpath(dir,sub))
			end
		else
			break
		end
	end
	-- single select
	if #paths == 0 then
		table.insert(paths,value)
	end
	-- note native windows dialog does not allow multi-select to include directories.
	-- If it did, each to-level directory contents would get dumped into the target dir
	-- should add an option to mupload to include create top level dirs
	-- gtk/linux doesn't allow either
	con:mupload(paths,remotepath)
	itree:refresh_tree_by_path(remotepath)
end

local function do_mkdir_dialog(data)
	local remotepath = data:fullpath()
	local dirname = iup.Scanf("Create directory\n"..remotepath.."%64.11%s\n",'');
	if dirname then
		gui.dbgmsg('mkdir: %s\n',dirname)
		add_status(con:mkdir_m(fsutil.joinpath_cam(remotepath,dirname)))
		itree:refresh_tree_by_path(remotepath)
	else
		gui.dbgmsg('mkdir canceled\n')
	end
end

local function do_delete_dialog(data)
	local msg
	local fullpath = data:fullpath()
	if data.stat.is_dir then
		msg = 'delete directory ' .. fullpath .. ' and all contents ?'
	else
		msg = 'delete ' .. fullpath .. ' ?'
	end
	if iup.Alarm('Confirm delete',msg,'OK','Cancel') == 1 then
		con:mdelete({fullpath})
		itree:refresh_tree_by_path(fsutil.dirname_cam(fullpath))
	end
end

local function do_properties_dialog(data) 
	local fullpath = data:fullpath()
	local ftype
	if data.stat.is_dir then
		ftype = 'directory'
	elseif data.stat.is_file then
		ftype = 'file'
	else
		ftype = 'other'
	end
	local size 
	if data.stat.is_dir then
		size = 'n/a'
	else
		size = tostring(data.stat.size)
	end
	local mtime = os.date('%c',chdku.ts_cam2pc(data.stat.mtime))

	iup.Alarm('Properties',string.format("%s\ntype: %s\nsize: %s\nmodifed: %s\n",fullpath,ftype,size,mtime),'OK')
end

function itree:refresh_tree_by_id(id)
	if not id then
		printf('refresh_tree_by_id: nil id\n')
		return
	end
	local oldstate=self['state'..id]
	local data=self:get_data(id)
	gui.dbgmsg('old state %s\n', tostring(oldstate))
	self:populate_branch(id,data:fullpath())
	if oldstate and oldstate ~= self['state'..id] then
		self['state'..id]=oldstate
	end
end

function itree:refresh_tree_by_path(path)
	gui.dbgmsg('refresh_tree_by_path: %s\n',tostring(path))
	local id = self:get_id_from_path(path)
	if id then
		gui.dbgmsg('refresh_tree_by_path: found %s\n',tostring(id))
		self:refresh_tree_by_id(id)
	else
		gui.dbgmsg('refresh_tree_by_path: failed to find %s\n',tostring(path))
	end
end

itree.dropfiles_cb=errutil.wrap(function(self,filename,num,x,y)
	-- note id -1 > not on any specific item
	local id = iup.ConvertXYToPos(self,x,y)
	gui.dbgmsg('dropfiles_cb: %s %d %d %d %d\n',filename,num,x,y,id)
	-- on unrecognized spot defaults to root
	if id == -1 then
		gui.infomsg("must drop on a directory\n")
		return iup.IGNORE
		-- TODO could default to root, or selected
		-- but without confirm it's would be easy to miss
		-- id = 0
	end
	local data = self:get_data(id)
	local remotepath = data:fullpath()
	if not data.stat.is_dir then
		-- TODO for single files we might want to just overwrite
		-- or drop back to parent?
		gui.infomsg("can't upload to non-directory %s\n",remotepath)
		return iup.IGNORE
	end

	local up_path = remotepath

	if lfs.attributes(filename,'mode') == 'directory' then
		-- if dropped item is dir, append the last directory component to the remote name
		-- otherwise we would just upload the contents
		up_path = fsutil.joinpath_cam(up_path,fsutil.basename(filename))
	end
	gui.infomsg("upload %s to %s\n",filename,remotepath)
	-- TODO no cancel, no overwrite options!
	-- unfortunately called for each dropped item
	con:mupload({filename},up_path)
	self:refresh_tree_by_path(remotepath)
end)

function itree:rightclick_cb(id)
	local data=self:get_data(id)
	if not data then
		return
	end
	if data.fullpath then
		gui.dbgmsg('tree right click: fullpath %s\n',data:fullpath())
	end
	if data.stat.is_dir then
		iup.menu{
			iup.item{
				title='Refresh',
				action=errutil.wrap(function()
					self:refresh_tree_by_id(id)
				end),
			},
			-- the default file selector doesn't let you multi-select with directories
			iup.item{
				title='Upload files...',
				action=errutil.wrap(function()
					do_upload_dialog(data:fullpath())
				end),
			},
			iup.item{
				title='Upload directory contents...',
				action=errutil.wrap(function()
					do_dir_upload_dialog(data)
				end),
			},
			iup.item{
				title='Download contents...',
				action=errutil.wrap(function()
					do_dir_download_dialog(data)
				end),
			},
			iup.item{
				title='Create directory...',
				action=errutil.wrap(function()
					do_mkdir_dialog(data)
				end),
			},
			iup.item{
				title='Delete...',
				action=errutil.wrap(function()
					do_delete_dialog(data)
				end),
			},
			iup.item{
				title='Properties...',
				action=errutil.wrap(function()
					do_properties_dialog(data)
				end),
			},
		}:popup(iup.MOUSEPOS,iup.MOUSEPOS)
	else
		iup.menu{
			iup.item{
				title='Download...',
				action=errutil.wrap(function()
					do_download_dialog(data)
				end),
			},
			iup.item{
				title='Delete...',
				action=errutil.wrap(function()
					do_delete_dialog(data)
				end),
			},
			iup.item{
				title='Properties...',
				action=errutil.wrap(function()
					do_properties_dialog(data)
				end),
			},
		}:popup(iup.MOUSEPOS,iup.MOUSEPOS)
	end
end

function itree:populate_branch(id,path)
	self['delnode'..id] = "CHILDREN"
	gui.dbgmsg('populate branch %s %s\n',id,path)
	if id == 0 then
		itree.state="collapsed"
	end		
	local list,msg = con:listdir(path,{stat='*'})
	if type(list) == 'table' then
		chdku.sortdir_stat(list)
		for i=#list, 1, -1 do
			st = list[i]
			if st.is_dir then
				self['addbranch'..id]=st.name
				self:set_data(self.lastaddnode,{name=st.name,stat=st,path=path})
				-- dummy, otherwise tree nodes not expandable
				-- TODO would be better to only add if dir is not empty
				self['addleaf'..self.lastaddnode] = 'dummy'
				self:set_data(self.lastaddnode,{dummy=true})
			else
				self['addleaf'..id]=st.name
				self:set_data(self.lastaddnode,{name=st.name,stat=st,path=path})
			end
		end
	end
end

itree.branchopen_cb=errutil.wrap(function(self,id)
	gui.dbgmsg('branchopen_cb %s\n',id)
	if not con:is_connected() then
		gui.dbgmsg('branchopen_cb not connected\n')
		return iup.IGNORE
	end
	local path
	if id == 0 then
		path = 'A/'
		local st,err=con:stat(path)
		if not st then
			add_status(st,err)
			st = {is_dir=true,size=0,mtime=0}
		end
		itree:set_data(0,{name='A/',stat=st,path=''})
	end
	local data = self:get_data(id)
	self:populate_branch(id,data:fullpath())
end)

-- empty the tree, and add dummy we always re-populate on expand anyway
-- this crashes in gtk
--[[
function itree:branchclose_cb(id)
	self['delnode'..id] = "CHILDREN"
	self['addleaf'..id] = 'dummy'
end
]]

function m.init()
	return
end

function m.get_container()
	return itree
end

function m.get_container_title()
	return "Files"
end

function m.on_dlg_run()
	itree.addbranch0="dummy"
	itree:set_data(0,{name='A/',stat={is_dir=true},path=''})
end
return m
