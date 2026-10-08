"""
ATM Prototype - Educational simulation (not connected to real banks).
"""

from datetime import datetime

# Mock accounts (fictional data only)
ACCOUNTS = {
    "100001": {"name": "Alice Johnson", "pin": "1234", "balance": 150000.00, "locked": False, "history": []},
    "100002": {"name": "Bob Smith", "pin": "5678", "balance": 85000.00, "locked": False, "history": []},
    "100003": {"name": "Carol Williams", "pin": "9012", "balance": 220000.00, "locked": False, "history": []},
}

MAX_PIN_ATTEMPTS = 3
MAX_WITHDRAWAL = 50000.00


def money(amount):
    """Format amount as currency."""
    return f"NGN {amount:,.2f}"


def log(account, tx_type, amount, status):
    """Save a transaction to the account history."""
    account["history"].append({
        "type": tx_type,
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
    })


def get_amount(prompt):
    """Ask for a positive number. Returns None if input is invalid."""
    try:
        amount = float(input(prompt).strip())
        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return None
        return round(amount, 2)
    except ValueError:
        print("Error: Please enter a valid number.")
        return None


def login():
    """Log in with account number and PIN. Returns (account_id, account) or (None, None)."""
    print("\n================================")
    print("        WELCOME TO ATM")
    print("================================")

    acc_id = input("\nEnter Account Number: ").strip()
    if acc_id not in ACCOUNTS:
        print("Error: Account not found.")
        return None, None

    account = ACCOUNTS[acc_id]

    if account["locked"]:
        print("Error: Account is locked. Contact your bank.")
        return None, None

    for attempt in range(MAX_PIN_ATTEMPTS):
        pin = input("Enter PIN: ").strip()
        if pin == account["pin"]:
            print(f"\nAuthentication successful. Welcome, {account['name']}!")
            return acc_id, account

        left = MAX_PIN_ATTEMPTS - attempt - 1
        if left > 0:
            print(f"Incorrect PIN. {left} attempt(s) left.")
        else:
            account["locked"] = True
            print("Error: Account locked after 3 failed attempts.")
            log(account, "LOGIN", 0, "FAILED")

    return None, None


def show_menu():
    """Print the main ATM menu."""
    print("\n----------- ATM MENU -----------")
    print("1. Check Balance")
    print("2. Withdraw Money")
    print("3. Deposit Money")
    print("4. Transfer Money")
    print("5. Change PIN")
    print("6. Transaction History")
    print("7. Exit / Eject Card")
    print("--------------------------------")


def check_balance(account):
    print(f"\nBalance: {money(account['balance'])}")
    log(account, "BALANCE", 0, "SUCCESS")


def withdraw(account):
    print(f"\nAvailable: {money(account['balance'])}")
    amount = get_amount("Enter withdrawal amount: ")
    if amount is None:
        return

    if amount > MAX_WITHDRAWAL:
        print(f"Error: Max withdrawal is {money(MAX_WITHDRAWAL)}.")
        log(account, "WITHDRAWAL", amount, "FAILED")
        return

    if amount > account["balance"]:
        print("Error: Insufficient funds.")
        log(account, "WITHDRAWAL", amount, "FAILED")
        return

    account["balance"] -= amount
    print(f"Success! Collected {money(amount)}. Balance: {money(account['balance'])}")
    log(account, "WITHDRAWAL", amount, "SUCCESS")


def deposit(account):
    amount = get_amount("Enter deposit amount: ")
    if amount is None:
        return

    account["balance"] += amount
    print(f"Success! Deposited {money(amount)}. Balance: {money(account['balance'])}")
    log(account, "DEPOSIT", amount, "SUCCESS")


def transfer(account, acc_id):
    to_id = input("Enter recipient account number: ").strip()

    if to_id == acc_id:
        print("Error: Cannot transfer to your own account.")
        return
    if to_id not in ACCOUNTS:
        print("Error: Recipient not found.")
        log(account, "TRANSFER", 0, "FAILED")
        return

    amount = get_amount("Enter transfer amount: ")
    if amount is None:
        return
    if amount > account["balance"]:
        print("Error: Insufficient funds.")
        log(account, "TRANSFER", amount, "FAILED")
        return

    recipient = ACCOUNTS[to_id]
    account["balance"] -= amount
    recipient["balance"] += amount
    print(f"Success! Sent {money(amount)} to {recipient['name']}.")
    log(account, f"TRANSFER OUT to {to_id}", amount, "SUCCESS")
    log(recipient, f"TRANSFER IN from {acc_id}", amount, "SUCCESS")


def change_pin(account):
    current = input("Enter current PIN: ").strip()
    if current != account["pin"]:
        print("Error: Wrong PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm = input("Confirm new PIN: ").strip()

    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("Error: PIN must be 4 digits.")
        return
    if new_pin != confirm:
        print("Error: PINs do not match.")
        return

    account["pin"] = new_pin
    print("Success! PIN updated.")
    log(account, "PIN CHANGE", 0, "SUCCESS")


def show_history(account):
    history = account["history"]
    if not history:
        print("\nNo transactions yet.")
        return

    print("\n--- Recent Transactions ---")
    for tx in history[-10:]:
        amt = money(tx["amount"]) if tx["amount"] else "-"
        print(f"{tx['time']} | {tx['type']} | {amt} | {tx['status']}")


def main():
    while True:
        acc_id, account = login()
        if account is None:
            again = input("\nTry again? (yes/no): ").strip().lower()
            if again not in ("yes", "y"):
                break
            continue

        # Main menu loop for this session
        while True:
            show_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                check_balance(account)
            elif choice == "2":
                withdraw(account)
            elif choice == "3":
                deposit(account)
            elif choice == "4":
                transfer(account, acc_id)
            elif choice == "5":
                change_pin(account)
            elif choice == "6":
                show_history(account)
            elif choice == "7":
                print(f"\nGoodbye, {account['name']}! Card ejected.")
                log(account, "LOGOUT", 0, "SUCCESS")
                break
            else:
                print("Error: Choose a number from 1 to 7.")

            if choice != "7":
                input("\nPress Enter to continue...")

        again = input("\nStart another session? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("ATM shutting down. Goodbye!")
            break


if __name__ == "__main__":
    main()
