-- 1. Database aur Schema banayein
CREATE DATABASE IF NOT EXISTS OPENSKY_DB;
USE DATABASE OPENSKY_DB;
CREATE SCHEMA IF NOT EXISTS BRONZE;
USE SCHEMA BRONZE;

-- 2. Snowflake mein Storage Integration banayein (IAM Role ke zariye)
CREATE OR REPLACE STORAGE INTEGRATION opensky_s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::048506328077:role/Snowflake_S3_Role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://opensky-bronze-ahmer-2026/');

-- 3. Integration ki details nikalne ke liye ye run karein
DESC INTEGRATION opensky_s3_int;