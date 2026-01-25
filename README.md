# Banking System GUI - Student Exercise

This is a hands-on lab exercise to learn CRUD operations, ACID transaction properties, and database-side business logic enforcement using MySQL, Python, and Tkinter.

## Overview

We have provided a skeleton GUI application for a banking system. Your task is to implement the backend logic to connect the application to a MySQL database and perform transactional operations.

## Tools & Technologies

### MySQL
A powerful, open-source Relational Database Management System (RDBMS) that stores and manages structured data using SQL.

**Alternatives:** MariaDB (a community-developed fork of MySQL, effectively a drop-in replacement)

### phpMyAdmin
A free software tool written in PHP, intended to handle the administration of MySQL over the Web. It supports operations on databases, tables, columns, relations, indexes, users, permissions, etc.

**Access:** http://localhost:8080 (after running docker-compose)

### Tkinter
The standard Python interface to the Tk GUI toolkit. It provides widgets such as buttons, labels, and text boxes to build desktop applications.

### PyMySQL
A pure-Python MySQL client library. It allows Python programs to connect to a MySQL server and execute SQL queries.

## Database Schema

You must create the following tables in your MySQL database to support the application:

### 1. Customers
Stores user identity.
- `customer_id` (int, PK)
- `name` (text)
- `tax_id` (text, unique)

### 2. Accounts
Stores individual bank accounts.
- `account_id` (int, PK)
- `customer_id` (FK)
- `balance` (decimal)

### 3. Transactions
Stores an audit log of all operations.
- `transaction_id` (int, PK)
- `account_id` (FK)
- `transaction_type` (text)
- `amount` (decimal)
- `created_at` (timestamp)

### 4. BankReserves
Stores the total cash holding of the bank branch.
- `branch_id` (int, PK)
- `total_reserve` (decimal)

### 5. AllCustomerTransactions (View)
A joined view for reporting.
- **Logic:** Join Customers ⋈ Accounts ⋈ Transactions
- **Columns:** CustomerName, AccountID, Type, Amount, Date

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Database
```bash
docker-compose up -d
```
This starts MySQL and phpMyAdmin.

### 3. Initialize the Database Schema
Run the SQL script to create tables:
```bash
mysql -h localhost -u bankuser -pbankpass banking < init_db.sql
```

**Or use phpMyAdmin:**
- Open http://localhost:8080
- Login: `bankuser` / `bankpass`
- Select `banking` database
- Click "SQL" tab
- Copy and paste the content from `init_db.sql`
- Click "Go"

### 4. Run the Application
```bash
python banking_gui.py
```

## Lab Tasks

Open the provided `banking_gui.py` file and complete the following TODO sections:

### 1. Server Connection
Implement logic to `connect()` and `disconnect()` from the MySQL database server. Handle connection errors gracefully.

**Status:** ✅ Already implemented

### 2. Banking Operations

#### a) Open Account
Implement SQL to insert a new customer and account.

**Requirements:**
- Insert into Customers table (or find existing by tax_id)
- Insert into Accounts table
- Handle initial deposit if provided

#### b) Deposit (Transaction)
**Requirements:**
- Update the specific Account balance (+Amount)
- Update the BankReserves total reserve (+Amount)
- **CRITICAL:** These updates must be wrapped in a transaction block. If one fails, both must roll back.

**SQL Structure:**
```sql
START TRANSACTION;
-- Your SQL statements here
COMMIT; -- or ROLLBACK on error
```

#### c) Withdraw (Transaction)
**Requirements:**
- Check if the Account has sufficient funds (Balance ≥ Amount)
- Update the Account balance (-Amount)
- Update the BankReserves total reserve (-Amount)
- **CRITICAL:** All steps must be atomic.

**Key Concept:** Use `SELECT ... FOR UPDATE` to lock the row and prevent race conditions.

#### d) Transfer (Transaction)
**The core ACID test.** Move money from Account A to Account B.

**Requirements:**
- Wrap operations in a `START TRANSACTION ... COMMIT` block
- Lock both accounts with SELECT FOR UPDATE
- Check sufficient funds in sender account
- Update both account balances
- Log two transaction records (TRANSFER_OUT, TRANSFER_IN)
- If any step fails (e.g., insufficient funds), `ROLLBACK` the entire transaction

#### e) Check Balance
Query and display the current balance for a given account.

#### f) Bank Statement
Query the `AllCustomerTransactions` view to display the transaction history.

## Advanced Challenges (TODO2)

After completing the basic implementation, try these advanced database-side features:

### Database Constraints
- Add `CHECK` constraint: `balance >= 0` (prevents overdraft)
- Add `CHECK` constraint: `amount > 0` (ensures positive amounts)

### Database Triggers
- Create trigger to auto-update `BankReserves` when account balance changes
- Create trigger to validate sufficient funds before withdrawal
- Learn the trade-off between application-side vs database-side logic

### Stored Procedures
- Create `transfer_money(from_id, to_id, amount)` stored procedure
- Encapsulate complex transaction logic in the database

See `init_db.sql` for syntax examples and guidance.

## Testing ACID Properties

Run the stress test to verify your implementation handles concurrent transactions correctly:

```bash
python test_acid.py
```

This will:
1. Create 10 test accounts with $1,000 each
2. Run 20 concurrent threads performing random transactions
3. Verify money is conserved (ACID properties)

**Expected outcome:** If implemented correctly, the sum of all balances should equal the initial total, proving Atomicity and Consistency.

## Learning Objectives

By completing this lab, you will learn:

- ✅ **CRUD operations** (Create, Read, Update, Delete)
- ✅ **SQL transactions** with explicit `START TRANSACTION`, `COMMIT`, `ROLLBACK`
- ✅ **ACID properties** (Atomicity, Consistency, Isolation, Durability)
- ✅ **Row-level locking** with `FOR UPDATE` to prevent race conditions
- ✅ **Error handling** with try/except and rollback
- ✅ **Database constraints** (CHECK, UNIQUE, FOREIGN KEY)
- ✅ **Database triggers** (BEFORE/AFTER INSERT/UPDATE/DELETE)
- ✅ **Stored procedures** for complex operations
- ✅ **Concurrency testing** with multi-threaded stress tests

## Database Credentials

- **Host:** localhost:3306
- **User:** bankuser
- **Password:** bankpass
- **Database:** banking

## phpMyAdmin Access

- **URL:** http://localhost:8080
- **Username:** bankuser
- **Password:** bankpass

## Project Files

- `banking_gui.py` - Main GUI application (students implement TODOs)
- `init_db.sql` - Database schema initialization
- `test_acid.py` - ACID properties stress test
- `docker-compose.yml` - MySQL and phpMyAdmin setup
- `requirements.txt` - Python dependencies
- `task.tex` - Original LaTeX assignment (reference)

## Tips for Success

1. **Start with simple operations** (Check Balance) before complex ones (Transfer)
2. **Test each operation** individually before stress testing
3. **Use phpMyAdmin** to inspect database state while debugging
4. **Read error messages carefully** - MySQL provides detailed transaction errors
5. **Use FOR UPDATE** to prevent race conditions in concurrent scenarios
6. **Always ROLLBACK on error** - partial updates violate ACID properties

## Submission Requirements

Submit the following files:

1. **`banking_gui.py`** - Your completed implementation with all TODO sections filled in
2. **`init_db.sql`** - Database schema (include TODO2 if implemented)
3. **`test_acid.py`** - Your completed ACID stress test implementation
4. **`test_acid_results.txt`** - Console output from running the stress test

---

**Good luck! 🎓**
