import requests
import fitz  # PyMuPDF for PDF extraction
import pytesseract
from PIL import Image
import io
import re

# Google Gemini API Key (Replace with actual key)
GEMINI_API_KEY = "AIzaSyBBrbcoe-aytImlkNydv1BKGKV9-iJaqq4"

# API URL for Gemini
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Function to call Google Gemini API
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "temperature": 0.2}
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join([page.get_text("text") for page in doc])

# Function to extract text from images using OCR
def extract_text_from_image(image_file):
    image = Image.open(io.BytesIO(image_file))
    return pytesseract.image_to_string(image)

# Function to summarize text using Gemini
def generate_summary(text):
    prompt = f"Summarize this document concisely:\n{text}"
    return call_gemini(prompt)

# Function to answer queries based on document content
def answer_query(document_text, user_query):
    prompt = f"Document: {document_text}\n\nQ: {user_query}\nA:"
    return call_gemini(prompt)

# Function to extract questions from a question paper PDF
def extract_questions_from_qp(qp_text):
    question_patterns = [r"Q\d+\..*?", r"\d+\)..*?"]
    questions = []
    for pattern in question_patterns:
        questions.extend(re.findall(pattern, qp_text, re.DOTALL))
    return questions

# Function to find answers in subject PDF
def find_answers_from_subject_pdf(subject_text, questions):
    answers = {}
    for question in questions:
        prompt = f"Find the best answer for this question from the document:\n\nQuestion: {question}\nDocument: {subject_text}\n\nAnswer:"
        answers[question] = call_gemini(prompt)
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
    return call_gemini(prompt)

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
            evaluation_results[question] = {"student_answer": student_answer, "ideal_answer": ideal_answer, "feedback": feedback}
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
    print("Evaluation Results:", results)
