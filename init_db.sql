-- Banking System Database Schema
-- Run this file to initialize the database tables and views

-- 1. Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    tax_id VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Accounts table
CREATE TABLE IF NOT EXISTS Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    -- TODO TODO2: Add CHECK constraint - balance >= 0 (prevents overdraft)
    CONSTRAINT check_accounts_balance_nonnegative CHECK (balance >= 0)
);

-- 3. Transactions table
-- transaction_type: 'DEPOSIT', 'WITHDRAW', 'TRANSFER_IN', 'TRANSFER_OUT', 'OPEN_ACCOUNT'
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    -- TODO TODO2: Add CHECK constraint - amount > 0
);

-- 4. BankReserves table
CREATE TABLE IF NOT EXISTS BankReserves (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    total_reserve DECIMAL(15, 2) DEFAULT 0.00
);

-- Initialize BankReserves with a default branch
INSERT INTO BankReserves (total_reserve) 
SELECT 0.00 
WHERE NOT EXISTS (SELECT 1 FROM BankReserves);

-- 5. AllCustomerTransactions View
DROP VIEW IF EXISTS AllCustomerTransactions;

CREATE VIEW AllCustomerTransactions AS
SELECT 
    c.name AS CustomerName,
    t.account_id AS AccountID,
    t.transaction_type AS Type,
    t.amount AS Amount,
    t.created_at AS Date
FROM Transactions t
JOIN Accounts a ON t.account_id = a.account_id
JOIN Customers c ON a.customer_id = c.customer_id
ORDER BY t.created_at DESC;

-- =============================================================================
-- TODO2 CHALLENGES: Database Triggers & Stored Procedures
-- =============================================================================
-- Students can implement these to move business logic into the database!

-- TODO2 Part 1: Add CHECK Constraints
-- Syntax: ALTER TABLE table_name ADD CONSTRAINT constraint_name CHECK (condition);
-- Example: ALTER TABLE Accounts ADD CONSTRAINT chk_balance CHECK (balance >= 0);
-- 
-- Your tasks:
-- 1. Add CHECK constraint on Accounts.balance to prevent negative balances
-- 2. Add CHECK constraint on Transactions.amount to ensure positive amounts


-- TODO2 Part 2: Create Trigger to Auto-Update BankReserves
-- Syntax for triggers:
-- DELIMITER $$
-- CREATE TRIGGER trigger_name
-- AFTER/BEFORE INSERT/UPDATE/DELETE ON table_name
-- FOR EACH ROW
-- BEGIN
--     -- Your SQL statements here
--     -- Use NEW.column_name for new values
--     -- Use OLD.column_name for old values
-- END$$
-- DELIMITER ;
--
-- Your task: Create a trigger that automatically updates BankReserves.total_reserve
-- whenever an Account.balance changes. Calculate the difference between NEW and OLD balance.


-- TODO2 Part 3: Create Trigger to Validate Sufficient Funds
-- Use BEFORE UPDATE trigger with SIGNAL to raise an error
-- Syntax for raising errors:
-- IF condition THEN
--     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Your error message';
-- END IF;
--
-- Your task: Create a trigger that prevents account balance from going negative


-- TODO2 Part 4: Create Stored Procedure for Transfer
-- Syntax for stored procedures:
-- DELIMITER $$
-- CREATE PROCEDURE procedure_name(
--     IN param1 datatype,
--     IN param2 datatype,
--     OUT result datatype
-- )
-- BEGIN
--     DECLARE variable_name datatype;
--     
--     START TRANSACTION;
--     -- Your SQL statements
--     -- Use SELECT ... INTO variable to get values
--     -- Use IF/ELSE for conditional logic
--     COMMIT;
-- END$$
-- DELIMITER ;
--
-- Your task: Create transfer_money(from_account_id, to_account_id, transfer_amount)
-- that handles the entire transfer operation with proper error handling

