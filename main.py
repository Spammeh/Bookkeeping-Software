import os, re, mysql.connector, csv
from PyInquirer import prompt, Separator
from dotenv import load_dotenv
import ledger, transactions, accounts

# Load environment variables from .env file
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# ... Other functions ...

# Inside the main() function
def main():
    print("Bookkeeping Application")

    while True:
        questions = [
            {
                'type': 'list',
                'name': 'choice',
                'message': 'Select an option:',
                'choices': [
                    'Log Transaction',
                    'Edit Transaction by ID',
                    'Delete Transaction by ID',
                    'View Accounts',
                    'View Ledger',
                    'View Transactions',
                    'Add Account', 
                    'Remove Account', 
                    'Edit Account',
                    'Export Ledger to CSV',
                    'Exit'
                ]
            }
        ]
        
        answer = prompt(questions)
        choice = answer['choice']

        if choice == 'Log Transaction':
            transactions.log_transaction()
            ledger.generate_ledger_entries()

        elif choice == 'Edit Transaction by ID':
            transaction_id = input("\nEnter the ID of the transaction to edit: ")  # Keep transaction ID as string
            transactions.edit_transaction_by_id(transaction_id)
            ledger.generate_ledger_entries()  # Generate ledger entries after editing transaction

        elif choice == 'Delete Transaction by ID':
            transaction_id = input("\nEnter the ID of the transaction to delete: ")
            transactions.delete_transaction_by_id(transaction_id)
            ledger.generate_ledger_entries()  # Generate ledger entries after deleting transaction

        elif choice == 'View Transactions':
            transactions.view_transactions()

        elif choice == 'View Ledger':  # Add code to view ledger entries
            ledger.view_ledger()

        elif choice == 'Add Account':
            accounts.add_account()

        elif choice == 'Remove Account':
            accounts.remove_account()

        elif choice == 'Edit Account':
            accounts.edit_account()

        elif choice == 'View Accounts':
            accounts.view_accounts()

        elif choice == 'Export Ledger to CSV':
            filename = input("Enter the filename for the CSV export (e.g., ledger): ")
            if not filename.endswith('.csv'):
                filename += '.csv'
            ledger.export_ledger_to_csv(filename)

        elif choice == 'Exit':
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
