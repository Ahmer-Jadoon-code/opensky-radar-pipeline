USE DATABASE OPENSKY_DB;
USE SCHEMA BRONZE;

-- Table banayein (agar nahi bani hui)
CREATE OR REPLACE TABLE BRONZE.OPENSKY_RAW_DATA (
    raw_json VARIANT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- S3 Stage se data utha kar table mein COPY karein
COPY INTO BRONZE.OPENSKY_RAW_DATA (raw_json)
FROM @opensky_s3_stage;