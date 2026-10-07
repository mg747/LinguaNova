import sqlite3
import streamlit as st
import google.generativeai as genai
import time
from gtts import gTTS
import os
import base64
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import stripe

# Explicitly load .env from the same directory as app.py and override
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, '.env'), override=True)

# Firebase and Stripe Configuration Placeholders
# import firebase_admin
# from firebase_admin import credentials, auth
# stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")

# Database Setup
def init_db():
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  tab TEXT,
                  role TEXT, 
                  content TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_message(tab, role, content):
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO messages (tab, role, content) VALUES (?, ?, ?)", (tab, role, content))
    conn.commit()
    conn.close()

def load_messages(tab):
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE tab = ? ORDER BY timestamp ASC", (tab,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def clear_messages(tab):
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE tab = ?", (tab,))
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="LinguaNova", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")

# Futuristic 3D Dark Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

/* Main App Font */
html, body, [class*="css"], .stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp li {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem;
    color: #e0e6ed !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f0ff !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
}

.stApp {
    background-color: #05050a !important;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(13, 110, 253, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.08) 0%, transparent 50%);
    background-attachment: fixed;
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
}

.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px) scale(1.01) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* App Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(13, 110, 253, 0.1) 0%, rgba(0, 240, 255, 0.1) 100%);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: 20px;
    padding: 3rem 2rem;
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
    background: linear-gradient(45deg, transparent, rgba(0, 240, 255, 0.1), transparent);
    transform: rotate(45deg);
    animation: sweep 6s infinite linear;
}

@keyframes sweep {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

.hero-title {
    font-size: 4rem !important;
    font-weight: 900 !important;
    background: linear-gradient(to right, #00f0ff, #0055ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: 2px !important;
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
    margin-top: -0.5rem !important;
    color: #00ffaa !important;
    box-shadow: 0 0 15px rgba(0, 255, 170, 0.1) !important;
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

/* Inputs */
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
    border-radius: 8px !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    background: rgba(10, 10, 15, 0.8) !important;
    color: #00f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.95) !important;
    border-right: 1px solid rgba(0, 240, 255, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# Authentication State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="hero-container" style="max-width: 500px; margin: 100px auto;">
        <h2 style="font-size: 2.5rem; text-align: center;">Welcome Back</h2>
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
                # Placeholder for Firebase Auth: auth.sign_in_with_email_and_password(email, password)
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

# Sidebar Content
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-size: 1.5rem;'>LinguaNova</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00f0ff; letter-spacing: 2px;'>v4.0.0 // ONLINE</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### ⭐ Go Premium")
    st.markdown("<p style='font-size: 0.9rem; color: #a0aec0;'>Unlock unlimited coaching, priority matching, and premium voices.</p>", unsafe_allow_html=True)
    if st.button("Subscribe Now", use_container_width=True):
        st.info("Redirecting to secure Stripe checkout... (Simulation mode)")
        # In production: st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)
    
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
        except Exception as e:
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
            
    global_msgs = load_messages("global")
    
    if "partner_joined" not in st.session_state:
        st.session_state.partner_joined = False
        
    if not st.session_state.partner_joined:
        if st.button("📡 Find a Language Partner"):
            with st.spinner("Connecting..."):
                time.sleep(1)
                st.session_state.partner_joined = True
                save_message("global", "system", f"Connected with a genuine partner practicing {user_lang}. Their native language is {target_lang}.")
                st.rerun()
    else:
        for msg in global_msgs:
            render_msg(msg["role"], msg["content"])

        if prompt := st.chat_input("Message your partner...", key="global_input"):
            save_message("global", "user", prompt)
            render_msg("user", prompt)
            
            with st.spinner("AI Moderator analyzing..."):
                mod_prompt = f"The user is writing in {target_lang}. Message: '{prompt}'. If there are errors, provide a ONE-SENTENCE correction in English. If perfect, reply EXACTLY with 'Perfect'. Do not converse."
                try:
                    mod_response = model.generate_content(mod_prompt).text.strip()
                    if "Perfect" not in mod_response and "perfect" not in mod_response:
                        save_message("global", "moderator", mod_response)
                        render_msg("moderator", mod_response)
                except Exception:
                    pass
            
            with st.spinner("Partner is typing..."):
                partner_prompt = f"You are a native {target_lang} speaker doing a language exchange. User says: '{prompt}'. Reply naturally in {target_lang}. Keep it short (1-2 sentences). Add a brief cultural insight if relevant."
                try:
                    partner_response = model.generate_content(partner_prompt).text
                    save_message("global", "assistant", partner_response)
                    render_msg("assistant", partner_response)
                    
                    audio_html = generate_tts(partner_response, target_lang)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Connection issue with partner: {e}")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Disconnect & Clear Chat", key="clear_global"):
            st.session_state.partner_joined = False
            clear_messages("global")
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
    
    solo_msgs = load_messages("solo")
    for msg in solo_msgs:
        render_msg(msg["role"], msg["content"])

    prompt = st.chat_input("...or type here...", key="solo_input")
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
        save_message("solo", "user", user_input_text)
        render_msg("user", user_input_text)
        
        with st.spinner("Coach is thinking..."):
            system_instruction = f"You are an elite AI language coach for {practice_lang}. We are doing a roleplay: {scenario}. Reply in {practice_lang}. If they make a mistake, gently correct them in English in parentheses, provide the cultural context, and then continue the roleplay naturally."
            
            try:
                chat = model.start_chat(history=[{"role": "user", "parts": [{"text": system_instruction}]}])
                
                for m in solo_msgs:
                    if m["role"] in ["user", "assistant"]:
                        role = "user" if m["role"] == "user" else "model"
                        chat.history.append({"role": role, "parts": [{"text": m["content"]}]})
                    
                response = chat.send_message(user_input_text)
                save_message("solo", "assistant", response.text)
                render_msg("assistant", response.text)
                
                audio_html = generate_tts(response.text, practice_lang)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error connecting to AI Coach: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear Coach History", key="clear_solo"):
        clear_messages("solo")
        st.rerun()

# --- TAB 3: DICTIONARY ---
with tab3:
    st.markdown("### Smart Dictionary")
    
    with st.container(border=True):
        st.write("Query the global linguistic database for real-time translation and phonetics.")
        col_word, col_lang = st.columns(2)
        with col_word:
            word = st.text_input("Enter a word or phrase:")
        with col_lang:
            dict_lang = st.selectbox("Language of the word:", LANGUAGES, index=LANGUAGES.index("English"), key="dict_lang")
        
        style = st.selectbox("Dictionary Style:", ["Oxford Concise", "Cambridge", "Collins", "Urban Dictionary", "Lexico"])
        lookup_clicked = st.button("Look up", type="primary")
        
    if lookup_clicked:
        if not word:
            st.warning("Please enter a word.")
        else:
            with st.spinner(f"Searching {style}..."):
                prompt = f"""
                You are a dictionary engine simulating the style of '{style}'.
                Provide a detailed entry for the {dict_lang} word/phrase '{word}'.
                Include:
                1. Phonetic spelling.
                2. Part of speech.
                3. Meaning/Definition.
                4. Two example sentences (with English translations if the word is not English).
                Keep the formatting clean and engaging.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='dict-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    audio_html = generate_tts(word, dict_lang)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                        st.success("🔊 Audio pronunciation played!")
                except Exception as e:
                    st.error(f"Error fetching dictionary entry: {e}")

st.markdown('<div class="app-footer">© 2026 LinguaNova AI. All rights reserved. | <a href="/About" target="_self">About</a> | <a href="/Contact" target="_self">Contact</a></div>', unsafe_allow_html=True)
