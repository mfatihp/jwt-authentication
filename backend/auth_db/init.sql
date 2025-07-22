CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,,
    hpass TEXT NOT NULL
);

-- INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
-- INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com');
