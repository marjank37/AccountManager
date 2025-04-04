from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, Listbox
from tkinter.filedialog import asksaveasfilename
import csv

from Entities.login_in import Login
from Entities.account_manager import AccountManager
from Entities.transfer import Transfer

login = Login()
account_manager = AccountManager()
transfer_manager = Transfer(account_manager)

sample_accounts = [
    ("1001", "1466567890", "Marjan Kazemi", 1000000),
    ("1002", "2885678001", "Zahra Hosseini", 950000),
    ("1003", "4446789312", "Kiana Davar", 820000),
    ("1004", "4567756124", "Elnaz Naziri", 770000),
    ("1005", "5679264234", "Rohina Rak", 650000),
    ("1006", "6722270455", "Siamak Ghaderi", 990000),
    ("1007", "7111127656", "Bruno Pidad", 1200000),
    ("1008", "8001294567", "Rasool Asghari", 880000),
    ("1009", "6016645678", "Hassan Asghari", 700000),
    ("1010", "0124163589", "Elnaz Eimandash", 1050000)
]
for acc in sample_accounts:
    account_manager.add_account(*acc)

def show_login_form():
    login_window = Toplevel()
    login_window.title("Login")

    Label(login_window, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(login_window, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        if login.validate(username, password):
            messagebox.showinfo("Login", "Login successful!")
            login_window.destroy()
            show_main_form()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    Button(login_window, text="Login", command=check_login).grid(row=2, column=0, columnspan=2, pady=10)

def show_main_form():
    main_window = Toplevel()
    main_window.title("Account Management")
    main_window.geometry("900x600")

    for i in range(14):
        main_window.grid_rowconfigure(i, weight=1)
    for i in range(3):
        main_window.grid_columnconfigure(i, weight=1)

    Label(main_window, text="Account Number").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    acc_entry = Entry(main_window)
    acc_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    Label(main_window, text="National ID").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    nat_entry = Entry(main_window)
    nat_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    Label(main_window, text="Owner Name").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    owner_entry = Entry(main_window)
    owner_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    Label(main_window, text="Balance").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    bal_entry = Entry(main_window)
    bal_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    listbox = Listbox(main_window)
    listbox.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def refresh_listbox():
        listbox.delete(0, "end")
        for acc in account_manager.account_list:
            listbox.insert("end", f"{acc.account_number} | {acc.national_id} | {acc.owner_name} | {acc.balance}")

    def on_select_account(event):
        selected = listbox.curselection()
        if not selected:
            return
        data = listbox.get(selected[0])
        parts = data.split(" | ")
        if len(parts) == 4:
            acc_entry.delete(0, "end")
            acc_entry.insert(0, parts[0])
            nat_entry.delete(0, "end")
            nat_entry.insert(0, parts[1])
            owner_entry.delete(0, "end")
            owner_entry.insert(0, parts[2])
            bal_entry.delete(0, "end")
            bal_entry.insert(0, parts[3])

    listbox.bind("<Double-Button-1>", on_select_account)

    def create_account():
        try:
            amount = float(bal_entry.get())
            account_manager.add_account(
                acc_entry.get(),
                nat_entry.get(),
                owner_entry.get(),
                amount
            )
            messagebox.showinfo("Success", "Account created successfully.")
            refresh_listbox()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_account():
        listbox.delete(0, "end")
        term = acc_entry.get().strip() or nat_entry.get().strip() or owner_entry.get().strip()
        if not term:
            messagebox.showwarning("Search", "Enter account number, national ID, or name.")
            return
        results = account_manager.search_account(term)
        if not results:
            messagebox.showinfo("Result", "No account found.")
            return
        for acc in results:
            listbox.insert("end", f"{acc.account_number} | {acc.national_id} | {acc.owner_name} | {acc.balance}")

    def update_account():
        try:
            amount = float(bal_entry.get())
            account_manager.update_account(
                acc_entry.get(),
                nat_entry.get(),
                owner_entry.get(),
                amount
            )
            messagebox.showinfo("Success", "Account updated.")
            refresh_listbox()
        except:
            messagebox.showerror("Error", "Balance must be a number.")

    def delete_account():
        account_manager.delete_account(acc_entry.get())
        messagebox.showinfo("Success", "Account deleted.")
        refresh_listbox()

    Label(main_window, text="From Account").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    from_entry = Entry(main_window)
    from_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

    Label(main_window, text="To Account").grid(row=8, column=0, sticky="e", padx=5, pady=5)
    to_entry = Entry(main_window)
    to_entry.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

    Label(main_window, text="Transfer Amount").grid(row=9, column=0, sticky="e", padx=5, pady=5)
    amount_entry = Entry(main_window)
    amount_entry.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

    def transfer_money():
        try:
            amount = float(amount_entry.get())
            result = transfer_manager.transfer(from_entry.get(), to_entry.get(), amount)
            if "Success" in result:
                refresh_listbox()
                messagebox.showinfo("Result", result)
            else:
                messagebox.showerror("Error", result)
        except:
            messagebox.showerror("Error", "Transfer amount must be a number.")

    Button(main_window, text="Create Account", command=create_account).grid(row=4, column=0, sticky="ew", padx=5)
    Button(main_window, text="Search", command=search_account).grid(row=4, column=1, sticky="ew", padx=5)
    Button(main_window, text="Update", command=update_account).grid(row=5, column=0, sticky="ew", padx=5)
    Button(main_window, text="Delete", command=delete_account).grid(row=5, column=1, sticky="ew", padx=5)
    Button(main_window, text="Transfer", command=transfer_money).grid(row=10, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def export_accounts():
        file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Account Number", "National ID", "Owner Name", "Balance"])
            for acc in account_manager.account_list:
                writer.writerow([acc.account_number, acc.national_id, acc.owner_name, acc.balance])
        messagebox.showinfo("Success", "Accounts exported to CSV.")

    def export_transactions():
        acc_number = acc_entry.get()
        if not acc_number:
            messagebox.showerror("Error", "Enter an account number.")
            return
        transactions = account_manager.transactions.get(acc_number)
        if not transactions:
            messagebox.showinfo("Info", "No transactions found for this account.")
            return
        file_path = f"transactions_{acc_number}.csv"
        with open(file_path, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Transaction"])
            for tr in transactions:
                writer.writerow([tr])
        messagebox.showinfo("Success", f"Transactions exported to {file_path}.")

    Button(main_window, text="Export Accounts CSV", command=export_accounts).grid(row=11, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    Button(main_window, text="Export Transactions", command=export_transactions).grid(row=12, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    refresh_listbox()

# -------------------------------
root = Tk()
root.withdraw()
show_login_form()
root.mainloop()
