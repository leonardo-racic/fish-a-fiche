# The first import module is only to guarantee a secure variable typing.
from __future__ import annotations
from account_module import Account
from uuid import uuid4 as get_uuid4
import hashlib


def get_hash(this_text: str) -> str:
    return hashlib.sha256(this_text.encode()).hexdigest()



def get_uuid() -> str:
    return str(get_uuid4())


class ServerAccountManager:
    def __init__(self) -> None:
        self.accounts: list[Account] = []
        print(f"ServerAccountManager created.")


    def create_account(self, input_username: str, input_password: str) -> Account:
        new_account: Account = Account(input_username, get_hash(input_password), get_uuid())
        return new_account


    def set_account(self, input_username: str, input_password: str) -> None:
        new_account: Account = self.create_account(input_username, input_password)
        self.accounts.append(new_account)
        print(f"Account with username {input_username} created.")
    

    def get_account_info_by_username(self, account_username: str) -> Account:
        for account in self.accounts:
            if account.get_username() == account_username:
                return account
        print(f"Account with username {account_username} not found.")
        
    

    def delete_account(self, account: Account) -> None:
        self.accounts.remove(account)
        print(f"Account with username {account.get_username()} deleted.")
    

    def delete_account_by_username(self, account_username: str) -> None:
        account: Account = self.get_account_info_by_username(account_username)
        if account is not None:
            self.delete_account(account)
            print(f"Account with username {account_username} deleted.")
        else:
            print(f"Account with username {account_username} cannot be deleted.")


    def get_accounts(self) -> list[Account]:
        return self.accounts
    

    def has_account(self, specific_account: Account) -> bool:
        return specific_account in self.get_accounts()
    

    def has_account_username(self, current_username: str) -> bool:
        current_account: Account = self.get_account_info_by_username(current_username)
        if current_account is not None:
            return True
        return False


    def is_login_valid(self, username: str, password: str) -> tuple[bool, bool, bool]:
        is_input_valid: bool = username != "" and password != ""
        if not is_input_valid:
            print(f"The login input is not valid.")
            return (False, False, False)
         
        password_hash: str = get_hash(password)
        target_account: Account = self.get_account_info_by_username(username)
        username_exists: bool = target_account is not None
        password_correct: bool = target_account.check_password(password_hash) if username_exists else False
        if username_exists:
            if password_correct:
                print(f"Login is successfull.")
            else:
                print(f"Login is not successfull : the password is incorrect.")
        else:
            print(f"Login is not successfull : the account with username {username} does not exist.")
        return (is_input_valid, username_exists, password_correct)


    @staticmethod
    def is_sign_up_input_valid(username: str, password: str) -> bool:
        if username == "" or password == "":
            return False
        return True