# Simple AI agent to order the basic clauses of a SQL query
from pydantic import BaseModel, Field
from typing import List, Optional

class OrderedSQL(BaseModel):
    ordered_clauses: List[str] = Field(description="The SQL clauses sorted in the correct order: " \
    "SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT.")
    corrected_query: str = Field(description="The SQL query with the proper syntax and styling")
    
