from langchain.embeddings import HuggingFaceEmbeddings



#embedding function
def get_embedding():
    return HuggingFaceEmbeddings(model_name="thenlper/gte-small")


