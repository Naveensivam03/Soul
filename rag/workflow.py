from gemini_ai import *
from database import *
from summary_database import *


#get the input from the user
user_input = input("Enter you message: ")
input_text = chunk_form(user_input)

#provide to the ai
results = query_anima_rag(user_input)

store_into_database(results)
print(results)
