import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'bankuser',
    'password': 'bankpass',
    'database': 'banking',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F5F5F5")

        self.connection = None
        
        self.create_widgets()
        self.connect_db()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Banking System", font=("Helvetica", 32, "bold"), bg="#F5F5F5", fg="black")
        title_label.pack(pady=20)

        # Connection Status
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Disconnected")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="black", font=("Helvetica", 16), bg="#F5F5F5")
        status_label.pack(pady=5)

        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Bind tab selection to auto-refresh
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Create tabs
        self.create_open_account_tab()
        self.create_deposit_tab()
        self.create_withdraw_tab()
        self.create_transfer_tab()
        self.create_balance_tab()
        self.create_reserves_tab()
        self.create_accounts_tab()
        self.create_statement_tab()

    def create_open_account_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Open Account")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Customer Name:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_name_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_name_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Tax ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_tax_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_tax_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="Initial Deposit:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_deposit_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_deposit_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(frame, text="Create Account", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.open_account, pady=10, padx=20).grid(row=3, column=0, columnspan=2, pady=30)

    def create_deposit_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Deposit")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.deposit_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.deposit_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.deposit_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.deposit_amount_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(frame, text="Deposit", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.deposit, pady=10, padx=20).grid(row=2, column=0, columnspan=2, pady=30)

    def create_withdraw_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Withdraw")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.withdraw_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.withdraw_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.withdraw_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.withdraw_amount_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(frame, text="Withdraw", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.withdraw, pady=10, padx=20).grid(row=2, column=0, columnspan=2, pady=30)

    def create_transfer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transfer")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="From Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_from_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_from_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="To Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_to_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_to_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_amount_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(frame, text="Transfer", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.transfer, pady=10, padx=20).grid(row=3, column=0, columnspan=2, pady=30)

    def create_balance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Check Balance")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.balance_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.balance_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Button(frame, text="Check Balance", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.check_balance, pady=10, padx=20).grid(row=1, column=0, columnspan=2, pady=30)

        self.balance_result = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), fg="black", bg="#F5F5F5")
        self.balance_result.grid(row=2, column=0, columnspan=2, pady=20)

    def create_reserves_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Bank Reserves")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(expand=True)

        tk.Label(frame, text="Branch Total Reserve", font=("Helvetica", 28, "bold"), bg="#F5F5F5", fg="black").pack(pady=30)

        self.reserves_result = tk.Label(frame, text="", font=("Helvetica", 48, "bold"), fg="#006400", bg="#F5F5F5")
        self.reserves_result.pack(pady=50)

        tk.Button(frame, text="Refresh", font=("Helvetica", 18), 
                 bg="white", fg="black", command=self.refresh_reserves, pady=10, padx=20).pack(pady=20)

    def create_accounts_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="All Accounts")

        tk.Button(tab, text="Refresh Accounts", font=("Helvetica", 18), 
                 command=self.refresh_accounts, pady=5, padx=15).pack(pady=10)

        columns = ("Account ID", "Customer Name", "Tax ID", "Balance")
        self.accounts_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=250)
        
        self.accounts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview", 
                       rowheight=60, 
                       font=("Helvetica", 20), 
                       background="white",
                       foreground="black",
                       fieldbackground="white",
                       borderwidth=1,
                       relief="solid")
        style.configure("Treeview.Heading", 
                       font=("Helvetica", 28, "bold"),
                       background="lightgray",
                       foreground="black")
        style.map("Treeview", background=[("selected", "#0078D7")])

        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.accounts_tree.yview)
        self.accounts_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_tab_changed(self, event):
        """Auto-refresh when switching tabs"""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        if tab_text == "All Accounts":
            self.refresh_accounts()
        elif tab_text == "Transactions":
            self.refresh_statement()
        elif tab_text == "Bank Reserves":
            self.refresh_reserves()

    def create_statement_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")

        tk.Button(tab, text="Refresh Transactions", font=("Helvetica", 18), 
                 command=self.refresh_statement, pady=5, padx=15).pack(pady=10)

        columns = ("Customer", "Account ID", "Type", "Amount", "Date")
        self.statement_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.statement_tree.heading(col, text=col)
            self.statement_tree.column(col, width=220)
        
        self.statement_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.statement_tree.yview)
        self.statement_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def connect_db(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
            
            self.connection = pymysql.connect(**DB_CONFIG)
            self.status_var.set("Status: Connected to Database")
            print("Connected to database.")
        except pymysql.MySQLError as e:
            self.status_var.set(f"Status: Connection Failed: {e}")
            messagebox.showerror("Connection Error", f"Could not connect to database:\n{e}")

    def __del__(self):
        if self.connection and self.connection.open:
            self.connection.close()

    # --- TODO: Implement these methods ---

    def open_account(self):
        """
        TODO: Implement account creation with transaction
        
        Application Logic:
        1. Get input values from entry fields
        2. Validate inputs
        3. START TRANSACTION
        4. Check if customer exists by tax_id
        5. Insert Customer if new
        6. Insert Account
        7. If initial_deposit > 0: Update account balance, BankReserves, insert Transaction
        8. COMMIT
        9. Handle errors with ROLLBACK
        
        TODO2 - Database Constraints & Triggers:
        - Add CHECK constraint: initial deposit >= 0
        - Create TRIGGER: after INSERT on Accounts with initial deposit,
          automatically update BankReserves and insert into Transactions
        - Add UNIQUE constraint on Customers.tax_id (already exists)
        """
        # TODO 1 ----
        # get inputs from entries
        customer_name = self.open_name_entry.get().strip()
        tax_id = self.open_tax_entry.get().strip()
        initial_deposit = self.open_deposit_entry.get().strip()

        # validate inputs
        if customer_name == "" or tax_id == "" or initial_deposit == "":
            messagebox.showerror("Input error", "Inputs cannot be empty")
            return
        elif (float(initial_deposit) < 0):
            messagebox.showerror("Input error", "Initial Deposit must be non-negative number")
            return
        
        # start transaction
        try:
            initial_deposit = float(initial_deposit)
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # check if custom exist via tax_id
                cursor.execute("SELECT customer_id FROM Customers WHERE tax_id = %s", (tax_id, ))
                duplicate = cursor.fetchone()
                if (duplicate == None):
                    # insert new customer if not
                    cursor.execute("INSERT INTO Customers (name, tax_id) VALUES (%s, %s)", (customer_name, tax_id))
                    customer_id = cursor.lastrowid
                else:
                    customer_id = duplicate['customer_id']
            
                # insert new account
                cursor.execute("INSERT INTO Accounts (customer_id, balance) VALUES (%s, 0)", (customer_id, ))

                # update Accounts balance and insert into transaction, BankReserves total_reserve already handled by trigger
                if (initial_deposit > 0):
                    account_id = cursor.lastrowid
                    cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_id = %s", (initial_deposit, account_id))
                    cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                                   (account_id, "OPEN_ACCOUNT", initial_deposit)
                    )

            # commit changes
            self.connection.commit()
            messagebox.showinfo("Success", "Open new account successfully.")

        except Exception:
            self.connection.rollback()
            messagebox.showerror("Error", "Failed to open account.")
            raise

    def deposit(self):
        """
        TODO: Implement deposit with transaction
        
        Application Logic:
        1. Get account_id and amount from entries
        2. Validate inputs (amount > 0)
        3. START TRANSACTION
        4. Check account exists
        5. UPDATE Accounts balance
        6. UPDATE BankReserves
        7. INSERT into Transactions
        8. COMMIT
        9. Handle errors with ROLLBACK
        
        TODO2 - Database Triggers:
        - Create TRIGGER: AFTER UPDATE on Accounts.balance (when increased)
          automatically UPDATE BankReserves.total_reserve
        - Create TRIGGER: AFTER INSERT on Transactions of type 'DEPOSIT'
          to log or validate deposit operations
        - This way you only need to UPDATE Accounts and INSERT Transaction,
          the trigger handles BankReserves automatically!
        """
        # TODO 1 ----
        # get inputs from entries
        account_id = self.deposit_account_entry.get().strip()
        amount = self.deposit_amount_entry.get().strip()

        # validate inputs
        if (account_id == "" or amount == ""):
            messagebox.showerror("Input error", "Inputs cannot be empty")
            return
        elif (float(amount) <= 0):
            messagebox.showerror("Input error", "Amount must be positive number")
            return

        # start transaction
        try:
            account_id = int(account_id)
            amount = float(amount)
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # check if the account exist
                cursor.execute("SELECT account_id FROM Accounts WHERE account_id = %s", (account_id, ))
                exist = cursor.fetchone()
                if (exist == None):
                    messagebox.showerror("Input error", "No account found.")
                    return
                
                # update Accounts balance and insert into transaction, BankReserves total_reserve already handled by trigger
                account_id = exist['account_id']
                cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
                cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (account_id, 'DEPOSIT', amount)
                )

            # commit changes
            self.connection.commit()
            messagebox.showinfo("Success", "Deposit successfully.")

        except Exception:
            self.connection.rollback()
            messagebox.showerror("Error", "Failed to deposit.")
            raise

    def withdraw(self):
        """
        TODO: Implement withdraw with transaction
        
        Application Logic:
        1. Get account_id and amount
        2. Validate inputs (amount > 0)
        3. START TRANSACTION
        4. SELECT balance FOR UPDATE (lock row)
        5. Check sufficient funds
        6. UPDATE Accounts balance
        7. UPDATE BankReserves
        8. INSERT into Transactions
        9. COMMIT
        10. Handle errors with ROLLBACK
        
        TODO2 - Database Constraints & Triggers:
        - Add CHECK constraint: Accounts.balance >= 0
          (prevents overdraft at database level!)
        - Create TRIGGER: BEFORE UPDATE on Accounts.balance
          to validate sufficient funds and raise error if not
        - Create TRIGGER: AFTER UPDATE on Accounts.balance (when decreased)
          automatically UPDATE BankReserves.total_reserve
        - With these, database enforces business rules!
        """
        # TODO 1
        # get inputs from entries
        account_id = self.withdraw_account_entry.get().strip()
        amount = self.withdraw_amount_entry.get().strip()

        # validate inputs
        if (account_id == "" or amount == ""):
            messagebox.showerror("Input error", "Inputs cannot be empty")
            return
        elif (float(amount) <= 0):
            messagebox.showerror("Input error", "Amount must be positive number")
            return
        
        # start transaction
        try:
            account_id = int(account_id)
            amount = float(amount)
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # check if the account exist
                cursor.execute("SELECT account_id FROM Accounts WHERE account_id = %s", (account_id, ))
                exist = cursor.fetchone()
                if (exist == None):
                    messagebox.showerror("Input error", "No account found.")
                    return
                account_id = exist['account_id']
                
                # lock row
                cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE", (account_id, ))

                # check sufficient funds
                balance = float(cursor.fetchone()['balance'])
                if (balance - amount < 0):
                    messagebox.showerror("Error", "Insufficient funds.")
                    self.connection.rollback()
                    return
                
                # update Accounts balance and insert into transaction, BankReserves total_reserve already handled by trigger
                cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
                cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (account_id, 'WITHDRAW', amount)
                )

            # commit changes
            self.connection.commit()
            messagebox.showinfo("Success", "Withdraw successfully.")

        except Exception:
            self.connection.rollback()
            messagebox.showerror("Error", "Failed to withdraw.")
            raise

    def transfer(self):
        """
        TODO: Implement transfer with transaction (ACID test)
        
        Application Logic:
        1. Get from_account, to_account, amount
        2. Validate inputs (amount > 0, from != to)
        3. START TRANSACTION
        4. SELECT both accounts FOR UPDATE (lock both rows)
        5. Check sender has sufficient funds
        6. UPDATE sender balance (-amount)
        7. UPDATE receiver balance (+amount)
        8. INSERT 2 transaction records (TRANSFER_OUT, TRANSFER_IN)
        9. COMMIT
        10. Handle errors with ROLLBACK
        
        TODO2 - Stored Procedure + Triggers:
        - Create STORED PROCEDURE: transfer_money(from_id, to_id, amount)
          which handles all the logic in one database call
        - Add CHECK constraint: amount > 0 for transactions
        - Create TRIGGER: BEFORE INSERT on Transactions
          to validate transfer rules (e.g., no self-transfer)
        - Benefits: ACID guaranteed by database, less Python code,
          business logic centralized in database!
        """
        # TODO 1
        # get inputs from entries
        from_account = self.transfer_from_entry.get().strip()
        to_account = self.transfer_to_entry.get().strip()
        amount = self.transfer_amount_entry.get().strip()

        # validate inputs
        if (from_account == "" or to_account == "" or amount == ""):
            messagebox.showerror("Input error", "Inputs cannot be empty")
            return
        elif (from_account == to_account):
            messagebox.showerror("Input error", "Can't transfer to the same Account ID")
            return
        elif (float(amount) <= 0):
            messagebox.showerror("Input error", "Amount must be positive number")
            return
        
        # start transaction
        try:
            amount = float(amount)
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # check if the account exist
                cursor.execute("SELECT account_id FROM Accounts WHERE account_id IN (%s, %s)", (from_account, to_account))
                exist = cursor.fetchall()
                if (len(exist) != 2):
                    messagebox.showerror("Input error", "No account found.")
                    self.connection.rollback()
                    return
                
                # lock rows prevent deadlocks
                first = min(from_account, to_account)
                second = max(from_account, to_account)
                cursor.execute("SELECT account_id, balance FROM Accounts WHERE account_id = %s FOR UPDATE", (first, ))
                row1 = cursor.fetchone()
                cursor.execute("SELECT account_id, balance FROM Accounts WHERE account_id = %s FOR UPDATE", (second, ))
                row2 = cursor.fetchone()

                # determine which account is first
                if from_account == first:
                    balance = float(row1['balance'])
                else:
                    balance = float(row2['balance'])

                # check sufficient funds
                if (balance - amount < 0):
                    messagebox.showerror("Error", "Insufficient funds.")
                    self.connection.rollback()
                    return

                # update from_account balance, to_account balance and insert Transaction
                cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account))
                cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (from_account, 'TRANSFER_OUT', amount)
                )
                cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account))
                cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                               (to_account, 'TRANSFER_IN', amount)
                )

            # commit changes
            self.connection.commit()
            messagebox.showinfo("Success", "Transfer successfully.")

        except Exception:
            self.connection.rollback()
            messagebox.showerror("Error", "Failed to transfer.")
            raise

    def check_balance(self):
        """
        TODO: Implement balance check
        1. Get account_id
        2. SELECT balance FROM Accounts WHERE account_id = ?
        3. Display result in self.balance_result label
        """
        # get input from entry
        account_id = self.balance_account_entry.get().strip()
        if account_id == "":
            messagebox.showerror("Input error", "Account ID cannot be empty.")
            return;
    
        try:
            account_id = int(account_id)
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s", account_id)
                result = cursor.fetchone()
                if result == None:
                    self.balance_result.config(text = "No account found.")
                else:
                    self.balance_result.config(text = result["balance"])
        except Exception:
            self.balance_result.config(text = "Error")
            messagebox.showerror("Error", "Failed to check balance.")
            raise

    def refresh_accounts(self):
        """
        TODO: Implement accounts list refresh
        1. Clear existing tree items
        2. JOIN Accounts and Customers tables
        3. Fetch all rows
        4. Insert into accounts_tree
        """
        # clear existing tree items
        for row in self.accounts_tree.get_children():
            self.accounts_tree.delete(row)        
        
        try:
            with self.connection.cursor() as cursor:
                # join Accounts and Customers tables    
                cursor.execute("SELECT * FROM Accounts a JOIN Customers c ON a.customer_id = c.customer_id")

                # fetch all rows
                rows = cursor.fetchall()

                # insert into account_tree
                for row in rows:
                    self.accounts_tree.insert("", "end", values=(row['account_id'], row['name'], row['tax_id'], row['balance']))
        except Exception:
            messagebox.showerror("Error", "Failed to display account information.")
            raise

    def refresh_statement(self):
        """
        TODO: Implement transactions refresh
        1. Clear existing tree items
        2. SELECT from AllCustomerTransactions view
        3. Insert rows into statement_tree
        """
        # clear existing tree items
        for row in self.statement_tree.get_children():
            self.statement_tree.delete(row)        
        
        try:
            with self.connection.cursor() as cursor:
                # select from AllCustomerTransactions view  
                cursor.execute("SELECT * FROM AllCustomerTransactions")

                # fetch all rows
                rows = cursor.fetchall()

                # insert into statement_tree
                for row in rows:
                    self.statement_tree.insert("", "end", values=(row['CustomerName'], row['AccountID'], row['Type'], row['Amount'], row['Date']))
        except Exception:
            messagebox.showerror("Error", "Failed to display transaction information.")
            raise

    def refresh_reserves(self):
        """
        TODO: Implement reserves refresh
        1. SELECT total_reserve FROM BankReserves
        2. Display in reserves_result label with formatting
        """
        # Query bank reserves
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT total_reserve FROM BankReserves LIMIT 1")
                result = cursor.fetchone()
                
                if result:
                    # Display with thousands separator and 2 decimal places
                    self.reserves_result.config(text=f"${result['total_reserve']:,.2f}", fg="#006400")
                else:
                    self.reserves_result.config(text="No data", fg="red")
        except pymysql.MySQLError as e:
            self.reserves_result.config(text="Error", fg="red")
            messagebox.showerror("Database Error", f"Could not fetch reserves:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
