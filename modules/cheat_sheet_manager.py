from json import loads as load_json, dumps
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager


def check(csi: dict, cs: CheatSheet, info: str) -> None:
    if csi.get(info):
        cs.__dict__[info] = csi[info]


def json_to_cheat_sheet(cheat_sheet_info: dict) -> CheatSheet:
    new_cheat_sheet: CheatSheet = CheatSheet(
        cheat_sheet_info["title"],
        cheat_sheet_info["author_token"],
        cheat_sheet_info["content"],
        cheat_sheet_info["context"],
    )


    check(cheat_sheet_info, new_cheat_sheet, "date")
    check(cheat_sheet_info, new_cheat_sheet, "likes")
    check(cheat_sheet_info, new_cheat_sheet, "dislikes")
    check(cheat_sheet_info, new_cheat_sheet, "keywords")
    check(cheat_sheet_info, new_cheat_sheet, "comments")
    check(cheat_sheet_info, new_cheat_sheet, "token")
    check(cheat_sheet_info, new_cheat_sheet, "original_lang")


    return new_cheat_sheet


def read_cheat_sheet_json() -> dict:
    with open("cheat_sheet.json") as f:
        cheat_sheet_dict: dict = {}
        try:
            cheat_sheet_json: dict = load_json(f.read())["cheat_sheet"]
            for token, cheat_sheet_info in cheat_sheet_json.items():
                new_cheat_sheet: CheatSheet = json_to_cheat_sheet(cheat_sheet_info)
                cheat_sheet_dict[token] = new_cheat_sheet
        except Exception as e:
            with open("cheat_sheet.json", "w") as f:
                f.write(dumps({"cheat_sheet":{}}, indent=4))
        finally:
            return cheat_sheet_dict


class CheatSheetManager:
    def __init__(self) -> None:
        self.cheat_sheet: dict = read_cheat_sheet_json()
    

    def get_cheat_sheet(self, token: str) -> CheatSheet:
        with open("cheat_sheet.json", "r") as f:
            cheat_sheet_json: dict = load_json(f.read())["cheat_sheet"]
        cheat_sheet_info: dict = cheat_sheet_json.get(token)
        if cheat_sheet_info is None:
            return None
        return json_to_cheat_sheet(cheat_sheet_info)
    

    def update(self) -> None:
        self.cheat_sheet = read_cheat_sheet_json()
    

    def get_cheat_sheet_info(self, token: str) -> dict:
        cheat_sheet: CheatSheet = self.get_cheat_sheet(token)
        if cheat_sheet is None:
            return {}
        return cheat_sheet.get_info()
    

    def add_cheat_sheet(self, new_cheat_sheet: CheatSheet) -> None:
        with open("cheat_sheet.json") as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][new_cheat_sheet.token] = new_cheat_sheet.get_info()
        with open("cheat_sheet.json", "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()


    def create_new_cheat_sheet(self, cheat_sheet_info: dict) -> CheatSheet:
        new_cheat_sheet: CheatSheet = CheatSheet(
            cheat_sheet_info["title"],
            cheat_sheet_info["author_token"],
            cheat_sheet_info["content"],
            cheat_sheet_info["context"],
        )
        self.add_cheat_sheet(new_cheat_sheet)
        return new_cheat_sheet
    

    def add_comment_to_cheat_sheet(self, token: str, comment: dict) -> None:
        with open("cheat_sheet.json") as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][token]["comments"].append(comment)
        with open("cheat_sheet.json", "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()

    
    def modify_cheat_sheet(self, token: str, new_cheat_sheet_info: dict) -> None:
        with open("cheat_sheet.json") as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][token]["title"] = new_cheat_sheet_info["title"]
        cheat_sheet_data["cheat_sheet"][token]["content"] = new_cheat_sheet_info["content"]
        cheat_sheet_data["cheat_sheet"][token]["context"] = new_cheat_sheet_info["context"]
        with open("cheat_sheet.json", "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()

        