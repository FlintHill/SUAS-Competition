--[[
example of modifying a DNG IFD entry
]]
function hackcfa(infile,outfile,cfa)
	local dnglib=require'dng'
	local d,err=dnglib.load(infile)
	if not d then
		error(string.format('error %s loading input',tostring(err)))
	end
	local ifd=d:get_ifd{0,0}
	local oldcfa = d._lb:get_u32(ifd.byname.CFAPattern.off+8)
	d._lb:set_u32(ifd.byname.CFAPattern.off+8,cfa)
	printf('%s old cfa=0x%08x\n%s new cfa=0x%08x\n',infile,oldcfa,outfile,d._lb:get_u32(ifd.byname.CFAPattern.off+8))
	local fh,err = io.open(outfile,'wb')
	if not fh then
		error(string.format('error %s opening output',tostring(err)))
	end
	d._lb:fwrite(fh)
	fh:close()
end
