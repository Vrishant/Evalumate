import requests
import fitz  # PyMuPDF for PDF extraction
import pytesseract
from PIL import Image
import io
import re

# API Keys (Replace with actual keys)
GEMINI_API_KEY = "AIzaSyBBrbcoe-aytImlkNydv1BKGKV9-iJaqq4"
CLAUDE_API_KEY = "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"

# API URLs
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
CLAUDE_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Function to call Google Gemini API
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "temperature": 0.2}
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Function to call Anthropic Claude API
def call_claude(prompt):
    headers = {"Authorization": f"Bearer {CLAUDE_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "anthropic.claude-2.1", "messages": [{"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 500}
    response = requests.post(CLAUDE_API_URL, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join([page.get_text("text") for page in doc])

# Function to extract text from images using OCR
def extract_text_from_image(image_file):
    image = Image.open(io.BytesIO(image_file))
    return pytesseract.image_to_string(image)

# Function to summarize text using either API
def generate_summary(text, model="gemini"):
    prompt = f"Summarize this document concisely:\n{text}"
    return call_gemini(prompt) if model == "gemini" else call_claude(prompt)

# Function to answer queries based on document content
def answer_query(document_text, user_query, model="gemini"):
    prompt = f"Document: {document_text}\n\nQ: {user_query}\nA:"
    return call_gemini(prompt) if model == "gemini" else call_claude(prompt)

# Function to extract questions from a question paper PDF
def extract_questions_from_qp(qp_text):
    question_patterns = [r"Q\d+\..*?", r"\d+\)..*?"]
    questions = []
    for pattern in question_patterns:
        questions.extend(re.findall(pattern, qp_text, re.DOTALL))
    return questions

# Function to find answers in subject PDF
def find_answers_from_subject_pdf(subject_text, questions, model="gemini"):
    answers = {}
    for question in questions:
        prompt = f"Find the best answer for this question from the document:\n\nQuestion: {question}\nDocument: {subject_text}\n\nAnswer:"
        answers[question] = call_gemini(prompt) if model == "gemini" else call_claude(prompt)
    return answers

# Function to evaluate student answers
def evaluate_answer(student_answer, ideal_answer, model="gemini"):
    prompt = f"""
Evaluate the student's answer. Provide:
1. A similarity score (0-100).
2. Mistakes or missing points.
3. Where marks were lost.

Ideal Answer: {ideal_answer}
Student Answer: {student_answer}

Feedback:
"""
    return call_gemini(prompt) if model == "gemini" else call_claude(prompt)

# Main function to process QP, subject PDF, and compare with student responses
def evaluate_student_responses(qp_pdf, subject_pdf, student_responses, model="gemini"):
    qp_text = extract_text_from_pdf(qp_pdf)
    subject_text = extract_text_from_pdf(subject_pdf)

    questions = extract_questions_from_qp(qp_text)
    extracted_answers = find_answers_from_subject_pdf(subject_text, questions, model)

    evaluation_results = {}
    for question, student_answer in student_responses.items():
        ideal_answer = extracted_answers.get(question, "No matching answer found")
        if ideal_answer != "No matching answer found":
            feedback = evaluate_answer(student_answer, ideal_answer, model)
            evaluation_results[question] = {"student_answer": student_answer, "ideal_answer": ideal_answer, "feedback": feedback}
        else:
            evaluation_results[question] = {"error": "No matching answer found in subject PDF"}

    return evaluation_results

# Example Usage
if __name__ == "__main__":
    test_pdf = "sample.pdf"
    pdf_text = extract_text_from_pdf(test_pdf)
    
    print("Summary (Gemini):", generate_summary(pdf_text, "gemini"))
    print("Summary (Claude):", generate_summary(pdf_text, "claude"))

    print("Q&A (Gemini):", answer_query(pdf_text, "What is the main topic of the document?", "gemini"))
    print("Q&A (Claude):", answer_query(pdf_text, "What is the main topic of the document?", "claude"))

    qp_pdf = "question_paper.pdf"
    subject_pdf = "subject_content.pdf"
    student_responses = {
        "Q1. What is artificial intelligence?": "AI is when computers act like humans.",
        "Q2. Define machine learning.": "ML is a part of AI that learns from data."
    }

    results_gemini = evaluate_student_responses(qp_pdf, subject_pdf, student_responses, "gemini")
    results_claude = evaluate_student_responses(qp_pdf, subject_pdf, student_responses, "claude")

    print("Evaluation Results (Gemini):", results_gemini)
    print("Evaluation Results (Claude):", results_claude)
