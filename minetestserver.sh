#!/bin/sh

# This script is not init.d anymore! It is bunch of functions to call from systems units!
# Author: Andrey
# New version 2018.08

#Settings
SERVICE="minetestserver"
WORLD="justtest"
USERNAME="minetestuser"
PERMISSIONS="$USERNAME:$USERNAME"
MINETESTFOLDER="/home/$USERNAME/.minetest"
WORLDFOLDER="/home/$USERNAME/.minetest/worlds/$WORLD"
INVOCATION="/usr/local/bin/minetestserver"
OPTIONS="--worldname $WORLD --quiet"
RAMDISKSIZE="2G"

# Exit if the package is not installed
[ -x "$INVOCATION" ] || exit 0

# MINETEST SERVER
mt_start() {
    $INVOCATION $OPTIONS
}

# WHOLE WORLD DIRECTORY RAMDISK
mt_ramdisk_start() {
    if [ ! -d $WORLDFOLDER.safe ]; then
        exit 3
    fi
    mount -t ramfs -o size=$RAMDISKSIZE ramfs $WORLDFOLDER
    chown $PERMISSIONS $WORLDFOLDER
    rsync -q -t -W -r -og --chown=$PERMISSIONS $WORLDFOLDER.safe/ $WORLDFOLDER/
}
mt_ramdisk_stop() {
    rsync -q -t -W -r -og --chown=$PERMISSIONS $WORLDFOLDER/ $WORLDFOLDER.safe/
    umount $WORLDFOLDER
}

# MINETEST WEEKLY Backup
mt_backup() {
    rsync -q -t -W -r -og --chown=$PERMISSIONS $WORLDFOLDER.safe/ $WORLDFOLDER.backup/
}

# MINETEST DAYLY Save and Maintain
mt_save() {
    if [ -f $WORLDFOLDER/players.sqlite ]; then
        $MINETESTFOLDER/maintenance/clear_players.sqlite.py $WORLDFOLDER/players.sqlite
    fi
    rsync -q -t -W -r -og --chown=$PERMISSIONS $WORLDFOLDER/ $WORLDFOLDER.safe/
}


#Start-Stop here
case "$1" in
start)
mt_start
;;
ramdisk_start)
mt_ramdisk_start
;;
ramdisk_stop)
mt_ramdisk_stop
;;
backup)
mt_backup
;;
save)
mt_save
;;

*)
echo "Usage: From systemd {start|ramdisk_start|mt_ramdisk_stop}"
exit 1
;;
esac

exit 0
