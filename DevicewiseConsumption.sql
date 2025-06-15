WITH Numbered AS (
    SELECT 
        *,
        'Device' + CAST(ROW_NUMBER() OVER (ORDER BY Datetime) AS VARCHAR) AS Device_Type
    FROM energy
)
SELECT 
    Device_Type,
    SUM(PJME_MW) AS Total_Consumption
FROM Numbered
GROUP BY Device_Type
ORDER BY Device_Type;
