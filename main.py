import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import OrderedSQL
import sqlglot
from sqlglot.errors import ParseError


load_dotenv()

# initialize the model and the parser
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
structured_model = model.with_structured_output(OrderedSQL)

# prompt template design
system_prompt = """
You are a strict SQL compiler syntax validator.
The user will give you an incorrect SQL query where the basic clauses (SELECT, FROM, WHERE, etc)
are written out of order.
Your job is to reorder the clauses into the syntactically correct sequence.
 
When listing ordered_clauses, only include clauses that are genuinely present in the OUTER,
top-level query. Do not include a clause just because it commonly appears in SQL queries - only
include it if it is actually written in the outer query. Do not include clauses that only appear
inside a subquery in parentheses; those belong to the subquery, not the outer query.

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Fix the order of this query: {incorrect_query}")
])

sql_fixer = prompt | structured_model

# to confirm it's actually valid SQL before telling the user it's correct
def validate_query(query):
    try:
        sqlglot.parse_one(query)
        return True, None
    except ParseError as e:
        return False, str(e)

# to run the tool
if __name__ == "__main__":
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
            is_valid, error = validate_query(result.corrected_query)
 
            print(f"Corrected Query: {result.corrected_query}")
            print(f"Ordered List Components: {result.ordered_clauses}")
 
            if is_valid:
                print("Validation: Query parses as syntactically valid SQL\n")
            else:
                print(f"Validation: WARNING! Corrected query failed to parse: {error}\n")
 
        except Exception as e:
            print(f"Something went wrong while fixing the query: {e}\n")
 

