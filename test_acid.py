"""
ACID Properties Stress Test
============================
This script creates concurrent database transactions to demonstrate ACID properties.

Learning Objectives:
1. Atomicity - All operations in a transaction succeed or all fail
2. Consistency - Database goes from one valid state to another
3. Isolation - Concurrent transactions don't interfere with each other
4. Durability - Committed changes persist even after system failure

Students: Fill in the TODO sections with proper SQL queries using transactions.
"""

import pymysql
import threading
import time
import random
from typing import List

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'bankuser',
    'password': 'bankpass',
    'database': 'banking',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Test Configuration
NUM_ACCOUNTS = 10
NUM_THREADS = 20
TRANSACTIONS_PER_THREAD = 50
INITIAL_BALANCE = 1000.00


def get_connection():
    """Create a new database connection"""
    return pymysql.connect(**DB_CONFIG)


def setup_test_accounts():
    """
    Setup test accounts with initial balances
    Students: This is provided as an example
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Clear existing test data
            print("Setting up test accounts...")
            cursor.execute("DELETE FROM Transactions")
            cursor.execute("DELETE FROM Accounts")
            cursor.execute("DELETE FROM Customers WHERE name LIKE 'Test%'")
            cursor.execute("UPDATE BankReserves SET total_reserve = 0.00")
            
            # Create test customers and accounts
            for i in range(NUM_ACCOUNTS):
                cursor.execute(
                    "INSERT INTO Customers (name, tax_id) VALUES (%s, %s)",
                    (f"TestUser{i}", f"TEST{i:04d}")
                )
                customer_id = cursor.lastrowid
                
                cursor.execute(
                    "INSERT INTO Accounts (customer_id, balance) VALUES (%s, %s)",
                    (customer_id, INITIAL_BALANCE)
                )
                
            # Initialize bank reserves
            total_initial = NUM_ACCOUNTS * INITIAL_BALANCE
            cursor.execute(
                "UPDATE BankReserves SET total_reserve = %s WHERE branch_id = 1",
                (total_initial,)
            )
            
            conn.commit()
            print(f"Created {NUM_ACCOUNTS} test accounts with ${INITIAL_BALANCE} each")
            print(f"Total bank reserves: ${total_initial}")
    finally:
        conn.close()


def concurrent_transfer_worker(worker_id: int, results: List):
    """
    Worker thread that performs random transfers between accounts
    
    TODO: Students must implement the transfer logic with proper transactions
    
    Learning points:
    - Without proper transaction isolation, race conditions can occur
    - Use SELECT ... FOR UPDATE to lock rows
    - Use START TRANSACTION, COMMIT, ROLLBACK
    """
    conn = get_connection()
    success_count = 0
    failure_count = 0
    
    try:
        for i in range(TRANSACTIONS_PER_THREAD):
            # Random transfer between two accounts
            from_account = random.randint(1, NUM_ACCOUNTS)
            to_account = random.randint(1, NUM_ACCOUNTS)
            
            # Don't transfer to same account
            if from_account == to_account:
                continue
                
            amount = round(random.uniform(1.0, 50.0), 2)
            
            try:
                with conn.cursor() as cursor:
                    # TODO: Implement transfer with proper transaction
                    # 
                    # Steps:
                    # 1. START TRANSACTION
                    # 2. SELECT balance FROM Accounts WHERE account_id = from_account FOR UPDATE
                    # 3. Check if balance >= amount
                    # 4. SELECT balance FROM Accounts WHERE account_id = to_account FOR UPDATE
                    # 5. UPDATE sender balance (-amount)
                    # 6. UPDATE receiver balance (+amount)
                    # 7. INSERT into Transactions (2 records: TRANSFER_OUT, TRANSFER_IN)
                    # 8. COMMIT
                    # 
                    # If any step fails:
                    # - ROLLBACK
                    # - increment failure_count
                    # 
                    # Hints:
                    # - Use cursor.execute("START TRANSACTION")
                    # - Use FOR UPDATE to lock rows (prevents race conditions)
                    # - Use try/except to catch errors and rollback

                    first = min(from_account, to_account)
                    second = max(from_account, to_account)
                    
                    # start transaction
                    cursor.execute("START TRANSACTION")

                    # check if the account exist
                    cursor.execute("SELECT account_id FROM Accounts WHERE account_id IN (%s, %s)", (from_account, to_account))
                    exist = cursor.fetchall()
                    if (len(exist) != 2):
                        conn.rollback()
                        continue
                    
                    # lock rows
                    cursor.execute("SELECT account_id, balance FROM Accounts WHERE account_id = %s FOR UPDATE", (first, ))
                    row1 = cursor.fetchone()
                    cursor.execute("SELECT account_id, balance FROM Accounts WHERE account_id = %s FOR UPDATE", (second, ))
                    row2 = cursor.fetchone()

                    # determine which account is first
                    if from_account == first:
                        balance = float(row1['balance'])
                    else:
                        balance = float(row2['balance'])

                    # update tables
                    if balance >= amount:
                        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account))
                        cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account))
                        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (from_account, 'TRANSFER_OUT', amount)
                        )
                        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (to_account, 'TRANSFER_IN', amount)
                        )
                        conn.commit()
                        success_count += 1
                    else:
                        conn.rollback()
                
            except Exception as e:
                failure_count += 1
                # Rollback is handled in your TODO implementation
                conn.rollback()
                
        results.append({
            'worker_id': worker_id,
            'success': success_count,
            'failure': failure_count
        })
        
    finally:
        conn.close()


def concurrent_deposit_withdraw_worker(worker_id: int, results: List):
    """
    Worker thread that performs random deposits and withdrawals
    
    TODO: Students must implement deposit/withdraw with proper transactions
    
    Learning points:
    - Test atomicity: Both account balance AND bank reserves must update together
    - If one fails, the other must rollback
    """
    conn = get_connection()
    success_count = 0
    failure_count = 0
    
    try:
        for i in range(TRANSACTIONS_PER_THREAD):
            account_id = random.randint(1, NUM_ACCOUNTS)
            amount = round(random.uniform(10.0, 100.0), 2)
            operation = random.choice(['deposit', 'withdraw'])
            
            try:
                with conn.cursor() as cursor:
                    # TODO: Implement deposit or withdraw with proper transaction
                    #
                    # DEPOSIT steps:
                    # 1. START TRANSACTION
                    # 2. UPDATE Accounts balance (+amount)
                    # 3. UPDATE BankReserves total_reserve (+amount)
                    # 4. INSERT into Transactions
                    # 5. COMMIT
                    #
                    # WITHDRAW steps:
                    # 1. START TRANSACTION
                    # 2. SELECT balance FOR UPDATE
                    # 3. Check if balance >= amount
                    # 4. UPDATE Accounts balance (-amount)
                    # 5. UPDATE BankReserves total_reserve (-amount)
                    # 6. INSERT into Transactions
                    # 7. COMMIT
                    #
                    # Remember: If ANY step fails, ROLLBACK all changes!
                    
                    if operation == 'deposit':
                        cursor.execute('START TRANSACTION')

                        # check if the account exist
                        cursor.execute("SELECT account_id FROM Accounts WHERE account_id = %s", (account_id, ))
                        exist = cursor.fetchone()
                        if (exist == None):
                            conn.rollback()
                            continue

                        # lock rows
                        cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE", (account_id, ))
                        cursor.execute("SELECT total_reserve FROM BankReserves WHERE branch_id = 1 FOR UPDATE")

                        # update tables
                        cursor.execute('UPDATE Accounts SET balance = balance + %s WHERE account_id = %s', (amount, account_id))
                        cursor.execute("UPDATE BankReserves SET total_reserve = total_reserve + %s WHERE branch_id = 1", (amount, ))
                        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (account_id, 'DEPOSIT', amount)
                        )
                        conn.commit()
            
                    else:
                        cursor.execute('START TRANSACTION')

                        # check if the account exist
                        cursor.execute("SELECT account_id FROM Accounts WHERE account_id = %s", (account_id, ))
                        exist = cursor.fetchone()
                        if (exist == None):
                            conn.rollback()
                            continue

                        # lock row and check sufficient fund
                        cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE", (account_id, ))
                        cursor.execute("SELECT total_reserve FROM BankReserves WHERE branch_id = 1 FOR UPDATE")
                        balance = cursor.fetchone()['balance']
                        if (balance < amount):
                            conn.rollback()
                            continue
                        
                        # update tables
                        cursor.execute('UPDATE Accounts SET balance = balance - %s WHERE account_id = %s', (amount, account_id))
                        cursor.execute("UPDATE BankReserves SET total_reserve = total_reserve - %s WHERE branch_id = 1", (amount, ))
                        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (account_id, 'WITHDRAW', amount)
                        )
                        conn.commit()
                success_count += 1
                
            except Exception as e:
                failure_count += 1
                conn.rollback()
                
        results.append({
            'worker_id': worker_id,
            'success': success_count,
            'failure': failure_count
        })
        
    finally:
        conn.close()


def verify_consistency():
    """
    Verify ACID properties after stress test
    Students: This is provided to check your implementation
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Check 1: Sum of all account balances
            cursor.execute("SELECT SUM(balance) as total_accounts FROM Accounts WHERE customer_id IN (SELECT customer_id FROM Customers WHERE name LIKE 'Test%')")
            total_accounts = float(cursor.fetchone()['total_accounts']) or 0
            
            # Check 2: Bank reserves total
            cursor.execute("SELECT total_reserve FROM BankReserves WHERE branch_id = 1")
            total_reserves = float(cursor.fetchone()['total_reserve']) or 0
            
            # Check 3: Expected total (should remain constant)
            expected_total = NUM_ACCOUNTS * INITIAL_BALANCE
            
            print("\n" + "="*60)
            print("CONSISTENCY CHECK")
            print("="*60)
            print(f"Expected total:          ${expected_total:,.2f}")
            print(f"Sum of account balances: ${total_accounts:,.2f}")
            print(f"Bank reserves:           ${total_reserves:,.2f}")
            print(f"Difference (accounts):   ${abs(expected_total - total_accounts):,.2f}")
            print(f"Difference (reserves):   ${abs(expected_total - total_reserves):,.2f}")
            
            # ACID Property Check
            if abs(total_accounts - expected_total) < 0.01 and abs(total_reserves - expected_total) < 0.01:
                print("\n✅ CONSISTENCY: PASS - Money is conserved!")
                print("   This proves Atomicity and Consistency properties.")
            else:
                print("\n❌ CONSISTENCY: FAIL - Money was created or lost!")
                print("   Check your transaction implementation for bugs.")
                print("   Possible issues:")
                print("   - Missing ROLLBACK on error")
                print("   - Partial updates (updating account but not reserves)")
                print("   - Race conditions (not using FOR UPDATE)")
            
            # Count transactions
            cursor.execute("SELECT COUNT(*) as count FROM Transactions")
            transaction_count = cursor.fetchone()['count']
            print(f"\nTotal transactions logged: {transaction_count}")
            print("="*60)
            
    finally:
        conn.close()


def run_stress_test(test_type: str):
    """
    Run concurrent stress test
    
    Args:
        test_type: 'transfer' or 'deposit_withdraw'
    """
    print(f"\n{'='*60}")
    print(f"Running {test_type.upper()} stress test")
    print(f"Threads: {NUM_THREADS}, Transactions per thread: {TRANSACTIONS_PER_THREAD}")
    print(f"{'='*60}\n")
    
    threads = []
    results = []
    
    # Choose worker function
    worker_func = concurrent_transfer_worker if test_type == 'transfer' else concurrent_deposit_withdraw_worker
    
    # Start all threads
    start_time = time.time()
    for i in range(NUM_THREADS):
        t = threading.Thread(target=worker_func, args=(i, results))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    elapsed_time = time.time() - start_time
    
    # Summarize results
    total_success = sum(r['success'] for r in results)
    total_failure = sum(r['failure'] for r in results)
    
    print(f"\nCompleted in {elapsed_time:.2f} seconds")
    print(f"Successful transactions: {total_success}")
    print(f"Failed transactions: {total_failure}")
    print(f"Success rate: {(total_success / (total_success + total_failure) * 100):.1f}%")


if __name__ == "__main__":
    print("ACID Properties Stress Test")
    print("="*60)
    print("\nThis test will:")
    print("1. Create test accounts")
    print("2. Run concurrent transactions")
    print("3. Verify data consistency")
    print("\n⚠️  Students: You must implement the TODO sections first!")
    print("="*60)
    
    # Setup
    setup_test_accounts()
    
    # Choose test type
    print("\nChoose test type:")
    print("1. Transfer test (concurrent transfers between accounts)")
    print("2. Deposit/Withdraw test (concurrent deposits and withdrawals)")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        run_stress_test('transfer')
        verify_consistency()
    
    if choice in ['2', '3']:
        if choice == '3':
            setup_test_accounts()  # Reset for second test
        run_stress_test('deposit_withdraw')
        verify_consistency()
    
    print("\n" + "="*60)
    print("LEARNING POINTS:")
    print("="*60)
    print("1. ATOMICITY: All operations in a transaction succeed or fail together")
    print("2. CONSISTENCY: Money is never created or lost (sum is constant)")
    print("3. ISOLATION: Use FOR UPDATE to prevent race conditions")
    print("4. DURABILITY: Committed transactions persist in database")
    print("="*60)
