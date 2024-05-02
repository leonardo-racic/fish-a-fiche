# The first import module is only to guarantee a secure variable typing.
from __future__ import annotations
from .account_module import Account
from .cheat_sheet_module import CheatSheet, json_to_cheat_sheet
from json import loads as load_json, dumps as to_json
from flask import request
from terminal_log import inform
import hashlib
from environment_variable import account_path, cs_path


def get_hash(this_text: str) -> str:
    return hashlib.sha256(this_text.encode()).hexdigest()


def check(account: Account, account_json: dict, data: str) -> None:
    if account_json.get(data):
        account.__dict__[data] = account_json[data]


def json_to_account(account_json: dict) -> Account:
    new_account: Account = Account(
        account_json["username"],
        account_json["password"]
    )
    check(new_account, account_json, "description")
    check(new_account, account_json, "profile_picture")
    check(new_account, account_json, "id")
    check(new_account, account_json, "collections")
    new_account.cheat_sheet = []
    for cheat_sheet_info in account_json.get("cheat_sheet", []):
        cheat_sheet: CheatSheet = json_to_cheat_sheet(cheat_sheet_info)
        new_account.cheat_sheet.append(cheat_sheet)

    return new_account


def read_accounts_json() -> dict:
    with open(account_path) as f:
        accounts_json: dict = load_json(f.read())["accounts"]
        accounts_dict: dict = {}
        for token, account_info in list(accounts_json.items()):
            new_account: Account = json_to_account(account_info)
            for cheat_sheet_json in account_info["cheat_sheet"]:
                cheat_sheet: CheatSheet = json_to_cheat_sheet(cheat_sheet_json)
                new_account.add_cheat_sheet(cheat_sheet)
            accounts_dict[token] = new_account
        return accounts_dict

        
    


class ServerAccountManager:
    def __init__(self) -> None:
        self.accounts: dict = read_accounts_json()


    def update(self) -> None:
        self.accounts = read_accounts_json()


    def get_all_accounts(self) -> list[Account]:
        return list(self.get_accounts_dict().values())
    

    def get_all_account_info(self) -> list[dict]:
        accounts: list[Account] = self.get_all_accounts()
        return [account.get_info() for account in accounts]


    def create_account(self, input_username: str, input_password: str, description: str = "", profile_picture: str = "") -> Account:
        new_account: Account = Account(input_username, get_hash(input_password), profile_picture, description)
        new_account.cheat_sheet = []
        inform(f"{new_account} is being created")
        with open(account_path, "r") as f:
            json_data: dict = load_json(f.read())
        json_data["accounts"][new_account.get_id()] = new_account.get_info()
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
        inform(f"Account with id {new_account.get_id()} created successfully.")
        return new_account


    def get_account_by_token(self, token: str) -> Account:
        return self.get_accounts_dict().get(token, None)
    

    def get_account_info_by_token(self, token: str) -> dict | None:
        account: Account = self.get_account_by_token(token)
        i: dict | None
        if account is not None:
            i = account.get_info()
        else:
            i = None
        return i
    

    def delete_account(self, account: Account) -> None:
        with open(account_path, "r") as f:
            json_data: dict = load_json(f.read())
        account_id: str
        for account_id in list(json_data["accounts"].keys()):
            if account_id == account.get_id():
                json_data["accounts"].pop(account_id)
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()


    def get_accounts_dict(self) -> dict:
        self.update()
        return self.accounts
    

    def get_current_username_from_token(self, token: str) -> str:
        account: Account = self.get_account_by_token(token)
        if account is None:
            return ""
        return account.get_username()
    

    def has_account(self, specific_account: Account | None) -> bool:
        if specific_account is None:
            return False
        r: bool = specific_account in self.get_all_accounts()
        return r
    

    def has_account_username(self, current_username: str) -> bool:
        for account_info in self.get_all_account_info():
            if account_info["username"] == current_username:
                return True
        return False
    

    def get_account_by_username(self, username: str) -> Account | None:
        for account_info in self.get_all_account_info():
            if account_info["username"] == username:
                return Account(
                    account_info["username"],
                    account_info["password"],
                    account_info["profile_picture"],
                    account_info["description"],
                    account_info["id"],
                )
        return None
    

    def get_account_info_by_username(self, username: str) -> dict:
        target_account: Account | None = self.get_account_by_username(username)
        if target_account is None:
            return {}
        return target_account.get_info()


    def is_login_valid(self, username: str, password: str) -> tuple[bool, bool, bool]:
        is_input_valid: bool = username != "" and password != ""
        if not is_input_valid:
            return (False, False, False)
         
        target_account: Account | None = self.get_account_by_username(username)
        account_exists: bool = target_account is not None
        password_hash: str = get_hash(password)
        password_correct: bool = target_account.check_password(password_hash) if account_exists else False
        return (is_input_valid, account_exists, password_correct)


    def is_sign_up_input_valid(self, username: str, password: str) -> bool:
        if not self.is_username_valid(username):
            return False
        elif password == "":
            return False
        return True
    

    def get_user_account_info(self) -> dict:
        self.update()
        user_account: Account | None = self.get_user_account()
        if user_account is None:
            return {}
        return user_account.get_info()


    def get_user_account_token(self) -> str:
        return request.cookies.get("account-token", "")


    def get_user_account(self) -> Account | None:
        with open(account_path) as f:
            accounts_json: dict = load_json(f.read())["accounts"]
        account_token: str = self.get_user_account_token()
        target_account_info: Account | None = accounts_json.get(account_token)
        if target_account_info is None:
            return None
        target_account: Account = json_to_account(target_account_info)
        return target_account
    

    def is_user_logged_in(self) -> bool:
        account_info: dict = self.get_user_account_info()
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
        account_info: dict = self.get_user_account_info()
        if account_info != {}:
            with open(account_path) as f:
                data: dict = load_json(f.read())["accounts"]
            for current_account_info in data.values():
                if current_account_info["username"] == account_info["username"]:
                    if new_image_input != "":
                        current_account_info["profile_picture"] = new_image_input
                    current_account_info["description"] = description_input
                    current_account_info["username"] = username_input
                    break
            with open(account_path, "w") as f:
                f.write(to_json({"accounts": data}, indent=4))
            self.update()
    

    def add_cheat_sheet_to_user(self, cheat_sheet: CheatSheet) -> None:
        cheat_sheet_info: dict = cheat_sheet.get_info()
        with open(account_path, "r") as f:
            json_data: dict = load_json(f.read())
        json_data["accounts"][cheat_sheet.author_token]["cheat_sheet"].append(cheat_sheet_info)
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()


    def get_account_cheat_sheet_info(self, token: str) -> list:
        with open(account_path) as f:
            accounts_dict: dict = load_json(f.read())["accounts"]
        cs: list = accounts_dict[token]["cheat_sheet"]
        cheat_sheet: list = []
        with open(cs_path) as f:
            cs_dict: dict = load_json(f.read())["cheat_sheet"]
            for cs_info in cs:
                cheat_sheet.append(cs_dict[cs_info["token"]])
        return cheat_sheet


    def get_account_from_hashed_token(self, hashed_token: str) -> Account | None:
        for account in self.get_all_accounts():
            if get_hash(account.get_id()) == hashed_token:
                return account
        return None
    

    def get_account_info_from_hashed_token(self, hashed_token: str) -> dict | None:
        account: Account | None = self.get_account_from_hashed_token(hashed_token)
        if account is None:
            return None
        return account.get_info()


    def get_user_account_hashed_token(self) -> str:
        user_token: str = self.get_user_account_token()
        user_hashed_token: str = get_hash(user_token)
        return user_hashed_token
    

    def add_new_collection_to_account(self, collection: str, account_id: str, is_public: bool) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        current_account_info: dict = json_data["accounts"][account_id]
        if collection not in current_account_info["collections"]:
            current_account_info["collections"].append({
                "is_public": is_public,
                "cheat_sheet": [],
                "name": collection,
            })
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
    

    def add_new_collection_to_account_from_hashed_token(self, collection: str, hashed_account_id: str, is_public: bool) -> None:
        target_account: Account | None = self.get_account_from_hashed_token(hashed_account_id)
        if target_account is Account:
            self.add_new_collection_to_account(collection, target_account.get_id(), is_public)
    

    def add_cheat_sheet_to_collection(self, collection: str, account_id: str, cheat_sheet_token: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        current_account_info: dict = json_data["accounts"][account_id]
        target_collection: list = current_account_info["collections"][collection]
        if cheat_sheet_token not in target_collection:
            target_collection.append(cheat_sheet_token)
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
    

    def delete_collection(self, collection_name: str, account_id: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        current_account_info: dict = json_data["accounts"][account_id]
        collections: list = current_account_info["collections"]
        updated_collections: list = []
        for c in collections:
            if c["name"] != collection_name:
                updated_collections.append(c)
        current_account_info["collections"] = updated_collections
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()


    def get_collections(self, token: str) -> list:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        return json_data["accounts"][token].get("collections")
    

    def get_user_account_collections(self) -> list:
        return self.get_collections(self.get_user_account_token())


    def has_user_collection(self, collection_name: str) -> bool:
        collections: list = self.get_user_account_collections()
        for c in collections:
            if c["name"] == collection_name:
                return True
        return False
    

    def is_collection_public(self, account_id: str, collection_name: str) -> bool | None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        for c in target_account_json["collections"]:
            if c["name"] == collection_name:
                return c["is_public"]
        return None


    def toggle_collection_visibility(self, account_id, collection_name: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        for c in target_account_json["collections"]:
            if c["name"] == collection_name:
                c["is_public"] = not c["is_public"]
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
    

    def rename_collection(self, account_id: str, old_collection_name: str, new_collection_name: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        for c in target_account_json["collections"]:
            if c["name"] == old_collection_name:
                c["name"] = new_collection_name
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
    

    def save_to_collection(self, collection_name: str, cheat_sheet_token: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        current_account_info: dict = json_data["accounts"][self.get_user_account_token()]
        collections: list = current_account_info["collections"]
        for c in collections:
            if c["name"] == collection_name and cheat_sheet_token not in c["cheat_sheet"]:
                c["cheat_sheet"].append(cheat_sheet_token)
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
    

    def get_cheat_sheet_token_from_collection(self, account_id: str, collection_name: str) -> list | None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        for c in target_account_json["collections"]:
            if c["name"] == collection_name:
                return c["cheat_sheet"]
        return None
    

    def remove_cheat_sheet_from_collection(self, account_id: str, collection_name: str, cheat_sheet_token: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        for c in target_account_json["collections"]:
            has_removed: bool = False
            if c["name"] == collection_name:
                for cs in c["cheat_sheet"]:
                    if cs == cheat_sheet_token:
                        c["cheat_sheet"].remove(cheat_sheet_token)
                        has_removed = True
                        break
            if has_removed:
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))
        self.update()
        

    def delete_cheat_sheet(self, account_id: str, cheat_sheet_token: str) -> None:
        with open(account_path) as f:
            json_data: dict = load_json(f.read())
        target_account_json: dict = json_data["accounts"][account_id]
        cheat_sheet: list = target_account_json["cheat_sheet"]
        for c in cheat_sheet:
            if c["token"] == cheat_sheet_token:
                cheat_sheet.remove(c)
                break
        with open(account_path, "w") as f:
            f.write(to_json(json_data, indent=4))


if __name__ == "__main__":
    s: ServerAccountManager = ServerAccountManager()
    account: Account = s.create_account("Hello", "world")
    new_cs: CheatSheet = CheatSheet("Hello", "NNN", "za", "xc")
    new_cs.author_token = account.get_id()
    s.add_cheat_sheet_to_user(new_cs)

    
