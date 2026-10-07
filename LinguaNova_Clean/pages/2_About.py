import streamlit as st

st.set_page_config(page_title="About - LinguaNova", page_icon="ℹ️", layout="wide")

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
.glass-card {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover {
    transform: translateY(-5px) scale(1.01) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ About LinguaNova")

st.markdown("""
<div class="glass-card">
    <h2>LinguaNova v4.0</h2>
    <p style="color: #a0aec0; font-size: 1.2rem;">Built to bridge the world through state-of-the-art super intelligence. Master nuances, perfect accents, and connect genuinely.</p>
    <p>Our mission is to break down language barriers and create a truly global community where anyone can learn any language, anytime, anywhere.</p>
</div>

<div class="glass-card">
    <h3>Why LinguaNova?</h3>
    <div style="display: flex; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 250px; background: rgba(0,240,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,240,255,0.1);">
            <h4 style="font-size: 1.1rem; color: #fff;">🌍 Global Connectivity</h4>
            <p style="color: #a0aec0; font-size: 1rem;">Connect with native speakers around the world instantly. Practice in real-time with our AI-moderated chat system that ensures a safe and productive learning environment.</p>
        </div>
        <div style="flex: 1; min-width: 250px; background: rgba(177,0,255,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(177,0,255,0.1);">
            <h4 style="font-size: 1.1rem; color: #fff;">🤖 AI Coaching</h4>
            <p style="color: #a0aec0; font-size: 1rem;">Our elite AI language coach is available 24/7. Practice real-world scenarios, get instant feedback on your pronunciation, and learn cultural nuances.</p>
        </div>
        <div style="flex: 1; min-width: 250px; background: rgba(0,255,170,0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,255,170,0.1);">
            <h4 style="font-size: 1.1rem; color: #fff;">📖 Smart Dictionary</h4>
            <p style="color: #a0aec0; font-size: 1rem;">More than just definitions. Get phonetic spellings, audio pronunciations, and contextual example sentences to truly understand how words are used.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
