QUESTION_GENERATION_PROMPT = """
Generate 10 unique multiple choice questions to diagnose different types of headaches.
Each question should be distinct and cover different aspects of headache symptoms.
Each question should have 4 options (a, b, c, d).
Format the output as a JSON with the following structure:
{
    "questions": [
        {
            "question": "Question text",
            "options": {
                "a": "Option A",
                "b": "Option B",
                "c": "Option C",
                "d": "Option D"
            }
        }
    ]
}

Make sure each question is unique and covers different aspects like:
- Location of pain
- Type of pain
- Duration
- Frequency
- Triggers
- Associated symptoms
- Time of day
- Impact on daily activities
- Previous treatments
- Family history
"""

DIAGNOSIS_PROMPT = """
Based on the following answers to headache-related questions, provide a diagnosis:
1. List the type of headache the patient is likely experiencing
2. Rate the severity (mild, moderate, severe)
3. Suggest immediate remedies
4. Recommend when to seek medical attention

Questions and answers:
{answers}

Format the response in a clear, structured manner with these sections:
1. Diagnosis
2. Severity
3. Immediate Remedies
4. When to Seek Medical Attention
""" 