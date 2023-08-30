import os, mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from prettytable import PrettyTable
from PyInquirer import prompt

# Load environment variables from .env file
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def add_subaccount(account_type, main_account_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        subaccount_name = input(f"Enter the name of the sub-account under '{main_account_name}': ")
        subaccount_code = input(f"Enter the code for the sub-account: ")

        # Generate the formatted sub-account ID
        subaccount_id = f"{account_type[0]}-{subaccount_code}"

        # Get the parent account ID
        query_parent = "SELECT id FROM accounts WHERE name = %s"
        cursor.execute(query_parent, (main_account_name,))
        parent_account_id = cursor.fetchone()[0]

        query = "INSERT INTO accounts (id, name, code, type, parent_account_id) VALUES (%s, %s, %s, %s, %s)"
        values = (subaccount_id, subaccount_name, subaccount_code, account_type, parent_account_id)
        cursor.execute(query, values)
        connection.commit()

        print(f"Sub-account '{subaccount_name}' under '{main_account_name}' added successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def add_account():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        account_type_prompt = {
            "type": "list",
            "message": "Select the account category:",
            "name": "account_type",
            "choices": ["Asset", "Expense", "Revenue", "Cash", "Liability", "Equity"]
        }
        account_type_answer = prompt(account_type_prompt)["account_type"]

        if account_type_answer in ["Asset", "Expense", "Revenue", "Cash", "Liability", "Equity"]:
            account_name = input(f"Enter the name of the {account_type_answer} account: ")
            account_code = input(f"Enter the code for the {account_type_answer} account: ")

            # Generate the formatted account ID
            account_id = f"{account_type_answer[0]}-{account_code}"

            query = "INSERT INTO accounts (id, name, code, type) VALUES (%s, %s, %s, %s)"
            values = (account_id, account_name, account_code, account_type_answer)
            cursor.execute(query, values)
            connection.commit()

            print(f"\n{account_type_answer} account '{account_name}' added successfully with ID: {account_id}.")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def remove_account():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        account_name = input("Enter the name of the account to remove: ")

        if not account_name:
            print("Account removal cancelled.")
            return

        query = "DELETE FROM accounts WHERE name = %s"
        cursor.execute(query, (account_name,))
        connection.commit()

        print(f"Account '{account_name}' removed successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def edit_account():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        account_name = input("Enter the name of the account to edit: ")

        if not account_name:
            print("Account editing cancelled.")
            return

        new_account_name = input("Enter the new name for the account: ")

        if not new_account_name:
            print("Account editing cancelled.")
            return

        query = "UPDATE accounts SET name = %s WHERE name = %s"
        cursor.execute(query, (new_account_name, account_name))
        connection.commit()

        print(f"Account '{account_name}' edited successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_account_name_by_id(account_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT name FROM accounts WHERE id = %s"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result['name'] if result else 'None'

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_accounts():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, name, code, type, parent_account_id FROM accounts"
        cursor.execute(query)
        accounts = cursor.fetchall()

        if not accounts:
            print("\nNo accounts found.")
        else:
            # Create a PrettyTable object
            table = PrettyTable()
            table.field_names = ["ID", "Name", "Code", "Type", "Parent Account"]

            for account in accounts:
                parent_account_id = account.get('parent_account_id', None)
                parent_account_name = get_account_name_by_id(parent_account_id)
                table.add_row([account['id'], account['name'], account['code'], account['type'], parent_account_name])

            print(table)  # Print the formatted table

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




