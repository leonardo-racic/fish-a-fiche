# The first import module is only to guarantee a secure variable typing.
from __future__ import annotations
from account_module import Account
from json import loads as load_json, dumps as to_json
from flask import request
import hashlib


def get_hash(this_text: str) -> str:
    return hashlib.sha256(this_text.encode()).hexdigest()


def read_accounts_json() -> list[Account]:
    with open("accounts.json", "r") as f:
        try:
            accounts_json_list: list[dict] = load_json(f.read())
            account_list: list[Account] = []
            for account_info in accounts_json_list:
                new_account: Account = Account(
                    account_info["username"],
                    account_info["password"],
                    account_info["profile_picture"],
                    account_info["description"]
                )
                account_list.append(new_account)
            return account_list
        except Exception:
            with open("accounts.json", "w") as f:
                f.write("[]")
            return []
        
    


class ServerAccountManager:
    def __init__(self) -> None:
        self.accounts: list[Account] = read_accounts_json()
        print(f"ServerAccountManager created.")


    def create_account(self, input_username: str, input_password: str, description: str = "", profile_picture: str = "") -> Account:
        new_account: Account = Account(input_username, get_hash(input_password), profile_picture, description)
        with open("accounts.json", "r") as f:
            json_data: list[dict] = load_json(f.read())
        json_data.append(new_account.get_info())
        with open("accounts.json", "w") as f:
            f.write(to_json(json_data, indent=4))
        self.accounts = read_accounts_json()
        return new_account


    def set_account(self, input_username: str, input_password: str, description: str, profile_picture: str) -> None:
        _new_account: Account = self.create_account(input_username, input_password, description, profile_picture)
        print(f"Account with username {input_username} created.")
    

    def get_account_info_by_username(self, account_username: str) -> tuple[dict, bool]:
        a: Account; username_exists: bool
        a, username_exists = self.get_account_by_username(account_username)
        if username_exists:
            return (a.get_info(), True)
        return (None, False)

    

    def get_account_by_username(self, account_username: str) -> tuple[Account, bool]:
        for account in self.accounts:
            if account.get_username() == account_username:
                return (account, True)
        return (None, False)

    

    def delete_account(self, account: Account) -> None:
        self.accounts.remove(account)
        with open("accounts.json", "r") as f:
            json_data: list[dict] = load_json(f.read())
        json_data.remove(account.get_info())
        with open("accounts.json", "w") as f:
            f.write(to_json(json_data, indent=4))
        self.accounts = read_accounts_json()
        print(f"Account with username {account.get_username()} deleted.")
    

    def delete_account_by_username(self, account_username: str) -> None:
        account: Account
        account, exists = self.get_account_by_username(account_username)
        if exists:
            self.delete_account(account)
            print(f"Account with username {account_username} deleted.")
        else:
            print(f"Account with username {account_username} cannot be deleted.")


    def get_accounts(self) -> list[Account]:
        self.accounts = read_accounts_json()
        return self.accounts
    

    def has_account(self, specific_account: Account) -> bool:
        return specific_account in self.get_accounts()
    

    def has_account_username(self, current_username: str) -> bool:
        username_exists: bool
        _, username_exists = self.get_account_info_by_username(current_username)
        print(current_username, username_exists)
        return username_exists


    def is_login_valid(self, username: str, password: str) -> tuple[bool, bool, bool]:
        is_input_valid: bool = username != "" and password != ""
        if not is_input_valid:
            print(f"The login input is not valid.")
            return (False, False, False)
         
        target_account: Account; username_exists: bool
        target_account, username_exists = self.get_account_by_username(username)
        password_hash: str = get_hash(password)
        password_correct: bool = target_account.check_password(password_hash) if username_exists else False
        if username_exists:
            if password_correct:
                print(f"Login is successfull.")
            else:
                print(f"Login is not successfull : the password is incorrect.")
        else:
            print(f"Login is not successfull : the account with username {username} does not exist.")
        return (is_input_valid, username_exists, password_correct)


    def is_sign_up_input_valid(self, username: str, password: str) -> bool:
        if not self.is_username_valid(username):
            return False
        elif password == "":
            return False
        return True
    

    def get_user_account_info(self) -> tuple[dict, bool]:
        account_info_cookie: dict = load_json(request.cookies.get("account-info", "{}"))
        user_account_info: dict; username_exists: bool
        user_account_info, username_exists = self.get_account_info_by_username(account_info_cookie.get("username", ""))
        if not username_exists:
            return ({}, False)
        return self.get_account_info_by_username(user_account_info["username"])


    def get_user_account(self) -> Account:
        account_info: dict
        account_info, _ = self.get_user_account_info()
        if account_info is not None:
            return Account(
                account_info["username"],
                account_info["password"],
                account_info["profile_picture"],
                account_info["description"],
            )
        else:
            return None
    

    def is_user_logged_in(self) -> bool:
        account_info: dict
        account_info, _ = self.get_user_account_info()
        return account_info != {}


    def is_username_valid(self, username: str, check_if_username_exists: bool = False) -> bool:
        if username == "":
            return False
        elif "/" in username:
            return False
        elif self.has_account_username(username) and check_if_username_exists:
            return False
        print(f"username {username} is valid")
        return True
    
    
    def modify_profile(self, new_image_input: str, description_input: str, username_input: str) -> None:
        account_info: dict 
        account_info, _ = self.get_user_account_info()
        if account_info is not None:
            with open("accounts.json") as f:
                data = load_json(f.read())
            for current_account_info in data:
                if current_account_info["username"] == account_info["username"]:
                    current_account_info["profile_picture"] = new_image_input
                    current_account_info["description"] = description_input
                    current_account_info["username"] = username_input
                    break
            with open("accounts.json", "w") as f:
                f.write(to_json(data, indent=4))
            self.accounts = read_accounts_json()
        else:
            print(f"Account info cannot be modified.")


if __name__ == "__main__":
    print(read_accounts_json())