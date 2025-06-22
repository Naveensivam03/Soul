from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
import uuid
from datetime import datetime , timezone
from embeddings import get_embedding
from summary_ai import summary_para
import document
#path to the old database i mean chroma
PATH = './chroma'





def get_datas():

    #current date 
    curr_date = datetime.now()

    #load the db
    db = Chroma(persist_directory = PATH , embedding_function = get_embedding())

    #retrive all the docs from the db
    all_docs = db.get()
    
    metadatas = all_docs['metadatas']
    documents = all_docs["documents"]

    #filter by date
    filtered_chunks = [
        doc for doc, meta in zip(documents, metadatas)
        if meta and "timestamp" in meta and meta["timestamp"].startswith(curr_date)
    ]

    # Merge into one paragraph
    full_paragraph = " ".join(chunk.strip() for chunk in filtered_chunks if chunk.strip())
    return full_paragraph
