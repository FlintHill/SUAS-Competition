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
util=require'util'
util:import()
errutil=require'errutil'
ustime=require'ustime'
fsutil=require'fsutil'
prefs=require'prefs'
varsubst=require'varsubst'
chdku=require'chdku'
cli=require'cli'
exp=require'exposure'
dng=require'dng'
dngcli=require'dngcli'

--[[
Command line arguments
--]]
function bool_opt(rest)
	if rest == '-' then
		return true,false
	elseif rest ~= '' then
		return false
	end
	return true,true
end

cmd_opts = {
	{
		opt="g",
		help="start GUI - default if GUI available and no options given",
		process=bool_opt,
	},
	{
		opt="i",
		help="start interactive cli",
		process=bool_opt,
	},
	{
		opt="c",
		help='connect at startup, with optional device spec e.g. -c"-d001 -bbus-0"',
		process=function(rest)
			if rest then
				options.c = rest
			else
				options.c = true
			end
			return true,options.c
		end,
	},
	{
		opt="e",
		help='execute cli command, multiple allowed, e.g -e"u DISKBOOT.BIN" -ereboot',
		process=function(rest)
			if type(options.e) == 'table' then
				table.insert(options.e,rest)
			else 
				options.e = {rest}
			end
			return true,options.e
		end,
	},
	{
		opt="r",
		help='specify startup command file, if no file given skip default startup files',
		process=function(rest)
			if rest and rest ~= '' then
				options.r = rest
			else
				options.r = true
			end
			return true,options.r
		end,
	},
	{
		opt="h",
		help="help",
		process=bool_opt,
	},
}

function print_help()
	printf(
[[
CHDK PTP control utility
Usage: chdkptp [options]
Options:
]])
	for i=1,#cmd_opts do
		printf(" -%-2s %s\n",cmd_opts[i].opt,cmd_opts[i].help)
	end
end

-- option values
options = {}
cmd_opts_map = {}
-- defaults TODO from prefs
function process_options(args)
	local i
	for i=1,#cmd_opts do
		options[cmd_opts[i].opt] = false
		cmd_opts_map[cmd_opts[i].opt] = cmd_opts[i]
	end

	while #args > 0 do
		local arg = table.remove(args,1)
		local s,e,cmd,rest = string.find(arg,'^-([a-zA-Z0-9])=?(.*)')
--		printf("opt %s rest (%s)[%s]\n",tostring(cmd),type(rest),tostring(rest))
		if s and options[cmd] ~= nil then
			local r,val=cmd_opts_map[cmd].process(rest,args)
			if r then
				options[cmd] = val
			else
				errf("malformed option %s\n",arg)
			end
		else
			errf("unrecognized argument %s\n",arg)
			invalid = true
		end
	end

	if options.h or invalid then
		print_help()
		return true
	end
end

--[[
return directory for rc files etc
def_path can be used to set the default if nothing reasonable is found, default nil
]]
function get_chdkptp_home(def_path)
	local path=sys.getenv('CHDKPTP_HOME')
	if not path then
		path=sys.getenv('HOME')
		if not path then
			return def_path
		end
	end
	return path
end

function do_rc_file(name)
	local path
	-- -r with no file
	if options.r == true then
		return
	elseif not options.r then
		path=get_chdkptp_home()
		if not path then
			return
		end
		-- fix . to _ on windows
		-- TODO check for both ?
		if sys.ostype() == 'Windows' and string.sub(name,1,1) == '.' then
			name = '_'..string.sub(name,2,-1)
		end
		path=fsutil.joinpath(path,name)
	else
		path = options.r
	end
	if lfs.attributes(path,'mode') ~= 'file' then
		-- if file specified on the command line, warn when not found
		if options.r then
			warnf('rc %s not found\n',path)
		end
		return false
	end
	prefs._allow_unreg(true) -- allow currently unknown prefs to be set
	local status, msg=cli:execfile(path)
	prefs._allow_unreg(false)
	if not status then
		warnf('rc %s failed: %s\n',path,tostring(msg))
		return false
	end
	return true
end

function do_connect_option()
	if options.c then
		local cmd="connect"
		if type(options.c) == 'string' then
			cmd = cmd .. ' ' .. options.c
		end
		cli:print_status(cli:execute(cmd));
	end
end

function do_execute_option()
	if options.e then
		for i=1,#options.e do
			cli:print_status(cli:execute(options.e[i]))
		end
	end
end

local function check_versions()
	if prefs.warn_deprecated and util.is_lua_ver(5,1) then
		util.warnf("Lua 5.1 is deprecated\n")
	end
	local v=chdk.program_version()
	if v.MAJOR ~= 0 or v.MINOR ~= 5 then
		error("incompatible chdkptp binary version")
	end
	-- TODO could check IUP and CD, but need to be initialized
end

function do_gui_startup()
	printf('starting gui...\n')
	if guisys.init() then
		gui=require('gui')
		do_rc_file('.chdkptpguirc')
		check_versions()
		return gui:run()
	else
		printf('gui not supported')
		os.exit(1)
	end
end

local function do_no_gui_startup()
	do_rc_file('.chdkptprc')
	check_versions()
	do_connect_option()
	do_execute_option()
	if options.i then
		return cli:run()
	end
end
prefs._add('warn_deprecated','boolean','warn on deprecated libraries',true)
prefs._add('core_verbose','number','ptp core verbosity',0,
	function(self)
		return corevar.get_verbose()
	end,
	function(self,val)
		corevar.set_verbose(val)
	end
)
prefs._add('err_trace','string',"stack trace on error, values: 'always', 'critical', 'never'",'critical',
	function(self)
		return errutil.do_traceback
	end,
	function(self,val)
		if not util.in_table({'always','critical','never'},val) then
			return false,'invalid value'
		end
		errutil.do_traceback = val
	end
)

con=chdku.connection()
dngcli.init_cli()

local args = sys.getargs()
if #args > 0 then
	process_options(args)
	if options.g then
		do_gui_startup()
	else
		do_no_gui_startup()
	end
-- if no options, start gui if available or cli if not
elseif guisys.caps().IUP then
	do_gui_startup()
else
	options.i=true
	do_no_gui_startup()
end
