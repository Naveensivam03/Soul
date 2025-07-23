from gemini_ai import *
from database import *
from summary_database import *
from cachesummary import store_daily_summary


#get the input from the user
user_input = input("Enter your message: ")


#provide to the ai
results = query_anima_rag(user_input)
input_text = chunk_form(user_input)

# Store in database
store_into_database(input_text)

# Cache the daily summary
store_daily_summary(input_text)

print(results)
