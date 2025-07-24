CREATE TABLE IF NOT EXISTS users_app (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);