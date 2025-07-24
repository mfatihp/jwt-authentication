CREATE TABLE IF NOT EXISTS users_auth (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hpass TEXT NOT NULL
);