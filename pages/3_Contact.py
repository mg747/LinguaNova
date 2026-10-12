import streamlit as st
import time

st.set_page_config(page_title="Contact - LinguaNova", page_icon="📞", layout="wide")

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

/* Contact Channel Card */
.contact-channel-card {
    background: linear-gradient(135deg, rgba(13, 110, 253, 0.1), rgba(0, 240, 255, 0.05));
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}
.contact-channel-card:hover {
    border-color: #00f0ff;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
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

st.title("📞 Contact & Support Hub")

# Department Selector Cards
st.markdown("### 📡 Select Support Channel")
channel_cols = st.columns(4)

channels = [
    {"name": "Technical Support", "icon": "🛠️", "desc": "Bugs, login & platform issues", "email": "tech@linguanova.ai", "sla": "< 2 hours"},
    {"name": "Partnerships", "icon": "🤝", "desc": "Enterprise & educator licensing", "email": "partners@linguanova.ai", "sla": "< 24 hours"},
    {"name": "Media & Press", "icon": "🎙️", "desc": "Interviews, kits & PR", "email": "press@linguanova.ai", "sla": "< 12 hours"},
    {"name": "Community Discord", "icon": "💬", "desc": "Join 15,000+ global polyglots", "email": "discord.gg/linguanova", "sla": "Instant"}
]

if "selected_channel" not in st.session_state:
    st.session_state.selected_channel = channels[0]

for idx, col in enumerate(channel_cols):
    ch = channels[idx]
    is_active = (st.session_state.selected_channel["name"] == ch["name"])
    border_style = "2px solid #00f0ff" if is_active else "1px solid rgba(0,240,255,0.2)"
    bg_style = "rgba(0, 240, 255, 0.12)" if is_active else "rgba(15, 15, 25, 0.6)"
    
    with col:
        st.markdown(f"""
        <div style="background: {bg_style}; border: {border_style}; border-radius: 12px; padding: 1.2rem; text-align: center; height: 160px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem;">{ch['icon']}</div>
            <div style="font-family: 'Orbitron'; font-weight: 700; color: #fff; margin-top: 6px; font-size: 0.95rem;">{ch['name']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">{ch['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select {ch['name']}", key=f"btn_ch_{idx}", use_container_width=True):
            st.session_state.selected_channel = ch
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Active Contact Card and Form Grid
active_ch = st.session_state.selected_channel

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown(f"""
    <div class="glass-card" style="border: 2px solid #00f0ff; box-shadow: 0 0 25px rgba(0, 240, 255, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 2.2rem;">{active_ch['icon']}</span>
            <span style="background: rgba(0, 255, 170, 0.2); color: #00ffaa; border: 1px solid #00ffaa; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-family: 'Orbitron';">🟢 ONLINE</span>
        </div>
        <h3 style="margin-top: 1rem; color: #00f0ff;">{active_ch['name']} Card</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem;">{active_ch['desc']}</p>
        <hr style="border-color: rgba(0, 240, 255, 0.2); margin: 1rem 0;">
        <div style="font-size: 1rem; line-height: 2;">
            <div><b>📧 Contact Link:</b> <span style="color: #00f0ff;">{active_ch['email']}</span></div>
            <div><b>⚡ Guaranteed SLA:</b> <span style="color: #00ffaa;">{active_ch['sla']}</span></div>
            <div><b>📍 Operations:</b> <span>123 Innovation Drive, Tech City, TC 90210</span></div>
            <div><b>🌐 Platform Status:</b> <span style="color: #00f0ff;">All Global Voice Relays Operational</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h4>💬 Community Voice Room</h4>
        <p style="color: #94a3b8; font-size: 0.95rem;">Looking for quick conversation practice with real people? Join our public voice lounges open 24/7 on Discord.</p>
        <a href="https://discord.com" target="_blank" style="text-decoration: none;">
            <button style="background: #5865F2; color: #fff; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                Launch Discord Lounge 🚀
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    with st.container(border=True):
        st.markdown(f"### ✉️ Dispatch Message to {active_ch['name']}")
        
        c_name, c_email = st.columns(2)
        with c_name:
            sender_name = st.text_input("Your Name:", placeholder="e.g. Alex Mercer")
        with c_email:
            sender_email = st.text_input("Your Email:", placeholder="e.g. alex@example.com")
            
        subject = st.text_input("Subject:", value=f"Inquiry: {active_ch['name']}")
        message_body = st.text_area("Message Details:", height=150, placeholder="Type your inquiry or feedback here...")
        
        if st.button("🚀 Send Priority Message", use_container_width=True):
            if sender_name and sender_email and message_body:
                ticket_id = f"LN-{int(time.time()) % 100000:05d}"
                st.markdown(f"""
                <div class="glass-card" style="border: 2px solid #00ffaa; background: rgba(0, 255, 170, 0.08); margin-top: 1rem;">
                    <h3 style="color: #00ffaa; margin-bottom: 0.4rem;">✅ Message Dispatched Successfully!</h3>
                    <p style="color: #e2e8f0; font-size: 1.05rem;">
                        Thank you, <b>{sender_name}</b>. Your transmission has been queued for <b>{active_ch['name']}</b>.
                    </p>
                    <div style="background: rgba(0,0,0,0.5); padding: 12px; border-radius: 8px; font-family: 'Orbitron'; font-size: 0.9rem; color: #00f0ff;">
                        TICKET REF: #{ticket_id} | ESTIMATED RESPONSE: {active_ch['sla']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Please fill in all required fields (Name, Email, Message) before submitting.")

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
