import streamlit as st

st.set_page_config(page_title="About - LinguaNova", page_icon="ℹ️", layout="wide")

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
    line-height: 1.6;
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
.glass-card {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-bottom: 1.8rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.glass-card:hover {
    transform: translateY(-4px) scale(1.008) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

.feature-pill {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(0, 240, 255, 0.1);
    border: 1px solid rgba(0, 240, 255, 0.3);
    color: #00f0ff;
    font-weight: 600;
    font-size: 0.9rem;
    margin: 4px;
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

st.title("ℹ️ About LinguaNova")

# Hero Section
st.markdown("""
<div class="glass-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <h2>LinguaNova // Genesis & Vision</h2>
            <p style="color: #00f0ff; font-family: 'Orbitron'; font-size: 1rem;">NEXT-GEN NEURAL LANGUAGE PLATFORM</p>
        </div>
        <div>
            <span class="feature-pill">🌐 50+ Languages</span>
            <span class="feature-pill">🤖 Gemini 3.7 Flash Powered</span>
            <span class="feature-pill">🎮 Language Arcade</span>
            <span class="feature-pill">🎙️ Real-Time Voice Synthesis</span>
        </div>
    </div>
    <hr style="border-color: rgba(0, 240, 255, 0.2); margin: 1.5rem 0;">
    <p style="font-size: 1.2rem; color: #f1f5f9;">
        Human connection shouldn't be limited by geographic borders or dialectical barriers. <b>LinguaNova</b> was engineered to break down language divides through real-time artificial intelligence, natural immersion, and interactive gamification.
    </p>
    <p style="color: #94a3b8; font-size: 1.05rem;">
        Traditional language learning forces users to memorize sterile vocabulary tables and conjugations in isolation. LinguaNova flips this model upside down: you practice authentic conversational exchanges with native-speaking counterparts, roleplay realistic scenarios with an elite 24/7 AI Voice Coach, and sharpen your quick-fire instincts through arcade-style games.
    </p>
</div>
""", unsafe_allow_html=True)

# Three Core Pillars
st.markdown("### 🧬 Architectural Pillars")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🌍</div>
        <h3 style="font-size: 1.25rem;">Global Exchange</h3>
        <p style="color: #94a3b8; font-size: 1rem;">
            Pair with worldwide partners practicing in reciprocal channels. Every message passes through an automated Neural Moderator that provides non-intrusive instant grammar corrections while preserving organic conversation flow.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🤖</div>
        <h3 style="font-size: 1.25rem;">Adaptive AI Coach</h3>
        <p style="color: #94a3b8; font-size: 1rem;">
            Practice high-stakes job interviews, casual street dialogue, or cafe ordering with voice-enabled roleplays. The AI dynamically adapts difficulty, provides cultural nuance tips, and pronounces native responses via neural audio synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🎮</div>
        <h3 style="font-size: 1.25rem;">Gamified Immersion</h3>
        <p style="color: #94a3b8; font-size: 1rem;">
            Language acquisition happens fastest when you have fun. Earn Experience Points (XP), maintain daily streaks, unlock futuristic tier ranks, and compete in rapid Vocab Blitz and Sentence Architect puzzles.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Deep Dive Details
st.markdown("""
<div class="glass-card" style="margin-top: 1.5rem;">
    <h3>🚀 What Makes LinguaNova Different?</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
        <div style="background: rgba(0,240,255,0.04); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(0,240,255,0.15);">
            <h4 style="color: #00f0ff; font-size: 1.05rem;">🧠 Zero Latency Feedback</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Powered by cutting-edge neural models to evaluate phonetics, syntax, and tone in milliseconds.</p>
        </div>
        <div style="background: rgba(177,0,255,0.04); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(177,0,255,0.15);">
            <h4 style="color: #b100ff; font-size: 1.05rem;">💾 Lesson Archiving & Export</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Save your favorite exchanges and export full study guides to take with you offline anywhere.</p>
        </div>
        <div style="background: rgba(0,255,170,0.04); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(0,255,170,0.15);">
            <h4 style="color: #00ffaa; font-size: 1.05rem;">🛡️ Safe & Private Space</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Automated safety moderation ensures all interactions remain respectful, constructive, and educational.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Social Share & Call to action
st.markdown("### 📢 Share LinguaNova")
st.markdown("""
<div class="glass-card" style="text-align: center;">
    <p style="font-size: 1.1rem; color: #e0e6ed; margin-bottom: 1rem;">
        Join thousands of learners mastering new tongues across the globe. Share your journey with friends!
    </p>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://twitter.com/intent/tweet?text=I'm%20learning%20languages%20with%20next-gen%20AI%20on%20LinguaNova!%20Check%20it%20out%20🚀&url=https://linguanova.streamlit.app" target="_blank" style="text-decoration: none; padding: 8px 16px; border-radius: 8px; background: #000; color: #fff; border: 1px solid #00f0ff; font-weight: bold;">𝕏 Share on Twitter</a>
        <a href="https://api.whatsapp.com/send?text=Check%20out%20LinguaNova%20-%20the%20AI%20language%20learning%20platform:%20https://linguanova.streamlit.app" target="_blank" style="text-decoration: none; padding: 8px 16px; border-radius: 8px; background: #25D366; color: #fff; font-weight: bold;">💬 Share on WhatsApp</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://linguanova.streamlit.app" target="_blank" style="text-decoration: none; padding: 8px 16px; border-radius: 8px; background: #0077b5; color: #fff; font-weight: bold;">💼 Share on LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

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
