USE bookkeeping;

CREATE TABLE transactions (
    id VARCHAR(8) NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    debit_account VARCHAR(50) NOT NULL,
    credit_account VARCHAR(50) NOT NULL,
    processed_for_ledger BOOLEAN DEFAULT FALSE
);

CREATE TABLE ledger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(8) NOT NULL,
    date DATE NOT NULL,
    description VARCHAR(255) NOT NULL,
    debit_account VARCHAR(50) NOT NULL,
    credit_account VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions (id)
);

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
