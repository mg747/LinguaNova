import sqlite3
import json
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chat_history.db')

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  tab TEXT,
                  role TEXT, 
                  content TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                  
    # User Profile table
    c.execute('''CREATE TABLE IF NOT EXISTS user_profile
                 (id INTEGER PRIMARY KEY,
                  username TEXT DEFAULT 'CyberLearner',
                  avatar_seed TEXT DEFAULT 'VIPLearner',
                  primary_lang TEXT DEFAULT 'English',
                  target_lang TEXT DEFAULT 'Spanish',
                  xp INTEGER DEFAULT 150,
                  streak INTEGER DEFAULT 3,
                  last_login_date TEXT,
                  goal_minutes INTEGER DEFAULT 20)''')
                  
    # Saved Sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS saved_sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  tab TEXT,
                  messages_json TEXT,
                  summary TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                  
    # Game Scores table
    c.execute('''CREATE TABLE IF NOT EXISTS game_scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  game_type TEXT,
                  score INTEGER,
                  max_score INTEGER,
                  language TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Seed initial user profile if not exists
    c.execute("SELECT COUNT(*) FROM user_profile WHERE id = 1")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO user_profile (id, username, avatar_seed, primary_lang, target_lang, xp, streak, last_login_date, goal_minutes)
                     VALUES (1, 'CyberLearner', 'VIPLearner', 'English', 'Spanish', 150, 3, ?, 20)""", 
                     (date.today().isoformat(),))
                     
    conn.commit()
    conn.close()

def save_message(tab, role, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO messages (tab, role, content) VALUES (?, ?, ?)", (tab, role, content))
    conn.commit()
    conn.close()

def load_messages(tab):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE tab = ? ORDER BY timestamp ASC", (tab,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def clear_messages(tab):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE tab = ?", (tab,))
    conn.commit()
    conn.close()

def get_user_profile():
    init_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, avatar_seed, primary_lang, target_lang, xp, streak, last_login_date, goal_minutes FROM user_profile WHERE id = 1")
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "username": row[0],
            "avatar_seed": row[1],
            "primary_lang": row[2],
            "target_lang": row[3],
            "xp": row[4],
            "streak": row[5],
            "last_login_date": row[6],
            "goal_minutes": row[7]
        }
    return {
        "username": "CyberLearner",
        "avatar_seed": "VIPLearner",
        "primary_lang": "English",
        "target_lang": "Spanish",
        "xp": 150,
        "streak": 3,
        "last_login_date": date.today().isoformat(),
        "goal_minutes": 20
    }

def update_user_profile(username=None, avatar_seed=None, primary_lang=None, target_lang=None, goal_minutes=None):
    current = get_user_profile()
    conn = get_connection()
    c = conn.cursor()
    c.execute("""UPDATE user_profile SET 
                 username = ?, avatar_seed = ?, primary_lang = ?, target_lang = ?, goal_minutes = ?
                 WHERE id = 1""", (
        username if username is not None else current["username"],
        avatar_seed if avatar_seed is not None else current["avatar_seed"],
        primary_lang if primary_lang is not None else current["primary_lang"],
        target_lang if target_lang is not None else current["target_lang"],
        goal_minutes if goal_minutes is not None else current["goal_minutes"]
    ))
    conn.commit()
    conn.close()

def add_xp(amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE user_profile SET xp = xp + ? WHERE id = 1", (amount,))
    c.execute("SELECT xp FROM user_profile WHERE id = 1")
    new_xp = c.fetchone()[0]
    conn.commit()
    conn.close()
    return new_xp

def claim_daily_checkin():
    profile = get_user_profile()
    today_str = date.today().isoformat()
    if profile["last_login_date"] == today_str:
        return False, "Already claimed today! Come back tomorrow to keep your streak going."
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE user_profile SET streak = streak + 1, xp = xp + 35, last_login_date = ? WHERE id = 1", (today_str,))
    conn.commit()
    conn.close()
    return True, "Streak increased! +35 XP awarded for daily check-in!"

def save_chat_session(title, tab_name):
    messages = load_messages(tab_name)
    if not messages:
        return False, "No messages to save in this session."
        
    conn = get_connection()
    c = conn.cursor()
    messages_json = json.dumps(messages)
    summary = f"{len(messages)} messages ({datetime.now().strftime('%b %d, %Y %H:%M')})"
    c.execute("INSERT INTO saved_sessions (title, tab, messages_json, summary) VALUES (?, ?, ?, ?)",
              (title or f"Session - {tab_name.title()} ({datetime.now().strftime('%b %d')})", tab_name, messages_json, summary))
    conn.commit()
    conn.close()
    add_xp(40)
    return True, "Chat session successfully archived! +40 XP gained."

def get_saved_sessions():
    init_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, tab, messages_json, summary, created_at FROM saved_sessions ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    sessions = []
    for r in rows:
        try:
            msgs = json.loads(r[3])
        except Exception:
            msgs = []
        sessions.append({
            "id": r[0],
            "title": r[1],
            "tab": r[2],
            "messages": msgs,
            "summary": r[4],
            "created_at": r[5]
        })
    return sessions

def delete_saved_session(session_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM saved_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def record_game_score(game_type, score, max_score, language):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO game_scores (game_type, score, max_score, language) VALUES (?, ?, ?, ?)",
              (game_type, score, max_score, language))
    conn.commit()
    conn.close()
    earned_xp = score * 15
    if earned_xp > 0:
        add_xp(earned_xp)
    return earned_xp

def get_stats():
    init_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages")
    total_messages = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM saved_sessions")
    total_sessions = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*), COALESCE(SUM(score), 0) FROM game_scores")
    game_row = c.fetchone()
    total_games = game_row[0]
    total_score = game_row[1]
    
    conn.close()
    profile = get_user_profile()
    
    # Calculate Level based on XP
    # Level 1: 0-99, Level 2: 100-249, Level 3: 250-499, Level 4: 500-999, Level 5: 1000+
    xp = profile["xp"]
    if xp < 100:
        level_name = "Novice Explorer"
        level_num = 1
        level_progress = xp / 100
        next_threshold = 100
    elif xp < 250:
        level_name = "Apprentice Speaker"
        level_num = 2
        level_progress = (xp - 100) / 150
        next_threshold = 250
    elif xp < 500:
        level_name = "Fluent Voyager"
        level_num = 3
        level_progress = (xp - 250) / 250
        next_threshold = 500
    elif xp < 1000:
        level_name = "Cyber Polyglot"
        level_num = 4
        level_progress = (xp - 500) / 500
        next_threshold = 1000
    else:
        level_name = "Neural Grandmaster"
        level_num = 5
        level_progress = 1.0
        next_threshold = 1000
        
    return {
        "profile": profile,
        "total_messages": total_messages,
        "total_sessions": total_sessions,
        "total_games": total_games,
        "total_score": total_score,
        "level_name": level_name,
        "level_num": level_num,
        "level_progress": min(max(level_progress, 0.0), 1.0),
        "next_threshold": next_threshold
    }

init_db()
