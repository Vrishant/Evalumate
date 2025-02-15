import nltk
import pdfplumber
import pytesseract
import cv2
import numpy as np
import chromadb
import anthropic  # Claude API
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

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("documents")

# Claude API Key (replace with your key)
ANTHROPIC_API_KEY = (
    "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"
)


def preprocess_text(text):
    """Tokenizes, removes stopwords, and lemmatizes text"""
    words = word_tokenize(text)
    words = [
        lemmatizer.lemmatize(w.lower())
        for w in words
        if w.isalnum() and w.lower() not in stop_words
    ]
    return " ".join(words)


def extract_text_from_pdf(pdf_path):
    """Extracts text from PDF files"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return preprocess_text(text)


def extract_text_from_image(image_path):
    """Extracts text from images using OCR"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return preprocess_text(text)


def store_text_in_chromadb(document_text, doc_id):
    """Stores document text in ChromaDB with embeddings"""
    sentences = sent_tokenize(document_text)
    embeddings = embedder.encode(sentences, convert_to_numpy=True)

    for idx, sentence in enumerate(sentences):
        collection.add(
            ids=[f"{doc_id}_{idx}"],
            embeddings=[embeddings[idx].tolist()],
            metadatas=[{"text": sentence}],
        )


def retrieve_relevant_sentences(query, top_k=3):
    """
    Retrieve top-k most relevant sentences using ChromaDB similarity search.
    """
    query_embedding = embedder.encode([query], convert_to_numpy=True).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    return (
        [match["text"] for match in results["metadatas"][0]]
        if results["metadatas"]
        else []
    )


def generate_answer_with_rag(question):
    """Uses ChromaDB + Claude AI to generate a more accurate response"""
    retrieved_context = retrieve_relevant_sentences(question, top_k=5)
    context_text = (
        " ".join(retrieved_context)
        if retrieved_context
        else "No relevant context found."
    )

    prompt = f"""
    You are an AI assistant that strictly answers based on the provided document.
    Answer the following question using only the retrieved context:
    
    Context: {context_text}
    Question: {question}
    
    If the context does not contain relevant information, reply: "I don't have enough information to answer this."
    """

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3", max_tokens=512, messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text  # Extract the response text


def extract_questions(qp_text):
    """Extracts questions from question paper text"""
    return [q.strip() for q in qp_text.split("\n") if q.strip().startswith("Q")]


def evaluate_answers(student_answers, ideal_answers):
    """Evaluates student answers against ideal answers"""
    results = {}
    for question, student_answer in student_answers.items():
        ideal_answer = ideal_answers.get(question, "No matching answer found")
        if ideal_answer != "No matching answer found":
            similarity_score = (
                len(set(student_answer.split()) & set(ideal_answer.split()))
                / len(set(ideal_answer.split()))
                * 100
            )
            results[question] = {
                "student_answer": student_answer,
                "ideal_answer": ideal_answer,
                "similarity_score": round(similarity_score, 2),
            }
        else:
            results[question] = {"error": "No matching answer found in subject PDF"}
    return results


"""
# Example Workflow
if __name__ == "__main__":
    # Process PDFs
    subject_pdf_text = extract_text_from_pdf("subject.pdf")
    qp_pdf_text = extract_text_from_pdf("question_paper.pdf")

    # Store subject PDF text in ChromaDB
    store_text_in_chromadb(subject_pdf_text, "subject_doc")

    # Retrieve Answers with RAG Model
    questions = extract_questions(qp_pdf_text)
    ideal_answers = {q: generate_answer_with_rag(q) for q in questions}

    # Example Student Responses
    student_responses = {
        "Q1. What is AI?": "AI is when computers try to act like humans.",
        "Q2. Define Machine Learning.": "ML is about computers learning patterns."
    }

    # Evaluate Student Answers
    evaluation_results = evaluate_answers(student_responses, ideal_answers)
    print("\n📌 Evaluation Results:", evaluation_results)
"""
