# RAMDISK_setup
Script to setup Minetest server as Linux systemd service.
With Ramdisk, backup ...

Now, as of 2018.09 script make one ramdisk for whole minetest world directory

Running as service ensures that minetestserver will start when server start.
Script stores map database and other world files completely in RAM.
Creates backups of world.
# TODO - clear and backup tebug.txt file.
# TODO - regularly archive auth.txt file
# TODO - regularly run maintenance scripts
# TODO - rewrite maintenance scripts

# TODO - find and fix problem, when map file is broken
