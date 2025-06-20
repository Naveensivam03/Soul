from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
import uuid
from datetime import datetime
from embeddings import get_embedding

#path to the old database i mean chroma
PATH = './chroma'

#path to the summary chroma
PATH_SUMM = './chroma_sum'


#current date 
curr_date = datetime.now()

def get_datas():
    #load the db
    db = Chroma(persist_directory = PATH , embedding_function = get_embedding())

    #retrive all the docs from the db
    all_docs = db.get()
    ids = all_docs['chunk_id']
    metadatas = all_docs['metadata']
    documents = all_docs["documents"]

    #filter by date
    iltered_chunks = [
        doc for doc, meta in zip(documents, metadatas)
        if meta and "timestamp" in meta and meta["timestamp"].startswith(curr_date)
    ]

    # Merge into one paragraph
    full_paragraph = " ".join(chunk.strip() for chunk in filtered_chunks if chunk.strip())
    return full_paragraph


#load that into the ai model for summary and load that result back by converting that into the embeddings into a new path.
