sudo sh -c 'echo 1000 > /sys/module/usbcore/parameters/usbfs_memory_mb'
/usr/bin/udisks --mount /dev/sda1
