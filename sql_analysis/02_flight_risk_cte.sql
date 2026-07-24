-- Query 1: Rule-Based Flight Risk Scoring (No ML Required)

WITH risk_scores AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY "Department", "JobRole", "Age") AS employee_id,
        "Department",
        "JobRole",
        "JobLevel",
        "MonthlyIncome",
        "YearsSinceLastPromotion",
        "JobSatisfaction",
        "StockOptionLevel",
        "overtime_month_ratio",
        "Cluster_Name",
        "Attrition",
        -- Score each risk factor
        CASE WHEN overtime_month_ratio > 0.5 THEN 2 ELSE 0 END +
        CASE WHEN "StockOptionLevel" = 0 THEN 2 ELSE 0 END +
        CASE WHEN "MonthlyIncome" < 5000 AND "JobLevel" <= 2 THEN 1 ELSE 0 END +
        CASE WHEN "YearsSinceLastPromotion" >= 3 THEN 1 ELSE 0 END +
        CASE WHEN "JobSatisfaction" <= 2 THEN 1 ELSE 0 END
        AS flight_risk_score
    FROM employee_master
),
flagged_employees AS (
    SELECT *,
        CASE 
            WHEN flight_risk_score >= 5 THEN 'Critical'
            WHEN flight_risk_score >= 3 THEN 'High'
            WHEN flight_risk_score >= 1 THEN 'Medium'
            ELSE 'Low'
        END AS risk_level
    FROM risk_scores
)
SELECT 
    employee_id,
    "Department",
    "JobRole",
    "JobLevel",
    "MonthlyIncome",
    "Cluster_Name",
    flight_risk_score,
    risk_level,
    "Attrition"
FROM flagged_employees
ORDER BY flight_risk_score DESC;

-- Query 2: Department Risk Summary
WITH risk_scores AS (
    SELECT 
        "Department",
        CASE WHEN overtime_month_ratio > 0.5 THEN 2 ELSE 0 END +
        CASE WHEN "StockOptionLevel" = 0 THEN 2 ELSE 0 END +
        CASE WHEN "MonthlyIncome" < 5000 AND "JobLevel" <= 2 THEN 1 ELSE 0 END +
        CASE WHEN "YearsSinceLastPromotion" >= 3 THEN 1 ELSE 0 END +
        CASE WHEN "JobSatisfaction" <= 2 THEN 1 ELSE 0 END
        AS flight_risk_score
    FROM employee_master
),
risk_levels AS (
    SELECT 
        "Department",
        CASE 
            WHEN flight_risk_score >= 5 THEN 'Critical'
            WHEN flight_risk_score >= 3 THEN 'High'
            WHEN flight_risk_score >= 1 THEN 'Medium'
            ELSE 'Low'
        END AS risk_level
    FROM risk_scores
)
SELECT 
    "Department",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN risk_level = 'Critical' THEN 1 ELSE 0 END) AS critical_count,
    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_count,
    SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) AS low_count
FROM risk_levels
GROUP BY "Department"
ORDER BY critical_count DESC;

-- Query 3: Financial Exposure by Risk Level
WITH risk_scores AS (
    SELECT 
        "MonthlyIncome",
        CASE WHEN overtime_month_ratio > 0.5 THEN 2 ELSE 0 END +
        CASE WHEN "StockOptionLevel" = 0 THEN 2 ELSE 0 END +
        CASE WHEN "MonthlyIncome" < 5000 AND "JobLevel" <= 2 THEN 1 ELSE 0 END +
        CASE WHEN "YearsSinceLastPromotion" >= 3 THEN 1 ELSE 0 END +
        CASE WHEN "JobSatisfaction" <= 2 THEN 1 ELSE 0 END
        AS flight_risk_score
    FROM employee_master
),
risk_with_cost AS (
    SELECT 
        flight_risk_score,
        CASE 
            WHEN flight_risk_score >= 5 THEN 'Critical'
            WHEN flight_risk_score >= 3 THEN 'High'
            WHEN flight_risk_score >= 1 THEN 'Medium'
            ELSE 'Low'
        END AS risk_level,
        "MonthlyIncome" * 12 * 1.5 AS replacement_cost
    FROM risk_scores
)
SELECT 
    risk_level,
    COUNT(*) AS employee_count,
    ROUND(AVG(replacement_cost), 0) AS avg_replacement_cost,
    ROUND(SUM(replacement_cost), 0) AS total_financial_exposure
FROM risk_with_cost
GROUP BY risk_level
ORDER BY 
    CASE risk_level 
        WHEN 'Critical' THEN 1 
        WHEN 'High' THEN 2 
        WHEN 'Medium' THEN 3 
        ELSE 4 
    END;