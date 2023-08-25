import pandas as pd
from bookkeeping import BookkeepingSystem

def generate_accounts_summary(accounts):
    accounts_data = [{'Account': account.name, 'Balance': account.balance} for account in accounts.values()]
    accounts_df = pd.DataFrame(accounts_data)
    return accounts_df

def generate_transactions_report(transactions, accounts):
    transactions_data = []
    for transaction in transactions:
        transaction_entry = {'Date': transaction.date, 'Description': transaction.description}
        for account, amount, debit in transaction.entries:
            account_col = f"{account.name} (Debit)" if debit else f"{account.name} (Credit)"
            transaction_entry[account_col] = amount
        transactions_data.append(transaction_entry)
    
    transactions_df = pd.DataFrame(transactions_data)
    transactions_df = transactions_df.fillna(0)
    return transactions_df
