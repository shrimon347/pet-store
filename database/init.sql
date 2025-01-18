CREATE DATABASE pet_store;
-- Connect to the already existing database
\c pet_store;
-- Create Enum Types
CREATE TYPE pet_gender AS ENUM ('male', 'female', 'unknown');
CREATE TYPE pet_status AS ENUM ('available', 'sold', 'under_treatment');
-- Create Species Table
CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    version INT NOT NULL DEFAULT 0
);
-- Create Pets Table
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    species_id INT NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    age INT NOT NULL,
    breed VARCHAR(255),
    gender pet_gender NOT NULL,
    status pet_status NOT NULL,
    version INT NOT NULL DEFAULT 0
);