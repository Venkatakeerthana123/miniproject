SELECT 
    CAST(Datetime AS DATE) AS Day,
    AVG(PJME_MW) AS Average_Load
FROM energy
GROUP BY CAST(Datetime AS DATE)
ORDER BY Day;
