from valkey import Valkey
from datetime import datetime, timedelta
from output_logger import log_valkey_operation

# Initialize the Valkey client
valkey_client = Valkey()

def store_daily_summary(input_text: str):
    """Store daily summary in Valkey cache keyed by date"""
    # Create a key based on the current date
    date_key = datetime.now().strftime("%Y-%m-%d")
    
    # Get existing summary for today (if any)
    existing_summary = valkey_client.get(date_key)
    
    if existing_summary:
        # Append to existing summary
        existing_summary = existing_summary.decode('utf-8')
        combined_summary = existing_summary + "\n" + input_text
        valkey_client.set(date_key, combined_summary)
        log_valkey_operation("UPDATE", date_key, combined_summary, "SUCCESS")
    else:
        # Store new summary for today
        valkey_client.set(date_key, input_text)
        log_valkey_operation("CREATE", date_key, input_text, "SUCCESS")

def get_daily_summary(date_str: str = None):
    """Retrieve daily summary from cache"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    summary = valkey_client.get(date_str)
    if summary:
        return summary.decode('utf-8')
    else:
        return None

def get_recent_summaries(days: int = 3):
    """Get summaries from the last N days"""
    summaries = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        summary = get_daily_summary(date_str)
        if summary:
            summaries.append(f"[{date_str}]: {summary}")
    return "\n\n".join(summaries)
