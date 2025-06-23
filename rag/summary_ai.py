import os
import google.generativeai as genai
from dotenv import load_dotenv
from embeddings import get_embedding
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Pro (text-only, free-tier)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

#for summary of the paragraph and send back 


# def summary_para(para):
#     prompt = f'''
#         Act as a world-class expert in both mental therapy and summarization. 
#         Read the entire input carefully. Then, generate a single summary of no more than 50 words, 
#         capturing all core insights, emotional depth, and key points without omitting anything essential. 
#         Output only the summary, with no preambles, labels, or extra text.

#         and the para is "{para}
#             '''
#     response = model.generate_content(prompt)
#     res_text = response.text
#     return res_text


