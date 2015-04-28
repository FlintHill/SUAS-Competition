
#!perl
#---------------------------------------------------------------------------
# Fetches last N files (based on date/time of pic) from camera.  (montana123)
#---------------------------------------------------------------------------
my $numFilesToGet=1;
#---------------------------------------------------------------------------

printf("\n  Fetching file list. \n");
my @fileListResponse = `ptpcam --chdk="luar require('lptpgui').dcimdl(false)"`;
sleep 2;
my @downLoadResponse = `ptpcam --chdk="download A/ptpgui.txt fileList.txt"`;
sleep 2;

printf("\n  Fetching last $numFilesToGet files.\n");
open FH, "<fileList.txt" or die $!; my @fileList=<FH>; close FH;
my $lastFile  = $#fileList;
my $firstFile = $lastFile-($numFilesToGet-1);

for ($i=$firstFile;$i<=$lastFile;$i++) {
    ($path,$name,$datetime,$junk)=split(/\|/,$fileList[$i]);
    #printf("$path-$name-$datetime-$junk\n");
    $result=`ptpcam --chdk="download $path$name $name"`;
    printf ("  > $path - $name result= $result\n");
    sleep 2;
}

printf("\n  --\nAll done.\nHit ENTER to quit."); $response=<stdin>; exit (0);