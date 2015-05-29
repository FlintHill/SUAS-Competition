--[[ 
gui scratchpad
based on the button example from the IUP distribution
this file is licensed under the same terms as the IUP examples
]]
local gui = {}
local live = require'gui_live'
local tree = require'gui_tree'
local user = require'gui_user'
local icon = require'gui_icon'

-- make global for easier testing
gui.live = live
gui.tree = tree
gui.user = user
gui.sched = require'gui_sched'

connect_icon = iup.label{
	image = icon.on,
	iminactive = icon.off,
	active = "NO",
}

connect_label = iup.label{
	title = string.format("host:%d.%d cam:-.- ",chdku.apiver.MAJOR,chdku.apiver.MINOR),
}

-- creates a button
btn_connect = iup.button{ 
	title = "Connect",
	size = "48x"
}

gui.cam_dropdown = iup.list{
	VISIBLECOLUMNS="10",
	DROPDOWN="YES",
}

gui.cam_dropdown.valuechanged_cb=errutil.wrap(function(self)
	local v=tonumber(self.value)
	-- 0 means none selected. Callback can be called with this (multiple times) when list is emptied
	if v == 0 then
		return
	end

	gui.dbgmsg('cam_dropdown set %s\n',tostring(v))

	con=chdku.connection(gui.cached_devs[v])
	if con:is_connected() then
		con:update_connection_info()
	else
		con.condev=con:get_con_devinfo()
	end
	gui.dbgmsg('cam_dropdown new con %s:%s\n',con.condev.dev,con.condev.bus)
	-- TODO cams should be in the tree
	gui.tree.get_container().state = 'COLLAPSED' -- force refresh when switching cams
end)

--[[
info printf - message to be printed at normal verbosity
]]
gui.infomsg = util.make_msgf( function() return prefs.gui_verbose end, 1)
gui.dbgmsg = util.make_msgf( function() return prefs.gui_verbose end, 2)

-- parse a NxM attribute and return as numbers
function gui.parsesize(size)
	local w,h=string.match(size,'(%d+)x(%d+)')
	return tonumber(w),tonumber(h)
end

--[[
wrapper that catches and prints errors
]]
gui.exec=errutil.wrap(function(code,opts)
	con:exec(code,opts)
end)
function gui.execquick(code,opts)
	opts = util.extend_table({nodefaultlibs=true},opts)
	gui.exec(code,opts)
end

function gui.update_mode_dropdown(cur)
	gui.dbgmsg('update mode dropdown %s\n',tostring(cur))
	gui.mode_dropdown["1"] = nil -- empty the list
	if not gui.mode_list or not cur or cur == 0 then
		return
	end
	gui.mode_map = {}
	local curid
	for i=1,#gui.mode_list do
		gui.mode_dropdown[tostring(i)] = gui.mode_list[i].name
		-- list index to chdk value
		gui.mode_map[i] = gui.mode_list[i].id
		if cur == gui.mode_list[i].id then
			curid = i 
		end
	end
	gui.mode_dropdown.value = curid
	gui.dbgmsg('new value %s\n',tostring(gui.mode_map[curid]))
end

local function clear_mode_list()
	gui.mode_list = nil
	gui.mode_map = nil
	gui.update_mode_dropdown()
end

function gui.update_mode_list()
	gui.mode_list = nil
	gui.mode_map = nil
	local modes,cur = con:execwait([[
capmode=require'capmode'
local l={}
local i=1
for id,name in ipairs(capmode.mode_to_name) do
	if capmode.valid(id) then
		l[i] = {name=name,id=id}
		i = i + 1
	end
end
return l,capmode.get()
]])
	-- TODO need to do something about play,
	-- would be good to select the current mode in rec mode
	gui.mode_list = modes
	gui.update_mode_dropdown(cur)
end

function gui.set_connection_status(status)
	if status then
		gui.last_connection_status = true
		connect_icon.active = "YES"
		btn_connect.title = "Disconnect"
		-- if connection was initialized in a different chdku con wrapper
		-- connection info might not be up to date
		if not con.apiver then
			con:update_connection_info()
		end
		connect_label.title = string.format("host:%d.%d cam:%d.%d",
											chdku.apiver.MAJOR,chdku.apiver.MINOR,
											con.apiver.MAJOR,con.apiver.MINOR)
		gui.update_mode_list()
	else
		gui.last_connection_status = false
		connect_icon.active = "NO"
		btn_connect.title = "Connect"
		connect_label.title = string.format("host:%d.%d cam:-.-",chdku.apiver.MAJOR,chdku.apiver.MINOR)
		clear_mode_list()
	end
	live.on_connect_change(con)
end

function gui.update_connection_status()
	gui.set_connection_status(con:is_connected())
end

function gui.update_cam_list(devs)
	gui.cam_dropdown["1"] = nil -- empty the list
	local curid
	for i,dev in ipairs(devs) do
		-- TODO name would be nice, but will might hose other connections
		local s=string.format("%s:%s",dev.bus,dev.dev)
		gui.cam_dropdown[tostring(i)] = s
		gui.dbgmsg('cam_dropdown %d=%s\n',i,s)
		if con.condev and con.condev.dev == dev.dev and con.condev.bus == dev.bus then
			gui.dbgmsg('cur %d\n',i)
			curid = i 
		end
	end
	gui.cached_devs = devs
	if #devs > 0 then
		if curid then
			gui.dbgmsg('cam_dropdown: current %s\n',tostring(curid))
			gui.cam_dropdown.value = curid
		else
			gui.dbgmsg('cam_dropdown: current not found, default to 1\n')
			gui.cam_dropdown.value = 1
			gui.cam_dropdown:valuechanged_cb()
		end
	else
		gui.cam_dropdown.value = 0 -- none
	end
end

local function timer_update_connection_status()
	local new_status = con:is_connected()
	if new_status ~= gui.last_connection_status then
		gui.set_connection_status(new_status)
	end
	local devs = chdk.list_usb_devices()
	if not util.compare_values(devs,gui.cached_devs) then
		gui.update_cam_list(devs)
	end
end

btn_connect.action=errutil.wrap(function(self)
	if con:is_connected() then
		con:disconnect()
	else
		con:connect()
	end
	gui.update_connection_status()
end)

-- console input
inputtext = iup.text{ 
	expand = "HORIZONTAL",
}

-- console output
statustext = iup.text{ 
	multiline = "YES",
	readonly = "YES",
	expand = "YES",
	formatting = "YES",
	scrollbar = "VERTICAL",
	autohide = "YES",
	visiblelines="2",
	appendnewline="NO",
}


function statusprint(...)
	local args={...}
	local s = tostring(args[1])
	for i=2,#args do
		s=s .. ' ' .. tostring(args[i])
	end
	statustext.append = s
	statusupdatepos()
end

-- TODO it would be better to only auto update if not manually scrolled up
-- doesn't work all the time
function statusupdatepos()
	local pos = statustext.count -- iup 3.5 only
	if not pos then
		pos = string.len(statustext.value)
	end
	local l = iup.TextConvertPosToLinCol(statustext,pos)
	local h = math.floor(tonumber(string.match(statustext.size,'%d+x(%d+)'))/8)
	--print(l,h)
	if l > h then
		l=l-h + 1
		--print('scrollto',l)
		statustext.scrollto = string.format('%d:1',l)
	end
end

--[[
switch play / rec mode, update capture mode dropdown
TODO the cli command should integrate with this
]]
switch_mode=errutil.wrap(function(m)
	local capmode
	if m == 0 then
		gui.execquick('if get_mode() then switch_mode_usb(0) end')
	else
		-- switch mode, wait for complete, return current mode
		capmode=con:execwait([[
if not get_mode() then
	switch_mode_usb(1)
end
local i=0
local capmode = require'capmode'
while capmode.get() == 0 and i < 300 do
	sleep(10)
	i=i+1
end
return capmode.get()
]])
	end
	gui.update_mode_dropdown(capmode)
end)
-- creates a button
btn_exec = iup.button{ 
	title = "Execute",
}

cam_btns={}
function cam_btn(name,title)
	if not title then
		title = name
	end
	cam_btns[name] = iup.button{
		title=title,
		size='31x15', -- couldn't get normalizer to work for some reason
		action=function(self)
			gui.execquick('click("' .. name .. '")')
		end,
	}
end
cam_btn("erase")
cam_btn("up")
cam_btn("print")
cam_btn("left")
cam_btn("set")
cam_btn("right")
cam_btn("display","disp")
cam_btn("down")
cam_btn("menu")

gui.mode_dropdown = iup.list{
	VISIBLECOLUMNS="10",
	DROPDOWN="YES",
}
function gui.mode_dropdown:valuechanged_cb()
	gui.dbgmsg('mode_dropdown %s\n',tostring(self.value))
	local v = tonumber(self.value)
	-- 0 means none selected. Callback can be called with this (multiple times) when list is emptied
	if v == 0 then
		return
	end
	if not gui.mode_map or not gui.mode_map[v] then
		gui.infomsg('tried to set invalid mode %s\n',tostring(v))
		return
	end
	gui.execquick(string.format('set_capture_mode(%d)',gui.mode_map[v]))
end

cam_btn_frame = iup.vbox{
	iup.hbox{ 
		cam_btns.erase,
		cam_btns.up,
		cam_btns.print,
	},
	iup.hbox{ 
		cam_btns.left,
		cam_btns.set,
		cam_btns.right,
	},
	iup.hbox{ 
		cam_btns.display,
		cam_btns.down,
		cam_btns.menu,
	},

	iup.label{separator="HORIZONTAL"},
	iup.hbox{ 
		iup.button{
			title='zoom+',
			size='45x15',
			action=function(self)
				gui.execquick('click("zoom_in")')
			end,
		},
		iup.fill{
		},
		iup.button{
			title='zoom-',
			size='45x15',
			action=function(self)
				gui.execquick('click("zoom_out")')
			end,
		},
		expand="HORIZONTAL",
	},

	iup.hbox{ 
		iup.button{
			title='wheel l',
			size='45x15',
			action=function(self)
				gui.execquick('post_levent_to_ui("RotateJogDialLeft",1)')
			end,
		},
		iup.fill{
		},
		iup.button{
			title='wheel r',
			size='45x15',
			action=function(self)
				gui.execquick('post_levent_to_ui("RotateJogDialRight",1)')
			end,
		},
		expand="HORIZONTAL",
	},

	iup.label{separator="HORIZONTAL"},

	iup.hbox{ 
		-- TODO we should have a way to press shoot half and have it stay down,
		-- so we can do normal shooting proccess
		iup.button{
			title='shoot half',
			size='45x15',
			action=function(self)
				gui.execquick(string.format([[
local timeout=%d
local rec,vid = get_mode()
if rec and not vid then
	press("shoot_half")
	local n = 0
	repeat
		sleep(10)
		n = n + 10
	until get_shooting() == true or n > timeout
	release("shoot_half")
else
	press("shoot_half") 
	sleep(1000)
	release("shoot_half")
end
]],prefs.gui_shoot_half_timeout))
			end,
		},
		iup.fill{
		},
		iup.button{
			title='video',
			size='45x15',
			action=function(self)
				gui.execquick('click("video")')
			end,
		},
		expand="HORIZONTAL",
	},

	iup.button{
		title='shoot',
		size='94x15',
		action=function(self)
			-- video seems to need a small delay after half press to reliably start recording
			gui.execquick([[
local rec,vid = get_mode()
if rec and not vid then
	shoot()
else
	if vid then
		press('shoot_half')
		sleep(200)
	end
	click('shoot_full')
end
]])
		end,
	},
	iup.label{separator="HORIZONTAL"},
	iup.hbox{
		iup.button{
			title='rec',
			size='45x15',
			action=function(self)
				switch_mode(1)
			end,
		},
		iup.fill{},
		iup.button{
			title='play',
			size='45x15',
			action=function(self)
				switch_mode(0)
			end,
		},
		expand="HORIZONTAL",
	},
	iup.label{separator="HORIZONTAL"},
	iup.hbox{
		gui.mode_dropdown,
	},
	iup.fill{},
	iup.hbox{
		iup.button{
			title='shutdown',
			size='45x15',
			action=function(self)
				gui.execquick('shut_down()')
			end,
		},
		iup.fill{},
		iup.button{
			title='reboot',
			size='45x15',
			action=function(self)
				gui.execquick('reboot()')
			end,
		},
		expand="HORIZONTAL",
	},
	expand="VERTICAL",
	nmargin="4x4",
	ngap="2"
}

tree.init()
live.init()
user.init()

contab = iup.vbox{
	statustext,
}

maintabs = iup.tabs{
	contab,
	tree.get_container(),
	live.get_container(),
    user.get_container(),
	tabtitle0='Console',
	tabtitle1=tree.get_container_title(),
	tabtitle2=live.get_container_title(),
    tabtitle3=user.get_container_title(),
}

live.set_tabs(maintabs)

inputbox = iup.hbox{
	inputtext, 
	btn_exec,
}
leftbox = iup.vbox{
	maintabs,
--				statustext,
	inputbox,
	nmargin="4x4",
	ngap="2"
}

--[[
TODO this is lame, move console output for min-console or full tab
]]
function maintabs:tabchange_cb(new,old)
	--print('tab change')
	if new == contab then
		iup.SaveClassAttributes(statustext)
		iup.Detach(statustext)
		iup.Insert(contab,nil,statustext)
		iup.Map(statustext)
		iup.Refresh(dlg)
		statusupdatepos()
	elseif old == contab then
		iup.SaveClassAttributes(statustext)
		iup.Detach(statustext)
		iup.Insert(leftbox,inputbox,statustext)
		iup.Map(statustext)
		iup.Refresh(dlg)
		statusupdatepos()
	end
	gui.resize_for_content() -- this may trigger a second refresh, but needed
	live.on_tab_change(new,old)
end
-- creates a dialog
dlg = iup.dialog{
	iup.vbox{ 
		iup.hbox{ 
			connect_icon,
			connect_label,
			iup.fill{},
			gui.cam_dropdown,
			btn_connect;
			nmargin="4x2",
		},
		iup.label{separator="HORIZONTAL"},
		iup.hbox{
			leftbox,
			iup.vbox{
			},
			cam_btn_frame,
		},
	};
	title = "CHDK PTP", 
	resize = "YES", 
	menubox = "YES", 
	maxbox = "YES",
	minbox = "YES",
    icon = icon.logo,
	menu = menu,
	rastersize = "700x560",
	padding = '2x2'
}
function gui.content_size()
	return gui.parsesize(dlg[1].rastersize)
end
--[[
size the dialog large enough for the content
]]
function gui.resize_for_content(refresh)
	local cw,ch= gui.content_size()
	local w,h=gui.parsesize(dlg.clientsize)
	--[[
	print("resize_for_content dlg:"..w.."x"..h)
	print("resize_for_content content:"..cw.."x"..ch)
	--]]
	if not (w and cw and h and ch) then
		return
	end
	local update
	if w < cw then
		w = cw
		update = true
	end
	if h < ch then
		h = ch
		update = true
	end
	if update then
		dlg.clientsize = w..'x'..h
		iup.Refresh(dlg)
	end
end

function dlg:resize_cb(w,h)
	--[[
	local cw,ch=gui.content_size()
	print("dlg Resize: Width="..w.."   Height="..h)
	print("dlg content: Width="..cw.."   Height="..ch)
	--]]
	self.clientsize=w.."x"..h
end

cmd_history = {
	pos = 1,
	prev = function(self) 
		if self[self.pos - 1]  then
			self.pos = self.pos - 1
			return self[self.pos]
--[[
		elseif #self > 1 then
			self.pos = #self
			return self[self.pos]
--]]
		end
	end,
	next = function(self) 
		if self[self.pos + 1]  then
			self.pos = self.pos + 1
			return self[self.pos]
		end
	end,
	add = function(self,value) 
		table.insert(self,value)
		self.pos = #self+1
	end
}

function inputtext:k_any(k)
	if k == iup.K_CR then
		btn_exec:action()
	elseif k == iup.K_UP then
		local hval = cmd_history:prev()
		if hval then
			inputtext.value = hval
		end
	elseif k == iup.K_DOWN then
		inputtext.value = cmd_history:next()
	end
end

--[[
mock file object that sends to gui console
]]
status_out = {
	write=function(self,...)
		statusprint(...)
	end
}

function add_status(status,msg)
	if status then
		if msg then
			printf('%s',msg)
		end
	else 
		printf("ERROR: %s\n",tostring(msg))
	end
end

-- resume with input line, yield returns as result
-- currently the only place it should yield
function gui.cli_readline(prompt)
	return coroutine.yield('readline')
end

-- no erruitl.wrap here, calls are protected by cli
function btn_exec:action()
	printf('> %s\n',inputtext.value)
	cmd_history:add(inputtext.value)
	if string.find(inputtext.value,'^!') then
		add_status(cli:execute(inputtext.value))
	else
		if gui.cli_thread_status == 'readline' then
			local s
			s,gui.cli_thread_status=coroutine.resume(gui.cli_thread,inputtext.value)
		else
			printf('busy %s\n',tostring(gui.cli_thread_status))
		end
	end
	inputtext.value=''
	if cli.finished then
		dlg:hide()
	end
end

function gui.chdku_sleep(time)
	-- in lua 5.1 just use sys.sleep
	if util.lua_ver_minor < 2 then
		sys.sleep(time)
		return
	end
	-- if not in the cli thread, can't yield
	if coroutine.status(gui.cli_thread) ~= 'running' then
		sys.sleep(time)
		return
	end
	-- if time is less than scheduler interval, just sleep
	-- TODO might want to fudge a bit
	if time < tonumber(gui.sched.timer.time) then
		sys.sleep(time)
		return
	end
	gui.sched.run_after(time,function()
		local s 
		s,gui.cli_thread_status=coroutine.resume(gui.cli_thread)
	end)
	coroutine.yield('sleep')
end

function gui.schedule_dev_check()
	if gui.connection_check then
		gui.connection_check:cancel()
	end
	if prefs.gui_dev_check_interval > 0 then
		gui.connection_check = gui.sched.run_repeat(prefs.gui_dev_check_interval,timer_update_connection_status)
	end
end

function gui:run()
	-- shows dialog
	dlg:showxy( iup.CENTER, iup.CENTER)

	tree.on_dlg_run()
	util.util_stdout = status_out
	util.util_stderr = status_out
	do_connect_option()
	do_execute_option()
	live.on_dlg_run()
	gui.resize_for_content()

	cli.readline = gui.cli_readline
	gui.cli_thread = coroutine.create(function() cli:run() end)
	local s
	s,gui.cli_thread_status = coroutine.resume(gui.cli_thread)

	-- TODO in lua 5.1, can't use xpcall because rsint needs to yield in readline
	if util.is_lua_ver(5,1) and cli.names.rsint then
		cli.names.rsint.noxpcall=true
	end
	gui.sched.init_timer(20)
	chdku.sleep = gui.chdku_sleep
	
	gui.schedule_dev_check()

	if (iup.MainLoopLevel()==0) then
		iup.MainLoop()
	end
end
prefs._add('gui_verbose','number','control verbosity of gui',1)
prefs._add('gui_dev_check_interval','number','connection/device list check time in ms, 0=never',500,
	nil, -- default getter
	function(self,val)
		self.value = val
		if val < 100 and val ~= 0 then
			return false, 'invalid value'
		end
		-- if timer already running, reset
		if gui.sched.timer then
			gui.schedule_dev_check()
		end
	end
)
prefs._add('gui_shoot_half_timeout','number','max time to wait for shoot_half, in ms',3000)
return gui
