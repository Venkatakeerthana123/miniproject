-- Average Load by Region and Hour of Day
SELECT 
    Region,
    CAST(DATEPART(HOUR, Datetime) AS VARCHAR) AS TimeSegment,
    'Hourly' AS Segment_Type,
    AVG(PJME_MW) AS Avg_Load
FROM energy
GROUP BY Region, DATEPART(HOUR, Datetime)

UNION ALL

-- Total Load by Region and Day
SELECT 
    Region,
    CAST(CAST(Datetime AS DATE) AS VARCHAR) AS TimeSegment,
    'Daily' AS Segment_Type,
    SUM(PJME_MW) AS Avg_Load
FROM energy
GROUP BY Region, CAST(Datetime AS DATE)

UNION ALL

-- Average Load by Region and Day of Week
SELECT 
    Region,
    DATENAME(WEEKDAY, Datetime) AS TimeSegment,
    'DayOfWeek' AS Segment_Type,
    AVG(PJME_MW) AS Avg_Load
FROM energy
GROUP BY Region, DATENAME(WEEKDAY, Datetime)

UNION ALL

-- Monthly Load Trends by Region
SELECT 
    Region,
    FORMAT(Datetime, 'yyyy-MM') AS TimeSegment,
    'Monthly' AS Segment_Type,
    SUM(PJME_MW) AS Avg_Load
FROM energy
GROUP BY Region, FORMAT(Datetime, 'yyyy-MM')
