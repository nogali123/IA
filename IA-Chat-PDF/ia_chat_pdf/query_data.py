# query_data.py

import sqlite3
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from .get_embedding_function import get_embedding_function  # Importando a função de embedding local

CHROMA_PATH = "chroma"
DATABASE_FILE = "responses.db"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context:{question}(Responder em Portugues Brasileiro)
"""

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS corrections
                 (query_text TEXT PRIMARY KEY, correct_response TEXT)''')
    conn.commit()
    conn.close()

def query_rag(query_text: str):
    initialize_database()

    # Check if there is a correct response stored in the database
    correct_response = load_correct_response_from_db(query_text)

    if correct_response:
        return correct_response

    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Consult the model
    model = Ollama(model="Mistral")
    response_text = model.invoke(prompt)

    return response_text

def load_correct_response_from_db(query_text):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT correct_response FROM corrections WHERE query_text = ?', (query_text,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def save_correct_response_to_db(query_text, correct_response):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO corrections (query_text, correct_response) VALUES (?, ?)', (query_text, correct_response))
    conn.commit()
    conn.close()


def query_correct_response(response, query_text):
    save_correct_response_to_db(query_text, response)

