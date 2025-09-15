import streamlit as st
from storage import load_data, save_data

def notes_section(model):
    st.markdown("<div class='notes-container'>", unsafe_allow_html=True)

    # --- Load storage ---
    data = load_data()
    if "notes" not in st.session_state:
        st.session_state.notes = data.get("notes", [])

    # --- Notes Generator Form ---
    with st.form("notes_form"):
        grade = st.number_input("Grade", min_value=1, max_value=12, value=10)
        subject = st.text_input("Subject", value="Science")
        topic = st.text_input("Topic", value="Photosynthesis")
        submit = st.form_submit_button("Generate Notes")

    if submit:
        prompt = f"""
You are a helpful teacher. 
Create detailed, structured study notes for Grade {grade} students.
Subject: {subject}
Topic: {topic}

Format:
1. Title
2. Short introduction
3. Key points (bullet style)
4. Explanations/examples if necessary
5. Summary at the end
"""
        with st.spinner("Generating notes..."):
            try:
                result = model.generate([prompt])
                notes_text = result.generations[0][0].text
            except Exception as e:
                st.error(f"Error generating notes: {e}")
                st.stop()

            # save to session + storage
            new_note = {"grade": grade, "subject": subject, "topic": topic, "notes": notes_text}
            st.session_state.notes.append(new_note)
            data["notes"] = st.session_state.notes
            save_data(data)
            st.success("✅ Notes saved!")

    # --- Display Saved Notes ---
    if st.session_state.notes:
        st.markdown("<h3 style='color:#FFD700;'>📚 Saved Notes</h3>", unsafe_allow_html=True)

        for i, note in enumerate(st.session_state.notes):
            with st.expander(f"Grade {note['grade']} - {note['subject']} - {note['topic']}"):
                st.markdown(
                    f"<p style='white-space: pre-wrap; color:white;'>{note['notes']}</p>",
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)
