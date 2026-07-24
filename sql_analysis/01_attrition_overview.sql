-- Query 1: Overall Attrition Summary
SELECT 
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS attrition_rate_pct
FROM employee_master;


-- Query 2: Attrition rate by department
SELECT 
    "Department",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS attrition_rate_pct
from employee_master
GROUP BY "Department";

-- Query 3: Attrition rate by job level
SELECT 
    "JobLevel",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS attrition_rate_pct
from employee_master
GROUP BY "JobLevel"
ORDER BY "JobLevel";

-- Query 4: Attrition rate by cluster segment
SELECT 
    "Cluster_Name",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(
        SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS attrition_rate_pct
from employee_master
GROUP BY "Cluster_Name";
