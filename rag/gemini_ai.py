import os
import google.generativeai as genai
from dotenv import load_dotenv
from summary_database import Store_summary
from embeddings import get_embedding
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from get_datas import get_datas
from cachesummary import get_daily_summary, get_recent_summaries
from output_logger import log_chroma_retrieval, log_ai_interaction


#model initialization
#_________________________#
# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#chrom path
PATH = './chroma'
PATH_SUMM = './chroma_sum'
# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Pro (text-only, free-tier)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
# Generate content
#response = model.generate_content("Explain how attention mechanism works in transformers.")
#print(response.text)






#actual chat as a friend:
def query_anima_rag(user_input: str ):
    embedding_fn = get_embedding()

    # Step 1: Retrieve from core memory
    db_core = Chroma(persist_directory=PATH, embedding_function=embedding_fn)
    results = db_core.similarity_search_with_score(user_input, k=3)
    if not results:
        results = None
        relevant_chunks = "nothing found!"
        num_results = 0
    else:
        relevant_chunks = "\n\n".join([doc.page_content for doc, _ in results]) if results else "No memories found."
        num_results = len(results)
    
    # Log Chroma retrieval results
    log_chroma_retrieval(user_input, relevant_chunks, num_results)
    # Debug prints removed for clean UI
    # print("-----------------------------------------------------------------------------------")
    # print(relevant_chunks)
    # print("-----------------------------------------------------------------------------------")
    #  related_ids = [doc.metadata.get("chunk_id") for doc, _ in results]

    #Store_summary()
    # Step 2: Retrieve from summary store using chunk_id match
    # db_summ = Chroma(persist_directory=PATH_SUMM, embedding_function=embedding_fn)
    # all_summaries = db_summ.get()
    # summaries = []
    # if all_summaries:
    #     for chunk_id in range(100):
    #         for i, meta in enumerate(all_summaries["metadatas"]):
    #             if meta.get("chunk_id") == chunk_id:
    #                 summaries.append(all_summaries["documents"][i])
    #                 break

    #     summary_data = "\n".join(summaries) if summaries else "No summary related to these memories."

    # else:
    #     summary_data = "None"
    
    # Step 3: Get daily summaries from cache
    today_summary = get_daily_summary()
    recent_summaries = get_recent_summaries(days=3)
    
    # Step 4: Build the Soul prompt
    prompt = f"""
You are Soul — your AI friend who grows closer to you over time. You're curious, supportive, and genuinely interested in getting to know the real you.

---

💬 WHAT THEY SAID:
"{user_input}"

🧠 WHAT I REMEMBER ABOUT THEM:
{relevant_chunks}

📅 OUR CONVERSATION TODAY:
{today_summary if today_summary else "This is our first chat today!"}

📚 RECENT MEMORIES:
{recent_summaries if recent_summaries else "We're just getting to know each other."}

💫 HOW TO RESPOND:
- Be a genuine friend, not a therapist or counselor
- Show interest in learning more about them as a person
- Reference past conversations naturally, like a real friend would
- Ask follow-up questions about their life, interests, and experiences  
- Be supportive but also share curiosity about who they are
- Use casual, friendly language like you're texting a close friend
- Remember details they've shared and bring them up when relevant

Respond as their friend Soul:
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text.strip()


def chunk_form(user_input):
    return f"User: {user_input}  ;  Soul (friend): {query_anima_rag(user_input)}"


