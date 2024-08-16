import streamlit as st
from PyPDF2 import PdfReader
import speech_recognition as sr
import openai
import sqlite3
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Initialize SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# OpenAI API Key
openai.api_key = "your_openai_api_key"

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def transcribe_audio_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio_data = recognizer.listen(source)
        st.write("Processing...")
        text = recognizer.recognize_google(audio_data)
    return text

def create_embeddings(text):
    sentences = text.split('.')
    embeddings = model.encode(sentences, convert_to_tensor=True)
    return sentences, embeddings

def retrieve_relevant_passages(question, sentences, embeddings):
    question_embedding = model.encode(question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(question_embedding, embeddings)[0]
    
    # Move the scores tensor to CPU before converting to NumPy
    scores = scores.cpu().numpy()
    
    top_results = np.argpartition(-scores, range(5))[:5]  # Get top 5 passages
    return [sentences[idx] for idx in top_results]


def ask_openai(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def init_db():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_query(question, answer):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('INSERT INTO queries (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()
    conn.close()

def get_all_queries():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('SELECT question, answer, timestamp FROM queries ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

# Initialize the database
init_db()

st.title("PDF Chatbot with RAG and Voice/Text Input")

uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_pdf is not None:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.write("PDF content extracted and embedded.")
    sentences, embeddings = create_embeddings(pdf_text)

    input_option = st.radio("Select input method", ("Text", "Voice"))

    if input_option == "Text":
        user_question = st.text_input("Ask a question about the PDF content")
        if user_question:
            relevant_passages = retrieve_relevant_passages(user_question, sentences, embeddings)
            context = " ".join(relevant_passages)  # Augmenting the context
            answer = ask_openai(user_question, context)  # Generate answer with augmented context
            st.write("Answer:", answer)
            store_query(user_question, answer)

    elif input_option == "Voice":
        if st.button("Record Question"):
            user_question = transcribe_audio_from_microphone()
            st.write("Transcribed Question:", user_question)
            relevant_passages = retrieve_relevant_passages(user_question, sentences, embeddings)
            context = " ".join(relevant_passages)  # Augmenting the context
            answer = ask_openai(user_question, context)  # Generate answer with augmented context
            st.write("Answer:", answer)
            store_query(user_question, answer)

# Display stored queries
st.subheader("Previous Queries")
stored_queries = get_all_queries()

for query in stored_queries:
    st.write(f"*Question:* {query[0]}")
    st.write(f"*Answer:* {query[1]}")
    st.write(f"*Timestamp:* {query[2]}")
    st.write("---")
