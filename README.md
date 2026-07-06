# SQL Clause Fixer

A small AI agent that takes a syntactically out-of-order SQL query (e.g. clauses like `LIMIT`, `WHERE`, `ORDER BY` in the wrong sequence) and returns the correctly ordered version, using an LLM with structured output parsing.

## What it does

Given something like:

```
SELECT * WHERE age > 21 LIMIT 10 FROM users ORDER BY created_at DESC
```

The agent reorders the clauses into valid SQL syntax and returns:
- The corrected, properly ordered query
- A list of the clauses in their correct sequence

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
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
python fixer.py
```

Enter a SQL query when prompted, and the agent will return the corrected version. Type `quit` to exit.

## Example

```
Enter your SQL query (or 'quit' to exit): SELECT * WHERE age > 21 LIMIT 10 FROM users ORDER BY created_at DESC
Corrected Query: SELECT * FROM users WHERE age > 21 ORDER BY created_at DESC LIMIT 10
Ordered List Components: ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'LIMIT']
```

## Notes

- Swapping LLM providers only requires changing the model import/init in `fixer.py`; the prompt, schema, and parsing logic stay the same.
- Free-tier rate limits apply depending on the provider used.