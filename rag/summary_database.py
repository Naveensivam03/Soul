from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
import uuid
from datetime import datetime , timezone
from embeddings import get_embedding
from gemini_ai import summary_para
import document
#path to the old database i mean chroma
PATH = './chroma'

#path to the summary chroma
PATH_SUMM = './chroma_sum'



def get_datas():

    #current date 
    curr_date = datetime.now()

    #load the db
    db = Chroma(persist_directory = PATH , embedding_function = get_embedding())

    #retrive all the docs from the db
    all_docs = db.get()
    ids = all_docs['chunk_id']
    metadatas = all_docs['metadata']
    documents = all_docs["documents"]

    #filter by date
    filtered_chunks = [
        doc for doc, meta in zip(documents, metadatas)
        if meta and "timestamp" in meta and meta["timestamp"].startswith(curr_date)
    ]

    # Merge into one paragraph
    full_paragraph = " ".join(chunk.strip() for chunk in filtered_chunks if chunk.strip())
    return full_paragraph


#load that into the ai model for summary and load that result back by converting that into the embeddings into a new path.


def Store_summary():
    uid = uuid.uuid4()
    with open("uid.txt","r") as f:
        ids = f.readlines()
        f.close()
    while str(uid) in ids:
        uid = uuid.uuid4()
    
    #input_text 
    input_text = summary_para()
    #metadata to added to the input text
    
    metadata = {
        "chunk_id ":str(uid)  ,   #uid for unique to determine the chunk
        "timestamp" : datetime.now(timezone.utc).isoformat()
    }

    #wrap everything in teh document to load it into chroma
    docs = document(page_content = input_text , metadata = metadata)

    #load the content and change it into embeddings and store it in the database

    db = Chroma(persist_directory = PATH_SUMM , embedding_function = get_embedding())
    db.add_document([docs])
    db.persist()
    print(f"✅ summary stored chunk (ID: {metadata['chunk_id']}) with timestamp : {metadata['timestamp']}.")


