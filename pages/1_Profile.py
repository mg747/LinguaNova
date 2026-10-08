import streamlit as st

st.set_page_config(page_title="Profile - LinguaNova", page_icon="👤", layout="wide")

# Check Auth
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in on the main page to view your profile.")
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
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover {
    transform: translateY(-5px) scale(1.01) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
/* Inputs */
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
    border-radius: 8px !important;
    border: 2px solid rgba(0, 240, 255, 0.5) !important;
    background: #ffffff !important;
    color: #000000 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    padding: 0.75rem 1.25rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
}
.stSelectbox svg {
    fill: #000000 !important;
    width: 24px !important;
    height: 24px !important;
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
/* Hide placeholders globally */
::placeholder { color: transparent !important; }
</style>
""", unsafe_allow_html=True)

st.title("👤 User Profile")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=VIPLearner&colors=00f0ff" width="150" style="border-radius: 50%; margin-bottom: 1rem; border: 2px solid #00f0ff; box-shadow: 0 0 15px #00f0ff;">
        <h3>VIP LEARNER</h3>
        <p style="color: #a0aec0; font-family: 'Orbitron'; font-size: 0.9rem;">TIER 1 (PREMIUM)</p>
        <span style="background-color: rgba(0, 255, 170, 0.2); color: #00ffaa; border: 1px solid #00ffaa; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-family: 'Orbitron';">ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3>Learning Progress</h3>
        <p><strong>Spanish:</strong> Level B1</p>
        <div style="background-color: rgba(255,255,255,0.1); border-radius: 8px; width: 100%; height: 12px; margin-bottom: 1rem; border: 1px solid rgba(0,240,255,0.3);">
            <div style="background: linear-gradient(90deg, #0055ff, #00f0ff); width: 65%; height: 100%; border-radius: 8px; box-shadow: 0 0 10px #00f0ff;"></div>
        </div>
        <p><strong>French:</strong> Level A1</p>
        <div style="background-color: rgba(255,255,255,0.1); border-radius: 8px; width: 100%; height: 12px; margin-bottom: 1rem; border: 1px solid rgba(0,240,255,0.3);">
            <div style="background: linear-gradient(90deg, #0055ff, #00f0ff); width: 20%; height: 100%; border-radius: 8px; box-shadow: 0 0 10px #00f0ff;"></div>
        </div>
        <p><strong>Japanese:</strong> Beginner</p>
        <div style="background-color: rgba(255,255,255,0.1); border-radius: 8px; width: 100%; height: 12px; margin-bottom: 1rem; border: 1px solid rgba(0,240,255,0.3);">
            <div style="background: linear-gradient(90deg, #ff0055, #ff0055); width: 10%; height: 100%; border-radius: 8px; box-shadow: 0 0 10px #ff0055;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <h3>Recent Activity</h3>
    <ul style="color: #a0aec0; font-size: 1rem; line-height: 1.8;">
        <li><span style="color: #00f0ff;">[✓]</span> Completed <em>Ordering at a Cafe</em> simulation in FRENCH. (T-minus 2 hours)</li>
        <li><span style="color: #00f0ff;">[✓]</span> Synced with GLOBAL PARTNER on SPANISH channel. (T-minus 24 hours)</li>
        <li><span style="color: #00f0ff;">[✓]</span> 5 new data packets queried from ARCHIVE. (T-minus 24 hours)</li>
    </ul>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="app-footer">© 2026 LinguaNova AI. All rights reserved. | <a href="/About" target="_self">About</a> | <a href="/Contact" target="_self">Contact</a></div>', unsafe_allow_html=True)


