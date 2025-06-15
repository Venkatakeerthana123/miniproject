SELECT 
    Region,
    AVG(PJME_MW) AS Regional_Avg_Load
FROM energy
GROUP BY Region;
