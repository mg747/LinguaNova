import streamlit as st

st.set_page_config(page_title="Contact - LinguaNova", page_icon="📞", layout="wide")

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
.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px) scale(1.01) !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
    box-shadow: 0 15px 40px 0 rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 15, 25, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
    transition: all 0.4s ease !important;
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius: 8px !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    background: rgba(10, 10, 15, 0.8) !important;
    color: #00f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    padding: 0.5rem 1rem !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #00f0ff !important;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
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
</style>
""", unsafe_allow_html=True)

st.title("📞 Contact Us")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>Get in Touch</h3>
        <p style="color: #a0aec0;">Have questions, feedback, or need support? We'd love to hear from you!</p>
        <p><strong>Email:</strong> support@linguanova.ai</p>
        <p><strong>Twitter:</strong> @LinguaNovaAI (Twitter/X)</p>
        <p><strong>Office:</strong> 123 Innovation Drive, Tech City, TC 90210</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>Send a Message</h3>", unsafe_allow_html=True)
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=150)
        
        if st.button("Send Message"):
            if name and email and message:
                st.success("Your message has been sent successfully! We will get back to you shortly.")
            else:
                st.error("Please fill in all required fields (Name, Email, Message).")
