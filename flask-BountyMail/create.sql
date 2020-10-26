DROP TABLE IF EXISTS bounty;

CREATE TABLE bounty (

    id INTEGER PRIMARY KEY,
    photo BLOB NOT NULL,
    photoPath TEXT,
    demands TEXT NOT NULL,
    photoName TEXT NOT NULL,
    amount INTEGER NOT NULL

)
