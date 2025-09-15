import streamlit as st
from storage import load_data, save_data

def learn_section(model):
    st.markdown("<div class='learning-container'>", unsafe_allow_html=True)

    # --- Load storage ---
    data = load_data()
    if "conversations" not in st.session_state:
        st.session_state.conversations = data.get("conversations", [])
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = 0

    # --- Start a new conversation ---
    with st.form("new_conversation_form"):
        grade = st.number_input("Grade", min_value=1, max_value=12, value=1, key="learn_grade")
        subject = st.text_input("Subject", value="English", key="learn_subject")
        if st.form_submit_button("Start New Conversation"):
            if subject.strip():
                new_convo = {"grade": grade, "subject": subject, "chat_history": []}
                st.session_state.conversations.append(new_convo)
                st.session_state.current_conversation = len(st.session_state.conversations) - 1

                # Save immediately
                save_data({"conversations": st.session_state.conversations})
                st.rerun()

    # --- Show existing conversations ---
    if st.session_state.conversations:
        conversation_titles = [f"(Grade {c['grade']}, {c['subject']})" for c in st.session_state.conversations]
        conversation_tabs = st.tabs(conversation_titles)

        for i, tab in enumerate(conversation_tabs):
            with tab:
                convo = st.session_state.conversations[i]

                # --- Chat container ---
                chat_container = st.container()
                for message in convo["chat_history"]:
                    cls = "user" if message["role"] == "user" else "ai"
                    chat_container.markdown(
                        f"<div class='chat-message {cls}'>{message['content']}</div>",
                        unsafe_allow_html=True
                    )

                # --- User input ---
                user_input = st.text_input("Ask a question about the subject:", key=f"chat_input_{i}")
                if st.button("Send", key=f"send_button_{i}"):
                    if user_input.strip():
                        convo["chat_history"].append({"role": "user", "content": user_input})

                        # Generate AI response
                        chat_template = f"""
You are an expert teacher for Grade {convo['grade']} in {convo['subject']}, aligned with the Curriculum Development Centre (CDC) of Nepal.
Respond to the student's question: '{user_input}'.
Rules:
1. Use simple, grade-appropriate language.
2. Keep the response concise (50-100 words).
3. Include a relevant example if possible.
4. Avoid culturally insensitive or biased content.
5. Answer directly and encourage further questions.
"""
                        with st.spinner("Generating response..."):
                            try:
                                result = model.generate([chat_template])
                                ai_response = result.generations[0][0].text
                                convo["chat_history"].append({"role": "ai", "content": ai_response})
                            except Exception as e:
                                st.error(f"Error generating response: {e}")

                        # Save after every message
                        save_data({"conversations": st.session_state.conversations})
                        st.rerun()

                # --- Delete individual conversation ---
                if st.button("Delete This Conversation", key=f"delete_{i}"):
                    st.session_state.conversations.pop(i)
                    st.session_state.current_conversation = 0
                    save_data({"conversations": st.session_state.conversations})
                    st.rerun()

        # --- Clear all conversations ---
        if st.button("Clear All Conversations"):
            st.session_state.conversations = []
            st.session_state.current_conversation = 0
            save_data({"conversations": []})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
