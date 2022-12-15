CREATE TABLE IF NOT EXISTS users (
    "id" SERIAL PRIMARY KEY,
	"first_name" VARCHAR(20) ,
    "last_name" VARCHAR(20),
	"email" VARCHAR(20) ,
	"phone_number" VARCHAR(10),
    "wallet_address" VARCHAR NOT NULL,
    "date_created" TIMESTAMP,
    "id_type" INT,
    "id_number" VARCHAR,
    "nonce" INT ,
    "is_verified" BOOLEAN,
    "unique_str" VARCHAR(8) UNIQUE
);

CREATE TABLE IF NOT EXISTS properties (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT REFERENCES USERS(ID),
	"date_created" TIMESTAMP,
    "property_address" VARCHAR NOT NULL,
    "property_docs" VARCHAR,
    "is_verified" BOOLEAN,
    "unique_str" VARCHAR(8) UNIQUE
);
