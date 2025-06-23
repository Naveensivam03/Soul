from gemini_ai import *
from database import *
from summary_database import *


#get the input from the user
user_input = input("Enter you message: ")


#provide to the ai
results = query_anima_rag(user_input)
input_text = chunk_form(user_input)
store_into_database(input_text)
print(results)
