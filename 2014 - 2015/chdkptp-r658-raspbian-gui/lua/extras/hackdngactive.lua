--[[
modify dng active area
]]
function hackaa(infile,outfile,top,left,bottom,right)
	local dnglib=require'dng'
	local d,err=dnglib.load(infile)
	if not d then
		error(string.format('error %s loading input',tostring(err)))
	end
	local aa_new={top,left,bottom,right}
	local aa_names={'top','left','bottom','right'}
	local ifd=d:get_ifd{0,0}
	local aa_old=ifd.byname.ActiveArea:getel_array()
	local aa_off=d._lb:get_u32(ifd.byname.ActiveArea.off + 8)
	for i,v in ipairs(aa_new) do
		printf("%s %d->%d\n",aa_names[i],aa_old[i],v)
		d._lb:set_u32(aa_off,v)
		aa_off = aa_off + 4
	end
	local fh,err = io.open(outfile,'wb')
	if not fh then
		error(string.format('error %s opening output',tostring(err)))
	end
	d._lb:fwrite(fh)
	fh:close()
end
