# Chat Scholar

## Problem Statement:
In today's digital age, students are inundated with information from textbooks, research papers, and online resources. Navigating this vast sea of knowledge and extracting meaningful insights can be overwhelming. Chat Scholar addresses this challenge by providing an AI-powered platform that simplifies academic learning and enhances the writing process.

## Objective:
Chat Scholar has two primary objectives.
1.	Academic Research and Understanding: Chat Scholar provides clear and concise answers, summaries, and explanations tailored to the student's specific questions and the content of their documents.
How it works:
1.	Document Upload and Processing: Users upload PDF documents, and the application extracts the textual content.
2.	Text Embedding and Semantic Search: The extracted text is processed, embeddings are generated, and a semantic search engine (using FAISS) allows for efficient retrieval of relevant information.
3.	Question Answering: Students' questions are processed, compared to the indexed content, and the most relevant information is used to generate a comprehensive answer using the OpenAI LLM.

Key Inputs: 
For this particular project, we would need the below key inputs:
•	Chat Scholar
o	Upload the document (pdf) for which you want chat bot.

## Architecture:


- **Step 1: Data Collection:**
Once the document is uploaded it initiates chat scholar which automatically convert the extract the data from the document and convert the data into small chunks size. 
- **Step 2: Embeddings Generation**
In this stage, textual data is converted into numerical embeddings using advanced techniques. These embeddings capture the semantic relationships within the data, enabling to retrieve and analyze information efficiently
- **Step 3: Query Execution **
Once the processing is done, Chat Scholar uses OpenAI Large Language Model (LLM) to generate the response. Both context and query is passed to the LLM to generate the best possible response.


## USAGE:
## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git https://github.com/osamaalschame/Scholar-Chat-with-LLM.git
cd Scholar-Chat-with-LLM
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables by creating a `.env` file:
```env
GOOGLE_API_KEY=your_api_key_here
model_name=model_name
```
5. Run the application:
```bash
python app.py
```





