# 📊 SQL Interview Prep Sheet — Ramish

> For product companies and BFSI GCCs targeting 14-18 LPA
> Focus: what mid-level Java devs get asked about SQL

---

## 1. JOINs — Must Know

### Types of JOINs
| JOIN | Returns | Use Case |
|------|---------|----------|
| INNER JOIN | Matching rows from both | Most common — get related data |
| LEFT JOIN | All left + matching right | Find left rows even if no match |
| RIGHT JOIN | All right + matching left | Less common, but know it |
| FULL OUTER JOIN | All rows from both | Find unmatched on both sides |
| CROSS JOIN | Cartesian product | Generate combinations |
| SELF JOIN | Table joined to itself | Hierarchies (employee→manager) |

### Practice Queries
```sql
-- Employees and their departments
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- Employees with no department (LEFT JOIN + NULL filter)
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
WHERE d.id IS NULL;

-- Manager hierarchy (self-join)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### ⚡ Common Interview Question
"Find the second highest salary in each department."
```sql
SELECT dept_id, salary
FROM (
    SELECT emp_id, dept_id, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;
```

---

## 2. Window Functions — Must Know

These separate mid-level from junior. Know them cold.

| Function | What it does | Example |
|----------|-------------|---------|
| ROW_NUMBER() | Unique sequential number | Rank rows 1,2,3... |
| RANK() | Rank with gaps on ties | 1,1,3,4... |
| DENSE_RANK() | Rank without gaps | 1,1,2,3... |
| LAG() | Previous row's value | Compare to previous |
| LEAD() | Next row's value | Compare to next |
| SUM() OVER() | Running total | Cumulative sum |
| AVG() OVER() | Running average | Moving average |
| FIRST_VALUE() | First value in partition | Get earliest record |
| NTILE(n) | Divide into n buckets | Quartiles, percentiles |

### Practice Queries
```sql
-- Running total of transactions per account
SELECT account_id, txn_date, amount,
       SUM(amount) OVER (PARTITION BY account_id ORDER BY txn_date) AS running_total
FROM transactions;

-- Compare each transaction to previous
SELECT account_id, txn_date, amount,
       LAG(amount, 1) OVER (PARTITION BY account_id ORDER BY txn_date) AS prev_amount,
       amount - LAG(amount, 1) OVER (PARTITION BY account_id ORDER BY txn_date) AS diff
FROM transactions;

-- Top 3 highest paid employees per department
SELECT * FROM (
    SELECT emp_name, dept_id, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk <= 3;

-- Year-over-year growth
SELECT year, revenue,
       LAG(revenue, 1) OVER (ORDER BY year) AS prev_year_revenue,
       ROUND((revenue - LAG(revenue, 1) OVER (ORDER BY year)) * 100.0 /
             LAG(revenue, 1) OVER (ORDER BY year), 2) AS yoy_growth_pct
FROM yearly_revenue;
```

### ⚡ Common Interview Question
"Find employees who earn more than their department average."
```sql
SELECT emp_name, dept_id, salary
FROM (
    SELECT emp_name, dept_id, salary,
           AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
    FROM employees
) t
WHERE salary > dept_avg;
```

---

## 3. GROUP BY & Aggregation — Must Know

```sql
-- Department-wise employee count and avg salary
SELECT dept_id,
       COUNT(*) AS emp_count,
       AVG(salary) AS avg_salary,
       MAX(salary) AS max_salary,
       MIN(salary) AS min_salary
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;
```

### Key Rules
- `WHERE` filters BEFORE grouping, `HAVING` filters AFTER
- Non-aggregated columns in SELECT must appear in GROUP BY
- `COUNT(*)` counts rows; `COUNT(column)` counts non-null values
- `COUNT(DISTINCT column)` counts unique non-null values

### ⚡ Common Interview Question
"Find departments with more than 3 employees earning above 50k."
```sql
SELECT dept_id, COUNT(*) AS high_earner_count
FROM employees
WHERE salary > 50000
GROUP BY dept_id
HAVING COUNT(*) > 3;
```

---

## 4. Subqueries vs CTEs — Must Know

### Subquery
```sql
SELECT emp_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### CTE (Common Table Expression) — Preferred for readability
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT e.emp_name, e.salary, d.avg_sal
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_sal;
```

### Recursive CTE — Know the concept
```sql
-- Find all subordinates of a manager (org hierarchy)
WITH RECURSIVE org_chain AS (
    SELECT emp_id, emp_name, manager_id, 1 AS level
    FROM employees
    WHERE emp_id = 1  -- start from CEO
    UNION ALL
    SELECT e.emp_id, e.emp_name, e.manager_id, o.level + 1
    FROM employees e
    JOIN org_chain o ON e.manager_id = o.emp_id
)
SELECT * FROM org_chain ORDER BY level;
```

### ⚡ Correlated vs Non-correlated Subquery
- **Non-correlated:** Runs once, independent of outer query. `(SELECT AVG(salary) FROM employees)`
- **Correlated:** Runs for each row of outer query. `WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id)`
- Correlated subqueries are slower — know when to convert to a JOIN.

---

## 5. Indexing — Must Know (for interviews, not just queries)

### Types
| Index | When to use |
|-------|------------|
| B-Tree (default) | Equality + range queries, sorting |
| Hash | Equality only (no range) |
| Composite | Multiple column filters |
| Partial (WHERE) | Index subset of rows |
| Unique | Enforce uniqueness + lookup |

### When to Index
- Columns in WHERE clauses (high selectivity)
- Columns used in JOIN conditions
- Columns in ORDER BY / GROUP BY
- Foreign keys (often auto-indexed in PostgreSQL, NOT in MySQL)

### When NOT to Index
- Low selectivity (gender, boolean)
- Tables with heavy writes, light reads
- Small tables (scan is faster than index lookup)

### ⚡ Common Interview Question
"What's the difference between a clustered and non-clustered index?"
- **Clustered:** Determines physical order of rows. One per table. Leaf nodes = actual data.
- **Non-clustered:** Separate structure pointing to rows. Multiple per table. Leaf nodes = pointers.

### EXPLAIN / EXPLAIN ANALYZE
```sql
-- Always analyze slow queries
EXPLAIN ANALYZE
SELECT * FROM transactions
WHERE account_id = 123 AND txn_date >= '2026-01-01';

-- Look for:
-- - Seq Scan (bad on large tables — needs index)
-- - Index Scan (good)
-- - Bitmap Heap Scan (acceptable)
-- - Nested Loop vs Hash Join (Hash Join is better for large datasets)
```

---

## 6. Normalization & Denormalization — Know the Concepts

### Normal Forms
| NF | Rule | Example |
|----|------|---------|
| 1NF | Atomic values, no repeating groups | Split "phone1,phone2" into rows |
| 2NF | 1NF + no partial dependency on composite key | Move non-key attributes to own table |
| 3NF | 2NF + no transitive dependency | Move dept_name to departments table |
| BCNF | 3NF + every determinant is a candidate key | Stricter version of 3NF |

### Denormalization (for read-heavy systems)
- Sometimes you add redundant data for query speed
- Common in data warehouses, reporting systems
- Trade-off: faster reads vs update anomalies + storage

---

## 7. Transactions & Isolation — Must Know (especially for banking!)

### ACID Properties
| Property | Meaning |
|----------|---------|
| Atomicity | All or nothing — rollback on failure |
| Consistency | Valid state before and after |
| Isolation | Concurrent transactions don't interfere |
| Durability | Committed data survives crashes |

### Isolation Levels (PostgreSQL)
| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Use Case |
|-------|-----------|---------------------|--------------|----------|
| READ UNCOMMITTED | Possible | Possible | Possible | Never use in banking |
| READ COMMITTED | No | Possible | Possible | Default (Postgres) |
| REPEATABLE READ | No | No | Possible | Reporting |
| SERIALIZABLE | No | No | No | Financial transactions |

### Key Terms
- **Dirty Read:** Reading uncommitted data from another transaction
- **Non-Repeatable Read:** Same query returns different results within a transaction
- **Phantom Read:** New rows appear/disappear in repeated range queries
- **Deadlock:** Two transactions waiting on each other — DB kills one

### ⚡ Common Interview Question
"How would you handle a money transfer between two accounts?"
```sql
BEGIN;
-- Check source has enough balance
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- Debit source
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
-- Credit destination
UPDATE accounts SET balance = balance + 500 WHERE id = 2;
-- Log the transfer
INSERT INTO transfers (from_id, to_id, amount, created_at)
VALUES (1, 2, 500, NOW());
COMMIT;
-- On error: ROLLBACK;
```

---

## 8. Set Operations — Nice to Have

```sql
-- UNION: combine, remove duplicates
SELECT city FROM customers
UNION
SELECT city FROM suppliers;

-- UNION ALL: combine, keep duplicates (faster)
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;

-- INTERSECT: rows in both
SELECT product_id FROM orders
INTERSECT
SELECT product_id FROM returns;

-- EXCEPT (MINUS in Oracle): rows in first but not second
SELECT product_id FROM orders
EXCEPT
SELECT product_id FROM returns;
```

---

## 9. Performance Tuning Tips — Must Know

1. **Avoid SELECT *** — name your columns (index coverage, network)
2. **Use LIMIT** — don't return millions of rows
3. **Avoid functions on indexed columns** in WHERE — `WHERE LOWER(name) = 'ramish'` skips index
4. **Use EXPLAIN ANALYZE** — profile before optimizing
5. **Batch large INSERTs** — `INSERT ... VALUES (...), (...), (...)` not 1000 single inserts
6. **Use connection pooling** — HikariCP for Spring Boot
7. **Avoid N+1 queries** — use JOIN FETCH or @EntityGraph in JPA
8. **Index foreign keys** — PostgreSQL does automatically, MySQL does NOT
9. **Partition large tables** — by date range for time-series data
10. **Use materialized views** for expensive aggregate queries

---

## 10. Common Interview Questions — Rapid Fire

1. **Difference between WHERE and HAVING?**
   WHERE filters before grouping; HAVING filters after.

2. **Difference between UNION and UNION ALL?**
   UNION removes duplicates (sorts internally); UNION ALL keeps all rows (faster).

3. **What is a trigger? When to use / not use?**
   Auto-runs on INSERT/UPDATE/DELETE. Use for audit logs. Avoid for business logic — hard to debug.

4. **What is a view?**
   Virtual table from a stored query. Use for security (column/row hiding) and simplifying complex queries.

5. **Difference between DELETE, TRUNCATE, DROP?**
   DELETE: row-level, DML, can rollback, fires triggers. TRUNCATE: table-level, DDL, can't rollback in some DBs, faster. DROP: removes table entirely.

6. **What is a stored procedure vs function?**
   Procedure: can modify data, no return value (OUT params). Function: must return a value, can be used in SELECT.

7. **How do you optimize a slow query?**
   EXPLAIN ANALYZE → check for sequential scans → add indexes → rewrite query (avoid subqueries, use JOINs) → consider denormalization → partition table.

8. **What is the difference between RANK() and DENSE_RANK()?**
   RANK: 1,1,3,4 (gaps after ties). DENSE_RANK: 1,1,2,3 (no gaps).

9. **How to find duplicate rows?**
   ```sql
   SELECT email, COUNT(*) as cnt
   FROM users
   GROUP BY email
   HAVING COUNT(*) > 1;
   ```

10. **What is a materialized view?**
    A view whose result is physically stored and refreshed periodically. Faster reads, stale data.

---

## Practice Resources
- **LeetCode SQL 50** — free, 50 problems, medium difficulty
- **SQLZoo** — interactive tutorials
- **HackerRank SQL** — basic to advanced
- **Mode Analytics SQL Tutorial** — free, practical

---

## Self-Assessment Checklist
- [ ] I can write all 4 JOIN types from memory
- [ ] I can use ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD
- [ ] I can explain ACID and all 4 isolation levels
- [ ] I can write a money transfer transaction with proper locking
- [ ] I can read an EXPLAIN ANALYZE output
- [ ] I know when to use an index and when not to
- [ ] I can write CTEs and recursive CTEs
- [ ] I can find duplicates, second-highest salary, top-N per group
