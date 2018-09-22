#! /bin/sh

SERVICE="minetestserver"
RAMDISKSERVICE="minetestramdisk"
BACKUPSERVICE="minetestbackup"
SAVESERVICE="minetestsave"
WORLD="justtest"
USERNAME="minetestuser"
PERMISSIONS="$USERNAME:$USERNAME"
MINETESTFOLDER="/home/$USERNAME/.minetest"
WORLDFOLDER="/home/$USERNAME/.minetest/worlds/$WORLD"

echo "Clean before Minetestserver RAMDISK install..."

# Try to stop and clean old style init.d service or new systemd service
service $SERVICE stop
update-rc.d -f $SERVICE remove
rm /etc/init.d/$SERVICE
systemctl disable $SERVICE.service
rm /etc/systemd/system/$SERVICE.service
service $RAMDISKSERVICE stop
systemctl disable $RAMDISKSERVICE.service
rm /etc/systemd/system/$RAMDISKSERVICE.service
service $BACKUPSERVICE stop
systemctl disable $BACKUPSERVICE.service
rm /etc/systemd/system/$BACKUPSERVICE.service
systemctl disable $BACKUPSERVICE.timer
rm /etc/systemd/system/$BACKUPSERVICE.timer
service $SAVESERVICE stop
systemctl disable $SAVESERVICE.service
rm /etc/systemd/system/$SAVESERVICE.service
systemctl disable $SAVESERVICE.timer
rm /etc/systemd/system/$SAVESERVICE.timer

echo "Minetestserver install..."

# create user for service if not exists
if [ ! id -u $USERNAME > /dev/null 2>&1 ]; then
    useradd -m $USERNAME
    usermod -L $USERNAME
    usermod -G $USERNAME user
fi

# Executable for services
cp --no-preserve=mode,ownership minetestserver.sh /usr/local/bin/
chmod +x /usr/local/bin/minetestserver.sh

# Register game service
cp --no-preserve=mode,ownership $SERVICE.service /etc/systemd/system/   # /usr/lib/systemd/system/ # More correct, but only works on nev servers
systemctl enable $SERVICE.service

# Adapt world directory to be used with ramdisk
if [ ! -d $WORLDFOLDER.safe ]; then
    mv $WORLDFOLDER $WORLDFOLDER.safe
    mkdir $WORLDFOLDER
    chown $PERMISSIONS $WORLDFOLDER/
fi

echo "Minetestserver RAMDISK install..."

# Register RAMDISK service
cp --no-preserve=mode,ownership $RAMDISKSERVICE.service /etc/systemd/system/
systemctl enable $RAMDISKSERVICE.service

echo "Minetestserver BACKUP install..."

# Register BACKUP service and timer
cp --no-preserve=mode,ownership $BACKUPSERVICE.service /etc/systemd/system/
systemctl enable $BACKUPSERVICE.service
cp --no-preserve=mode,ownership $BACKUPSERVICE.timer /etc/systemd/system/
systemctl enable $BACKUPSERVICE.timer

# Register SAVE service and timer
cp --no-preserve=mode,ownership $SAVESERVICE.service /etc/systemd/system/
systemctl enable $SAVESERVICE.service
cp --no-preserve=mode,ownership $SAVESERVICE.timer /etc/systemd/system/
systemctl enable $SAVESERVICE.timer

# TODO Register ARCHIVE service and timer
# TODO Register MAINTENANCE service and timer

# Executable for maintenance
cp --no-preserve=mode,ownership clear_players.py $MINETESTFOLDER/
chmod +x $MINETESTFOLDER/clear_players.py


echo "End of Minetestserver install"
