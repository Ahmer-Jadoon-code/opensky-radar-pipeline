USE DATABASE OPENSKY_DB;
CREATE SCHEMA IF NOT EXISTS GOLD;
USE SCHEMA GOLD;

-- Har mulk (country) ke hisaab se jahazon ki total tadad aur unki average speed/altitude nikalna
CREATE OR REPLACE TABLE GOLD.FLIGHTS_BY_COUNTRY AS
SELECT 
    origin_country,
    COUNT(DISTINCT icao24) AS total_active_flights,
    AVG(velocity) AS avg_velocity,
    AVG(baro_altitude) AS avg_altitude,
    CURRENT_TIMESTAMP() AS updated_at
FROM OPENSKY_DB.SILVER.OPENSKY_CLEANED
WHERE origin_country IS NOT NULL AND origin_country != ''
GROUP BY origin_country
ORDER BY total_active_flights DESC;