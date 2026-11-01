"""
Page 6: AI Career Chat
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
from core.llm import LLMProvider

def render_chatbot(student_profile: dict, roadmap_data: dict, llm: LLMProvider):
    st.markdown("## 💬 AI Career Advisory Assistant")
    st.markdown(
        "Chat directly with the CareerCompass conversational agent. "
        "The assistant maintains context from your student profile, identified skill gaps, "
        "and O*NET occupational benchmarks."
    )

    if not student_profile:
        st.info("ℹ️ Complete the student onboarding form or load a sample profile to provide context for the assistant.")

    # Context String
    target_career = roadmap_data.get("selected_career", {})
    context_str = (
        f"Candidate Name: {student_profile.get('full_name', 'Student')}\n"
        f"Education: {student_profile.get('education_level', '')} in {student_profile.get('degree_branch', '')}\n"
        f"Target Career: {target_career.get('canonical_name', student_profile.get('career_goal', 'Technology Role'))} "
        f"(O*NET Code: {target_career.get('onetsoc_code', 'N/A')})\n"
        f"Declared Skills: {', '.join(student_profile.get('technical_skills', []))}\n"
        f"Interests: {', '.join(student_profile.get('interests', []))}\n"
        f"Roadmap Duration: {student_profile.get('learning_duration_months', 6)} Months"
    )

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    f"Hello {student_profile.get('full_name', 'there')}! I'm your CareerCompass AI Advisor. "
                    f"I see you are targeting **{target_career.get('canonical_name', 'your dream tech role')}**. "
                    "How can I help you today? You can ask me about projects to build, technical interview preparation, "
                    "how to close specific skill gaps, or course suggestions!"
                )
            }
        ]

    # Quick prompt buttons
    st.markdown("**Suggested Quick Inquiries:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        if st.button("💡 What project should I build first?", use_container_width=True):
            st.session_state.chat_messages.append({"role": "user", "content": "What project should I build first to impress hiring managers?"})
            reply = llm.chat_reply(st.session_state.chat_messages, context_str=context_str)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    with q_col2:
        if st.button("💼 How do I prepare for technical interviews?", use_container_width=True):
            st.session_state.chat_messages.append({"role": "user", "content": "How do I prepare for technical interviews and placement drives?"})
            reply = llm.chat_reply(st.session_state.chat_messages, context_str=context_str)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    with q_col3:
        if st.button("🎓 Which certifications are worth the money?", use_container_width=True):
            st.session_state.chat_messages.append({"role": "user", "content": "Which certifications are most respected for this role?"})
            reply = llm.chat_reply(st.session_state.chat_messages, context_str=context_str)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_query = st.chat_input("Ask CareerCompass about skills, roadmaps, interview prep, or career strategies...")
    if user_query:
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing O*NET benchmarks and profile context..."):
                reply = llm.chat_reply(st.session_state.chat_messages, context_str=context_str)
                st.markdown(reply)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
