--[[
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
module for user tab in gui
a place for user defined stuff
]]

local m={}

function m.get_container_title()
    return "User"
end

function m.init()
    m.dest = "" -- destination path for download, default is chdkptp dir
    return
end

function m.get_container()
    local usertab = iup.vbox{
        margin="4x4",
        m.remote_capture_ui(),
    }
    return usertab
end

--[[
remote capture function as gui function
* Destination - dialog for file destination, default is chdkptp dir
* JPG Remote Shoot - shoot and save a JPG file in the destination (only available for cameras that support filewrite_task)
* DNG Remote Shoot - shoot and save a DNG file in the destination
]]
function m.remote_capture_ui()
    local gui_frame = iup.frame{
        title="Remote Capture",
        iup.vbox{
            gap="10",
            iup.button{
                title="Destination",
                size="75x15",
                fgcolor="0 0 255",
                action=function(self)
                    local dlg=iup.filedlg{
                        dialogtype = "DIR",
                        title = "Destination",
                    }
                    dlg:popup(iup_centerparent, iup_centerparent)
                    if dlg.status == "0" then
                        m.dest = dlg.value
                        gui.infomsg("download destination %s\n", m.dest)
                    end
                end,
            },
            iup.button{
                title="JPG Remote Shoot",
                size="75x15",
                fgcolor="255 0 0",
                tip="Does not work for all cameras!",
                action=function(self)
                    local cmd = m.dest ~= "" and string.format("rs '%s'", m.dest) or "rs"
                    add_status(cli:execute(cmd))
                end,
            },
            iup.button{
                title="DNG Remote Shoot",
                size="75x15",
                fgcolor="255 0 0",
                action=function(self)
                    local cmd = m.dest ~= "" and string.format("rs '%s' -dng", m.dest) or "rs -dng"
                    add_status(cli:execute(cmd))
                end,
            },
        },
    }
    return gui_frame
end

return m
