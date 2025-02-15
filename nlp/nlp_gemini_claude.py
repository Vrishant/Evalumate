# Standard Library
import io
import re

# Third-Party
import cv2
import fitz  # PyMuPDF for PDF extraction
import numpy as np
import pytesseract
import requests
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image

# API Keys (Replace with actual keys)
GEMINI_API_KEY = "AIzaSyBBrbcoe-aytImlkNydv1BKGKV9-iJaqq4"
CLAUDE_API_KEY = "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"

# API URLs
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
CLAUDE_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load Pre-trained MobileNetV2 for Image Classification
model = MobileNetV2(weights="imagenet")

# Load pre-trained EAST text detector
east_model = "frozen_east_text_detection.pb"
net = cv2.dnn.readNet(east_model)

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

# Function to detect text in images
def detect_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blob = cv2.dnn.blobFromImage(gray, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    scores, _ = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])
    return np.max(scores) > 0.5  # Returns True if text is detected

# Function to extract text from images
def extract_text_from_image(image_file):
    image = Image.open(io.BytesIO(image_file))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    if detect_text(image_cv):
        return pytesseract.image_to_string(image)  # Run OCR
    else:
        return "No text detected, processing as an image..."

# Function to classify non-text images
def classify_image(image_file):
    img = Image.open(io.BytesIO(image_file))
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    return preds.argmax()  # Returns the predicted class index

# Function to process document (PDF or Image)
def process_document(file_path, file_type="pdf"):
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "image":
        with open(file_path, "rb") as f:
            image_bytes = f.read()
        extracted_text = extract_text_from_image(image_bytes)
        
        if "No text detected" in extracted_text:
            return f"Image classified as: {classify_image(image_bytes)}"
        return extracted_text

# Function to summarize text
def generate_summary(text, model="gemini"):
    prompt = f"Summarize this document concisely:\n{text}"
    return call_gemini(prompt) if model == "gemini" else call_claude(prompt)

# Function to answer queries based on document content
def answer_query(document_text, user_query, model="gemini"):
    prompt = f"Document: {document_text}\n\nQ: {user_query}\nA:"
    return call_gemini(prompt) if model == "gemini" else call_claude(prompt)

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

# Main function to evaluate student responses
def evaluate_student_responses(qp_pdf, subject_pdf, student_responses, model="gemini"):
    qp_text = extract_text_from_pdf(qp_pdf)
    subject_text = extract_text_from_pdf(subject_pdf)
    
    questions = re.findall(r"Q\d+\..*?", qp_text, re.DOTALL)
    extracted_answers = {q: answer_query(subject_text, q, model) for q in questions}
    
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
    pdf_text = process_document("sample.pdf", "pdf")
    print("Summary:", generate_summary(pdf_text))
    print("Q&A:", answer_query(pdf_text, "What is the main topic?"))
