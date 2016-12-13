README

This program, cropper, can go through a directory full of images
and crop anything that might potentially be a target. In order to
run it;

1 - Takes the images you'd like to parse though, name the files 0.jpg
through n.jpg
2 - place the 'cropper' executable in the directory with the images
3 - make a subdirectory named 'crops'
4 - navigate to the directory in terminal
5 - run './cropper [pixels per inch] [n (number of images)]'
6 - sit back while potential crops are saved in the 'crops' subdirectory
which you created

There is a still a large amount of false positives - however, the 
vast majority of these are only found on takeoff/landing, when the 
images are full of interesting shapes like chairs, people, and other
bold/artifical things
