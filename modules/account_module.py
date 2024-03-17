from uuid import uuid4 as get_uuid
from .cheat_sheet_module import CheatSheet, json_to_cheat_sheet
from typing import List


class Account:
    def __init__(
        self,
        username: str,
        password: str,
        profile_picture: str = "",
        description: str = "...",
        id: str = "",
        cheat_sheet: List[CheatSheet] = [],
        collections: dict = {},
    ) -> None:
        self.id: str = str(get_uuid()) if id == "" else id
        self.username: str = username
        self.password: str = password # keep in mind that the password is hashed before being passed.
        self.profile_picture: str = profile_picture
        self.description: str = description
        self.cheat_sheet: list[CheatSheet] = cheat_sheet
        self.collections: list = collections


    def __str__(self) -> str:
        return f"Account({self.get_id()})"
    

    def __repr__(self) -> str:
        return f"Account({self.get_id()})"
    

    def __eq__(self, other_account: object) -> bool:
        if isinstance(other_account, Account):
            return self.get_id() == other_account.get_id()
        return False
    

    def check_password(self, a_password_hash: str) -> bool:
        return self.get_password() == a_password_hash


    def get_username(self) -> str:
        return self.username
    

    def get_password(self) -> str:
        return self.password
    

    def get_description(self) -> str:
        return self.description
    

    def get_profile_picture(self) -> str:
        return self.profile_picture
    

    def get_id(self) -> str:
        return self.id
    

    def get_collections(self) -> dict:
        return self.collections
    

    def get_cheat_sheet(self) -> list:
        return self.cheat_sheet
    

    def get_cheat_sheet_info(self) -> list:
        cheat_sheet_info: list = []
        for cs in self.get_cheat_sheet():
            cheat_sheet_info.append(cs.get_info())
        return cheat_sheet_info


    def get_info(self) -> dict:
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "description": self.get_description(),
            "profile_picture": self.get_profile_picture(),
            "id": self.get_id(),
            "cheat_sheet": self.get_cheat_sheet_info(),
            "collections": self.get_collections(),
        }
    

    def add_cheat_sheet(self, new_cheat_sheet: CheatSheet):
        if new_cheat_sheet not in self.cheat_sheet:
            self.cheat_sheet.append(new_cheat_sheet)


if __name__ == "__main__":
    account: Account = Account("test", "test")
    input_password: str = "test"
