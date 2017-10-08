#!/usr/bin/env python

#Deletes player inventory file if there are only certain, easily obtainable items 

import os
import string
import re

SERVICE="minetestserver"
WORLD="justtest"
USERNAME="minetestuser"
MINETESTFOLDER="/home/"+USERNAME+"/.minetest"
WORLDFOLDER="/home/"+USERNAME+"/.minetest/worlds/"+WORLD+""

path = WORLDFOLDER+'/players.safe/'
# path = WORLDFOLDER+'/players/'


simple_stuff_secure=re.compile(
    "List main 32\n"+"Width 0\n" +
    "(Empty\n|Item default:pick_wood( 1 (\d){0,5}){0,1}\n|Item default:torch( 1| 2| 3){0,1}\n|Item default:apple( 1| 2| 3){0,1}\n|Item bones:bones( 1| 2| 3){0,1}\n|Item default:cobble( 1| 2| 3){0,1}\n){5,5}"+
    "(Empty\n){27,27}" +
    "EndInventoryList\n" +
    "(List hand 1\n" + "Width 0\n" + "Empty\n" + "EndInventoryList\n){0,1}" + #upgrade from new version ~4.16
    "List craft 9\n" +"Width 3\n" +
    "(Empty\n|Item default:pick_wood( 1 (\d){0,5}){0,1}\n|Item default:torch( 1| 2| 3){0,1}\n|Item default:apple( 1| 2| 3){0,1}\n|Item bones:bones( 1| 2| 3){0,1}\n|Item default:cobble( 1| 2| 3){0,1}\n){9,9}"+
    "EndInventoryList\n" +
    "List craftpreview 1\nWidth 0\nEmpty\nEndInventoryList\nList craftresult 1\nWidth 0\nEmpty\nEndInventoryList\nEndInventory" +
    "$"
    )
simple_stuff_unsecure=re.compile(
    "List main 32\n"+"Width 0\n" +
    "(Empty\n|Item default:pick_wood( 1 (\d){0,5}){0,1}\n|Item default:torch( 1| 2| 3| 4){0,1}\n|Item default:apple( 1| 2| 3| 4){0,1}\n|Item bones:bones( 1| 2| 3| 4){0,1}\n|Item default:cobble( 1| 2| 3| 4| 5){0,1}\n){32,32}"+
    "EndInventoryList\n" +
    "(List hand 1\n" + "Width 0\n" + "Empty\n" + "EndInventoryList\n){0,1}" + #upgrade from new version ~4.16
    "List craft 9\n" +"Width 3\n" +
    "(Empty\n|Item default:pick_wood( 1 (\d){0,5}){0,1}\n|Item default:torch( 1| 2| 3| 4){0,1}\n|Item default:apple( 1| 2| 3| 4){0,1}\n|Item bones:bones( 1| 2| 3| 4){0,1}\n|Item default:cobble( 1| 2| 3| 4| 5){0,1}\n){9,9}"+
    "EndInventoryList\n" +
    "List craftpreview 1\nWidth 0\nEmpty\nEndInventoryList\nList craftresult 1\nWidth 0\nEmpty\nEndInventoryList\nEndInventory" +
    "" #upgrade from new version
    )
pick_collector=re.compile( "Item default:pick_wood(| 1 (\d){3,5})\n" )

def mk_int(s):
    s = s.strip()
    return int(s) if s else 0


i=0

for fname in os.listdir(path):    # change directory as needed
    try:
        f=open(path+fname, 'r') # open file
        data=f.read()
        f.close()
        simple_inventory=0
        if simple_stuff_unsecure.search(data)!=None:
            simple_inventory=1
        elif simple_stuff_secure.search(data)!=None:
            if len( pick_collector.findall(data) )<3:
                simple_inventory=1
        if simple_inventory==1:
            os.remove(path+fname)
            #print(path+fname)
            i+=1

    except IOError:
        print("ERROR;", fname)


print(i)
