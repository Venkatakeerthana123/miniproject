SELECT 
    Device_Type,
    CAST(Datetime AS DATE) AS Day,
    SUM(PJME_MW) AS Total_Load
FROM energy
GROUP BY Device_Type, CAST(Datetime AS DATE)
ORDER BY Device_Type, Day;
