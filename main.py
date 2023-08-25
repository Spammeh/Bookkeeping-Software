from bookkeeping import BookkeepingSystem
from reconciliation import reconcile_accounts, reconcile_external_transactions, display_reconciliation_reports
from reports import generate_accounts_summary, generate_transactions_report

# Rest of the code remains the same...
def main():
    print("Welcome to the Bookkeeping System!")
    bookkeeping = BookkeepingSystem()

    while True:
        print("\n----------------------")
        print("   Bookkeeping Menu   ")
        print("----------------------")
        print("1. Record Transaction")
        print("2. Edit Transaction")
        print("3. Remove Transaction")
        print("4. View Accounts")
        print("5. Add Account")
        print("6. Remove Account")
        print("7. Generate Reports")
        print("8. Reconcile Transactions")
        print("9. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            record_transaction(bookkeeping)

        elif choice == '2':
            edit_transaction(bookkeeping)

        elif choice == '3':
            remove_transaction(bookkeeping)

        elif choice == '4':
            view_accounts(bookkeeping)

        elif choice == '5':
            account_name = input("Enter account name to add: ")
            bookkeeping.add_account(account_name)
            print(f"Account '{account_name}' added.")

        elif choice == '6':
            account_name = input("Enter account name to remove: ")
            bookkeeping.remove_account(account_name)

        elif choice == '7':
            accounts_summary = generate_accounts_summary(bookkeeping.accounts)
            transactions_report = generate_transactions_report(bookkeeping.transactions, bookkeeping.accounts)
            print("\nAccounts Summary:")
            print(accounts_summary)
            print("\nTransactions Report:")
            print(transactions_report)
        
        elif choice == '8': 
            reconcile_accounts(bookkeeping)

        elif choice == '9': 
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

if __name__ == "__main__":
    main()

