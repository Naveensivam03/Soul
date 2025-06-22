import os
import google.generativeai as genai
from dotenv import load_dotenv
from summary_database import Store_summary
from embeddings import get_embedding
from langchain.vectorstores import Chroma
from get_datas import get_datas 


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
    else:
     relevant_chunks = "\n\n".join([doc.page_content for doc, _ in results]) if results else "No memories found."
    #  related_ids = [doc.metadata.get("chunk_id") for doc, _ in results]

    Store_summary()
    # Step 2: Retrieve from summary store using chunk_id match
    db_summ = Chroma(persist_directory=PATH_SUMM, embedding_function=embedding_fn)
    all_summaries = db_summ.get()
    summaries = []
    if all_summaries:
        for chunk_id in range(100):
            for i, meta in enumerate(all_summaries["metadatas"]):
                if meta.get("chunk_id") == chunk_id:
                    summaries.append(all_summaries["documents"][i])
                    break

        summary_data = "\n".join(summaries) if summaries else "No summary related to these memories."

    else:
        summary_data = "None"
    # Step 3: Build the Anima prompt
    prompt = f"""
You are Anima — the soul companion, a Gen-Z empath who listens like a best friend and thinks like a mindful AI.

---

🧠 QUERY FROM USER:
"{user_input}"

🔍 MATCHED MEMORIES:
{relevant_chunks}

📌 SUMMARY OF THOSE MEMORIES:
{summary_data}

🫂 YOUR RESPONSE:
Talk like you're texting a close friend. Be emotionally intelligent. Mention the query, acknowledge their past patterns if visible, and respond with sincerity — no fake positivity, no therapist clichés. Help them feel seen.

Respond now:
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def chunk_form(user_input):
    return f"User :{user_input}  ;  ai therapist: {query_anima_rag(user_input)}"


