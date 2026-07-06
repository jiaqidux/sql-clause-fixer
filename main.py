import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import OrderedSQL

load_dotenv()

# initialize the model and the parser
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
structured_model = model.with_structured_output(OrderedSQL)

# prompt template design
system_prompt = """
You are a strict SQL compiler syntax validator.
The user will give you an incorrect SQL query where the basic clauses (SELECT, FROM, WHERE, etc)
are written out of order. 
Your job is to reorder the clauses into the sintactically correct sequence.

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Fix the order of this query: {incorrect_query}")
])

sql_fixer = prompt | structured_model

# to run
while True:
    try:
        incorrect_input = input("Enter your SQL query (or 'quit' to exit): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        break

    if incorrect_input.lower() == "quit":
        break
    if not incorrect_input:
        continue

    try:
        result = sql_fixer.invoke({"incorrect_query": incorrect_input})
        print(f"Corrected Query: {result.corrected_query}")
        print(f"Ordered List Components: {result.ordered_clauses}\n")
    except Exception as e:
        print(f"Something went wrong while fixing the query: {e}\n")

