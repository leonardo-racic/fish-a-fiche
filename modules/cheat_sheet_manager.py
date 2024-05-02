from __future__ import annotations
from json import loads as load_json, dumps
from .cheat_sheet_module import CheatSheet, get_uuid
from environment_variable import cs_path, account_path


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
    check(cheat_sheet_info, new_cheat_sheet, "comments")
    check(cheat_sheet_info, new_cheat_sheet, "token")
    check(cheat_sheet_info, new_cheat_sheet, "original_lang")


    return new_cheat_sheet


def read_cheat_sheet_json() -> dict:
    with open(cs_path) as f:
        cheat_sheet_dict: dict = {}
        try:
            cheat_sheet_json: dict = load_json(f.read())["cheat_sheet"]
            for token, cheat_sheet_info in cheat_sheet_json.items():
                new_cheat_sheet: CheatSheet = json_to_cheat_sheet(cheat_sheet_info)
                cheat_sheet_dict[token] = new_cheat_sheet
        except Exception as e:
            with open(cs_path, "w") as f:
                f.write(dumps({"cheat_sheet":{}}, indent=4))
        finally:
            return cheat_sheet_dict


class CheatSheetManager:
    def __init__(self) -> None:
        self.cheat_sheet: dict = read_cheat_sheet_json()
    

    def get_cheat_sheet(self, token: str) -> CheatSheet | None:
        with open(cs_path, "r") as f:
            cheat_sheet_json: dict = load_json(f.read())["cheat_sheet"]
        cheat_sheet_info: dict | None = cheat_sheet_json.get(token)
        if cheat_sheet_info is None:
            return None
        return json_to_cheat_sheet(cheat_sheet_info)
    

    def update(self) -> None:
        self.cheat_sheet = read_cheat_sheet_json()
    

    def get_cheat_sheet_info(self, token: str) -> dict:
        cheat_sheet: CheatSheet | None = self.get_cheat_sheet(token)
        if cheat_sheet is None:
            return {}
        return cheat_sheet.get_info()
    

    def add_cheat_sheet(self, new_cheat_sheet: CheatSheet) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][new_cheat_sheet.token] = new_cheat_sheet.get_info()
        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()


    def create_new_cheat_sheet(self, cheat_sheet_info: dict) -> CheatSheet:
        new_cheat_sheet: CheatSheet = CheatSheet(
            cheat_sheet_info["title"],
            cheat_sheet_info["author_token"],
            cheat_sheet_info["content"],
            cheat_sheet_info["context"],
        )
        new_cheat_sheet.token = str(get_uuid())
        self.add_cheat_sheet(new_cheat_sheet)
        return new_cheat_sheet
    

    def add_comment_to_cheat_sheet(self, token: str, comment: dict) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][token]["comments"].append(comment)
        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()

    
    def modify_cheat_sheet(self, token: str, new_cheat_sheet_info: dict) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())
        cheat_sheet_data["cheat_sheet"][token]["title"] = new_cheat_sheet_info["title"]
        cheat_sheet_data["cheat_sheet"][token]["content"] = new_cheat_sheet_info["content"]
        cheat_sheet_data["cheat_sheet"][token]["context"] = new_cheat_sheet_info["context"]
        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
        self.update()

    
    def delete_cheat_sheet(self, token: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())
        if token in cheat_sheet_data["cheat_sheet"]:
            del cheat_sheet_data["cheat_sheet"][token]
            with open(cs_path, "w") as f:
                f.write(dumps(cheat_sheet_data, indent=4))


    def remove_comment(self, cheat_sheet_token: str, comment_content: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())

        cheat_sheet: dict = cheat_sheet_data["cheat_sheet"][cheat_sheet_token]
        for comment in cheat_sheet["comments"]:
            if comment["content"] == comment_content:
                comments: list = cheat_sheet["comments"]
                comments.remove(comment)
                break

        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))


    def add_like(self, cheat_sheet_token: str, user_token: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())

        cheat_sheet: dict = cheat_sheet_data["cheat_sheet"][cheat_sheet_token]
        cheat_sheet["likes"].append(user_token)

        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
    

    def remove_like(self, cheat_sheet_token: str, user_token: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())

        cheat_sheet: dict = cheat_sheet_data["cheat_sheet"][cheat_sheet_token]
        if user_token in cheat_sheet["likes"]:
            cheat_sheet["likes"].remove(user_token)

        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
    

    def add_dislike(self, cheat_sheet_token: str, user_token: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())

        cheat_sheet: dict = cheat_sheet_data["cheat_sheet"][cheat_sheet_token]
        cheat_sheet["dislikes"].append(user_token)

        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))
    

    def remove_dislike(self, cheat_sheet_token: str, user_token: str) -> None:
        with open(cs_path) as f:
            cheat_sheet_data: dict = load_json(f.read())

        cheat_sheet: dict = cheat_sheet_data["cheat_sheet"][cheat_sheet_token]
        if user_token in cheat_sheet["dislikes"]:
            cheat_sheet["dislikes"].remove(user_token)

        with open(cs_path, "w") as f:
            f.write(dumps(cheat_sheet_data, indent=4))