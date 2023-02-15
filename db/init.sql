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

CREATE TABLE IF NOT EXISTS aadhar(
"UID" VARCHAR(12) PRIMARY KEY,
"FirstName" VARCHAR(20) NOT NULL,
"LastName" VARCHAR(20) NOT NULL,
"DOB" VARCHAR(12) NOT NULL,
"Gender" VARCHAR(6) NOT NULL,
"Address" VARCHAR(255) ,
"Pincode" VARCHAR(10),
"PhoneNumber" VARCHAR(12) NOT NULL,
"EmailID" VARCHAR(50));

-- insert into aadhar (UID, FirstName, LastName, EmailID, Gender, DOB, Address, State, Pincode, PhoneNumber) values (935078894568, 'Amar', 'Singh', 'asingh@gmail.com', 'Male', '9/11/1989', 'A-203,BK Marg, Kanjur Marg (E)', 'Maharashtra', 400092, 1259981299);
-- insert into aadhar (UID, FirstName, LastName, EmailID, Gender, DOB, Address, State, Pincode, PhoneNumber) values (563013996155, 'Bilas', 'Trivedi', 'btrivedi@gmail.com', 'Male', '19/01/1992', 'B-203,CK Marg, Ghatkopar (E)', 'Maharashtra', 400094, 9981299901);
-- insert into aadhar (UID, FirstName, LastName, EmailID, Gender, DOB, Address, State, Pincode, PhoneNumber) values (419510692642, 'Ram', 'Gupta', 'rgupta@gmail.com', 'Male', '19/04/1982', 'C-403,MD Marg, Chembur (E)', 'Maharashtra', 400095, 9983299901);
-- insert into aadhar (UID, FirstName, LastName, EmailID, Gender, DOB, Address, State, Pincode, PhoneNumber) values (707976695869, 'Riya', 'Takaria', 'rtakaria@gmail.com', 'Female', '29/09/1998', 'C-307,HP Marg, Bhandup (E)', 'Maharashtra', 400099, 9983299801);
-- insert into aadhar (UID, FirstName, LastName, EmailID, Gender, DOB, Address, State, Pincode, PhoneNumber) values (688924056676, 'Samar', 'Khan', 'skhan@gmail.com', 'Male', '22/09/1992', 'A-107,RC Marg, Mumbra (E)', 'Maharashtra', 400013, 9983899801);

CREATE TABLE IF NOT EXISTS property(
"SaleDeedNumber" VARCHAR(16) PRIMARY KEY,
"MahaRERANumber" VARCHAR(12),
"UID" VARCHAR(12) REFERENCES AADHAR("UID"),
"Area" VARCHAR(20),
"Address" VARCHAR(255) ,
"Pincode" VARCHAR(10)
);

-- insert into property Values('1394/2015/SRO1','PL1238048425','935078894568','550 sqft','A-204,BK Marg, Kanjur Marg (E)',40092);
-- insert into property Values('2414/2019/SRO3','PL3928048425','419510692642','750 sqft','C-402,MD Marg, Chembur (E)',40095);
-- insert into property Values('1840/2003/SRO2','PL4428048445','707976695869','620 sqft','C-407,HP Marg, Bhandup (E)',40099);
-- insert into property Values('2941/2011/SRO3','PL5280468445','688924056676','620 sqft','A-102,RC Marg, Mumbra (E)',40013);
-- insert into property Values('3941/2010/SRO5','PL7280268447','563013996155','420 sqft','B-203,CK Marg, Ghatkopar (E))',40094);

CREATE TABLE IF NOT EXISTS aadhar_wallet(
    "UID" VARCHAR(12) PRIMARY KEY REFERENCES AADHAR("UID"),
    "wallet_address" VARCHAR(66)
);

CREATE TABLE IF NOT EXISTS listings(
    "property_id" VARCHAR(16) PRIMARY KEY REFERENCES PROPERTY("SaleDeedNumber"), 
    "deposit" INT,   
    "is_rent_eth" BOOLEAN NOT NULL,
    "eth_rent" DECIMAL(22,18),
    "rs_rent" DECIMAL(11,2),
    "metadata_id"  VARCHAR(8),
    "latitude" NUMERIC,
    "longitude" NUMERIC,
    "details" VARCHAR(256)
);