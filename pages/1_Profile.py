import streamlit as st
import os
import sys
import urllib.parse

# Ensure root path is accessible for db_helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db_helper

st.set_page_config(page_title="Profile & Progress - LinguaNova", page_icon="👤", layout="wide")

# Check Auth
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in on the main page to view your profile.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, .stApp, p, label, li {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    color: #e0e6ed;
    line-height: 1.5;
}

/* Prevent icon ligature breaking into text like arrow_down */
[data-testid*="stIcon"],
[class*="material-symbols"],
[class*="material-icons"],
details summary span:first-child,
[data-testid="stExpander"] summary span:first-child {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    font-size: 1.25rem !important;
    width: auto !important;
    margin-right: 8px !important;
    display: inline-block !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f0ff !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    margin-bottom: 0.8rem !important;
}
.stApp {
    background-color: #05050a !important;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(13, 110, 253, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.08) 0%, transparent 50%);
    background-attachment: fixed;
}
.main .block-container {
    padding-bottom: 120px !important;
}
.glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    border-radius: 16px !important;
    padding: 1.8rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px) scale(1.008) !important;
    border-color: rgba(0, 240, 255, 0.5) !important;
    box-shadow: 0 14px 40px 0 rgba(0, 240, 255, 0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* Stat Box */
.stat-box {
    background: rgba(0, 240, 255, 0.06);
    border: 1px solid rgba(0, 240, 255, 0.25);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
.stat-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #00f0ff;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
}
.stat-label {
    font-size: 0.95rem;
    color: #94a3b8;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Badge Tag */
.badge-unlocked {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px;
    border-radius: 14px;
    background: rgba(0, 255, 170, 0.12);
    border: 1px solid #00ffaa;
    color: #00ffaa;
    font-weight: 700;
    font-size: 0.9rem;
    box-shadow: 0 0 10px rgba(0, 255, 170, 0.2);
}
.badge-locked {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px;
    border-radius: 14px;
    background: rgba(100, 116, 139, 0.1);
    border: 1px dashed rgba(100, 116, 139, 0.4);
    color: #64748b;
    font-weight: 600;
    font-size: 0.9rem;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #0055ff 0%, #00f0ff 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', sans-serif !important;
    padding: 0.6rem 1.5rem !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6) !important;
    background: linear-gradient(90deg, #00f0ff 0%, #0055ff 100%) !important;
}

/* Inputs: clean white background, black bold text */
[data-baseweb="input"], [data-baseweb="base-input"], .stTextArea>div>div>textarea {
    background-color: #ffffff !important;
    border-radius: 8px !important;
    border: 2px solid rgba(0, 240, 255, 0.5) !important;
}
[data-baseweb="input"] input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
    color: #000000 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    padding: 0.6rem 1rem !important;
    -webkit-text-fill-color: #000000 !important;
}
[data-baseweb="input"]:focus-within, .stTextArea>div>div>textarea:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
}
.stSelectbox svg {
    fill: #000000 !important;
    width: 24px !important;
    height: 24px !important;
}

/* Footer with Social Icons */
.app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(5, 5, 10, 0.95);
    padding: 12px 24px;
    border-top: 1px solid rgba(0, 240, 255, 0.2);
    z-index: 999;
}
.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1300px;
    margin: 0 auto;
    flex-wrap: wrap;
    gap: 12px;
}
.social-icons a {
    color: #00f0ff !important;
    text-decoration: none !important;
    font-size: 1.15rem;
    margin-left: 14px;
    transition: transform 0.2s ease, color 0.2s ease;
    display: inline-block;
}
.social-icons a:hover {
    transform: translateY(-2px) scale(1.15);
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

stats = db_helper.get_stats()
profile = stats["profile"]

st.title("👤 User Profile & Progress Hub")

col_avatar, col_prog = st.columns([1, 2])

with col_avatar:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed={profile['avatar_seed']}&colors=00f0ff,0055ff,b100ff" width="140" style="border-radius: 50%; margin-bottom: 1rem; border: 3px solid #00f0ff; box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);">
        <h3 style="margin-bottom: 0.2rem;">{profile['username']}</h3>
        <p style="color: #00f0ff; font-family: 'Orbitron'; font-size: 0.95rem; margin-bottom: 0.5rem;">{stats['level_name'].upper()}</p>
        <span style="background-color: rgba(0, 255, 170, 0.2); color: #00ffaa; border: 1px solid #00ffaa; padding: 4px 14px; border-radius: 12px; font-size: 0.85rem; font-family: 'Orbitron';">LEVEL {stats['level_num']} // ONLINE</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Check-in button
    if st.button("🔥 Claim Daily Check-In", use_container_width=True):
        success, msg = db_helper.claim_daily_checkin()
        if success:
            st.success(msg)
            st.balloons()
            st.rerun()
        else:
            st.info(msg)

with col_prog:
    with st.container(border=True):
        st.markdown(f"### 📈 Level {stats['level_num']}: {stats['level_name']}")
        st.markdown(f"**Experience Points (XP):** `{profile['xp']} XP`")
        
        # Progress Bar towards next tier
        st.progress(stats['level_progress'])
        st.markdown(f"<p style='font-size: 0.9rem; color: #94a3b8;'>Progress to next milestone: {int(stats['level_progress']*100)}% (Goal: {stats['next_threshold']} XP)</p>", unsafe_allow_html=True)
        
        # 4 Core Stats Grid
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{profile['streak']}</div>
                <div class="stat-label">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{stats['total_messages']}</div>
                <div class="stat-label">Messages</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{stats['total_sessions']}</div>
                <div class="stat-label">Archived</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{stats['total_games']}</div>
                <div class="stat-label">Games Played</div>
            </div>
            """, unsafe_allow_html=True)

# Achievements Section
st.markdown("### 🏅 Neural Achievements")
with st.container(border=True):
    badges_html = ""
    badges_html += "<span class='badge-unlocked'>🌟 First Contact</span>" if stats['total_messages'] >= 1 else "<span class='badge-locked'>🔒 First Contact</span>"
    badges_html += "<span class='badge-unlocked'>⚡ Cyber Apprentice (100+ XP)</span>" if profile['xp'] >= 100 else "<span class='badge-locked'>🔒 Cyber Apprentice (100 XP)</span>"
    badges_html += "<span class='badge-unlocked'>🔥 Dedicated Voyager (3+ Day Streak)</span>" if profile['streak'] >= 3 else "<span class='badge-locked'>🔒 Dedicated Voyager (3 Days)</span>"
    badges_html += "<span class='badge-unlocked'>🎮 Arcade Challenger</span>" if stats['total_games'] >= 1 else "<span class='badge-locked'>🔒 Arcade Challenger</span>"
    badges_html += "<span class='badge-unlocked'>💾 Data Archivist</span>" if stats['total_sessions'] >= 1 else "<span class='badge-locked'>🔒 Data Archivist</span>"
    badges_html += "<span class='badge-unlocked'>🌌 Neural Master (500+ XP)</span>" if profile['xp'] >= 500 else "<span class='badge-locked'>🔒 Neural Master (500 XP)</span>"
    
    st.markdown(f"<div style='margin: 10px 0;'>{badges_html}</div>", unsafe_allow_html=True)

# Share Profile Progress
share_profile_txt = f"I'm Level {stats['level_num']} ({stats['level_name']}) on LinguaNova with {profile['xp']} XP and a {profile['streak']}-day streak! 🌐🔥"
encoded_p_txt = urllib.parse.quote(share_profile_txt)
p_t_url = f"https://twitter.com/intent/tweet?text={encoded_p_txt}&url=https://linguanova.streamlit.app"
p_w_url = f"https://api.whatsapp.com/send?text={encoded_p_txt}%20https://linguanova.streamlit.app"
p_l_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://linguanova.streamlit.app"

st.markdown(f"""
<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-top: 10px; padding: 10px 14px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px;">
    <span style="font-family: 'Orbitron'; font-size: 0.85rem; color: #00f0ff;">📢 SHARE STATUS:</span>
    <a href="{p_t_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #000; color: #fff; font-size: 0.82rem; font-weight: bold; border: 1px solid #333;">𝕏 Twitter</a>
    <a href="{p_w_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #25D366; color: #fff; font-size: 0.82rem; font-weight: bold;">💬 WhatsApp</a>
    <a href="{p_l_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #0077b5; color: #fff; font-size: 0.82rem; font-weight: bold;">💼 LinkedIn</a>
</div>
""", unsafe_allow_html=True)

# Profile Settings & Customization
with st.expander("⚙️ Customize Profile & Learning Goals"):
    with st.form("profile_form"):
        f_username = st.text_input("Display Name:", value=profile["username"])
        
        avatar_options = ["VIPLearner", "CyberSamurai", "NeonRunner", "CosmicEcho", "ByteMaster", "QuantumNova"]
        current_avatar_idx = avatar_options.index(profile["avatar_seed"]) if profile["avatar_seed"] in avatar_options else 0
        f_avatar = st.selectbox("Avatar Identity:", avatar_options, index=current_avatar_idx)
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            f_primary = st.text_input("Native Language:", value=profile["primary_lang"])
        with col_l2:
            f_target = st.text_input("Target Focus Language:", value=profile["target_lang"])
            
        f_goal = st.slider("Daily Study Goal (Minutes):", min_value=5, max_value=120, value=profile["goal_minutes"])
        
        if st.form_submit_button("Save Profile Changes"):
            db_helper.update_user_profile(
                username=f_username,
                avatar_seed=f_avatar,
                primary_lang=f_primary,
                target_lang=f_target,
                goal_minutes=f_goal
            )
            st.success("Profile updated successfully!")
            st.rerun()

# Saved Sessions Archive Viewer
st.markdown("### 💾 Saved Chat Sessions & Lesson Archives")
saved_sessions = db_helper.get_saved_sessions()

if not saved_sessions:
    st.info("No saved sessions yet. In Global Chat or AI Coach, click '💾 Save & Archive Session' to save your lessons and study them anytime!")
else:
    for s in saved_sessions:
        with st.expander(f"📁 {s['title']} — {s['summary']}"):
            st.caption(f"Archived on: {s['created_at']} | Channel: {s['tab'].upper()}")
            
            full_transcript = f"=== LinguaNova Lesson Archive ===\nTitle: {s['title']}\nDate: {s['created_at']}\nChannel: {s['tab']}\n\n"
            for m in s["messages"]:
                st.markdown(f"**{m['role'].upper()}:** {m['content']}")
                full_transcript += f"[{m['role'].upper()}]: {m['content']}\n\n"
                
            col_dl, col_del = st.columns([1, 1])
            with col_dl:
                st.download_button(
                    label="📥 Download Transcript (.txt)",
                    data=full_transcript,
                    file_name=f"LinguaNova_{s['tab']}_{s['id']}.txt",
                    mime="text/plain",
                    key=f"dl_{s['id']}"
                )
            with col_del:
                if st.button("🗑️ Delete Archive", key=f"del_{s['id']}"):
                    db_helper.delete_saved_session(s['id'])
                    st.success("Archive deleted.")
                    st.rerun()

# Footer with social media icons
st.markdown("""
<div class="app-footer">
    <div class="footer-content">
        <div style="color: #94a3b8; font-size: 0.9rem;">
            © 2026 <b style="color: #00f0ff;">LinguaNova AI</b>. All rights reserved. | <a href="/About" target="_self" style="color: #00f0ff; text-decoration: none;">About</a> | <a href="/Contact" target="_self" style="color: #00f0ff; text-decoration: none;">Contact</a>
        </div>
        <div class="social-icons">
            <a href="https://twitter.com" target="_blank" title="Follow us on X">𝕏</a>
            <a href="https://github.com" target="_blank" title="GitHub">🐙</a>
            <a href="https://discord.com" target="_blank" title="Discord Community">💬</a>
            <a href="https://linkedin.com" target="_blank" title="LinkedIn">💼</a>
            <a href="https://instagram.com" target="_blank" title="Instagram">📸</a>
            <a href="https://youtube.com" target="_blank" title="YouTube">▶️</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
