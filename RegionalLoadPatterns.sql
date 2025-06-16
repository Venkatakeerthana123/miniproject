SELECT 
    Region,
    CAST(Datetime AS DATE) AS Day,
    SUM(PJME_MW) AS Total_Load
FROM energy
GROUP BY Region, CAST(Datetime AS DATE)
ORDER BY Region, Day;
