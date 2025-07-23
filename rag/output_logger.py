"""
Simple Output Logger for Soul Project
Writes debug outputs to separate log files
"""

import os
from datetime import datetime

# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_to_file(filename, content):
    """Write content to a log file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join(LOG_DIR, filename)
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}]\n")
        f.write(str(content))
        f.write("\n" + "="*80 + "\n")

def log_chroma_retrieval(user_input, retrieved_chunks, num_results):
    """Log Chroma database retrieval results"""
    content = f"""USER INPUT: {user_input}
RESULTS FOUND: {num_results}
RETRIEVED CHUNKS:
{retrieved_chunks}"""
    log_to_file("chroma_retrieval.log", content)

def log_valkey_operation(operation, key, value=None, result=None):
    """Log Valkey cache operations"""
    content = f"""OPERATION: {operation}
KEY: {key}"""
    if value:
        content += f"\nVALUE: {value}"
    if result:
        content += f"\nRESULT: {result}"
    log_to_file("valkey_cache.log", content)

def log_database_storage(chunk_id, timestamp, content):
    """Log database storage operations"""
    log_content = f"""CHUNK ID: {chunk_id}
TIMESTAMP: {timestamp}
STORED CONTENT: {content}"""
    log_to_file("database_operations.log", log_content)

def log_ai_interaction(user_input, ai_response):
    """Log AI interactions"""
    content = f"""USER: {user_input}
ANIMA: {ai_response}"""
    log_to_file("ai_interactions.log", content)

def log_embeddings(model_name, input_text):
    """Log embedding generation"""
    content = f"""MODEL: {model_name}
INPUT: {input_text[:200]}..."""
    log_to_file("embeddings.log", content)
