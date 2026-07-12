# SQL Clause Fixer

A small LLM-powered tool that takes a syntactically out-of-order SQL query (e.g. clauses like `LIMIT`, `WHERE`, `ORDER BY` in the wrong sequence) and returns the correctly ordered version, using an LLM with structured output parsing. The corrected query is also validated with sqlglot before being returned, so the tool doesn't just trust the model's output blindly.

## What it does

Given something like:

```
SELECT * WHERE age > 21 LIMIT 10 FROM users ORDER BY created_at DESC
```

The agent reorders the clauses into valid SQL syntax and returns:
- The corrected, properly ordered query
- A list of the clauses in their correct sequence
- Whether the corrected query actually parses as valid SQL, checked with `sqlglot`

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   git clone https://github.com/jiaqidux/sql-clause-fixer.git
   cd sql-clause-fixer
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free API key from [Groq](https://console.groq.com/keys) and add it to a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_key
   ```

## Usage

Run the script:

```bash
python main.py
```

Enter a SQL query when prompted, and the agent will return the corrected version, along with whether it passed validation. Type `quit` to exit.

## Project structure
```
sql-clause-fixer/
├── main.py
├── schema.py
├── test_fixer.py
├── requirements.txt
├── .env
└── .gitignore
```

## Validation
 
To check that the fixer actually works (not just on easy cases, but on harder ones too) `test_fixer.py` runs it against 10 test queries covering missing JOINs, multiple misplaced clauses, aggregate queries with GROUP BY/HAVING, and subqueries (including a subquery whose own clauses are scrambled, not just the outer query). Each result is checked two ways: whether the corrected query parse as valid SQL with `sqlglot`, and if the reported clauses are actually in the right order.
 
```bash
python test_fixer.py
```
 
**Results (example run):**
 
```text
Total test cases: 10
Passed: 10
Failed (invalid SQL produced): 0
Failed (clause order incorrect): 0
Failed (exception raised): 0
```
 
One thing worth being clear about: this checks that the output is syntactically valid SQL with clauses in the correct order, not that the query's meaning was preserved exactly (e.g. column names or conditions weren't accidentally altered). Verifying that would need comparing the structure of the input and output more deeply, which this test suite doesn't currently do.

## Example

```
Enter your SQL query (or 'quit' to exit): SELECT * WHERE age > 21 LIMIT 10 FROM users ORDER BY created_at DESC
Corrected Query: SELECT * FROM users WHERE age > 21 ORDER BY created_at DESC LIMIT 10
Ordered List Components: ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'LIMIT']
Validation: Query parses as syntactically valid SQL
```
## Notes

- Swapping LLM providers only requires changing the model import/init in `main.py`; the prompt, schema, and parsing logic stay the same.
- Free-tier rate limits apply depending on the provider used.
- The `ordered_clauses` field only reports clauses present in the outer, top-level query, clauses inside a subquery aren't included separately, since the schema represents a flat list rather than a nested structure.
