class Transfer:
    def __init__(self, account_manager):
        self.account_manager = account_manager

    def transfer(self, from_account_number, to_account_number, amount):
        if from_account_number == to_account_number:
            return

        from_acc = None
        to_acc = None

        for acc in self.account_manager.account_list:
            if acc.account_number == from_account_number:
                from_acc = acc
            elif acc.account_number == to_account_number:
                to_acc = acc

        if not from_acc or not to_acc:
            return "can not find any account"

        if from_acc.balance < amount:
            return "the amount you have is not enough"

        from_acc.balance -= amount
        to_acc.balance += amount

        self.account_manager.transactions[from_account_number].append(f"payment {amount}  to account {to_account_number}")
        self.account_manager.transactions[to_account_number].append(f"Deposit  {amount} from account {from_account_number}")

        return "Success: successfully transferred"

