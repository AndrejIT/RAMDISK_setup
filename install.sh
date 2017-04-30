#! /bin/sh

SERVICE="minetestserver"
WORLD="justtest"
USERNAME="minetestuser"
MINETESTFOLDER="/home/$USERNAME/.minetest"
WORLDFOLDER="/home/$USERNAME/.minetest/worlds/$WORLD"



cp clear_players.py $MINETESTFOLDER/

chown $USERNAME:$USERNAME $MINETESTFOLDER/clear_players.py


chmod +x $MINETESTFOLDER/clear_players.py


adduser $USERNAME
usermod -L $USERNAME

usermod -G $USERNAME user

cp $SERVICE /etc/init.d/
chmod +x /etc/init.d/$SERVICE
update-rc.d $SERVICE defaults
