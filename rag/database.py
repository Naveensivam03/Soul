#import the necesary requirements
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
import uuid
from datetime import datetime , timezone
from embeddings import get_embedding
from langchain_core.documents import Document
from gemini_ai import chunk_form

#path to your chroma
PATH = "./chroma"

#since the input itself is the chunks
#load input from the whisper;
# user_input = "" #sample input from teh user through whisper.
# input_text = chunk_form(user_input)

def store_into_database(input_text):
    #store the unique id within the text file for current multiple time running:
    uid = uuid.uuid4()
    with open("uid.txt","r") as f:
        ids = f.readlines()
        f.close()
    while str(uid) in ids:
        uid = uuid.uuid4()
    
    #metadata to added to the input text
    
    metadata = {
        "chunk_id":str(uid)  ,   #uid for unique to determine the chunk
        "timestamp" : datetime.now(timezone.utc).isoformat()
    }

    #wrap everything in teh document to load it into chroma
    docs = Document(page_content = input_text , metadata = metadata)

    #load the content and change it into embeddings and store it in the database

    db = Chroma(persist_directory = PATH , embedding_function = get_embedding())
    db.add_documents([docs])
    db.persist()
    print(f"✅ Stored chunk (ID: {metadata['chunk_id']}) with timestamp : {metadata['timestamp']}.")



#