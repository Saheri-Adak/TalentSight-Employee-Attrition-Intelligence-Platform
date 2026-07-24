-- Query 1: Income percentile within job role and level

WITH IncomePercentiles AS (
    SELECT
        "JobRole",
        "JobLevel",
        "MonthlyIncome",
        NTILE(4) OVER (
            PARTITION BY "JobRole", "JobLevel"
            ORDER BY "MonthlyIncome"
        ) AS "IncomePercentile"
    FROM employee_master
),

MarketPositions AS (
    SELECT
        "JobRole",
        "JobLevel",
        "MonthlyIncome",
        "IncomePercentile",
        CASE
            WHEN "IncomePercentile" = 1 THEN 'Below Market'
            WHEN "IncomePercentile" = 2 THEN 'At Market'
            WHEN "IncomePercentile" = 3 THEN 'Above Market'
            WHEN "IncomePercentile" = 4 THEN 'High'
        END AS "MarketPosition"
    FROM IncomePercentiles
)

SELECT
    "JobRole",
    "JobLevel",
    "MonthlyIncome",
    "IncomePercentile",
    "MarketPosition"
FROM MarketPositions
ORDER BY
    "JobRole",
    "JobLevel",
    "MonthlyIncome";

-- Query 2: Employees earning below median for their role

WITH MedianIncome AS (
    SELECT
        "JobRole",
        "JobLevel",
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "MonthlyIncome") AS "MedianIncome"
    FROM employee_master
    GROUP BY "JobRole", "JobLevel"
)
SELECT
    e."JobRole",
    e."JobLevel",
    e."MonthlyIncome",
    m."MedianIncome",
    Case 
        WHEN e."MonthlyIncome" < m."MedianIncome" THEN 'Below Median'
        ELSE 'At or Above Median'
    END AS "IncomeComparison",

    m."MedianIncome"- e."MonthlyIncome" AS "IncomeGap"
FROM employee_master e
JOIN MedianIncome m ON e."JobRole" = m."JobRole" AND e."JobLevel" = m."JobLevel"
ORDER BY
    "IncomeGap" DESC;

-- Query 3: Average income by cluster segment

SELECT 
    "Cluster_Name",
    COUNT(*) AS employee_count,
    ROUND(AVG("MonthlyIncome"), 0) AS avg_income,
    ROUND(MIN("MonthlyIncome"), 0) AS min_income,
    ROUND(MAX("MonthlyIncome"), 0) AS max_income,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS attrited_count
FROM employee_master
GROUP BY "Cluster_Name"
ORDER BY avg_income DESC;
