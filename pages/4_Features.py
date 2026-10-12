import streamlit as st
import google.generativeai as genai
import os
import sys
import urllib.parse

# Ensure root path is accessible for db_helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db_helper

st.set_page_config(page_title="Features - LinguaNova", page_icon="✨", layout="wide")

# Check Auth
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in on the main page to view this page.")
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
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 1.8rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px) scale(1.008) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 14px 40px 0 rgba(0, 240, 255, 0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
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

/* Hide password visibility toggle completely */
[data-baseweb="input"] button, [data-testid="stTextInputPassword"] button, button[aria-label="Show password"], button[title="Show password"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
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
    text-transform: uppercase !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6) !important;
    background: linear-gradient(90deg, #00f0ff 0%, #0055ff 100%) !important;
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

# Shared Extensive Language List
ALL_LANGUAGES = sorted([
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

def render_share_bar(share_text, app_url="https://linguanova.streamlit.app"):
    encoded_text = urllib.parse.quote(share_text)
    encoded_url = urllib.parse.quote(app_url)
    
    t_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}"
    w_url = f"https://api.whatsapp.com/send?text={encoded_text}%20{encoded_url}"
    l_url = f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
    r_url = f"https://reddit.com/submit?url={encoded_url}&title={encoded_text}"
    
    st.markdown(f"""
    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-top: 12px; padding: 10px 14px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 10px;">
        <span style="font-family: 'Orbitron'; font-size: 0.85rem; color: #00f0ff;">📢 SHARE INSIGHT:</span>
        <a href="{t_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #000; color: #fff; font-size: 0.82rem; font-weight: bold; border: 1px solid #333;">𝕏 Twitter</a>
        <a href="{w_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #25D366; color: #fff; font-size: 0.82rem; font-weight: bold;">💬 WhatsApp</a>
        <a href="{l_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #0077b5; color: #fff; font-size: 0.82rem; font-weight: bold;">💼 LinkedIn</a>
        <a href="{r_url}" target="_blank" style="text-decoration: none; padding: 5px 12px; border-radius: 6px; background: #FF4500; color: #fff; font-size: 0.82rem; font-weight: bold;">🤖 Reddit</a>
    </div>
    """, unsafe_allow_html=True)

st.title("✨ AI Problem Solving & Tools")
st.markdown("<p style='color: #00f0ff; font-weight: 600;'>⚡ Earn +15 XP for every AI tool analysis completed!</p>", unsafe_allow_html=True)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.7-flash')
else:
    st.error("🔑 API Key not found! Please check your environment variables.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["✍️ Grammar Fixer", "🎭 Tone Analyzer", "🌉 Cultural Idioms"])

with tab1:
    st.markdown("### Grammar & Syntax Fixer")
    with st.container(border=True):
        st.write("Paste your text in any of 50+ languages to get AI-powered grammar, phonetic nuance, and syntax corrections.")
        
        c_lang, _ = st.columns([1, 1])
        with c_lang:
            g_lang = st.selectbox("Text Language:", ALL_LANGUAGES, index=ALL_LANGUAGES.index("Spanish"), key="g_lang_sel")
            
        text_to_fix = st.text_area("Your Text:", height=130, placeholder="Paste or type text to review...", key="grammar")
        if st.button("Fix Grammar", key="btn_fix_gram"):
            if text_to_fix.strip():
                with st.spinner("Analyzing text & syntax..."):
                    prompt = f"Fix any grammatical or stylistic errors in the following {g_lang} text and make it sound authentic and natural. Provide the corrected version, followed by a brief bullet-point explanation of changes in English:\n\n{text_to_fix}"
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
                    db_helper.add_xp(15)
                    st.toast("⚡ +15 XP earned!")
                    render_share_bar(f"Fixed my {g_lang} grammar on LinguaNova! Check out this AI learning platform:")
            else:
                st.warning("Please enter some text before analyzing.")

with tab2:
    st.markdown("### Tone & Sentiment Analyzer")
    with st.container(border=True):
        st.write("Understand the emotional resonance, politeness level, and formality behind any passage.")
        
        c_tlang, _ = st.columns([1, 1])
        with c_tlang:
            t_lang = st.selectbox("Text Language:", ALL_LANGUAGES, index=ALL_LANGUAGES.index("Japanese"), key="t_lang_sel")
            
        text_for_tone = st.text_area("Your Text:", height=130, placeholder="Enter text to analyze sentiment...", key="tone")
        if st.button("Analyze Tone", key="btn_ana_tone"):
            if text_for_tone.strip():
                with st.spinner("Analyzing tone & nuance..."):
                    prompt = f"Analyze the tone and sentiment of the following {t_lang} text. Specify the primary emotion, formality level (formal/casual/slang), social context, and how a native speaker would perceive it:\n\n{text_for_tone}"
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
                    db_helper.add_xp(15)
                    st.toast("⚡ +15 XP earned!")
                    render_share_bar(f"Analyzed {t_lang} conversational tone on LinguaNova! 🎭")
            else:
                st.warning("Please enter some text before analyzing.")

with tab3:
    st.markdown("### Cultural Idioms & Proverbs")
    with st.container(border=True):
        st.write("Unlock authentic colloquial idioms, folk proverbs, and metaphorical sayings across 50+ languages.")
        
        col_topic, col_ilang = st.columns(2)
        with col_topic:
            idiom_topic = st.text_input("Theme / Topic:", placeholder="e.g. Love, Hard Work, Rain, Courage, Friendship")
        with col_ilang:
            idiom_lang = st.selectbox("Target Language:", ALL_LANGUAGES, index=ALL_LANGUAGES.index("French"), key="idiom_lang_all")
            
        if st.button("Discover Idioms", key="btn_disc_idioms"):
            if idiom_topic.strip():
                with st.spinner("Retrieving cultural linguistic pearls..."):
                    prompt = f"Provide 3 common idioms, sayings, or proverbs in {idiom_lang} related to the theme '{idiom_topic}'. For each, provide:\n1. The original phrase in {idiom_lang}\n2. The literal word-for-word translation\n3. The true meaning and cultural usage in English."
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
                    db_helper.add_xp(15)
                    st.toast("⚡ +15 XP earned!")
                    render_share_bar(f"Discovered cool {idiom_lang} idioms about '{idiom_topic}' on LinguaNova! 🌉")
            else:
                st.warning("Please enter a theme or topic.")

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
