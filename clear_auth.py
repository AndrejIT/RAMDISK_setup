#!/usr/bin/env python

#Cleans auth.txt file. Need file owners.txt with list of players to preserve (can be generated by "map_unexplore" project)

import os
import string
import re

SERVICE="minetestserver"
WORLD="justtest"
USERNAME="minetestuser"
MINETESTFOLDER="/home/"+USERNAME+"/.minetest"
WORLDFOLDER="/home/"+USERNAME+"/.minetest/worlds/"+WORLD+""

owners_path = MINETESTFOLDER+'/owners.txt'
login_path=WORLDFOLDER+'/auth.txt'
new_login_path=WORLDFOLDER+'/auth.txt.new'
bac_login_path=WORLDFOLDER+'/auth.txt.bac'

def mk_int(s):
    s = s.strip()
    return int(s) if s else 0

f_owners = open(owners_path, 'r')
owners = f_owners.readlines()
owners_login=[]
for line in owners:
    owners_login.append(line[:-1])
owners_login = sorted(owners_login)
f_owners.close()

f_logins=open(login_path, 'r') # open file
logins=f_logins.readlines()
forsave_login = []
for line in logins:
    t = string.split(line, ':')
    if t[0] in owners_login:
        forsave_login.append(line)
    elif t[1]=='':
        pass
    elif mk_int(t[3])<1483228800: # 01/01/2017
        pass
    elif mk_int(t[3])>1496275200: # 06/01/2017
        pass
    else:
        forsave_login.append(line)
forsave_login = sorted(forsave_login)
f_logins.close()

i = 0

f_new_logins = open(new_login_path, 'w') # open file for write
for line in forsave_login:
    f_new_logins.write(line)
    i+= 1
f_new_logins.close()

os.rename(login_path, bac_login_path)
os.rename(new_login_path, login_path)

print(i)
