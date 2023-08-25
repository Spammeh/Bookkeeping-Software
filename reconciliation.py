import pandas as pd
from bookkeeping import BookkeepingSystem

def reconcile_accounts(bookkeeping):
    print("\nReconciliation Menu")
    print("--------------------")

    # Prompt user to choose a CSV file for reconciliation
    csv_file_path = input("Enter the path to the CSV file for reconciliation: ")

    # Load the external transactions from the chosen CSV file
    external_transactions = []
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                ext_date, ext_description, ext_amount, _ = row
                if ext_amount:  # Check if ext_amount is not empty
                    external_transactions.append((ext_date, ext_description, float(ext_amount)))
    except FileNotFoundError:
        print("CSV file not found.")
        return

    # Perform reconciliation
    reconciled_transactions = reconcile_external_transactions(external_transactions, bookkeeping)

    # Display the reconciliation reports
    display_reconciliation_reports(external_transactions, reconciled_transactions)


def reconcile_external_transactions(external_transactions, bookkeeping):
    reconciled_transactions = []
    for ext_date, ext_description, ext_amount in external_transactions:
        matching_transactions = []

        for transaction in bookkeeping.transactions:
            for account, amount, debit in transaction.entries:
                if account.name == "Bank Account" and amount == ext_amount:
                    matching_transactions.append((transaction, amount))

        if matching_transactions:
            print(f"External Transaction: {ext_date} - {ext_description} - {ext_amount}")
            print("Matching Recorded Transactions:")
            for idx, (trans, amount) in enumerate(matching_transactions):
                print(f"{idx + 1}. {trans.date} - {trans.description} - {amount}")
            
            choice = input("Enter the number of the matching transaction (or 'n' for none): ")
            if choice.isdigit() and int(choice) in range(1, len(matching_transactions) + 1):
                chosen_trans, chosen_amount = matching_transactions[int(choice) - 1]
                reconciled_transactions.append((ext_date, ext_description, ext_amount, chosen_trans.date, chosen_trans.description, chosen_amount))
                print("Transaction reconciled.")
            else:
                print("No transaction reconciled.")
    
    return reconciled_transactions

def display_reconciliation_reports(external_transactions, reconciled_transactions):
    print("\nReconciliation Reports")
    print("----------------------")

    # Display external transactions
    print("\nExternal Transactions:")
    print("----------------------")
    print("Date\t\t\tDescription\t\t\tAmount")
    print("-----------------------------------------------")
    for ext_date, ext_description, ext_amount in external_transactions:
        print(f"{ext_date}\t{ext_description}\t{ext_amount:.2f}")

    # Display reconciled transactions
    print("\nReconciled Transactions:")
    print("------------------------")
    print("External Date\t\tExternal Description\t\tExternal Amount\t\tMatched Date\t\tMatched Description\t\tMatched Amount")
    print("------------------------------------------------------------------------------------------------------------------------")
    for rec_date, rec_description, rec_amount, matched_date, matched_description, matched_amount in reconciled_transactions:
        print(f"{rec_date}\t{rec_description}\t{rec_amount:.2f}\t\t{matched_date}\t{matched_description}\t{matched_amount:.2f}")

    # ... (you can add more reports if needed)