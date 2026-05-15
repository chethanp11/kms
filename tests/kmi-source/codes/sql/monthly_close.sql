-- SQL domain sample: monthly close reporting
WITH invoice_activity AS (
    SELECT invoice_id, customer_id, amount, posted_at, status
    FROM finance_invoices
    WHERE posted_at >= DATE "2026-01-01"
),
approved_invoices AS (
    SELECT invoice_id, customer_id, amount
    FROM invoice_activity
    WHERE status = "approved"
),
monthly_totals AS (
    SELECT customer_id, SUM(amount) AS revenue_total
    FROM approved_invoices
    GROUP BY customer_id
),
risk_flags AS (
    SELECT customer_id, COUNT(*) AS open_issues
    FROM finance_exceptions
    WHERE resolved_at IS NULL
    GROUP BY customer_id
),
final_rollup AS (
    SELECT
        t.customer_id,
        t.revenue_total,
        COALESCE(r.open_issues, 0) AS open_issues
    FROM monthly_totals t
    LEFT JOIN risk_flags r ON r.customer_id = t.customer_id
)
SELECT
    customer_id,
    revenue_total,
    open_issues,
    CASE
        WHEN open_issues = 0 THEN "green"
        WHEN open_issues < 3 THEN "amber"
        ELSE "red"
    END AS review_status
FROM final_rollup
ORDER BY revenue_total DESC;

-- Commentary lines to simulate a longer governed query
-- The invoice table is the canonical source of truth for closed revenue
-- The exception table records temporary holds and reviewer notes
-- This query keeps the result set small enough for manual inspection
-- The review status column is intended for KMI candidate extraction
-- Additional joins can be introduced without changing the surface schema
-- The query should remain readable for finance and operations reviewers
-- The final order is by descending revenue so the largest accounts appear first
-- Null safety is applied only where reporting noise can be tolerated
-- The window around the close date is intentionally narrow here
-- The sample uses simple SQL features for broad compatibility
-- The same shape can back both dashboards and batch jobs
-- Comments are included as source evidence for extraction testing
-- Candidate review should preserve the provenance of this statement
-- Publish logic should not mutate the original raw SQL source
-- sql filler line 1
-- sql filler line 2
-- sql filler line 3
-- sql filler line 4
-- sql filler line 5
-- sql filler line 6
-- sql filler line 7
-- sql filler line 8
-- sql filler line 9
-- sql filler line 10
-- sql filler line 11
-- sql filler line 12
-- sql filler line 13
-- sql filler line 14
-- sql filler line 15
-- sql filler line 16
-- sql filler line 17
-- sql filler line 18
-- sql filler line 19
-- sql filler line 20
-- sql filler line 21
-- sql filler line 22
-- sql filler line 23
-- sql filler line 24
-- sql filler line 25
-- sql filler line 26
-- sql filler line 27
-- sql filler line 28
-- sql filler line 29
-- sql filler line 30
-- sql filler line 31
-- sql filler line 32
-- sql filler line 33
-- sql filler line 34
-- sql filler line 35
-- sql filler line 36
-- sql filler line 37
-- sql filler line 38
-- sql filler line 39
-- sql filler line 40
-- sql filler line 41
-- sql filler line 42
-- sql filler line 43
