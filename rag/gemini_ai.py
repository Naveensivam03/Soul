import os
import google.generativeai as genai
from dotenv import load_dotenv
from summary_database import get_datas

#model initialization
#_________________________#
# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(Gemini_api=GOOGLE_API_KEY)

# Load Gemini Pro (text-only, free-tier)
model = genai.GenerativeModel("gemini-pro")

# Generate content
#response = model.generate_content("Explain how attention mechanism works in transformers.")
#print(response.text)


#para 
para = get_datas()

#for summary of the paragraph and send back 
def summary_para(para):
    prompt = f'''
        Act as a world-class expert in both mental therapy and summarization. 
        Read the entire input carefully. Then, generate a single summary of no more than 50 words, 
        capturing all core insights, emotional depth, and key points without omitting anything essential. 
        Output only the summary, with no preambles, labels, or extra text.

        and the para is "{para}
            '''
    response = model.generate_content(prompt)
    res_text = response.text




