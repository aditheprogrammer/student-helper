import streamlit as st
import re

def quiz_section(model):
    st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)
    
    # --- Session State ---
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False

    # --- Quiz Generator Form ---
    if not st.session_state.quiz_generated:
        with st.form("quiz_form"):
            grade = st.number_input("Grade", min_value=1, max_value=12, value=1)
            subject = st.text_input("Subject", value="English")
            questionsnum = st.number_input("Number of Questions", min_value=1, max_value=10, value=5)
            submit = st.form_submit_button("Generate Quiz")

        if submit:
            st.session_state.questions = []
            st.session_state.answers = {}
            st.session_state.current_question = 0

            quiz_template = f"""
You are a quiz master.
Create {questionsnum} multiple-choice questions for Grade {grade} in {subject} 
based on the CDC Nepal curriculum.
Rules:
1. Each question must have exactly 4 options labeled A, B, C, D.
2. Only 1 option should be correct; the others plausible distractors.
3. Avoid trivial questions.
Format exactly like this:
Q1: Question text
A) Option1
B) Option2
C) Option3
D) Option4
Answer: B
"""

            with st.spinner("Generating quiz..."):
                try:
                    result = model.generate([quiz_template])
                    quiz_text = result.generations[0][0].text
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
                    st.stop()

                # --- Regex parser to capture all questions ---
                pattern = r"(Q\d+:.*?)(?=Q\d+:|$)"
                matches = re.findall(pattern, quiz_text, flags=re.DOTALL)

                for match in matches:
                    lines = [line.strip() for line in match.strip().split("\n") if line.strip()]
                    if len(lines) < 2:
                        continue
                    q_text = lines[0]
                    options = {}
                    answer = None
                    for line in lines[1:]:
                        if len(line) > 2 and line[1] == ")":
                            options[line[0]] = line[3:].strip()
                        elif line.startswith("Answer:"):
                            answer = line.split(":")[1].strip()
                    if q_text and options and answer:
                        st.session_state.questions.append({
                            "question": q_text,
                            "options": options,
                            "answer": answer
                        })

            if st.session_state.questions:
                st.session_state.quiz_generated = True
                st.rerun()
            else:
                st.error("Failed to generate valid questions. Try again.")

    if not st.session_state.quiz_generated:
        st.stop()

    # --- Progress Bar ---
    total_questions = len(st.session_state.questions)
    current_progress = (st.session_state.current_question + 1) / total_questions * 100
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar' style='width:{current_progress}%;'></div>
    </div>
    <p style='text-align:center;color:#fff;'>Question {st.session_state.current_question + 1} of {total_questions}</p>
    """, unsafe_allow_html=True)

    # --- Display Question ---
    idx = st.session_state.current_question
    qdata = st.session_state.questions[idx]
    st.markdown(f"<div class='question-box'> {qdata['question']}</div>", unsafe_allow_html=True)

    option_keys = list(qdata['options'].keys())
    option_classes = [f"option{i}" for i in range(len(option_keys))]

    # --- MCQ Options with Gradient and Checkmark ---
    with st.form(f"mcq_form_{idx}"):
        for i, k in enumerate(option_keys):
            selected = st.session_state.answers.get(idx, None)
            correct_class = ""
            if idx in st.session_state.answers and k == qdata['answer']:
                correct_class = "correct"  # adds checkmark

            checked = "checked" if selected == k else ""
            disabled = "disabled" if idx in st.session_state.answers else ""
            st.markdown(f"""
            <div class='mcq-radio'>
                <input type="radio" id="opt{idx}_{k}" name="q{idx}" value="{k}" {checked} {disabled}>
                <label class="{option_classes[i]} {correct_class}" for="opt{idx}_{k}">{k}) {qdata['options'][k]}</label>
            </div>
            """, unsafe_allow_html=True)

        submit_ans = st.form_submit_button("Submit Answer")
        if submit_ans and idx not in st.session_state.answers:
            # fallback: select first option if JS can't detect clicked one
            st.session_state.answers[idx] = option_keys[0]
            st.rerun()

    # --- Navigation ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Question") and st.session_state.current_question > 0:
            st.session_state.current_question -= 1
            st.rerun()
    with col2:
        if st.button("Next Question") and st.session_state.current_question < total_questions - 1:
            st.session_state.current_question += 1
            st.rerun()

    # --- Scoring ---
    if len(st.session_state.answers) == total_questions:
        score = total_questions - sum(1 for i, q in enumerate(st.session_state.questions)
                    if st.session_state.answers.get(i) == q['answer'])
        percentage = (score / total_questions) * 100
        if percentage == 100:
            feedback = "🟢 Excellent!"
        elif percentage >= 80:
            feedback = "🟡 Good job!"
        elif percentage >= 50:
            feedback = "🟠 Keep practicing!"
        else:
            feedback = "🔴 Needs improvement!"

        st.success(f"🎉 Quiz Finished! Your score: {score}/{total_questions} ({percentage:.0f}%) {feedback}")

        if st.button("Restart Quiz"):
            st.session_state.quiz_generated = False
            st.session_state.questions = []
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
