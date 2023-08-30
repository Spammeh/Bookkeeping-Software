import os, mysql.connector, csv
from mysql.connector import Error
from dotenv import load_dotenv
from prettytable import PrettyTable

# Load environment variables from .env file
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def generate_ledger_entries():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Retrieve transactions that haven't been processed for the ledger
        query = "SELECT * FROM transactions WHERE processed_for_ledger = 0"
        cursor.execute(query)
        transactions = cursor.fetchall()

        for transaction in transactions:
            transaction_id = transaction[0]
            date = transaction[1]
            description = transaction[2]
            debit_account = transaction[5]
            credit_account = transaction[6]
            amount = transaction[3]

            # Create a new ledger entry for the debit side
            debit_ledger_query = "INSERT INTO ledger (transaction_id, date, description, debit_account, credit_account, amount) VALUES (%s, %s, %s, %s, %s, %s)"
            debit_ledger_values = (transaction_id, date, description, debit_account, credit_account, amount)
            cursor.execute(debit_ledger_query, debit_ledger_values)

            # Create a new ledger entry for the credit side
            credit_ledger_query = "INSERT INTO ledger (transaction_id, date, description, debit_account, credit_account, amount) VALUES (%s, %s, %s, %s, %s, %s)"
            credit_ledger_values = (transaction_id, date, description, credit_account, debit_account, amount)
            cursor.execute(credit_ledger_query, credit_ledger_values)

            # Mark the transaction as processed for the ledger
            update_query = "UPDATE transactions SET processed_for_ledger = 1 WHERE id = %s"
            cursor.execute(update_query, (transaction_id,))
        
        connection.commit()
        print("Ledger entries generated successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def view_ledger():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ledger"
        cursor.execute(query)
        ledger_entries = cursor.fetchall()

        if not ledger_entries:
            print("\nNo ledger entries found.")
        else:
            table = PrettyTable()
            table.field_names = ["Transaction ID", "Date", "Description", "Debit Account", "Credit Account", "Amount"]
            for entry in ledger_entries:
                table.add_row([
                    entry['transaction_id'],
                    entry['date'],
                    entry['description'],
                    entry['debit_account'],
                    entry['credit_account'],
                    entry['amount']
                ])

            print(table)

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def export_ledger_to_csv(filename):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ledger"
        cursor.execute(query)
        ledger_entries = cursor.fetchall()

        if not ledger_entries:
            print("\nNo ledger entries to export.")
            return

        with open(filename, 'w', newline='') as csv_file:
            fieldnames = ["Transaction ID", "Date", "Description", "Debit Account", "Credit Account", "Amount"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for entry in ledger_entries:
                writer.writerow({
                    "Transaction ID": entry['transaction_id'],
                    "Date": entry['date'],
                    "Description": entry['description'],
                    "Debit Account": entry['debit_account'],
                    "Credit Account": entry['credit_account'],
                    "Amount": entry['amount']
                })

        print(f"Ledger entries exported to '{filename}' successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()