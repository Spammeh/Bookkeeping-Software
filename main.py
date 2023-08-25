import pandas as pd
from datetime import datetime

class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

class Transaction:
    def __init__(self, date, description):
        self.date = date
        self.description = description
        self.entries = []

    def add_entry(self, account, amount, debit=True):
        self.entries.append((account, amount, debit))
        if debit:
            account.balance += amount
        else:
            account.balance -= amount

class BookkeepingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts_from_csv()
        self.transactions = []
        self.load_transactions_from_csv()

    def add_account(self, account_name):
        self.accounts[account_name] = Account(account_name)
        self.save_accounts_to_csv()

    def remove_account(self, account_name):
        if account_name in self.accounts:
            del self.accounts[account_name]
            self.save_accounts_to_csv()
            print(f"Account '{account_name}' removed.")
        else:
            print(f"Account '{account_name}' not found.")

    def record_transaction(self, transaction):
        for account, amount, debit in transaction.entries:
            account.balance += amount if debit else -amount

        self.transactions.append(transaction)
        self.save_transactions_to_csv()
        print("Transaction recorded.")

    def create_transaction(self, date, description):
        return Transaction(date=date, description=description)

    def undo_transaction(self, transaction):
        for account, amount, debit in transaction.entries:
            account.balance += amount if debit else -amount

    def edit_transaction(self, transaction_index):
        if 0 <= transaction_index < len(self.transactions):
            transaction = self.transactions[transaction_index]
            self.undo_transaction(transaction)
            
            date = input("Enter updated transaction date (YYYY-MM-DD): ")
            description = input("Enter updated transaction description: ")
            new_transaction = self.create_transaction(date=date, description=description)

            for account, amount, debit in transaction.entries:
                account_name = account.name
                while True:
                    try:
                        new_amount = float(input(f"Enter updated amount for {account_name}: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                while True:
                    debit_credit = input(f"Updated debit or credit for {account_name}? (d/c): ").lower()
                    if debit_credit in ('d', 'c'):
                        new_debit = debit_credit == 'd'
                        break
                    else:
                        print("Invalid input. Please enter 'd' for debit or 'c' for credit.")
                new_transaction.add_entry(self.accounts[account_name], new_amount, new_debit)
            
            self.record_transaction(new_transaction)
            print("Transaction edited.")
        else:
            print("Invalid transaction index.")

    def remove_transaction(self, transaction_index):
        if 0 <= transaction_index < len(self.transactions):
            transaction = self.transactions[transaction_index]
            self.undo_transaction(transaction)
            del self.transactions[transaction_index]
            self.save_transactions_to_csv()  # Save the changes to the CSV
            print("Transaction removed.")
        else:
            print("Invalid transaction index.")

    def load_accounts_from_csv(self):
        try:
            df = pd.read_csv('accounts.csv')
            for _, row in df.iterrows():
                self.accounts[row['Account']] = Account(row['Account'])
        except FileNotFoundError:
            pass

    def save_accounts_to_csv(self):
        accounts_data = [{'Account': account.name, 'Balance': account.balance} for account in self.accounts.values()]
        accounts_df = pd.DataFrame(accounts_data)
        accounts_df.to_csv('accounts.csv', index=False)

    def save_to_csv(self, transaction):
        accounts_data = [{'Account': account.name, 'Balance': account.balance} for account in self.accounts.values()]
        accounts_df = pd.DataFrame(accounts_data)
        accounts_df.to_csv('accounts.csv', index=False)

    def load_transactions_from_csv(self):
        try:
            transactions_df = pd.read_csv('transactions.csv')
            for _, row in transactions_df.iterrows():
                transaction = Transaction(date=row['Date'], description=row['Description'])
                accounts = eval(row['Accounts'])
                amounts = eval(row['Amounts'])
                debits = eval(row['Debits'])
                for account_name, amount, is_debit in zip(accounts, amounts, debits):
                    account = self.accounts[account_name]
                    transaction.add_entry(account, amount, is_debit)
                self.transactions.append(transaction)
                # Update account balances based on loaded transactions
                self.update_account_balances(transaction)
        except FileNotFoundError:
            pass

    def save_transactions_to_csv(self):
        transactions_data = []
        for transaction in self.transactions:
            accounts = [entry[0].name for entry in transaction.entries]
            amounts = [entry[1] for entry in transaction.entries]
            debits = [entry[2] for entry in transaction.entries]
            transactions_data.append({
                'Date': transaction.date,
                'Description': transaction.description,
                'Accounts': accounts,
                'Amounts': amounts,
                'Debits': debits
            })

            # Update account balances before saving the transaction
            self.update_account_balances(transaction)

        transactions_df = pd.DataFrame(transactions_data)
        transactions_df.to_csv('transactions.csv', index=False)

    def generate_reports(self):
        # Generate accounts summary
        accounts_data = []
        for account_name, account in self.accounts.items():
            accounts_data.append({'Account': account_name, 'Balance': account.balance})
        accounts_df = pd.DataFrame(accounts_data)

        # Generate transactions DataFrame
        transactions_data = []
        for transaction in self.transactions:
            transaction_entry = {
                'Date': transaction.date,
                'Description': transaction.description
            }
            for account, amount, debit in transaction.entries:
                if debit:
                    account_col = f"{account.name} (Debit)"
                else:
                    account_col = f"{account.name} (Credit)"
                transaction_entry[account_col] = amount
            transactions_data.append(transaction_entry)
        transactions_df = pd.DataFrame(transactions_data)

        # Fill NaN values with 0
        accounts_df = accounts_df.fillna(0)
        transactions_df = transactions_df.fillna(0)

        return accounts_df, transactions_df
    
    def update_account_balances(self, transaction):
        for account, amount, debit in transaction.entries:
            if debit:
                account.balance -= amount
            else:
                account.balance += amount

# Rest of the code remains the same...
def main():
    print("Welcome to the Bookkeeping System!")
    bookkeeping = BookkeepingSystem()

    while True:
        print("\n----------------------")
        print("   Bookkeeping Menu   ")
        print("----------------------")
        print("1. Record Transaction")
        print("2. Add Account")
        print("3. Remove Account")
        print("4. View Accounts")
        print("5. Generate Reports")
        print("6. Edit Transaction")
        print("7. Remove Transaction")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            record_transaction(bookkeeping)

        elif choice == '2':
            account_name = input("Enter account name to add: ")
            bookkeeping.add_account(account_name)
            print(f"Account '{account_name}' added.")

        elif choice == '3':
            account_name = input("Enter account name to remove: ")
            bookkeeping.remove_account(account_name)

        elif choice == '4':
            view_accounts(bookkeeping)

        elif choice == '5':
            generate_reports(bookkeeping)

        elif choice == '6':
            edit_transaction(bookkeeping)

        elif choice == '7':
            remove_transaction(bookkeeping)

        elif choice == '8': 
            print("Exiting the Bookkeeping System.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

def edit_transaction(bookkeeping):
    transaction_index = int(input("Enter transaction index to edit: "))
    bookkeeping.edit_transaction(transaction_index)

def remove_transaction(bookkeeping):
    transaction_index = int(input("Enter transaction index to remove: "))
    bookkeeping.remove_transaction(transaction_index)

def record_transaction(bookkeeping):
    date = input("Enter transaction date (YYYY-MM-DD): ")
    description = input("Enter transaction description: ")
    transaction = bookkeeping.create_transaction(date=date, description=description)

    # Record entries for other accounts (excluding Inventory and Cash)
    while True:
        account_name = input("Enter account name (or 'end' to finish): ")
        if account_name.lower() == 'end':
            break
        elif account_name in bookkeeping.accounts:
            while True:
                try:
                    amount = float(input(f"Enter amount for {account_name}: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            while True:
                debit_credit = input(f"Debit or credit for {account_name}? (d/c): ").lower()
                if debit_credit in ('d', 'c'):
                    debit = debit_credit == 'd'
                    break
                else:
                    print("Invalid input. Please enter 'd' for debit or 'c' for credit.")

            if account_name == 'Inventory':
                # Handle inventory transactions based on debit or credit
                transaction.add_entry(bookkeeping.accounts[account_name], amount, debit=not debit)
            else:
                transaction.add_entry(bookkeeping.accounts[account_name], amount, debit=debit)
        else:
            print(f"Account '{account_name}' not found.")

    total_debits = sum(amount for _, amount, is_debit in transaction.entries if is_debit)
    total_credits = sum(amount for _, amount, is_debit in transaction.entries if not is_debit)

    if total_debits != total_credits:
        print("Transaction doesn't follow double-entry principles. Debits and credits must be equal.")
    else:
        bookkeeping.record_transaction(transaction)
        print("Transaction recorded.")

def view_accounts(bookkeeping):
    print("\nAccounts:")
    for account_name, account in bookkeeping.accounts.items():
        print(f"Account: {account_name}, Balance: {account.balance}")

def generate_reports(bookkeeping):
    accounts_df, transactions_df = bookkeeping.generate_reports()
    print("\nAccounts Summary:")
    print(accounts_df)
    print("\nTransactions:")
    print(transactions_df)

if __name__ == "__main__":
    main()

