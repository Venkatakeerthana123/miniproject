WITH Numbered AS (
    SELECT 
        *,
        'Region' + CAST(ROW_NUMBER() OVER (ORDER BY Datetime) AS VARCHAR) AS Region
    FROM energy
)
SELECT 
    Region,
    AVG(PJME_MW) AS Avg_Regional_Load
FROM Numbered
GROUP BY Region
ORDER BY Region;
