# simple AI agent to order the basic clauses of a SQL query
from pydantic import BaseModel, Field
from typing import List, Optional

class OrderedSQL(BaseModel):
    ordered_clauses: List[str] = Field(description=(
        "The clauses that actually appear in the OUTER/top-level query, in their correct order. "
        "Only include a clause name if it is genuinely present in the outer query. Do not include "
        "clauses that only appear inside a subquery, and do not include clauses that aren't present "
        "at all. Valid clause names: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT."
    ))
    corrected_query: str = Field(description="The SQL query with the proper syntax and styling")