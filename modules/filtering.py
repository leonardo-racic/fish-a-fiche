from environment_variable import cs_path, account_path
import json
from .server_account_manager import get_hash



def get_profiles() -> list:
    with open(account_path) as f:
        data: dict = json.loads(f.read())["accounts"]
    for id, info in list(data.items()):
        data[id]["id"] = get_hash(info["id"])
    data_values: list = list(data.values())
    return data_values


def filter_title(name: str = "") -> list:
    def filter_func(current_dict: dict) -> bool:
        current_title: str = current_dict["title"]
        condition: bool = name.casefold() in current_title.casefold()
        return condition
    
    with open(cs_path) as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    data_values: list = list(data.values())

    if name != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values


def filter_context(context: str = "") -> list:
    def filter_func(current_dict: dict) -> bool:
        current_context: str = current_dict["context"]
        condition: bool = False
        for keyword in context.split():
            if keyword in current_context.split():
                condition = True
                break
        return condition 

    with open(cs_path) as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    data_values: list = list(data.values())

    if context != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values


def filter_profiles(username: str = "") -> list:
    def filter_func(current_dict: dict) -> bool:
        current_username: str = current_dict["username"]
        condition: bool = username.casefold() in current_username
        return condition


    data_values: list = get_profiles()
    if username != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values