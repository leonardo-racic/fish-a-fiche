from uuid import uuid4 as get_uuid
from .cheat_sheet_module import CheatSheet
from typing import List


def cheat_sheet_to_json(cs: CheatSheet) -> dict:
    return {
        "title": cs.title,
        "likes": cs.likes,
        "author_token": cs.author_token,
        "token": cs.author_token,
        "comments": cs.comments,
        "dislikes": cs.dislikes,
        "content": cs.content,
        "context": cs.context,
        "keywords": cs.keywords,
        "date": cs.date,
        "original_lang": cs.original_lang,
    }


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
        self.cheat_sheet: List[CheatSheet] = cheat_sheet
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
    

    def get_cheat_sheet_json(self) -> list:
        cheat_sheet: list = []
        for cs in self.cheat_sheet:
            cheat_sheet.append(cheat_sheet_to_json(cs))
        return cheat_sheet
    

    def get_info(self) -> dict:
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "description": self.get_description(),
            "profile_picture": self.get_profile_picture(),
            "id": self.get_id(),
            "cheat_sheet": self.get_cheat_sheet_json(),
            "collections": self.get_collections(),
        }
    

    def add_cheat_sheet(self, new_cheat_sheet: CheatSheet):
        self.cheat_sheet.append(new_cheat_sheet)


if __name__ == "__main__":
    account: Account = Account("test", "test")
    input_password: str = "test"