# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import os
from pymongo import MongoClient

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "mohammed_poster_bot"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    # Test connection
    client.server_info()
    USE_MONGO = True
except Exception:
    USE_MONGO = False
    import sqlite3
    DB_FILE = "bot_database.db"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def init_db():
    if not USE_MONGO:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, first_name TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS fsub_channels (channel TEXT PRIMARY KEY)")
        cursor.execute("CREATE TABLE IF NOT EXISTS banned_users (user_id INTEGER PRIMARY KEY)")
        cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value INTEGER DEFAULT 1)")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('global_pm_search', 1)")
        conn.commit()
        conn.close()
    else:
        # Ensure default setting exists in Mongo
        if db.settings.find_one({"key": "global_pm_search"}) is None:
            db.settings.insert_one({"key": "global_pm_search", "value": 1})

def get_global_pm_search():
    try:
        if USE_MONGO:
            res = db.settings.find_one({"key": "global_pm_search"})
            return bool(res["value"]) if res else True
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'global_pm_search'")
            row = cursor.fetchone()
            conn.close()
            return bool(row[0]) if row else True
    except Exception:
        return True

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def set_global_pm_search(enabled):
    try:
        val = 1 if enabled else 0
        if USE_MONGO:
            db.settings.update_one({"key": "global_pm_search"}, {"$set": {"value": val}}, upsert=True)
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('global_pm_search', ?)", (val,))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def add_user(user_id, first_name):
    try:
        if USE_MONGO:
            db.users.update_one({"user_id": user_id}, {"$set": {"first_name": first_name}}, upsert=True)
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name))
            cursor.execute("UPDATE users SET first_name = ? WHERE user_id = ?", (first_name, user_id))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_all_users():
    try:
        if USE_MONGO:
            return [(u["user_id"], u.get("first_name", "user")) for u in db.users.find()]
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, first_name FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
    except Exception:
        return []

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def is_banned(user_id):
    try:
        if USE_MONGO:
            return db.banned_users.find_one({"user_id": user_id}) is not None
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,))
            banned = cursor.fetchone() is not None
            conn.close()
            return banned
    except Exception:
        return False

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def ban_user(user_id):
    try:
        if USE_MONGO:
            db.banned_users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def unban_user(user_id):
    try:
        if USE_MONGO:
            db.banned_users.delete_one({"user_id": user_id})
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_banned_users():
    try:
        if USE_MONGO:
            return [u["user_id"] for u in db.banned_users.find()]
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM banned_users")
            banned = [row[0] for row in cursor.fetchall()]
            conn.close()
            return banned
    except Exception:
        return []

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_fsub_channels():
    env_channels = os.environ.get("FORCE_SUB_CHANNELS", "")
    channels = [ch.strip() for ch in env_channels.split(",") if ch.strip()]
    try:
        if USE_MONGO:
            db_channels = [c["channel"] for c in db.fsub_channels.find()]
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT channel FROM fsub_channels")
            db_channels = [row[0] for row in cursor.fetchall()]
            conn.close()
        
        for ch in db_channels:
            if ch not in channels:
                channels.append(ch)
    except Exception:
        pass
    return channels

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def add_fsub_channel(channel):
    try:
        if USE_MONGO:
            db.fsub_channels.update_one({"channel": channel}, {"$set": {"channel": channel}}, upsert=True)
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO fsub_channels (channel) VALUES (?)", (channel,))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def remove_fsub_channel(channel):
    try:
        if USE_MONGO:
            db.fsub_channels.delete_one({"channel": channel})
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fsub_channels WHERE channel = ?", (channel,))
            conn.commit()
            conn.close()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #