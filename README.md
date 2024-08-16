# RAG
📄 PDF Chatbot with RAG and Voice/Text Input 🎤💬
🌟 Overview
Welcome to the PDF Chatbot project! This web-based application, powered by Streamlit, combines the magic of PDF text extraction, voice-to-text conversion, and intelligent question-answering. Whether you prefer typing or speaking, this tool allows you to interact with PDF documents and get insightful responses powered by OpenAI’s GPT-3.5-turbo model. Plus, it keeps track of your queries for future reference! 📚🤖

🚀 Features
PDF Text Extraction: Seamlessly extract and process text from your PDFs for easy querying. 📑

Voice-to-Text Conversion: Convert your spoken questions into text with cutting-edge speech recognition. 🎙️➡️📝

Text Embeddings: Utilize Sentence Transformers to create rich, semantic embeddings of the PDF content. 🧠🔍

Contextual Question Answering: Get accurate answers based on your PDF content and user queries using GPT-3.5-turbo. 💬🔎

Query Storage: Store and retrieve your previous queries and answers using a built-in SQLite database. 💾🗂️

Interactive Interface: Enjoy an intuitive web interface for uploading PDFs, selecting input methods, and viewing past queries. 🌐
🛠️ Installation
Get started with these simple steps:

Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/your-repository.git
cd your-repository
Install Dependencies:
Make sure you have Python 3.7+ installed, then run:

bash
Copy code
pip install -r requirements.txt
Set Up OpenAI API Key:
Replace "your_openai_api_key" in the script with your actual OpenAI API key. 🔑

Run the Application:
Launch the Streamlit app with:

bash
Copy code
streamlit run app.py


💡 Usage
Upload a PDF: Drag and drop your PDF into the uploader to extract and process the content. 📤📄

Choose Input Method:
Text: Type your question about the PDF and receive a detailed response. 🖊️🤔

Voice: Click “Record Question,” speak your query, and get the transcribed answer. 🎙️🔄



View Previous Queries: Check out your previous questions and answers along with timestamps. 🕒🔍
Demo Video 


https://github.com/user-attachments/assets/d96dfc96-4ee8-4b70-87d7-a6415e186e07


📝 Code Explanation
Text Extraction: Uses PyPDF2 to extract text from PDF files. 🧩📚

Voice Transcription: Converts spoken questions into text with speech_recognition. 🎙️➡️📝

Embeddings: Creates semantic embeddings using SentenceTransformers. 🌐🔍

Question Answering: Generates answers based on context using OpenAI’s GPT-3.5-turbo. 🤖🔎

Database Operations: Manages query storage and retrieval with SQLite. 🗄️🔑

🛠️ Requirements
Python 3.7+
Streamlit
PyPDF2
SpeechRecognition
OpenAI
SentenceTransformers
SQLite3
NumPy


Feel free to tweak any sections or add more emojis based on your style and preferences! 🌟
