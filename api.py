import streamlit as st
from langchain_ollama import OllamaLLM
from learn import learn_section
from quiz import quiz_section

# Load model
@st.cache_resource
def load_model():
    return OllamaLLM(model="mango")

model = load_model()
st.set_page_config(page_title="Student Helper App  🥭", layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>
body, .stApp, .block-container {
    background: #000000 !important;
    color: #ffffff;
}

.quiz-container, .learning-container {
    max-width: 700px;
    margin: auto;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
    font-weight: 600;
    font-size: 16px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    color: #FFD700 !important;
    cursor: pointer;
}

/* Question Box */
.question-box {
    padding: 30px 20px 25px 20px;
    font-size: 26px;
    font-weight: bold;
    color: #ffffff;
    text-align: center;
    margin-bottom: 28px;
    margin-top: 20px;
    border: none;
}

/* MCQ Radio Button Hack */
.mcq-radio input[type="radio"] {
    display: none;
}
.mcq-radio label {
    display: flex;
    align-items: center;
    position: relative;
    margin-bottom: 30px;
    min-height: 65px;
    border-radius: 12px;
    border: 1.5px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 12px rgba(255,255,255,0.1);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.3s, border 0.3s;
    font-size: 21px;
    font-weight: 500;
    letter-spacing: 0.01em;
    color: #fff;
    width: 68vw;
    max-width: 660px;
    overflow: hidden;
    padding-left: 60px;
}

/* Hover Effect */
.mcq-radio label:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(255,255,255,0.2);
}

/* Selected State */
.mcq-radio input[type="radio"]:checked + label {
    border: 3px solid #FFC107;
    box-shadow: 0 4px 16px #ffa50266;
    outline: 2px solid #FFEBCD;
}

/* Correct Answer Checkmark */
.mcq-radio label.correct::after {
    content: '';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    width: 30px;
    height: 30px;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 6L9 17l-5-5'/%3E%3C/svg%3E") no-repeat center center;
    background-size: contain;
}

/* Option gradients */
.option0 { background: linear-gradient(90deg, #ffd465 0%, #fd9338 100%); }
.option1 { background: linear-gradient(90deg, #54dedb 0%, #224EAB 100%); }
.option2 { background: linear-gradient(90deg, #fd82c1 0%, #fad65c 100%); }
.option3 { background: linear-gradient(90deg, #224EAB 0%, #b66cf7 100%); }
.option4 { background: linear-gradient(90deg, #3897aa 0%, #8be15a 100%); }

/* Progress Bar */
.progress-container {
    margin: 20px 0;
    width: 100%;
    max-width: 660px;
    height: 10px;
    background: rgba(255,255,255,0.1);
    border-radius: 5px;
    overflow: hidden;
}
.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #ffd465 0%, #fd9338 100%);
    transition: width 0.3s ease-in-out;
}

/* Chat Interface */
.chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 15px;
    border-radius: 12px;
    background: #000000;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.chat-message {
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 10px;
    font-size: 16px;
    line-height: 1.5;
    max-width: 70%;
    word-wrap: break-word;
}
.chat-message.user {
    background: linear-gradient(90deg, #ffd465 0%, #fd9338 100%);
    color: #000;
    margin-left: 30%;
    text-align: right;
    border-radius: 10px 10px 0 10px;
}
.chat-message.ai {
    background: linear-gradient(90deg, #224EAB 0%, #b66cf7 100%);
    color: #fff;
    margin-right: 30%;
    border-radius: 10px 10px 10px 0;
}

/* Input Area Styling */
.stTextInput > div > input {
    background: #1a1a1a;
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff;
    border-radius: 8px;
    padding: 8px 12px;
}
.stButton > button {
    background: linear-gradient(90deg, #ffd465 0%, #fd9338 100%);
    color: #000;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    transition: transform 0.2s, box-shadow 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Main App ----------------


# Sidebar Navigation
st.sidebar.title("Options")
page = st.sidebar.radio("Choose", ["Learn", "Quiz"])

# Pages
if page == "Learn":
    st.markdown("<h1 style='text-align:center;color:#FFD700;'>Learn 🥭</h1>", unsafe_allow_html=True)
    learn_section(model)

elif page == "Quiz":
    st.markdown("<h1 style='text-align:center;color:#FFD700;'>Quiz 🥭</h1>", unsafe_allow_html=True)
    quiz_section(model)

