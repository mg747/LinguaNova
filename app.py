import streamlit as st
import google.generativeai as genai
import time
from gtts import gTTS
import os
import base64
import urllib.parse
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import stripe
import db_helper

# Explicitly load .env from the same directory as app.py and override
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, '.env'), override=True)

# Initialize database
db_helper.init_db()

st.set_page_config(page_title="LinguaNova", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")

# Futuristic 3D Dark Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

/* Main App Font */
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

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f0ff !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    margin-bottom: 0.6rem !important;
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

/* Futuristic 3D Glass Cards */
.glass-card, .msg-card, .dict-card, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    margin-bottom: 1.5rem !important;
    word-break: break-word !important;
}

.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px) scale(1.008) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 14px 40px 0 rgba(0, 240, 255, 0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* App Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(0, 240, 255, 0.1) 100%);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(0, 240, 255, 0.1), inset 0 0 20px rgba(0, 240, 255, 0.05);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: linear-gradient(45deg, transparent, rgba(0, 240, 255, 0.08), transparent);
    transform: rotate(45deg);
    animation: sweep 6s infinite linear;
    z-index: 0;
    pointer-events: none;
}

@keyframes sweep {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

.hero-title {
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(to right, #00f0ff, #0055ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: 2px !important;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    position: relative;
    z-index: 1;
    font-size: 1.15rem !important;
}

/* Custom Message Cards */
.msg-user {
    border-left: 4px solid #00f0ff !important;
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.05) 0%, transparent 100%) !important;
}

.msg-assistant {
    border-left: 4px solid #b100ff !important;
    background: linear-gradient(90deg, rgba(177, 0, 255, 0.05) 0%, transparent 100%) !important;
}

.mod-card {
    background: rgba(0, 255, 170, 0.05) !important;
    border: 1px solid rgba(0, 255, 170, 0.2) !important;
    border-left: 4px solid #00ffaa !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    margin-bottom: 1rem !important;
    color: #00ffaa !important;
    box-shadow: 0 0 15px rgba(0, 255, 170, 0.1) !important;
}

/* Match AI Coach and Dictionary text */
.msg-card, .dict-card {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.15rem !important;
    line-height: 1.5 !important;
}

/* Tabs */
button[data-baseweb="tab"] p {
    color: #64748b !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    font-family: 'Orbitron', sans-serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #00f0ff !important;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.5) !important;
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
[data-baseweb="input"], [data-baseweb="base-input"], .stTextArea>div>div>textarea, [data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    border-radius: 8px !important;
    border: 2px solid rgba(0, 240, 255, 0.5) !important;
}
[data-baseweb="input"] input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, [data-testid="stChatInput"] textarea {
    color: #000000 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    padding: 0.6rem 1rem !important;
    -webkit-text-fill-color: #000000 !important;
}
[data-baseweb="input"]:focus-within, .stTextArea>div>div>textarea:focus, [data-testid="stChatInput"] textarea:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
}
.stSelectbox svg {
    fill: #000000 !important;
    width: 24px !important;
    height: 24px !important;
}

/* Hide password visibility toggle completely */
[data-baseweb="input"] button, [data-testid="stTextInputPassword"] button, button[aria-label="Show password"], button[title="Show password"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.95) !important;
    border-right: 1px solid rgba(0, 240, 255, 0.1) !important;
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

def render_share_bar(share_text, app_url="https://linguanova.streamlit.app"):
    encoded_text = urllib.parse.quote(share_text)
    encoded_url = urllib.parse.quote(app_url)
    
    t_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}"
    w_url = f"https://api.whatsapp.com/send?text={encoded_text}%20{encoded_url}"
    l_url = f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
    
    st.markdown(f"""
    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-top: 12px; padding: 10px 14px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px;">
        <span style="font-family: 'Orbitron'; font-size: 0.85rem; color: #00f0ff;">📢 SHARE LESSON:</span>
        <a href="{t_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #000; color: #fff; font-size: 0.82rem; font-weight: bold; border: 1px solid #333;">𝕏 Twitter</a>
        <a href="{w_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #25D366; color: #fff; font-size: 0.82rem; font-weight: bold;">💬 WhatsApp</a>
        <a href="{l_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #0077b5; color: #fff; font-size: 0.82rem; font-weight: bold;">💼 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# Authentication State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="hero-container" style="max-width: 500px; margin: 80px auto;">
        <h2 style="font-size: 2.2rem; text-align: center;">Welcome Back</h2>
        <p style="text-align: center; color: #64748b;">Log in to your LinguaNova account</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### Log In")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Log In", use_container_width=True):
                if email and password:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
            st.markdown("<p style='text-align: center; font-size: 0.9rem; margin-top: 1rem; color: #64748b;'>(Use any credentials to test the app)</p>", unsafe_allow_html=True)
    st.stop()

# API Key Validation
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.7-flash')
else:
    st.error("🔑 API Key not found! Please create a `.env` file in this folder and add `GEMINI_API_KEY=your_key_here`.")
    st.stop()

LANGUAGES = sorted([
    "English", "Spanish", "French", "German", "Japanese", "Chinese (Mandarin)", 
    "Italian", "Portuguese", "Arabic", "Hindi", "Bengali", "Russian", "Korean",
    "Swahili", "Turkish", "Vietnamese", "Dutch", "Polish", "Indonesian", "Thai",
    "Edo", "Irish (Gaeilge)", "Igbo", "Yoruba", "Hausa", "Fulani", "Zulu", "Amharic",
    "Swedish", "Norwegian", "Danish", "Finnish", "Greek", "Hebrew", "Persian",
    "Urdu", "Punjabi", "Tamil", "Telugu", "Marathi", "Gujarati", "Malayalam",
    "Burmese", "Khmer", "Lao", "Malay", "Tagalog", "Cebuano", "Javanese", "Sundanese",
    "Hungarian", "Czech", "Slovak", "Romanian", "Bulgarian", "Serbian", "Croatian",
    "Ukrainian", "Afrikaans"
])

TTS_LANG_MAP = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
    "Japanese": "ja", "Chinese (Mandarin)": "zh-CN", "Italian": "it", 
    "Portuguese": "pt", "Arabic": "ar", "Hindi": "hi", "Bengali": "bn",
    "Russian": "ru", "Korean": "ko", "Turkish": "tr", "Vietnamese": "vi",
    "Dutch": "nl", "Polish": "pl", "Indonesian": "id", "Thai": "th",
    "Swahili": "sw", "Swedish": "sv", "Norwegian": "no", "Danish": "da",
    "Finnish": "fi", "Greek": "el", "Hebrew": "he", "Romanian": "ro",
    "Hungarian": "hu", "Czech": "cs", "Slovak": "sk", "Ukrainian": "uk",
    "Serbian": "sr", "Croatian": "hr", "Bulgarian": "bg", "Tagalog": "tl"
}

# Sidebar Content with Live Profile
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-size: 1.5rem;'>LinguaNova</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00f0ff; letter-spacing: 2px;'>v4.2.0 // ONLINE</p>", unsafe_allow_html=True)
    st.divider()
    
    # User Profile Snippet
    user_stats = db_helper.get_stats()
    profile = user_stats["profile"]
    st.markdown(f"""
    <div style="text-align: center; padding: 12px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 12px; margin-bottom: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed={profile['avatar_seed']}&colors=00f0ff" width="60" style="border-radius: 50%; border: 2px solid #00f0ff; box-shadow: 0 0 10px #00f0ff;">
        <div style="font-family: 'Orbitron'; font-size: 1rem; color: #fff; margin-top: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{profile['username']}</div>
        <div style="font-size: 0.85rem; color: #00f0ff; font-weight: 700;">⚡ {user_stats['level_name']} (Lvl {user_stats['level_num']})</div>
        <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 4px;">XP: <b style="color: #00ffaa;">{profile['xp']}</b> | Streak: <b style="color: #ffaa00;">{profile['streak']} 🔥</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⭐ Go Premium")
    st.markdown("<p style='font-size: 0.9rem; color: #a0aec0;'>Unlock unlimited coaching, priority matching, and premium voices.</p>", unsafe_allow_html=True)
    if st.button("Subscribe Now", use_container_width=True):
        st.info("Redirecting to secure Stripe checkout... (Simulation mode)")
    
    st.divider()
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

def generate_tts(text, lang):
    code = TTS_LANG_MAP.get(lang)
    if code:
        try:
            tts = gTTS(text=text, lang=code)
            tts.save("response.mp3")
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>'
        except Exception:
            return ""
    return ""

def render_msg(role, content):
    if role == "system":
        st.markdown(f"<div class='msg-card msg-system'>🛸 <b>SYS_MSG:</b> {content}</div>", unsafe_allow_html=True)
    elif role == "user":
        st.markdown(f"<div class='msg-card msg-user'>👤 <b>USER_NODE:</b><br>{content}</div>", unsafe_allow_html=True)
    elif role == "moderator":
        st.markdown(f"<div class='mod-card'>🛡️ <b>NEURAL_MODERATOR:</b> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='msg-card msg-assistant'>🤖 <b>SYNTH_PARTNER:</b><br>{content}</div>", unsafe_allow_html=True)

# App Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">LinguaNova</h1>
    <p class="hero-subtitle" style="color: #a0aec0; font-family: 'Rajdhani', sans-serif;">The intelligent platform to master any language, anywhere.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌍 Global Chat", "🤖 AI Coach", "📖 Smart Dictionary"])

# --- TAB 1: GLOBAL CHAT ---
with tab1:
    st.markdown("### Global Practice")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            user_lang = st.selectbox("I speak:", LANGUAGES, index=LANGUAGES.index("English"))
        with col2:
            target_lang = st.selectbox("I want to practice:", LANGUAGES, index=LANGUAGES.index("Spanish"))
            
    global_msgs = db_helper.load_messages("global")
    
    if "partner_joined" not in st.session_state:
        st.session_state.partner_joined = False
        
    if not st.session_state.partner_joined:
        if st.button("📡 Find a Language Partner"):
            with st.spinner("Connecting..."):
                time.sleep(1)
                st.session_state.partner_joined = True
                db_helper.save_message("global", "system", f"Connected with a genuine partner practicing {user_lang}. Their native language is {target_lang}.")
                st.rerun()
    else:
        for msg in global_msgs:
            render_msg(msg["role"], msg["content"])

        if prompt := st.chat_input(" ", key="global_input"):
            db_helper.save_message("global", "user", prompt)
            render_msg("user", prompt)
            db_helper.add_xp(10)
            
            with st.spinner("AI Moderator analyzing..."):
                mod_prompt = f"The user is writing in {target_lang}. Message: '{prompt}'. If there are errors, provide a ONE-SENTENCE correction in English. If perfect, reply EXACTLY with 'Perfect'. Do not converse."
                try:
                    mod_response = model.generate_content(mod_prompt).text.strip()
                    if "Perfect" not in mod_response and "perfect" not in mod_response:
                        db_helper.save_message("global", "moderator", mod_response)
                        render_msg("moderator", mod_response)
                except Exception:
                    pass
            
            with st.spinner("Partner is typing..."):
                partner_prompt = f"You are a native {target_lang} speaker doing a language exchange. User says: '{prompt}'. Reply naturally in {target_lang}. Keep it short (1-2 sentences). Add a brief cultural insight if relevant."
                try:
                    partner_response = model.generate_content(partner_prompt).text
                    db_helper.save_message("global", "assistant", partner_response)
                    render_msg("assistant", partner_response)
                    
                    audio_html = generate_tts(partner_response, target_lang)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Connection issue with partner: {e}")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Save Session & Archive Tools
        col_g1, col_g2, col_g3 = st.columns([1.5, 1, 1])
        with col_g1:
            g_title = st.text_input("Session Name:", placeholder="e.g. Spanish Basics Exchange", key="g_title_in")
        with col_g2:
            if st.button("💾 Save Session", key="btn_save_global"):
                ok, msg = db_helper.save_chat_session(g_title, "global")
                if ok:
                    st.success(msg)
                    st.balloons()
                    render_share_bar(f"Completed an authentic language exchange session in {target_lang} on LinguaNova! 🌍")
                else:
                    st.warning(msg)
        with col_g3:
            transcript_txt = "\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in global_msgs])
            st.download_button(
                "📥 Export (.txt)",
                data=transcript_txt,
                file_name=f"LinguaNova_Global_{int(time.time())}.txt",
                mime="text/plain",
                key="btn_dl_global"
            )
            
        if st.button("Disconnect & Clear Chat", key="clear_global"):
            st.session_state.partner_joined = False
            db_helper.clear_messages("global")
            st.rerun()

# --- TAB 2: AI Coach ---
with tab2:
    st.markdown("### 1-on-1 Voice Coach")
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            practice_lang = st.selectbox("Language to Master:", LANGUAGES, index=LANGUAGES.index("French"), key="solo_lang")
        with col2:
            scenario = st.selectbox("Roleplay Scenario:", ["Casual Conversation", "Job Interview", "Ordering at a Cafe", "Asking for Directions", "Meeting the In-laws"])
            
        st.markdown("<p style='font-weight: 600; color: #00f0ff; letter-spacing: 1px;'>🎙️ Initialize Voice Link:</p>", unsafe_allow_html=True)
        audio_bytes = audio_recorder(key="solo_audio", text="", recording_color="#ff0055", neutral_color="#00f0ff", icon_name="microphone", icon_size="2x")
    
    solo_msgs = db_helper.load_messages("solo")
    for msg in solo_msgs:
        render_msg(msg["role"], msg["content"])

    prompt = st.chat_input(" ", key="solo_input")
    user_input_text = prompt
    
    if audio_bytes and not prompt:
        with st.spinner("Transcribing audio..."):
            try:
                audio_part = {"mime_type": "audio/wav", "data": audio_bytes}
                transcription_response = model.generate_content([audio_part, f"Transcribe this audio in {practice_lang}. Only output the transcription."])
                user_input_text = transcription_response.text
            except Exception as e:
                st.error(f"Failed to transcribe audio: {e}")

    if user_input_text:
        db_helper.save_message("solo", "user", user_input_text)
        render_msg("user", user_input_text)
        db_helper.add_xp(10)
        
        with st.spinner("Coach is thinking..."):
            system_instruction = f"You are an elite AI language coach for {practice_lang}. We are doing a roleplay: {scenario}. Reply in {practice_lang}. If they make a mistake, gently correct them in English in parentheses, provide the cultural context, and then continue the roleplay naturally."
            
            try:
                chat = model.start_chat(history=[{"role": "user", "parts": [{"text": system_instruction}]}])
                
                for m in solo_msgs:
                    if m["role"] in ["user", "assistant"]:
                        role = "user" if m["role"] == "user" else "model"
                        chat.history.append({"role": role, "parts": [{"text": m["content"]}]})
                    
                response = chat.send_message(user_input_text)
                db_helper.save_message("solo", "assistant", response.text)
                render_msg("assistant", response.text)
                
                audio_html = generate_tts(response.text, practice_lang)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error connecting to AI Coach: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Save Session & Archive Tools
    col_c1, col_c2, col_c3 = st.columns([1.5, 1, 1])
    with col_c1:
        c_title = st.text_input("Coach Session Name:", placeholder=f"e.g. {practice_lang} {scenario}", key="c_title_in")
    with col_c2:
        if st.button("💾 Save Session", key="btn_save_coach"):
            ok, msg = db_helper.save_chat_session(c_title, "solo")
            if ok:
                st.success(msg)
                st.balloons()
                render_share_bar(f"Practiced {practice_lang} '{scenario}' with my AI Voice Coach on LinguaNova! 🤖🎙️")
            else:
                st.warning(msg)
    with col_c3:
        transcript_coach = "\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in solo_msgs])
        st.download_button(
            "📥 Export (.txt)",
            data=transcript_coach,
            file_name=f"LinguaNova_Coach_{int(time.time())}.txt",
            mime="text/plain",
            key="btn_dl_coach"
        )
        
    if st.button("Clear Coach History", key="clear_solo"):
        db_helper.clear_messages("solo")
        st.rerun()

# --- TAB 3: DICTIONARY ---
with tab3:
    st.markdown("### Smart Dictionary & Phonetics")
    
    with st.container(border=True):
        st.write("Query the global linguistic database for real-time definitions, phonetic breakdown, and native audio.")
        
        # Proper Search Bar Placement
        col_word, col_lang, col_btn = st.columns([2.5, 1.5, 1])
        with col_word:
            word = st.text_input("Search Term:", placeholder="Enter a word or phrase to look up...", key="dict_word_input")
        with col_lang:
            dict_lang = st.selectbox("Language:", LANGUAGES, index=LANGUAGES.index("English"), key="dict_lang")
        with col_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            lookup_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
        
        style = st.selectbox("Dictionary Style:", ["Oxford Concise", "Cambridge", "Collins", "Urban Dictionary", "Lexico"])
        
    if lookup_clicked:
        if not word.strip():
            st.warning("Please enter a word or phrase to search.")
        else:
            with st.spinner(f"Querying {style} database..."):
                prompt = f"""
                You are a dictionary engine simulating the style of '{style}'.
                Provide a detailed entry for the {dict_lang} word/phrase '{word}'.
                Include:
                1. Phonetic spelling.
                2. Part of speech.
                3. Meaning/Definition.
                4. Two example sentences (with English translations if the word is not English).
                Keep the formatting clean, elegant, and engaging.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='dict-card'>{response.text}</div>", unsafe_allow_html=True)
                    db_helper.add_xp(5)
                    
                    audio_html = generate_tts(word, dict_lang)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                        st.success("🔊 Audio pronunciation played! (+5 XP)")
                        
                    render_share_bar(f"Learned the meaning of '{word}' ({dict_lang}) on LinguaNova's Smart Dictionary! 📖")
                except Exception as e:
                    st.error(f"Error fetching dictionary entry: {e}")

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
