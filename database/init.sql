CREATE DATABASE pet_store;
\c pet_store;

-- Create Enum Types
CREATE TYPE pet_gender AS ENUM ('MALE', 'FEMALE', 'UNKNOWN');
CREATE TYPE pet_status AS ENUM ('AVAILABLE', 'SOLD', 'UNDER_TREATMENT');

-- Create Sequences
CREATE SEQUENCE pet_id_seq
    START WITH 1
    INCREMENT BY 50;

CREATE SEQUENCE species_id_seq
    START WITH 1
    INCREMENT BY 50;

-- Create Species Table
CREATE TABLE species (
    id BIGINT PRIMARY KEY DEFAULT nextval('species_id_seq'),
    name VARCHAR(255) NOT NULL UNIQUE,
    version INTEGER NOT NULL DEFAULT 0
);

-- Create Pets Table
CREATE TABLE pets (
    id BIGINT PRIMARY KEY DEFAULT nextval('pet_id_seq'),
    name VARCHAR(255) NOT NULL,
    species_id BIGINT NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    birthday DATE NOT NULL,
    breed VARCHAR(255),
    gender pet_gender NOT NULL,
    status pet_status NOT NULL,
    version INTEGER NOT NULL DEFAULT 0
);