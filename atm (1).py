import random
options = ["create account", "login", "exit"]
# Reading the stored users.txt
with open("users.txt", "r") as file:
    users_txt = file.read()
users_txt = users_txt.strip("users = ")
users_dict = eval(users_txt)


def create_account():
    name = " "
    
    while not name.isalpha():
        name = input("Enter your name: ")
        if not name.isalpha():
            print("Don't add characters to your name")


    deposit = 0
    while deposit < 50:
        deposit = float(input("Enter the initial deposit amount (more than 50 PKR): "))
        if deposit < 50:
            print("Initial deposit must be at least 50 PKR.")

    pin_code_str = "0"
    while len(pin_code_str) != 4 or not pin_code_str.isdigit():
        pin_code_str = input("Enter a 4-digit PIN code: ")
        if len(pin_code_str) != 4 or not pin_code_str.isdigit():
            print("PIN code must be a 4-digit number.")  

    account_number = str(random.randint(1000_000_0000, 9999_999_9999))
    username_string = str(random.randint(123,999))
    username = name + username_string
    status = "ACTIVE"
    currency = "PKR"
    statement = [f"Deposited of PKR {deposit}."]

    new_user = { account_number : {
        "name": name,
        "username": username,
        "pin_code": pin_code_str,
        "status": status,
        "balance_amount": deposit,
        "currency": currency,
        "statement": statement 
        } }
    return new_user


def user_adder(new_user):
    try:
        users_dict.update(new_user)
        with open("users.txt", "w") as file:
            file.write(str(users_dict))
    except Exception as e:
        pass



# Function to check in (log in) and access account options
def Check_in():
    username = input("Enter your account number or username: ")
    if username.isdigit():
        account_num = username
    else:
        available_users = [user_data for user_data in users_dict]
        for values in available_users:
            if users_dict[values]['username'] == username:
                current_user_dict = users_dict[values]
                account_num = values
   
 
    pin_attempt = 0

    while pin_attempt < 3:
        pin_code = input("Enter your PIN code: ")
        if pin_code == users_dict[account_num]["pin_code"]:
            break
        elif pin_attempt == 2:
            users_dict[account_num]["status"] = "BLOCKED"
            return
        else:
            pin_attempt += 1

    print("\n1. Account Detail\n2. Deposit\n3. Withdraw\n4. Update pin\n5. Check Statement\n6. Logout")

    while True:
        choice = input("Select an option: ")

        if choice == "1":
            print("Name:", users_dict[account_num]["name"])
            print("Username:", users_dict[account_num]["username"])
            print("Status:", users_dict[account_num]["status"])
            print(f"Balance: {users_dict[account_num]['balance_amount']} {users_dict[account_num]['currency']}")

        elif choice == "2":
            deposit_amount = float(input("Enter the deposit amount: "))
            if deposit_amount >= 50:
                updated_user_details = users_dict
                current_balance = updated_user_details[account_num]["balance_amount"]
                current_balance = current_balance
                updated_user_details[account_num]["statement"].append(f"Deposited of PKR {deposit_amount}.")
                print("Deposit successful.")
                with open("users.txt", "w") as file:
                    updated_user_details = str(updated_user_details)
                    file.write(updated_user_details)
            else:
                print("Deposit amount must be at least 50 PKR.")

        elif choice == "3":
            if users_dict[account_num]["status"] == "BLOCKED":
                print("Blocked users cannot withdraw unless status is ACTIVE.")
            else:
                withdrawal_amount = float(input("Enter the withdrawal amount: "))
                tax = withdrawal_amount * 0.01
                total_withdrawal = withdrawal_amount + tax

                if total_withdrawal <= users_dict[account_num]["balance_amount"]:
                    users_dict[account_num]["balance_amount"] -= total_withdrawal
                    users_dict[account_num]["statement"].append(f"Withdrawal of PKR {withdrawal_amount}.")
                    updated_user_details = users_dict
                    with open("users.txt", "w") as file:
                        updated_user_details = str(updated_user_details)
                        file.write(updated_user_details)
                    print("Withdrawal successful.")
                else:
                    print("Insufficient balance.")

        elif choice == "4":
            old_pin = input("Enter your old PIN code: ")
            if old_pin == users_dict[account_num]["pin_code"]:
                new_pin = input("Enter your new 4-digit PIN code: ")
                if len(new_pin) == 4 and new_pin.isdigit():
                    updated_user_details = users_dict
                    updated_user_details[account_num]["pin_code"] = new_pin
                    with open("users.txt", "w") as file:
                        updated_user_details = str(updated_user_details)
                        file.write(updated_user_details)
                    print("PIN code updated successfully.")
                else:
                    print("New PIN code must be a 4-digit number.")
            else:
                print("Incorrect old PIN code.")

        elif choice == "5":
            with open(f"{username}_statement") as statement_file:
                for entry in users_dict[account_num]["statement"]:
                    statement_file.write(entry + "\n")
                print("Statement saved to file.")

        elif choice == "6":
            print("Logged out successfully.")
            return

        else:
            print("Invalid option.")


while True:
    for option_num, option in enumerate(options):
        print(option_num, option)
    action = input("Enter choice\n")
    if action == "0":
        user_adder(create_account)
    elif action == "1":
        Check_in()
    elif action == "2":
        break

