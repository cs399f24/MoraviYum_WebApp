-- Create database
DROP DATABASE IF EXISTS moraviyum_database;
CREATE DATABASE IF NOT EXISTS moraviyum_database;
USE moraviyum_database;

-- Create tables
-- CREATE TABLE IF NOT EXISTS session ( 
    -- user_id VARCHAR(50),
    -- username VARCHAR(50),
    -- email VARCHAR(50)
-- );

CREATE TABLE IF NOT EXISTS usernames (
    -- email VARCHAR(50),
    user_handle VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS foods (
    vendor VARCHAR(255),
    food_name VARCHAR(255),
    food_id INT(5),
    price VARCHAR(255),
    calories INT(5),
    avg_rating FLOAT
);

CREATE TABLE IF NOT EXISTS images (
    food_id INT(5),
    image_url VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT(5),
    user_id VARCHAR(50),
    food_id VARCHAR(50),
    rating INT(1),
    review TEXT,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);