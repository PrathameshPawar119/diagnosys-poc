import streamlit as st
from llm_service import initialize_llm, generate_questions, get_diagnosis
import json

def initialize_session_state():
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

def main():
    st.set_page_config(
        page_title="Headache Diagnosis Assistant",
        page_icon="🏥",
        layout="centered"
    )
    
    initialize_session_state()
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Generate questions if not already generated
    if st.session_state.questions is None:
        st.session_state.questions = generate_questions(llm)
        while len(st.session_state.questions["questions"]) < 5:
            additional_questions = generate_questions(llm)
            st.session_state.questions["questions"].extend(additional_questions["questions"])
    
    st.title("Headache Diagnosis Assistant")
    st.write("Please answer the following questions about your headache symptoms.")
    
    # Progress bar
    total_questions = len(st.session_state.questions["questions"])
    progress = (st.session_state.current_question + 1) / total_questions
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {total_questions}")
    
    # Display current question
    current_q = st.session_state.questions["questions"][st.session_state.current_question]
    
    with st.form(f"question_{st.session_state.current_question}"):
        st.write(current_q["question"])
        
        # Display options
        answer = st.radio(
            "Select your answer:",
            options=list(current_q["options"].keys()),
            format_func=lambda x: current_q["options"][x],
            key=f"q_{st.session_state.current_question}"
        )
        
        # Store the answer
        st.session_state.answers[current_q["question"]] = current_q["options"][answer]
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.form_submit_button("Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < total_questions - 1:
                if st.form_submit_button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.form_submit_button("Submit for Diagnosis"):
                    st.session_state.diagnosis = get_diagnosis(llm, st.session_state.answers)
                    st.rerun()
    
    # Display diagnosis if available
    if st.session_state.diagnosis:
        st.header("Diagnosis Results")
        st.write(st.session_state.diagnosis)
        
        if st.button("Start New Diagnosis"):
            st.session_state.questions = None
            st.session_state.answers = {}
            st.session_state.diagnosis = None
            st.session_state.current_question = 0
            st.rerun()

if __name__ == "__main__":
    main() 