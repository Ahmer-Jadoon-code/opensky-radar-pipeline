USE DATABASE OPENSKY_DB;
CREATE SCHEMA IF NOT EXISTS SILVER;
USE SCHEMA SILVER;

-- JSON array ko flatten kar ke proper tabular format mein tabdeel karna
CREATE OR REPLACE TABLE SILVER.OPENSKY_CLEANED AS
SELECT 
    f.value[0]::STRING AS icao24,
    TRIM(f.value[1]::STRING) AS callsign,
    f.value[2]::STRING AS origin_country,
    f.value[5]::FLOAT AS longitude,
    f.value[6]::FLOAT AS latitude,
    f.value[7]::FLOAT AS baro_altitude,
    f.value[8]::BOOLEAN AS on_ground,
    f.value[9]::FLOAT AS velocity,
    f.value[10]::FLOAT AS true_track,
    CURRENT_TIMESTAMP() AS processed_at
FROM OPENSKY_DB.BRONZE.OPENSKY_RAW_DATA r,
LATERAL FLATTEN(input => r.raw_json:states) f;