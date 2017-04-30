# RAMDISK_setup
Script to setup Minetest server as Linux service.

Important! Right now scripts expect minetestserver to be compiled with modified map save path!
You can see how i did this at end of this readme.

Running as service ensures that minetestserver will start when server start.
If minetestserver crashes, script will bring it up, until crashes are persistent.
Script stores player files and map database completely in RAM.
Creates backups of player inventory files, auth.txt, map database and clears and backup tebug.txt file.




Here is how i modified minetest map folder:

commit 9caeb9cdc87e78827d96e2c0139e15dc1fd81384
Author: AndrejIT <AndrejIT@rambler.ru>
Date:   Mon Oct 24 16:11:27 2016 +0300

    Store map.sqlite and rollback.sqlite in it's own folder "map" so this folder can be put in ramdisk.

diff --git a/src/database-sqlite3.cpp b/src/database-sqlite3.cpp
index 095d485..0cbf4db 100644
--- a/src/database-sqlite3.cpp
+++ b/src/database-sqlite3.cpp
@@ -142,7 +142,7 @@ void Database_SQLite3::openDatabase()
 {
 	if (m_database) return;

-	std::string dbp = m_savedir + DIR_DELIM + "map.sqlite";
+	std::string dbp = m_savedir + DIR_DELIM + "map" + DIR_DELIM + "map.sqlite";

 	// Open the database connection

@@ -297,4 +297,3 @@ Database_SQLite3::~Database_SQLite3()

 	SQLOK_ERRSTREAM(sqlite3_close(m_database), "Failed to close database");
 }
-
diff --git a/src/map.cpp b/src/map.cpp
index 38f0fa3..7d13b4a 100644
--- a/src/map.cpp
+++ b/src/map.cpp
@@ -2804,7 +2804,7 @@ s16 ServerMap::findGroundLevel(v2s16 p2d)

 bool ServerMap::loadFromFolders() {
 	if (!dbase->initialized() &&
-			!fs::PathExists(m_savedir + DIR_DELIM + "map.sqlite"))
+			!fs::PathExists(m_savedir + DIR_DELIM + "map" + DIR_DELIM + "map.sqlite"))
 		return true;
 	return false;
 }
diff --git a/src/rollback.cpp b/src/rollback.cpp
index 4d34dec..930ab23 100644
--- a/src/rollback.cpp
+++ b/src/rollback.cpp
@@ -97,9 +97,9 @@ RollbackManager::RollbackManager(const std::string & world_path,
 	verbosestream << "RollbackManager::RollbackManager(" << world_path
 		<< ")" << std::endl;

-	std::string txt_filename = world_path + DIR_DELIM "rollback.txt";
+	std::string txt_filename = world_path + DIR_DELIM + "map" + DIR_DELIM "rollback.txt";
 	std::string migrating_flag = txt_filename + ".migrating";
-	database_path = world_path + DIR_DELIM "rollback.sqlite";
+	database_path = world_path + DIR_DELIM + "map" + DIR_DELIM "rollback.sqlite";

 	bool created = initDatabase();

@@ -970,4 +970,3 @@ std::list<RollbackAction> RollbackManager::getRevertActions(

 	return getActionsSince(first_time, actor_filter);
 }
-
