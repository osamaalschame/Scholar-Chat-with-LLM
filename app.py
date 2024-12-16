GOOGLE_API_KEY = "YOUR KEY"
model_name = "MODEL NAME"
# Import necessary libraries
import os, re
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from flask import Flask, render_template, request, redirect
from PyPDF2 import PdfReader

#Please install PdfReader
from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PyPDFLoader

from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


#os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

#Using this folder for storing the uploaded docs. Creates the folder at runtime if not present
DATA_DIR = "__data__"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

#Flask App
app = Flask(__name__)

vectorstore = None
conversation_chain = None
chat_history = []

class HumanMessage:
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return f'HumanMessage(content={self.content})'

class AIMessage:
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return f'AIMessage(content={self.content})'


def read_docs(pdf_docs):
    documents = []

    for pdf in pdf_docs:
        filename = os.path.join(DATA_DIR, pdf.filename)

        try:
            # Save the uploaded file to the temporary directory
            pdf.save(filename)

            # Load the PDF using PyPDFLoader
            loader = PyPDFLoader(filename)
            documents.extend(loader.load())

        except Exception as e:
            # Log an error and skip the problematic file
            print(f"Skipping {pdf.filename} due to error: {e}")

        finally:
            # Optionally clean up the temporary file
            if os.path.exists(filename):
                os.remove(filename)

    return documents


def get_text_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = ChatGoogleGenerativeAI(model=model_name, api_key=GOOGLE_API_KEY)

    vc = vectorstore.as_retriever()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
        memory=memory
    )
    return conversation_chain


@app.route('/')
def home():
    return render_template('new_home.html')


@app.route('/process', methods=['POST'])
def process_documents():
    global vectorstore, conversation_chain
    pdf_docs = request.files.getlist('pdf_docs')
    raw_text = read_docs(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)
    return redirect('/chat')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global vectorstore, conversation_chain, chat_history
    msgs = []
    
    if request.method == 'POST':
        user_question = request.form['user_question']
        
        response = conversation_chain.invoke({'question': user_question})
        chat_history = response['chat_history']
        
    return render_template('new_chat.html', chat_history=chat_history)

@app.route('/pdf_chat', methods=['GET', 'POST'])
def pdf_chat():
    return render_template('new_pdf_chat.html')



if __name__ == '__main__':
    app.run(debug=True)
