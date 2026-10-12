import streamlit as st
import google.generativeai as genai
import os
import sys
import json
import base64
from gtts import gTTS

# Ensure root path is accessible for db_helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db_helper

st.set_page_config(page_title="Arcade - LinguaNova", page_icon="🎮", layout="wide")

# Check Auth
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in on the main page to access the Language Arcade.")
    st.stop()

# Styling with sleek animations & glow
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

/* Arcade Stat Badge */
.arcade-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(177, 0, 255, 0.15));
    border: 1px solid #00f0ff;
    color: #00f0ff;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    margin-right: 10px;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
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

/* Footer fixed to bottom */
.app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(5, 5, 10, 0.95);
    padding: 12px;
    text-align: center;
    border-top: 1px solid rgba(0, 240, 255, 0.2);
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)

# API Setup
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.7-flash')
else:
    st.error("🔑 Gemini API Key not found. Please verify your environment.")
    st.stop()

# Helper for audio
TTS_LANG_MAP = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
    "Japanese": "ja", "Chinese (Mandarin)": "zh-CN", "Italian": "it", 
    "Portuguese": "pt", "Arabic": "ar", "Hindi": "hi", "Russian": "ru"
}

def play_audio(text, lang):
    code = TTS_LANG_MAP.get(lang, "en")
    try:
        tts = gTTS(text=text, lang=code)
        tts.save("game_sound.mp3")
        with open("game_sound.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>'
    except Exception:
        return ""

user_stats = db_helper.get_stats()
profile = user_stats["profile"]

st.title("🎮 Language Arcade")
st.markdown(f"""
<div>
    <span class="arcade-badge">⚡ XP: {profile['xp']}</span>
    <span class="arcade-badge">🔥 STREAK: {profile['streak']} DAYS</span>
    <span class="arcade-badge">🏆 RANK: {user_stats['level_name'].upper()}</span>
</div>
<br>
""", unsafe_allow_html=True)

game_tab1, game_tab2, game_tab3 = st.tabs(["⚡ Vocab Blitz", "🧩 Sentence Puzzle", "🕵️ Mystery Clues"])

# ==================== GAME 1: VOCAB BLITZ ====================
with game_tab1:
    st.markdown("### ⚡ Vocab Blitz Challenge")
    st.markdown("Test your rapid comprehension. Complete the quiz to earn XP and level up!")

    col1, col2 = st.columns([1, 1])
    with col1:
        game_lang = st.selectbox("Target Language:", ["Spanish", "French", "German", "Japanese", "Italian", "Portuguese", "Russian"], key="vb_lang")
    with col2:
        game_cat = st.selectbox("Challenge Topic:", ["Everyday Essentials", "Travel & Transit", "Cyberpunk & Tech", "Food & Restaurants", "Slang & Idioms"], key="vb_cat")

    if st.button("🚀 Start New Blitz Quiz", key="btn_start_blitz"):
        with st.spinner("AI Generating dynamic quiz challenges..."):
            prompt = f"""
            You are a language learning game engine. Generate 4 multiple choice questions for learning {game_lang} vocabulary about topic '{game_cat}'.
            Format your response strictly as valid JSON with no markdown formatting around it, matching this schema:
            [
              {{
                "question": "What is the meaning of [Target word] in English?",
                "target_word": "[Word in {game_lang}]",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": "Option A",
                "explanation": "Brief explanation of meaning and context."
              }}
            ]
            """
            try:
                res = model.generate_content(prompt).text.strip()
                # Clean JSON fences if present
                if res.startswith("```"):
                    res = res.split("```")[1]
                    if res.startswith("json"):
                        res = res[4:]
                questions = json.loads(res.strip())
                st.session_state.vb_questions = questions
                st.session_state.vb_submitted = False
                st.session_state.vb_answers = {}
                st.session_state.vb_lang_used = game_lang
                st.rerun()
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

    if "vb_questions" in st.session_state and st.session_state.vb_questions:
        questions = st.session_state.vb_questions
        with st.container(border=True):
            user_answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                choice = st.radio(
                    f"Select answer for Q{i+1}:", 
                    q["options"], 
                    key=f"q_{i}", 
                    label_visibility="collapsed"
                )
                user_answers[i] = choice
                st.markdown("---")

            if st.button("✅ Submit Answers", key="btn_submit_blitz"):
                score = 0
                st.session_state.vb_submitted = True
                
                for i, q in enumerate(questions):
                    selected = user_answers[i]
                    if selected == q["correct"]:
                        score += 1
                        st.success(f"**Q{i+1}: Correct!** {q['target_word']} = {q['correct']}. *{q['explanation']}*")
                    else:
                        st.error(f"**Q{i+1}: Incorrect.** You chose: {selected}. Correct: **{q['correct']}**. *{q['explanation']}*")
                
                earned_xp = db_helper.record_game_score("Vocab Blitz", score, len(questions), st.session_state.vb_lang_used)
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; margin-top: 1rem;">
                    <h3>🎉 Quiz Complete!</h3>
                    <p style="font-size: 1.3rem; color: #00f0ff;">Score: <b>{score} / {len(questions)}</b> | Earned: <b>+{earned_xp} XP</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                if score >= 3:
                    st.balloons()

# ==================== GAME 2: SENTENCE PUZZLE ====================
with game_tab2:
    st.markdown("### 🧩 Sentence Architect")
    st.markdown("Unscramble the target language sentence to match the English meaning.")

    sc_col1, sc_col2 = st.columns([1, 1])
    with sc_col1:
        sc_lang = st.selectbox("Language:", ["Spanish", "French", "German", "Japanese", "Italian"], key="sc_lang")
    with sc_col2:
        sc_diff = st.selectbox("Difficulty:", ["Beginner", "Intermediate", "Advanced"], key="sc_diff")

    if st.button("🎲 Generate Sentence Puzzle", key="btn_gen_puzzle"):
        with st.spinner("Creating puzzle..."):
            puzzle_prompt = f"""
            Create 1 sentence puzzle in {sc_lang} at {sc_diff} level.
            Return STRICTLY a JSON object without markdown fences:
            {{
                "english": "The English sentence here",
                "scrambled_words": ["word1", "word2", "word3", "word4", "word5"],
                "solution": "The complete correct sentence in {sc_lang}",
                "grammar_tip": "One key grammar insight about this sentence structure."
            }}
            """
            try:
                res = model.generate_content(puzzle_prompt).text.strip()
                if res.startswith("```"):
                    res = res.split("```")[1]
                    if res.startswith("json"):
                        res = res[4:]
                puzzle_data = json.loads(res.strip())
                st.session_state.puzzle_data = puzzle_data
                st.session_state.puzzle_lang = sc_lang
                st.rerun()
            except Exception as e:
                st.error(f"Error creating puzzle: {e}")

    if "puzzle_data" in st.session_state:
        p = st.session_state.puzzle_data
        with st.container(border=True):
            st.markdown(f"#### 🎯 Target Meaning: *\"{p['english']}\"*")
            
            # Show scrambled word tokens
            token_html = " ".join([f"<span class='arcade-badge' style='margin: 4px;'>{w}</span>" for w in p['scrambled_words']])
            st.markdown(f"<div style='margin: 15px 0;'>{token_html}</div>", unsafe_allow_html=True)
            
            user_sentence = st.text_input("Type the unscrambled sentence in " + st.session_state.puzzle_lang + ":", key="puzzle_input")
            
            if st.button("Check Solution", key="btn_check_puzzle"):
                if user_sentence.strip():
                    with st.spinner("Checking..."):
                        check_prompt = f"Target sentence: '{p['solution']}'. User typed: '{user_sentence.strip()}'. Are they equivalent or grammatically correct in {st.session_state.puzzle_lang}? Reply with YES or NO, followed by a one sentence explanation."
                        eval_res = model.generate_content(check_prompt).text.strip()
                        if eval_res.upper().startswith("YES"):
                            st.success(f"🎉 Spot on! **{p['solution']}**")
                            st.info(f"💡 Grammar Tip: {p['grammar_tip']}")
                            db_helper.record_game_score("Sentence Architect", 1, 1, st.session_state.puzzle_lang)
                            st.balloons()
                            audio = play_audio(p['solution'], st.session_state.puzzle_lang)
                            if audio:
                                st.markdown(audio, unsafe_allow_html=True)
                        else:
                            st.error(f"Not quite! Solution: **{p['solution']}**")
                            st.write(eval_res)
                else:
                    st.warning("Please type your sentence before submitting.")

# ==================== GAME 3: MYSTERY CLUES ====================
with game_tab3:
    st.markdown("### 🕵️ Mystery Dialogue Detective")
    st.markdown("Listen to what the NPC says in the target language and deduce where they are or what they're doing!")

    m_col1, m_col2 = st.columns([1, 1])
    with m_col1:
        m_lang = st.selectbox("Game Language:", ["Spanish", "French", "German", "Italian", "Japanese"], key="m_lang")
    with m_col2:
        m_theme = st.selectbox("Mystery Theme:", ["Mystery Location", "Secret Occupation", "Alien Artifact", "Culinary Dish"], key="m_theme")

    if st.button("🕵️ Start Mystery Investigation", key="btn_gen_mystery"):
        with st.spinner("Generating mystery dialogue..."):
            m_prompt = f"""
            Create a mystery guessing game in {m_lang} where an NPC speaks in {m_lang}.
            Theme: {m_theme}.
            Return STRICTLY a JSON object without markdown:
            {{
                "clues_target_lang": "2-3 sentences spoken by the character in {m_lang} giving vivid hints.",
                "english_translation": "Translation of the clues in English",
                "question": "Where is the speaker? or What is the speaker's job?",
                "choices": ["Choice A", "Choice B", "Choice C", "Choice D"],
                "correct_choice": "Choice A",
                "explanation": "Why this is correct."
            }}
            """
            try:
                res = model.generate_content(m_prompt).text.strip()
                if res.startswith("```"):
                    res = res.split("```")[1]
                    if res.startswith("json"):
                        res = res[4:]
                m_data = json.loads(res.strip())
                st.session_state.mystery_data = m_data
                st.session_state.mystery_lang = m_lang
                st.rerun()
            except Exception as e:
                st.error(f"Error loading mystery: {e}")

    if "mystery_data" in st.session_state:
        m = st.session_state.mystery_data
        with st.container(border=True):
            st.markdown(f"#### 📻 Incoming Transmission ({st.session_state.mystery_lang}):")
            st.markdown(f"<div class='glass-card' style='font-size: 1.25rem; color: #00f0ff;'>\"{m['clues_target_lang']}\"</div>", unsafe_allow_html=True)
            
            with st.expander("🔍 Reveal English Translation"):
                st.write(m['english_translation'])

            st.markdown(f"**Question: {m['question']}**")
            m_ans = st.radio("Your deduction:", m["choices"], key="mystery_choice")
            
            if st.button("Submit Deduction", key="btn_sub_mystery"):
                if m_ans == m["correct_choice"]:
                    st.success(f"🎯 Brilliant Detective! Correct: **{m['correct_choice']}**")
                    st.info(m["explanation"])
                    db_helper.record_game_score("Mystery Detective", 1, 1, st.session_state.mystery_lang)
                    st.balloons()
                else:
                    st.error(f"Case unsolved! The answer was **{m['correct_choice']}**.")
                    st.write(m["explanation"])

# Footer
st.markdown('<div class="app-footer">© 2026 LinguaNova AI. All rights reserved. | <a href="/About" target="_self">About</a> | <a href="/Contact" target="_self">Contact</a></div>', unsafe_allow_html=True)
