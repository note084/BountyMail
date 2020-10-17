DROP TABLE IF EXISTS bounty;

CREATE TABLE bounty (

    id SERIAL PRIMARY KEY,
    photo BLOB NOT NULL,
    photoPath TEXT,
    title TEXT NOT NULL,
    demands TEXT NOT NULL,
    photoName TEXT NOT NULL

)
