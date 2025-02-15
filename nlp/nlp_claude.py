import nltk
import pdfplumber
import pytesseract
import cv2
import numpy as np
from PIL import Image
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load Sentence Transformer Model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize NLTK Components
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    """ Tokenizes, removes stopwords, and lemmatizes text """
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w.isalnum() and w.lower() not in stop_words]
    return " ".join(words)

def extract_text_from_pdf(pdf_path):
    """ Extracts text from PDF files """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return preprocess_text(text)

def extract_text_from_image(image_path):
    """ Extracts text from images using OCR """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return preprocess_text(text)

def generate_embeddings(text_list):
    """ Generate embeddings for a list of sentences """
    return embedder.encode(text_list, convert_to_numpy=True)

def retrieve_relevant_sentences(query, text_sentences, text_embeddings, top_k=3):
    """
    Retrieve top-k most relevant sentences using cosine similarity.
    """
    query_embedding = embedder.encode([query], convert_to_numpy=True)
    
    # Compute cosine similarity
    similarities = np.dot(text_embeddings, query_embedding.T).flatten()
    
    # Get top-k matches
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    return [text_sentences[i] for i in top_indices]

def summarize_text(text, complexity="intermediate"):
    """ Generates a summary with different complexity levels """
    sentences = sent_tokenize(text)
    
    if complexity == "beginner":
        summary = " ".join(sentences[:len(sentences)//4])  # Take the first 25%
    elif complexity == "intermediate":
        summary = " ".join(sentences[:len(sentences)//2])  # Take the first 50%
    else:  # Expert
        summary = " ".join(sentences)  # Full text with minimal trimming

    return summary

def extract_questions(qp_text):
    """ Extracts questions from question paper text """
    return [q.strip() for q in qp_text.split("\n") if q.strip().startswith("Q")]

def find_answers(subject_text, questions):
    """ Finds relevant answers in subject document (using in-memory retrieval) """
    sentences = sent_tokenize(subject_text)
    sentence_embeddings = generate_embeddings(sentences)

    answers = {}
    for question in questions:
        retrieved_info = retrieve_relevant_sentences(question, sentences, sentence_embeddings)
        answers[question] = " ".join(retrieved_info) if retrieved_info else "No relevant answer found"
    
    return answers

def evaluate_answers(student_answers, ideal_answers):
    """ Evaluates student answers against ideal answers """
    results = {}
    for question, student_answer in student_answers.items():
        ideal_answer = ideal_answers.get(question, "No matching answer found")
        if ideal_answer != "No matching answer found":
            similarity_score = len(set(student_answer.split()) & set(ideal_answer.split())) / len(set(ideal_answer.split())) * 100
            results[question] = {
                "student_answer": student_answer,
                "ideal_answer": ideal_answer,
                "similarity_score": round(similarity_score, 2)
            }
        else:
            results[question] = {"error": "No matching answer found in subject PDF"}
    return results

# Example Workflow
if __name__ == "__main__":
    # Process PDFs
    subject_pdf_text = extract_text_from_pdf("subject.pdf")
    qp_pdf_text = extract_text_from_pdf("question_paper.pdf")

    # Summarization
    summary = summarize_text(subject_pdf_text, "intermediate")
    print("📌 Summary:", summary)

    # Retrieve Answers
    questions = extract_questions(qp_pdf_text)
    ideal_answers = find_answers(subject_pdf_text, questions)

    # Student Responses
    student_responses = {
        "Q1. What is AI?": "AI is when computers try to act like humans.",
        "Q2. Define Machine Learning.": "ML is about computers learning patterns."
    }

    # Evaluate Student Answers
    evaluation_results = evaluate_answers(student_responses, ideal_answers)
    print("\n📌 Evaluation Results:", evaluation_results)
