#!/usr/bin/env python

# Deletes player inventory data if there are only easily obtainable items
# Version for sqlite player database backend

import os
import string

import sys #to get parameters
import sqlite3

WORLD="justtest"
USERNAME="minetestuser"
WORLDFOLDER="/home/"+USERNAME+"/.minetest/worlds/"+WORLD+""

path = WORLDFOLDER+'/players.sqlite'

arguments = sys.argv
if(len(arguments) == 2 ):
    path = str(arguments[1])

myconn = sqlite3.connect(path)
playercursor = myconn.cursor()
mycursor = myconn.cursor()

# sqlite3 > .schema
# `player` (name, ..., creation_date, modification_date)
# `player_metadata` (player, metadata, value)
# `player_inventories` (player, inv_id, inv_width, inv_name, inv_size)
# `player_inventory_items` (player, inv_id, slot_id, item)

# Most popular inventory items
# SELECT * FROM (SELECT COUNT(*) AS n, CASE(INSTR(item, ' ') > 1) WHEN 1 THEN SUBSTR(item, 1, INSTR(item, ' ')-1) ELSE item END as item FROM player_inventory_items GROUP BY CASE(INSTR(item, ' ') > 1) WHEN 1 THEN SUBSTR(item, 1, INSTR(item, ' ')-1) ELSE item END ) AS S ORDER BY n DESC LIMIT 30;

# Estimate worth of player inventory - empty slot = 0 points; popular items = 1 point; all othet items = 10 points.
playercursor.execute('PRAGMA foreign_keys = ON;')   # So data from tables connected to `player` will be deleted automatically
playercursor.execute("SELECT name FROM player")
# playercursor.execute("SELECT distinct player FROM player_inventory_items")
playerrows = playercursor.fetchall()
for playerrow in playerrows:
    points = 0
    mycursor.execute("SELECT COALESCE(SUM(1), 0) FROM player_inventory_items WHERE player = ? AND CASE(INSTR(item, ' ') > 1) WHEN 1 THEN SUBSTR(item, 1, INSTR(item, ' ')-1) ELSE item END IN ('default:cobble', 'default:pick_wood', 'default:torch', 'default:apple', 'climbing_pick:pick_wood', 'bones:bones', 'default:mossycobble', 'default:clay_lump', 'default:coal_lump', 'default:stick', 'default:sword_stone', 'craft_guide:sign_wall', 'default:pick_stone', 'default:furnace', 'stairs:slab_cobble');", (playerrow[0],))
    row = mycursor.fetchone()
    points = points + row[0]
    mycursor.execute("SELECT COALESCE(SUM(10), 0) FROM player_inventory_items WHERE player = ? AND CASE(INSTR(item, ' ') > 1) WHEN 1 THEN SUBSTR(item, 1, INSTR(item, ' ')-1) ELSE item END NOT IN ('', 'default:cobble', 'default:pick_wood', 'default:torch', 'default:apple', 'climbing_pick:pick_wood', 'bones:bones', 'default:mossycobble', 'default:clay_lump', 'default:coal_lump', 'default:stick', 'default:sword_stone', 'craft_guide:sign_wall', 'default:pick_stone', 'default:furnace', 'stairs:slab_cobble');", (playerrow[0],))
    row = mycursor.fetchone()
    points = points + row[0]

    if (points < 6):
        playercursor.execute("DELETE FROM player WHERE name = ?", (playerrow[0],))
        print(playerrow[0])
myconn.commit()
mycursor.execute("VACUUM")
