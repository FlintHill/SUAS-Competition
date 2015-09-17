--[[
example of downloading and deleting form DCIM directory
]]
function dcimdl(destdir,del,pretend) 
	if pretend then
		pretend = '-pretend '
	else
		pretend = ''
	end
	local dcim,err=con:listdir('A/DCIM')
	if not dcim then
		printf('error listing directory %s\n',tostring(err))
	end
	for i,dname in ipairs(dcim) do
		if dname ~= 'CANONMSC' then
			cli:print_status(cli:execute('mdl '..pretend..' -fmatch=%.[JDC][PNR][G2]$ DCIM/'..dname..' '..destdir))
			if del then
				cli:print_status(cli:execute('rm '..pretend..' -nodirs -fmatch=%.[JDC][PNR][G2]$ DCIM/'..dname))
			end
		end
	end
end
