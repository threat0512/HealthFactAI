import streamlit as st
from utils.api import search_health_claims, get_user_progress, generate_quiz, submit_quiz_answers, track_quiz_activity, track_quiz_answers
from utils.state import is_authenticated

def save_fact_for_user(**kwargs):
    """Placeholder function - progress is tracked automatically via API"""
    pass


def render_quiz() -> None:
    """Render the quiz page with health claim checker and quiz mode"""
    
    if not is_authenticated():
        st.error("🔐 Please log in to access the quiz functionality.")
        return

    # Quiz Generation from Search
    st.markdown("---")
    
    # Check if there's a claim from search
    quiz_claim = getattr(st.session_state, "quiz_claim", "")
    generate_quiz_trigger = getattr(st.session_state, "generate_quiz", False)
    
    if quiz_claim and generate_quiz_trigger:
        st.markdown("### 🧠 Generate Quiz from Search")
        st.info(f"**Claim from search:** {quiz_claim}")
        
        # Auto-generate quiz when coming from search
        # Clear the trigger first
        st.session_state.generate_quiz = False
        
        # Generate quiz with loading
        with st.spinner("🧠 Generating quiz questions..."):
            quiz_data = generate_quiz(quiz_claim)
        
        if quiz_data and not quiz_data.get("error"):
            # Store quiz data in session state
            st.session_state["current_quiz"] = quiz_data
            st.session_state["quiz_answers"] = {}
            
            # Track quiz generation activity
            questions_count = len(quiz_data.get("questions", []))
            track_quiz_activity(quiz_claim, questions_count)
            
            # Clear the quiz claim since we've used it
            if hasattr(st.session_state, "quiz_claim"):
                del st.session_state.quiz_claim
            st.success("✅ Quiz generated successfully!")
            st.rerun()
        else:
            error_msg = quiz_data.get("error", "Unknown error") if quiz_data else "Failed to generate quiz"
            st.error(f"❌ Error generating quiz: {error_msg}")
            # Clear the quiz claim on error too
            if hasattr(st.session_state, "quiz_claim"):
                del st.session_state.quiz_claim
    
    # Display Current Quiz
    current_quiz = st.session_state.get("current_quiz")
    if current_quiz:
        st.markdown("### 📝 Current Quiz")
        st.write(f"**Topic:** {current_quiz.get('claim', 'Unknown')}")
        
        questions = current_quiz.get("questions", [])
        quiz_id = current_quiz.get("quiz_id", "")
        
        # Limit to 5 questions max
        questions = questions[:5]
        
        if questions:
            # Initialize answers if not exists
            if "quiz_answers" not in st.session_state:
                st.session_state["quiz_answers"] = {}
            
            # Display questions
            for i, question in enumerate(questions):
                st.markdown(f"**Question {i+1}:** {question.get('question', '')}")
                
                options = question.get("options", [])
                if options:
                    # Use unique key for each question
                    answer_key = f"q_{i}"
                    selected_answer = st.radio(
                        "Select your answer:",
                        options,
                        key=answer_key,
                        index=None
                    )
                    
                    # Store answer in session state
                    if selected_answer:
                        st.session_state["quiz_answers"][i] = selected_answer
                
                st.markdown("---")
            
            # Submit Quiz Button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📋 Submit Quiz", type="primary", use_container_width=True):
                    # Check if all questions are answered
                    if len(st.session_state.get("quiz_answers", {})) < len(questions):
                        st.error("❌ Please answer all questions before submitting.")
                    else:
                        # Prepare answers in order
                        answers = []
                        for i in range(len(questions)):
                            answers.append(st.session_state["quiz_answers"].get(i, ""))
                        
                        # Submit quiz with loading
                        with st.spinner("📋 Submitting and grading quiz..."):
                            result = submit_quiz_answers(quiz_id, answers)
                        
                        if result and not result.get("error"):
                            # Track quiz answers
                            question_results = result.get("results", [])
                            correct_answers = [qr.get("correct_answer", "") for qr in question_results]
                            track_quiz_answers(answers, correct_answers)
                            
                            # Store results and show them
                            st.session_state["quiz_results"] = result
                            st.session_state["show_results"] = True
                            st.rerun()
                        else:
                            error_msg = result.get("error", "Unknown error") if result else "Failed to submit quiz"
                            st.error(f"❌ Error submitting quiz: {error_msg}")
    
    # Display Quiz Results
    if st.session_state.get("show_results") and st.session_state.get("quiz_results"):
        st.markdown("### 🎯 Quiz Results")
        results = st.session_state["quiz_results"]
        
        # Overall score
        score = results.get("score", 0)
        total = results.get("total_questions", 0)
        percentage = results.get("score_percentage", 0)
        passed = results.get("passed", False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{score}/{total}")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%")
        with col3:
            if passed:
                st.success("✅ Passed!")
            else:
                st.error("❌ Failed")
        
        # Detailed results
        st.markdown("#### 📋 Detailed Results")
        question_results = results.get("results", [])
        current_quiz = st.session_state.get("current_quiz", {})
        questions = current_quiz.get("questions", [])
        
        for i, (question_result, question) in enumerate(zip(question_results, questions)):
            is_correct = question_result.get("is_correct", False)
            user_answer = question_result.get("user_answer", "")
            correct_answer = question_result.get("correct_answer", "")
            
            # Display question with result
            if is_correct:
                st.success(f"**Q{i+1}:** {question.get('question', '')}")
            else:
                st.error(f"**Q{i+1}:** {question.get('question', '')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Your answer:** {user_answer}")
            with col2:
                st.write(f"**Correct answer:** {correct_answer}")
            
            st.markdown("---")
        
        # Clear quiz button
        if st.button("🔄 Take Another Quiz"):
            # Clear all quiz-related session state
            keys_to_clear = ["current_quiz", "quiz_answers", "quiz_results", "show_results", "quiz_claim", "generate_quiz"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Manual Quiz Generation
    if not quiz_claim and not current_quiz:
        st.markdown("### 🧠 Generate Quiz Manually")
        manual_claim = st.text_input("Enter a health claim to generate quiz:")
        
        if st.button("Generate Quiz", key="manual_quiz") and manual_claim.strip():
            with st.spinner("🧠 Generating quiz questions..."):
                quiz_data = generate_quiz(manual_claim.strip())
            
            if quiz_data and not quiz_data.get("error"):
                st.session_state["current_quiz"] = quiz_data
                st.session_state["quiz_answers"] = {}
                st.success("✅ Quiz generated successfully!")
                st.rerun()
            else:
                error_msg = quiz_data.get("error", "Unknown error") if quiz_data else "Failed to generate quiz"
                st.error(f"❌ Error generating quiz: {error_msg}")

    # Recent facts after interactions
    st.markdown("---")