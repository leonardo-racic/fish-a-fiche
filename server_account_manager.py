from __future__ import annotations
from account_module import Account
from uuid import uuid4 as get_uuid4



def get_uuid() -> str:
    return str(get_uuid4())


class ServerAccountManager:
    def __init__(self) -> None:
        self.accounts: list[Account] = []
        print(f"ServerAccountManager created.")
    

    def create_account(self, input_username: str, input_password: str) -> Account:
        new_account: Account = Account(input_username, input_password, get_uuid())
        return new_account

    def set_account(self, input_username: str, input_password: str) -> None:
        new_account: Account = self.create_account(input_username, input_password)
        self.accounts.append(new_account)
        print(f"Account with id {new_account.id} created and pushed.")

    
    def get_account_info_by_id(self, account_id: str) -> Account:
        for account in self.accounts:
            if account.id == account_id:
                return account
        print(f"Account with id {account_id} not found.")
        return None
    

    def delete_account(self, account: Account) -> None:
        self.accounts.remove(account)
        print(f"Account with id {account.id} deleted.")
    

    def delete_account_by_id(self, account_id: str) -> None:
        account: Account = self.get_account_info_by_id(account_id)
        if account is not None:
            self.delete_account(account)
            print(f"Account with id {account_id} deleted.")
        else:
            print(f"Account with id {account_id} cannot be delted.")
    

    def get_accounts(self) -> list[Account]:
        return self.accounts
    

    def has_account(self, specific_account: Account) -> bool:
        return specific_account in self.accounts