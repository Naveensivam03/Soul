from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from typing import List
import uuid
from datetime import datetime , timezone
from embeddings import get_embedding
# from summary_ai import summary_para
from langchain_core.documents import Document
from get_datas import get_datas
#path to the old database i mean chroma
PATH = './chroma'

#path to the summary chroma
PATH_SUMM = './chroma_sum'




#load that into the ai model for summary and load that result back by converting that into the embeddings into a new path.


def Store_summary():
    #para 
    para = get_datas()
    
    uid = uuid.uuid4()
    # with open("uid.txt","r") as f:
    #     ids = f.readlines()
    #     f.close()
    # while str(uid) in ids:
    #     uid = uuid.uuid4()
    
    #input_text 
    input_text = summary_para(para)
    #metadata to added to the input text
    
    metadata = {
        "chunk_id":str(uid)  ,   #uid for unique to determine the chunk
        "timestamp" : datetime.now(timezone.utc).isoformat()
    }

    #wrap everything in teh document to load it into chroma
    docs = Document(page_content = input_text , metadata = metadata)

    #load the content and change it into embeddings and store it in the database

    db = Chroma(persist_directory = PATH_SUMM , embedding_function = get_embedding())
    db.add_documents([docs])
    db.persist()
    print(f"✅ summary stored chunk (ID: {metadata['chunk_id']}) with timestamp : {metadata['timestamp']}.")


