from Entities.account import Account

class AccountManager:
    def __init__(self):
        self.account_list = []
        self.transactions = {}

    def add_account(self, account_number, national_id, owner_name, balance):
        for acc in self.account_list:
            if acc.account_number == account_number:
                raise ValueError("Account number already exists.")
        new_account = Account(account_number, national_id, owner_name, balance)
        self.account_list.append(new_account)
        self.transactions[account_number] = []

    def search_account(self, term):
        term = str(term).strip()
        return [
            acc for acc in self.account_list
            if term == str(acc.account_number) or
               term == str(acc.national_id) or
               term.lower() in acc.owner_name.lower()
        ]

    # in this model for searching you should enter completed national id, if we want to search based on the
    #some part of national id
    #def search_account(self, term):
    #term = str(term).strip()
    #return [
        #acc for acc in self.account_list
        #if term in str(acc.account_number) or
           #term in str(acc.national_id) or
           #term.lower() in acc.owner_name.lower()]



    def update_account(self, account_number, new_national_id, new_owner_name, new_balance):
        for acc in self.account_list:
            if acc.account_number == account_number:
                acc.national_id = new_national_id
                acc.owner_name = new_owner_name
                acc.balance = new_balance
                self.transactions[account_number].append(
                    f"Account updated: {new_owner_name}, Balance: {new_balance}"
                )
                return
        raise ValueError("Account not found.")

    def delete_account(self, account_number):
        self.account_list = [acc for acc in self.account_list if acc.account_number != account_number]
        self.transactions.pop(account_number, None)
