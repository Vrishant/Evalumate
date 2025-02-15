import requests
import fitz  # PyMuPDF for PDF extraction
import pytesseract
from PIL import Image
import io
import re

# OpenRouter API Key (Replace with your actual key)
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Function to make API requests to OpenRouter (Claude)
def claude_api_request(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anthropic.claude-2.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }
    response = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " ".join([page.get_text("text") for page in doc])
    return text

# Function to extract text from images using OCR
def extract_text_from_image(image_file):
    image = Image.open(io.BytesIO(image_file))
    text = pytesseract.image_to_string(image)
    return text

# Function to summarize text using Claude API
def generate_summary(text):
    prompt = f"Summarize this document concisely:\n{text}"
    return claude_api_request(prompt)

# Function to answer queries based on document content
def answer_query(document_text, user_query):
    prompt = f"Document: {document_text}\n\nQ: {user_query}\nA:"
    return claude_api_request(prompt)

# Function to extract questions from a question paper PDF
def extract_questions_from_qp(qp_text):
    question_patterns = [r"Q\d+\..*?", r"\d+\)..*?"]
    questions = []
    for pattern in question_patterns:
        matches = re.findall(pattern, qp_text, re.DOTALL)
        questions.extend(matches)
    return questions

# Function to find answers in subject PDF
def find_answers_from_subject_pdf(subject_text, questions):
    answers = {}
    for question in questions:
        prompt = f"Find the best answer for this question from the document:\n\nQuestion: {question}\nDocument: {subject_text}\n\nAnswer:"
        answers[question] = claude_api_request(prompt)
    return answers

# Function to evaluate student answers
def evaluate_answer(student_answer, ideal_answer):
    prompt = f"""
Evaluate the student's answer. Provide:
1. A similarity score (0-100).
2. Mistakes or missing points.
3. Where marks were lost.

Ideal Answer: {ideal_answer}
Student Answer: {student_answer}

Feedback:
"""
    return claude_api_request(prompt)

# Main function to process QP, subject PDF, and compare with student responses
def evaluate_student_responses(qp_pdf, subject_pdf, student_responses):
    qp_text = extract_text_from_pdf(qp_pdf)
    subject_text = extract_text_from_pdf(subject_pdf)
    
    questions = extract_questions_from_qp(qp_text)
    extracted_answers = find_answers_from_subject_pdf(subject_text, questions)
    
    evaluation_results = {}
    for question, student_answer in student_responses.items():
        ideal_answer = extracted_answers.get(question, "No matching answer found")
        if ideal_answer != "No matching answer found":
            feedback = evaluate_answer(student_answer, ideal_answer)
            evaluation_results[question] = {
                "student_answer": student_answer,
                "ideal_answer": ideal_answer,
                "feedback": feedback
            }
        else:
            evaluation_results[question] = {"error": "No matching answer found in subject PDF"}

    return evaluation_results

# Example Usage
if __name__ == "__main__":
    test_pdf = "sample.pdf"
    pdf_text = extract_text_from_pdf(test_pdf)
    print("Summary:", generate_summary(pdf_text))

    print("Q&A:", answer_query(pdf_text, "What is the main topic of the document?"))

    qp_pdf = "question_paper.pdf"
    subject_pdf = "subject_content.pdf"
    student_responses = {
        "Q1. What is artificial intelligence?": "AI is when computers act like humans.",
        "Q2. Define machine learning.": "ML is a part of AI that learns from data."
    }

    results = evaluate_student_responses(qp_pdf, subject_pdf, student_responses)
    print(results)
