import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Features - LinguaNova", page_icon="✨", layout="wide")

# Check Auth
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in on the main page to view this page.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp li {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem;
    color: #e0e6ed !important;
}
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
.glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px) scale(1.01) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
/* Footer fixed to bottom */
.app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(5, 5, 10, 0.95);
    padding: 15px;
    text-align: center;
    border-top: 1px solid rgba(0, 240, 255, 0.2);
    z-index: 999;
}
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

/* Inputs */
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
    padding: 0.75rem 1.25rem !important;
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
</style>
""", unsafe_allow_html=True)

st.title("✨ AI Problem Solving & Tools")

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
        st.write("Paste your text here to get AI-powered grammar and syntax corrections.")
        text_to_fix = st.text_area("Your Text", height=150, key="grammar")
        if st.button("Fix Grammar"):
            if text_to_fix:
                with st.spinner("Analyzing text..."):
                    prompt = f"Fix any grammatical errors in the following text and make it sound natural. Provide the corrected version, followed by a brief explanation of the changes made:\n\n{text_to_fix}"
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter some text.")

with tab2:
    st.markdown("### Tone & Sentiment Analyzer")
    with st.container(border=True):
        st.write("Understand the emotion and tone behind any piece of text.")
        text_for_tone = st.text_area("Your Text", height=150, key="tone")
        if st.button("Analyze Tone"):
            if text_for_tone:
                with st.spinner("Analyzing tone..."):
                    prompt = f"Analyze the tone and sentiment of the following text. Tell me the primary emotion, the level of formality, and how it might be perceived by a reader:\n\n{text_for_tone}"
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter some text.")

with tab3:
    st.markdown("### Cultural Idioms & Proverbs")
    with st.container(border=True):
        st.write("Learn the cultural idioms related to a specific topic or word.")
        idiom_topic = st.text_input("Enter a topic (e.g., 'Rain', 'Friendship', 'Time')")
        idiom_lang = st.selectbox("Language", ["Spanish", "French", "Japanese", "Chinese", "German", "Italian", "Arabic"])
        if st.button("Discover Idioms"):
            if idiom_topic:
                with st.spinner("Fetching idioms..."):
                    prompt = f"Provide 3 common idioms or proverbs in {idiom_lang} related to '{idiom_topic}'. For each, include the original phrase, the literal translation, and the actual meaning in English."
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='glass-card'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a topic.")


st.markdown('<div class="app-footer">© 2026 LinguaNova AI. All rights reserved. | <a href="/About" target="_self">About</a> | <a href="/Contact" target="_self">Contact</a></div>', unsafe_allow_html=True)



