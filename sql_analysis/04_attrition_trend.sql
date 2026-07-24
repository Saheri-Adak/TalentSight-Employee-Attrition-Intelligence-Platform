-- Query 1: Month-over-month quits rate change using LAG()

SELECT 
    "Year",
    "Month",
    "Quits_Rates",
    LAG("Quits_Rates") OVER (ORDER BY "Year", "Month") AS "Previous_Quits_Rates",
    "Quits_Rates" - LAG("Quits_Rates") OVER (ORDER BY "Year", "Month") AS "Quits_Rates_Change",
    CASE
       WHEN "Quits_Rates" - LAG("Quits_Rates") OVER (ORDER BY "Year", "Month") > 0 THEN 'Increase'
       WHEN "Quits_Rates" - LAG("Quits_Rates") OVER (ORDER BY "Year", "Month") < 0 THEN 'Decrease'
       ELSE 'No Change'
    END AS "Change_Trend"
FROM
    bls_monthly;


-- Query 2: Running total of payroll cost over time

WITH MonthlyPayroll AS (
    SELECT
        "Year",
        "Month",
        SUM("TotalCompensation") AS MonthlyCompensation
    FROM payroll
    GROUP BY "Year", "Month"
),
PayrollRunningTotal AS (
    SELECT
        "Year",
        "Month",
        MonthlyCompensation,
        SUM(MonthlyCompensation) OVER (
            ORDER BY "Year", "Month"
        ) AS Cumulative_total_compensation
    FROM MonthlyPayroll
)

SELECT *
FROM PayrollRunningTotal;

-- Query 3: Salary Growth Ranking per Employee

WITH first_salary AS (
    SELECT
        "EmployeeNumber",
        "EmployeeName",
        "BaseSalary" AS first_base_salary,
        ROW_NUMBER() OVER (
            PARTITION BY "EmployeeNumber"
            ORDER BY "Year", "Month"
        ) AS rn
    FROM payroll
),

last_salary AS (
    SELECT
        "EmployeeNumber",
        "EmployeeName",
        "BaseSalary" AS last_base_salary,
        ROW_NUMBER() OVER (
            PARTITION BY "EmployeeNumber"
            ORDER BY "Year" DESC, "Month" DESC
        ) AS rn
    FROM payroll
),

salary_growth AS (
    SELECT
        f."EmployeeNumber",
        f."EmployeeName",
        f.first_base_salary,
        l.last_base_salary,
        ROUND(
            (
                (l.last_base_salary - f.first_base_salary) * 100.0
                / f.first_base_salary
            )::numeric,
            2
        ) AS growth_rate_pct
    FROM first_salary f
    JOIN last_salary l
        ON f."EmployeeNumber" = l."EmployeeNumber"
    WHERE f.rn = 1
      AND l.rn = 1
)

SELECT
    "EmployeeNumber",
    "EmployeeName",
    first_base_salary,
    last_base_salary,
    growth_rate_pct,
    RANK() OVER (ORDER BY growth_rate_pct DESC) AS salary_growth_rank
FROM salary_growth
ORDER BY salary_growth_rank;