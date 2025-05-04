import google.generativeai as genai
from dotenv import load_dotenv
from prompts import QUESTION_GENERATION_PROMPT, DIAGNOSIS_PROMPT
import os
import json

load_dotenv()

def initialize_llm():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_questions(llm):
    response = llm.generate_content(QUESTION_GENERATION_PROMPT)
    try:
        questions_data = json.loads(response.text)
        # Ensure we have unique questions
        unique_questions = []
        seen_questions = set()
        
        for q in questions_data["questions"]:
            question_text = q["question"].strip().lower()
            if question_text not in seen_questions:
                seen_questions.add(question_text)
                unique_questions.append(q)
        
        return {"questions": unique_questions}
    except json.JSONDecodeError:
        # Fallback questions if parsing fails
        return {
            "questions": [
                {
                    "question": "Where is your headache located?",
                    "options": {
                        "a": "Front of head",
                        "b": "Back of head",
                        "c": "One side of head",
                        "d": "All over head"
                    }
                },
                {
                    "question": "How would you describe the pain?",
                    "options": {
                        "a": "Throbbing",
                        "b": "Constant pressure",
                        "c": "Sharp/stabbing",
                        "d": "Dull ache"
                    }
                },
                {
                    "question": "How long does your headache typically last?",
                    "options": {
                        "a": "Less than 1 hour",
                        "b": "1-4 hours",
                        "c": "4-24 hours",
                        "d": "More than 24 hours"
                    }
                },
                {
                    "question": "How often do you experience headaches?",
                    "options": {
                        "a": "Once a month or less",
                        "b": "2-3 times per month",
                        "c": "Once a week",
                        "d": "Multiple times per week"
                    }
                },
                {
                    "question": "What usually triggers your headache?",
                    "options": {
                        "a": "Stress",
                        "b": "Lack of sleep",
                        "c": "Certain foods",
                        "d": "Weather changes"
                    }
                }
            ]
        }

def get_diagnosis(llm, answers):
    formatted_answers = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])
    prompt = DIAGNOSIS_PROMPT.format(answers=formatted_answers)
    response = llm.generate_content(prompt)
    return response.text 