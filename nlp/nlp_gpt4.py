import fitz  # PyMuPDF for PDF extraction
import pytesseract
from PIL import Image
import io
import openai  # GPT-4 for NLP
import re

# OpenAI API Key (Replace with your actual key)
openai.api_key = "your-api-key"

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

# Function to summarize extracted text using GPT-4
def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Summarize this document concisely."},
                  {"role": "user", "content": text}],
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"]

# Function to answer user queries based on document content
def answer_query(document_text, user_query):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer the query based on the provided document."},
            {"role": "user", "content": f"Document: {document_text}\nQuery: {user_query}"}
        ],
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]

# Function to extract questions from a question paper PDF
def extract_questions_from_qp(qp_text):
    """Extract questions from the question paper using regex patterns."""
    question_patterns = [
        r"Q\d+\..*?",  # Matches Q1. or Q2. etc.
        r"\d+\)..*?",  # Matches 1) or 2)
    ]
    questions = []
    for pattern in question_patterns:
        matches = re.findall(pattern, qp_text, re.DOTALL)
        questions.extend(matches)
    
    return questions

# Function to find answers in subject PDF based on extracted questions
def find_answers_from_subject_pdf(subject_text, questions):
    answers = {}
    for question in questions:
        match = re.search(rf"{re.escape(question)}(.*?)(Q\d+|\d+\)|$)", subject_text, re.DOTALL)
        if match:
            extracted_answer = match.group(1).strip()
            answers[question] = extracted_answer
        else:
            answers[question] = "Answer not found in document"
    return answers

# Function to evaluate student answers with detailed feedback
def evaluate_answer(student_answer, ideal_answer):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Evaluate the student's answer. Provide:\n1. A similarity score (0-100).\n2. Mistakes or missing points.\n3. Reasons why marks were lost."},
            {"role": "user", "content": f"Ideal Answer: {ideal_answer}\nStudent Answer: {student_answer}\nFeedback:"}
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]

# Main function to process QP and subject PDF, then compare with student responses
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
                "feedback": feedback  # Now includes mistakes & mark deduction reasoning
            }
        else:
            evaluation_results[question] = {"error": "No matching answer found in subject PDF"}

    return evaluation_results

# Example Usage
if __name__ == "__main__":
    # Summarization Example
    test_pdf = "sample.pdf"  # Replace with actual PDF file
    pdf_text = extract_text_from_pdf(test_pdf)
    print("Summary:", generate_summary(pdf_text))

    # Question-Answering Example
    print("Q&A:", answer_query(pdf_text, "What is the main topic of the document?"))

    # Answer Evaluation Example
    qp_pdf = "question_paper.pdf"  # Replace with actual QP PDF path
    subject_pdf = "subject_content.pdf"  # Replace with actual subject content PDF path
    student_responses = {
        "Q1. What is artificial intelligence?": "AI is the ability of machines to perform human-like tasks.",
        "Q2. Define machine learning.": "ML is a subset of AI that focuses on training algorithms on data."
    }

    results = evaluate_student_responses(qp_pdf, subject_pdf, student_responses)
    print(results)
