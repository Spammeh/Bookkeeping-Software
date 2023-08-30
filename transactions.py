import os, re, mysql.connector, uuid
from mysql.connector import Error
from dotenv import load_dotenv
from PyInquirer import prompt, Separator
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

def log_transaction():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        questions = [
            {
                'type': 'input',
                'name': 'new_date',
                'message': 'Date (YYYY-MM-DD):'
            },
            {
                'type': 'input',
                'name': 'new_description',
                'message': 'Description:'
            },
            {
                'type': 'input',
                'name': 'new_amount',
                'message': 'Amount:'
            },
            {
                'type': 'input',
                'name': 'new_category',
                'message': 'Category:'
            },
            {
                'type': 'list',
                'name': 'new_debit_account',
                'message': 'Debit Account:',
                'choices': get_account_names()  # Get account names from the database
            },
            {
                'type': 'list',
                'name': 'new_credit_account',
                'message': 'Credit Account:',
                'choices': get_account_names()  # Get account names from the database
            }
        ]

        answers = prompt(questions)

        new_date = answers['new_date']
        new_description = answers['new_description']
        new_amount = float(answers['new_amount'])
        new_category = answers['new_category']
        new_debit_account = answers['new_debit_account']
        new_credit_account = answers['new_credit_account']

        if not new_date or not new_description or not new_category or not new_debit_account or not new_credit_account:
            print("Transaction logging cancelled.")
            return

        new_id = str(uuid.uuid4())[:8]
        query = "INSERT INTO transactions (id, date, description, amount, category, debit_account, credit_account) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (new_id, new_date, new_description, new_amount, new_category, new_debit_account, new_credit_account)

        cursor.execute(query, values)
        connection.commit()

        print("\nTransaction logged successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Add this helper function to get account names from the accounts table
def get_account_names():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT name FROM accounts"
        cursor.execute(query)
        account_names = [account[0] for account in cursor.fetchall()]
        return account_names

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_transactions():
    try:
        connection = mysql.connector.connect(**db_config)
        query = "SELECT * FROM transactions ORDER BY date"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        transactions = cursor.fetchall()

        if not transactions:
            print("\nNo transactions found.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "Date", "Description", "Amount", "Category", "Debit Account", "Credit Account"]
            for transaction in transactions:
                table.add_row([
                    transaction['id'],
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['category'],
                    transaction['debit_account'],
                    transaction['credit_account']
                ])

            print(table)

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def edit_transaction_by_id(transaction_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT * FROM transactions WHERE id = %s"
        cursor.execute(query, (transaction_id,))
        transaction = cursor.fetchone()

        if not transaction:
            print("\nTransaction not found.")
            return

        date = transaction[1]
        description = transaction[2]
        amount = transaction[3]
        category = transaction[4]
        debit_account = transaction[5]
        credit_account = transaction[6]

        print("\nExisting Transaction:")
        print("ID:", transaction_id)
        print("Date:", date)
        print("Description:", description)
        print("Amount:", amount)
        print("Category:", category)
        print("Debit Account:", debit_account)
        print("Credit Account:", credit_account)
        print("=" * 30)

        edit_choices = [
            {"name": "Date"},
            {"name": "Description"},
            {"name": "Amount"},
            {"name": "Category"},
            {"name": "Debit Account"},
            {"name": "Credit Account"},
            Separator(),
            {"name": "Cancel"}
        ]

        edit_prompt = {
            "type": "checkbox",
            "message": "Choose fields to edit:",
            "name": "fields_to_edit",
            "choices": edit_choices,
            "validate": lambda answer: "You must choose at least one field to edit."
            if len(answer) == 0 else True,
        }

        edit_answers = prompt(edit_prompt)

        fields_to_edit = edit_answers["fields_to_edit"]

        for field in fields_to_edit:
            if field == "Date":
                new_date_input = input("\nEnter new date (YYYY-MM-DD), press Enter to keep existing: ")
                if new_date_input:
                    if re.match(r"\d{4}-\d{2}-\d{2}", new_date_input):
                        date = new_date_input
                    else:
                        print("Invalid date format. Please use YYYY-MM-DD.")
            elif field == "Description":
                new_description_input = input("\nEnter new description, press Enter to keep existing: ")
                if new_description_input:
                    description = new_description_input
            elif field == "Amount":
                new_amount_input = input("\nEnter new amount, press Enter to keep existing: ")
                if new_amount_input:
                    amount = float(new_amount_input)
            elif field == "Category":
                new_category_input = input("\nEnter new category, press Enter to keep existing: ")
                if new_category_input:
                    category = new_category_input
            elif field == "Debit Account":
                new_debit_account_input = input("\nEnter new debit account, press Enter to keep existing: ")
                if new_debit_account_input:
                    debit_account = new_debit_account_input
            elif field == "Credit Account":
                new_credit_account_input = input("\nEnter new credit account, press Enter to keep existing: ")
                if new_credit_account_input:
                    credit_account = new_credit_account_input
            elif field == "Cancel":
                print("\nEditing cancelled.")
                return

        update_query = "UPDATE transactions SET date = %s, description = %s, amount = %s, category = %s, debit_account = %s, credit_account = %s WHERE id = %s"
        cursor.execute(update_query, (date, description, amount, category, debit_account, credit_account, transaction_id))
        connection.commit()

        print("\nChanges made:")
        print("ID:", transaction_id)
        print("Date:", date)
        print("Description:", description)
        print("Amount:", amount)
        print("Category:", category)
        print("Debit Account:", debit_account)
        print("Credit Account:", credit_account)
        print("\nTransaction edited successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_transaction_by_id(transaction_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        delete_prompt = {
            "type": "confirm",
            "message": f"Are you sure you want to delete transaction with ID {transaction_id}?",
            "name": "confirm_delete",
            "default": False,
        }

        confirm_delete = prompt(delete_prompt)["confirm_delete"]

        if not confirm_delete:
            print("\nDeletion cancelled.")
            return

        # Delete ledger entries related to the transaction
        delete_ledger_query = "DELETE FROM ledger WHERE transaction_id = %s"
        cursor.execute(delete_ledger_query, (transaction_id,))

        # Delete the transaction
        delete_transaction_query = "DELETE FROM transactions WHERE id = %s"
        cursor.execute(delete_transaction_query, (transaction_id,))
        connection.commit()

        print("\nTransaction and related ledger entries deleted successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
