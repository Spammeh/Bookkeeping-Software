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