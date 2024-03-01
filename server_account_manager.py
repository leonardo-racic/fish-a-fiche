# The first import module is only to guarantee a secure variable typing.
from __future__ import annotations
from account_module import Account
from json import loads as load_json, dumps as to_json
from flask import request
from terminal_log import inform
import hashlib


def get_hash(this_text: str) -> str:
    return hashlib.sha256(this_text.encode()).hexdigest()


def read_accounts_json() -> dict:
    with open("accounts.json", "r") as f:
        try:
            accounts_json: dict = load_json(f.read())["accounts"]
            accounts_dict: dict = {}
            for token, account_info in accounts_json.items():
                new_account: Account = Account(
                    account_info["username"],
                    account_info["password"],
                    account_info["profile_picture"],
                    account_info["description"]
                )
                accounts_dict[token] = new_account
            return accounts_dict
        except Exception:
            with open("accounts.json", "w") as f:
                f.write("{\n    \"accounts\":{}\n}")
            return []
        
    


class ServerAccountManager:
    def __init__(self) -> None:
        self.accounts: dict = read_accounts_json()

    
    def get_all_account_info(self) -> list:
        return list(self.get_accounts().values())


    def create_account(self, input_username: str, input_password: str, description: str = "", profile_picture: str = "") -> Account:
        new_account: Account = Account(input_username, get_hash(input_password), profile_picture, description)
        inform(f"{new_account} is being created")
        with open("accounts.json", "r") as f:
            json_data: dict = load_json(f.read())
        json_data["accounts"][new_account.get_id()] = new_account.get_info()
        with open("accounts.json", "w") as f:
            f.write(to_json(json_data, indent=4))
        self.accounts = read_accounts_json()
        return new_account


    def get_account_by_token(self, token: str) -> tuple[Account, bool]:
        if token not in self.get_accounts():
            return (None, False)
        return (self.get_accounts[token], True)
    

    def delete_account(self, account: Account) -> None:
        self.get_accounts().pop(account.get_id())
        with open("accounts.json", "r") as f:
            json_data: dict = load_json(f.read())["accounts"]
        json_data.pop(account.get_id())
        with open("accounts.json", "w") as f:
            f.write(to_json(json_data, indent=4))
        self.accounts = read_accounts_json()


    def get_accounts(self) -> dict:
        self.accounts = read_accounts_json()
        return self.accounts
    

    def has_account(self, specific_account: Account) -> bool:
        return specific_account in self.get_all_account_info()
    

    def has_account_username(self, current_username: str) -> bool:
        for account_info in self.get_all_account_info():
            if account_info["username"] == current_username:
                return True
        return False


    def is_login_valid(self, username: str, password: str) -> tuple[bool, bool, bool]:
        is_input_valid: bool = username != "" and password != ""
        if not is_input_valid:
            return (False, False, False)
         
        target_account: Account; username_exists: bool
        target_account, username_exists = self.get_account_by_username(username)
        password_hash: str = get_hash(password)
        password_correct: bool = target_account.check_password(password_hash) if username_exists else False
        return (is_input_valid, username_exists, password_correct)


    def is_sign_up_input_valid(self, username: str, password: str) -> bool:
        if not self.is_username_valid(username):
            return False
        elif password == "":
            return False
        return True
    

    def get_user_account_info(self) -> tuple[dict, bool]:
        user_account: Account; user_account_exists: bool
        user_account, user_account_exists = self.get_user_account()
        if not user_account_exists:
            return ({}, False)
        return (user_account.get_info(), True)


    def get_user_account(self) -> tuple[Account, bool]:
        account_token: str = load_json(request.cookies.get("account-token", "{}"))
        user_account: Account; user_account_exists: bool
        user_account, user_account_exists = self.get_account_by_token(account_token)
        if not user_account_exists:
            return (None, False)
        return (user_account, True)
    

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
        return True
    
    
    def modify_profile(self, new_image_input: str, description_input: str, username_input: str) -> None:
        account_info: dict 
        account_info, _ = self.get_user_account_info()
        if account_info is not None:
            with open("accounts.json") as f:
                data: dict = load_json(f.read())["accounts"]
            for current_account_info in data.values():
                if current_account_info["username"] == account_info["username"]:
                    current_account_info["profile_picture"] = new_image_input
                    current_account_info["description"] = description_input
                    current_account_info["username"] = username_input
                    break
            with open("accounts.json", "w") as f:
                f.write(to_json(data, indent=4))
            self.accounts = read_accounts_json()



if __name__ == "__main__":
    s: ServerAccountManager = ServerAccountManager()
    s.create_account("User2332", "€uehfiuzhefoizef")
    