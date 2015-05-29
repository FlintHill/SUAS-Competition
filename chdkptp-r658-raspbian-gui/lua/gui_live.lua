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
module for live view gui
]]
local stats=require'gui_live_stats'

local m={
	vp_par = 2, -- pixel aspect ratio for viewport 1:n, n=1,2
	bm_par = 1, -- pixel aspect ratio for bitmap 1:n, n=1,2
	vp_aspect_factor = 1, -- correction factor for height values when scaling for aspect
--[[
note - these are 'private' but exposed in the module for easier debugging
container -- outermost widget
icnv -- iup canvas
vp_active -- viewport streaming selected
bm_active -- bitmap streaming selected
timer -- timer for fetching updates
statslabel -- text for stats
]]
	skip_frames = 0, -- number of frames to drop based on how much longer than desired rate the last one took
	skip_count = 0, -- total number skipped
}

local screen_aspects = {
	[0]=4/3,
	16/9,
}

function m.live_support()
	local caps = guisys.caps()
	return (caps.CD and caps.LIVEVIEW)
end

function m.get_current_frame_data()
	if m.dump_replay then
		return m.dump_replay_frame
	end
	return con.live
end

local vp_toggle=iup.toggle{
	title="Viewfinder",
	action=function(self,state)
		m.vp_active = (state == 1)
	end,
}

local bm_toggle = iup.toggle{
	title="UI Overlay",
	action=function(self,state)
		m.bm_active = (state == 1)
	end,
}

local aspect_toggle = iup.toggle{
	title="Scale for A/R",
	value="ON",
}
					
local function get_fb_selection()
	local what=0
	if m.vp_active then
		what = 1
	end
	if m.bm_active then
		what = what + 4
		what = what + 8 -- palette TODO shouldn't request if we don't understand type, but palette type is in dynamic data
	end
	return what
end

--[[
update canvas size from frame
]]

local function update_canvas_size()
	local lv = m.get_current_frame_data()
	if not lv then
		return
	end
	local vp_w = lv.vp:get_screen_width()/m.vp_par
	local vp_h
	if aspect_toggle.value == 'ON' then
		vp_h = vp_w/screen_aspects[lv.lcd_aspect_ratio]
		m.vp_aspect_factor = vp_h/lv.vp:get_screen_height()
	else
		m.vp_aspect_factor = 1
		vp_h = lv.vp:get_screen_height()
	end

	local w,h = gui.parsesize(m.icnv.rastersize)
	
	local update
	if w ~= vp_w then
		update = true
	end
	if h ~= vp_h then
		update = true
	end
	if update then
		m.icnv.rastersize = vp_w.."x"..vp_h
		iup.Refresh(m.container)
		gui.resize_for_content()
	end
end

local vp_par_toggle = iup.toggle{
	title="Viewfinder 1:1",
	action=function(self,state)
		if state == 1 then
			m.vp_par = 1
		else
			m.vp_par = 2
		end
	end,
}

local bm_par_toggle = iup.toggle{
	title="Overlay 1:1",
	value="1",
	action=function(self,state)
		if state == 1 then
			m.bm_par = 1
		else
			m.bm_par = 2
		end
	end,
}
local bm_fit_toggle = iup.toggle{
	title="Overlay fit",
	value="ON",
}

local function update_should_run()
	-- is the tab current?
	if m.tabs.value ~= m.container then
		return false
	end
	-- is any view active
	if not (m.vp_active or m.bm_active) then
		return false
	end

	-- in dump replay
	if m.dump_replay then
		return true
	end

	if not m.live_con_valid then
		return false
	end
	-- return soft status, connection errors will reset quickly
	return gui.last_connection_status
end

local last_frame_fields = {}
local last_fb_fields = {
	vp={},
	bm={}
}
local last_bm_fields = {}

local palette_size_for_type={
	16*4,
	16*4,
	256*4,
	16*4,
}

-- reset last frame fields so reload or new connection will be a "change"
local function reset_last_frame_vals()
	for i,f in ipairs(chdku.live_fields) do
		last_frame_fields[f]=nil
	end
	for j,fb in ipairs({'vp','bm'}) do
		for i,f in ipairs(chdku.live_fb_desc_fields) do
			last_fb_fields[fb][f]=nil
		end
	end
end

local function update_frame_data(frame)
	local dirty
	for i,f in ipairs(chdku.live_fields) do
		local v = frame[f]
		if v ~= last_frame_fields[f] then
			dirty = true
		end
	end
	for j,fb in ipairs({'vp','bm'}) do
		for i,f in ipairs(chdku.live_fb_desc_fields) do
			local v = frame[fb][f]
			if v ~= last_fb_fields[fb][f] then
				dirty = true
			end
		end
	end

	if dirty then
		gui.dbgmsg('update_frame_data: changed\n')
		for i,f in ipairs(chdku.live_fields) do
			local v = frame[f]
			gui.dbgmsg("%s:%s->%s\n",f,tostring(last_frame_fields[f]),v)
			last_frame_fields[f]=v
		end
		for j,fb in ipairs({'vp','bm'}) do
			for i,f in ipairs(chdku.live_fb_desc_fields) do
				local v = frame[fb][f]
				gui.dbgmsg("%s.%s:%s->%s\n",fb,f,tostring(last_fb_fields[fb][f]),v)
				last_fb_fields[fb][f]=v
			end
		end

		-- for big palettes this lags, optional
		if prefs.gui_dump_palette and last_frame_fields.palette_data_start > 0 then
			printf('palette:\n')
			local c=0

			local bytes = {frame._frame:byte(last_frame_fields.palette_data_start+1,
										last_frame_fields.palette_data_start+palette_size_for_type[last_frame_fields.palette_type])}
			for i,v in ipairs(bytes) do
				printf("0x%02x,",v)
				c = c + 1
				if c == 16 then
					printf('\n')
					c=0
				else
					printf(' ')
				end
			end
		end
	end
end

-- TODO this is just to allow us to read/write a binary integer record size
local dump_recsize = lbuf.new(4)

--[[
lbuf - optional lbuf to re-use, if possible
fh - file handle
returns (possibly new) lbuf or nil on eof
]]
local function read_dump_rec(lb,fh)
	if not dump_recsize:fread(fh) then
		return
	end
	local len = dump_recsize:get_u32()
	if not lb or lb:len() ~= len then
		lb = lbuf.new(len)
	end
	if lb:fread(fh) then -- on EOF, return nil
		return lb
	end
end

local function init_dump_replay()
	m.dump_replay = false
	m.dump_replay_file = io.open(m.dump_replay_filename,"rb")
	if not m.dump_replay_file then
		printf("failed to open dumpfile\n")
		return
	end
	local magic = m.dump_replay_file:read(4)
	if magic ~= 'chlv' then
		printf("unrecognized file\n")
		return
	end

	reset_last_frame_vals()
--	m.dump_replay_file:seek('set',4)
	local header = read_dump_rec(nil,m.dump_replay_file)

	if not header then
		printf("failed to read header\n")
		return
	end

	-- TODO should be defined somewhere
	if header:get_u32() ~= 1 then
		printf("incompatible version %s\n",tostring(header:get_u32()))
		return
	end
	gui.infomsg("loading dump ver %s.%s\n",tostring(header:get_u32()),tostring(header:get_u32(4)))
	m.dump_replay = true
	if not m.dump_replay_frame then
		m.dump_replay_frame = chdku.live_wrap()
	end
end

local function end_dump_replay()
	m.dump_replay = false
	m.dump_replay_file:close()
	m.dump_replay_file=nil
	m.dump_replay_frame=nil
	stats:stop()
end

local function read_dump_frame()
	stats:start()
	stats:start_xfer()

	local data = read_dump_rec(m.dump_replay_frame._frame,m.dump_replay_file)
	-- EOF, loop
	if not data then
		end_dump_replay()
		init_dump_replay()
		data = read_dump_rec(m.dump_replay_frame._frame,m.dump_replay_file)
	end
	m.dump_replay_frame._frame = data
	if prefs.gui_force_replay_palette ~= -1 then
		m.dump_replay_frame._frame:set_u32(chdku.live_frame_map.palette_type,prefs.gui_force_replay_palette)
	end

	update_frame_data(m.dump_replay_frame)
	stats:end_xfer(m.dump_replay_frame._frame:len())
	-- TODO
	update_canvas_size()
end

local function end_dump()
	if con.live and con.live.dump_fh then
		gui.infomsg('%d bytes recorded to %s\n',tonumber(con.live.dump_size),tostring(con.live.dump_fn))
		con:live_dump_end()
	end
end

local function record_dump()
	if not m.dump_active then
		return
	end
	if not con.live.dump_fh then
		local status,err = con:live_dump_start()
		if not status then
			printf('error starting dump:%s\n',tostring(err))
			m.dump_active = false
			-- TODO update checkbox
			return
		end
		printf('recording to %s\n',con.live.dump_fn)
	end
	local status,err = con:live_dump_frame()
	if not status then
		printf('error dumping frame:%s\n',tostring(err))
		end_dump()
		m.dump_active = false
	end
end

local function toggle_dump(ih,state)
	m.dump_active = (state == 1)
	-- TODO this should be called on disconnect etc
	if not m.dumpactive then
		end_dump()
	end
end

local function toggle_play_dump(self,state)
	if state == 1 then
		local filedlg = iup.filedlg{
			dialogtype = "OPEN",
			title = "File to play", 
			filter = "*.lvdump", 
		} 
		filedlg:popup (iup.ANYWHERE, iup.ANYWHERE)

		local status = filedlg.status
		local value = filedlg.value
		if status ~= "0" then
			gui.dbgmsg('play dump canceled\n')
			self.value = "OFF"
			return
		end
		gui.infomsg('playing %s\n',tostring(value))
		m.dump_replay_filename = value
		init_dump_replay()
	else
		end_dump_replay()
	end
end


local function timer_action(self)
	if update_should_run() then
		-- not keeping up, skip
		if m.skip_frames > 0 then
			m.skip_count = m.skip_count + 1
			m.skip_frames = m.skip_frames - 1
			return
		end
		if m.dump_replay then
			read_dump_frame()
			m.icnv:action()
		else
			stats:start()
			local what=get_fb_selection()
			if what == 0 then
				return
			end
			stats:start_xfer()
			local status,err = con:live_get_frame(what)
			if not status then
				end_dump()
				printf('error getting frame: %s\n',tostring(err))
				gui.update_connection_status() -- update connection status on error, to prevent spamming
				stats:stop()
			else
				stats:end_xfer(con.live._frame:len())
				update_frame_data(con.live)
				record_dump()
				update_canvas_size()
			end
		end
		m.icnv:action()
		local total_time = stats:get_last_total_ms()
		if prefs.gui_live_dropframes and total_time > m.frame_time then
			-- skipping ones seems to be enough, just letting the normal
			-- gui run for a short time would probably do it too
			m.skip_frames = 1
		end
	else
		stats:stop()
	end
	m.statslabel.title = stats:get() .. string.format('\nDropped: %d',m.skip_count)
end

function m.set_frame_time(time)
	m.frame_time = time
	if prefs.gui_live_sched then
		if m.timer then
			iup.Destroy(m.timer)
			m.timer=nil
		end
		if not m.sched then
			m.sched=gui.sched.run_repeat(m.frame_time,function()
				local cstatus,msg = xpcall(timer_action,errutil.format)
				if not cstatus then
					printf('live timer update error\n%s',tostring(msg))
					-- TODO could stop live updates here, for now just spam the console
				end
			end)
		else
			m.sched.time = m.frame_time
		end
	else
		if m.sched then
			m.sched:cancel()
			m.sched=nil
		end
		if m.timer then
			iup.Destroy(m.timer)
		end
		m.timer = iup.timer{ 
			time = tostring(m.frame_time),
			action_cb = function()
				-- use xpcall so we don't get a popup every frame
				local cstatus,msg = xpcall(timer_action,errutil.format)
				if not cstatus then
					printf('live timer update error\n%s',tostring(msg))
					-- TODO could stop live updates here, for now just spam the console
				end
			end,
		}
	end
	m.update_run_state()
end

local function update_fps(val)
	val = tonumber(val)
	if val == 0 then
		return
	end
	val = math.floor(1000/val)
	if val ~= m.frame_time then
		stats:stop()
		m.set_frame_time(val)
	end
end

local function redraw_canvas(self)
	if m.tabs.value ~= m.container then
		return;
	end
	local ccnv = self.dccnv
	stats:start_frame()
	ccnv:Activate()
	ccnv:Clear()
	local lv = m.get_current_frame_data()
	if lv and lv._frame then
		if m.vp_active then
			m.vp_img = liveimg.get_viewport_pimg(m.vp_img,lv._frame,m.vp_par == 2)
			if m.vp_img then
				if aspect_toggle.value == "ON" then
					m.vp_img:put_to_cd_canvas(ccnv,
						lv.vp.margin_left/m.vp_par,
						lv.vp.margin_bot*m.vp_aspect_factor,
						m.vp_img:width(),
						m.vp_img:height()*m.vp_aspect_factor)
				else
					m.vp_img:put_to_cd_canvas(ccnv,
						lv.vp.margin_left/m.vp_par,
						lv.vp.margin_bot)
				end
			end
		end
		if m.bm_active then
			m.bm_img = liveimg.get_bitmap_pimg(m.bm_img,lv._frame,m.bm_par == 2)
			if m.bm_img then
				-- NOTE bitmap assumed fullscreen, margins ignored
				if bm_fit_toggle.value == "ON" then
					m.bm_img:blend_to_cd_canvas(ccnv, 0, 0, lv.vp:get_screen_width()/m.vp_par, lv.vp:get_screen_height()*m.vp_aspect_factor)
				else
					m.bm_img:blend_to_cd_canvas(ccnv, 0, lv.vp:get_screen_height() - lv.bm.visible_height)
				end
			else
				print('no bm')
			end
		end
	end
	ccnv:Flush()
	stats:end_frame()
end

function m.init()
	if not m.live_support() then
		return false
	end
	local icnv = iup.canvas{rastersize="360x240",border="NO",expand="NO"}
	m.icnv = icnv
	m.statslabel = iup.label{size="90x64",alignment="ALEFT:ATOP"}
	m.container = iup.hbox{
		iup.frame{
			icnv,
		},
		iup.vbox{
			iup.frame{
				iup.vbox{
					vp_toggle,
					bm_toggle,
					vp_par_toggle,
					bm_par_toggle,
					bm_fit_toggle,
					aspect_toggle,
					iup.hbox{
						iup.label{title="Target FPS"},
						iup.text{
							spin="YES",
							spinmax="30",
							spinmin="1",
							spininc="1",
							value="10",
							action=function(self,c,newval)
								local v = tonumber(newval)
								local min = tonumber(self.spinmin)
								local max = tonumber(self.spinmax)
								if v and v >= min and v <= max then
									self.value = tostring(v)
									self.caretpos = string.len(tostring(v))
									update_fps(self.value)
								end
								return iup.IGNORE
							end,
							spin_cb=function(self,newval)
								update_fps(newval)
							end
						},
					},
					iup.button{
						title="Screenshot",
						action=function(self)
							-- quick n dirty screenshot
							local cnv = icnv.dccnv
							local w,h = cnv:GetSize()
							local bm = cd.CreateBitmap(w,h,cd.RGB)
							cnv:GetBitmap(bm,0,0)
							local lb=lbuf.new(w*h*3)
							local o=0
							for y=h-1,0,-1 do
								for x=0,w-1 do
									lb:set_u8(o,bm.r[y*w + x])
									o=o+1
									lb:set_u8(o,bm.g[y*w + x])
									o=o+1
									lb:set_u8(o,bm.b[y*w + x])
									o=o+1
								end
							end
							cd.KillBitmap(bm)
							local filename = 'chdkptp_'..os.date('%Y%m%d_%H%M%S')..'.ppm'
							local fh, err = io.open(filename,'wb')
							if not fh then
								warnf("failed to open %s: %s",tostring(filename),tostring(err))
								return
							end
							fh:write(string.format('P6\n%d\n%d\n%d\n', w, h,255))
							lb:fwrite(fh)
							fh:close()
							gui.infomsg('wrote %dx%d ppm %s\n',w,h,tostring(filename))

						end
					},
				},
				title="Stream"
			},
			iup.tabs{
				iup.vbox{
					m.statslabel,
					tabtitle="Statistics",
				},
				iup.vbox{
					tabtitle="Debug",
					iup.toggle{title="Dump to file",action=toggle_dump},
					iup.toggle{title="Play from file",action=toggle_play_dump},
					iup.button{
						title="Quick dump",
						action=function()
							add_status(cli:execute('lvdump'))
						end,
					},
				},
			},
		},
		margin="4x4",
		ngap="4"
	}

	function icnv:map_cb()
		if prefs.gui_context_plus then
			-- TODO UseContextPlus seems harmless if not built with plus support
			if guisys.caps().CDPLUS then
				cd.UseContextPlus(true)
				gui.infomsg("ContexIsPlus iup:%s cd:%s\n",tostring(cd.ContextIsPlus(cd.IUP)),tostring(cd.ContextIsPlus(cd.DBUFFER)))
			else
				gui.infomsg("context_plus requested but not available\n")
			end
		end
		self.ccnv = cd.CreateCanvas(cd.IUP,self)
		self.dccnv = cd.CreateCanvas(cd.DBUFFER,self.ccnv)
		if prefs.gui_context_plus and guisys.caps().CDPLUS then
			cd.UseContextPlus(false)
		end
		self.dccnv:SetBackground(cd.EncodeColor(32,32,32))
	end

	icnv.action=redraw_canvas

	function icnv:unmap_cb()
		self.dccnv:Kill()
		self.ccnv:Kill()
	end

	function icnv:resize_cb(w,h)
		gui.dbgmsg("Resize: Width="..w.."   Height="..h..'\n')
	end

	m.container_title='Live'
end

function m.set_tabs(tabs)
	m.tabs = tabs
end
function m.get_container()
	return m.container
end
function m.get_container_title()
	return m.container_title
end
function m.on_connect_change(lcon)
	m.live_con_valid = false
	if con:is_connected() then
		reset_last_frame_vals()
		if con:live_is_api_compatible() then
			m.live_con_valid = true
		else
			warnf('camera live view protocol not supported by this client, live view disabled')
		end
	end
end
-- check whether we should be running, update timer
function m.update_run_state(state)
	if state == nil then
		state = (m.tabs.value == m.container)
	end
	if state then
		if m.timer then
			m.timer.run = "YES"
		end
		m.skip_frames = 0
		m.skip_count = 0
		stats:start()
	else
		if m.timer then
			m.timer.run = "NO"
		end
		stats:stop()
	end
end
function m.on_tab_change(new,old)
	if not m.live_support() then
		return
	end
	if new == m.container then
		m.update_run_state(true)
	else
		m.update_run_state(false)
	end
end

-- for anything that needs to be intialized when everything is started
function m.on_dlg_run()
	m.set_frame_time(100)
end
prefs._add('gui_live_sched','boolean','use scheduler for live updates',false,
	nil,
	function(self,val) 
		self.value = val
		if m.frame_time then
			m.set_frame_time(m.frame_time)
		end
	end
)
-- windows degrades gracefully if req rate is too high
prefs._add('gui_live_dropframes','boolean','drop frames if target fps too high',(sys.ostype() ~= 'Windows'))
prefs._add('gui_dump_palette','boolean','dump live palette data on state change')
prefs._add('gui_context_plus','boolean','use IUP context plus if available')
prefs._add('gui_force_replay_palette','number','override palette type dump replay, -1 disable',-1)
return m
