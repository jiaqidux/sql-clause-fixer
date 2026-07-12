import sqlglot
from sqlglot.errors import ParseError
from main import sql_fixer

TEST_CASES = [
    "SELECT * WHERE age > 21 LIMIT 10 FROM users ORDER BY created_at DESC",
    "FROM users SELECT name WHERE id = 1",
    "SELECT name, age FROM users LIMIT 5 WHERE age > 30",
    "ORDER BY name SELECT * FROM employees",
    "SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5 WHERE salary > 50000",
    "SELECT users.name, orders.total FROM users WHERE orders.total > 100 JOIN orders ON users.id = orders.user_id",
    "LIMIT 20 SELECT * FROM products ORDER BY price WHERE price > 10",
    # already-correct query, to confirm the fixer doesn't break valid input
    "SELECT name, email FROM users WHERE active = 1 ORDER BY name LIMIT 25",
    "SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY name LIMIT 10 GROUP BY name",
    # a subquery whose own clauses are scrambled, not just the outer query
    "SELECT name FROM employees WHERE salary > (WHERE department = 'Sales' SELECT AVG(salary) FROM employees) ORDER BY name",
]

# canonical clause order the ordered_clauses list should respect
CANONICAL_ORDER = ["SELECT", "FROM", "JOIN", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]


def run_fixer():
    parse_failures = []
    order_failures = []
    exceptions = []

    for query in TEST_CASES:
        try:
            result = sql_fixer.invoke({"incorrect_query": query})
        except Exception as e:
            exceptions.append((query, str(e)))
            continue

        # to check if the corrected query actually parse as valid SQL
        try:
            sqlglot.parse_one(result.corrected_query)
        except ParseError as e:
            parse_failures.append((query, result.corrected_query, str(e)))

        # to check whether the returned clauses are in ascending order
        positions = [CANONICAL_ORDER.index(c) for c in result.ordered_clauses if c in CANONICAL_ORDER]
        if positions != sorted(positions):
            order_failures.append((query, result.ordered_clauses))

    total = len(TEST_CASES)
    passed = total - len(parse_failures) - len(order_failures) - len(exceptions)

    print(f"\nSQL Clause Fixer: Validation Test")
    print(f"Total test cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed (invalid SQL produced): {len(parse_failures)}")
    print(f"Failed (clause order incorrect): {len(order_failures)}")
    print(f"Failed (exception raised): {len(exceptions)}")

    if parse_failures:
        print(f"\nInvalid SQL produced")
        for original, corrected, error in parse_failures:
            print(f"Input:     {original}")
            print(f"Output:    {corrected}")
            print(f"Error:     {error}\n")

    if order_failures:
        print(f"\nClause order incorrect")
        for original, clauses in order_failures:
            print(f"Input:     {original}")
            print(f"Clauses:   {clauses}\n")

    if exceptions:
        print(f"\nExceptions raised")
        for original, error in exceptions:
            print(f"Input:     {original}")
            print(f"Error:     {error}\n")

    return passed, total


if __name__ == "__main__":
    run_fixer()