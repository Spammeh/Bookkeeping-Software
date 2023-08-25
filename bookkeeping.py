import pandas as pd
import csv
from accounts import Account
from transactions import Transaction

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
            df = pd.read_csv('files/accounts.csv')
            for _, row in df.iterrows():
                self.accounts[row['Account']] = Account(row['Account'])
        except FileNotFoundError:
            pass

    def save_accounts_to_csv(self):
        accounts_data = [{'Account': account.name, 'Balance': account.balance} for account in self.accounts.values()]
        accounts_df = pd.DataFrame(accounts_data)
        accounts_df.to_csv('files/accounts.csv', index=False)

    def save_to_csv(self, transaction):
        accounts_data = [{'Account': account.name, 'Balance': account.balance} for account in self.accounts.values()]
        accounts_df = pd.DataFrame(accounts_data)
        accounts_df.to_csv('files/accounts.csv', index=False)

    def load_transactions_from_csv(self):
        try:
            transactions_df = pd.read_csv('files/transactions.csv')
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
        transactions_df.to_csv('files/transactions.csv', index=False)

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