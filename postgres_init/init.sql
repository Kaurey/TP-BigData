CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(50),
    subscription_type VARCHAR(20)
);

INSERT INTO users (user_id, name, country, subscription_type) VALUES
(1, 'Alice', 'France', 'Premium'),
(2, 'Bob', 'USA', 'Free'),
(3, 'Charlie', 'UK', 'Premium'),
(4, 'Diana', 'France', 'Free'),
(5, 'Eve', 'Germany', 'Premium');
