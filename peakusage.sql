SELECT 
    DATEPART(HOUR, Datetime) AS Hour,
    MAX(PJME_MW) AS Peak_Load
FROM energy
GROUP BY DATEPART(HOUR, Datetime)
ORDER BY Peak_Load DESC;
