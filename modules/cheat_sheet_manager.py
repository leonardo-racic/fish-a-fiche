from json import loads as load_json, dumps
from .cheat_sheet_module import CheatSheet


def json_to_cheat_sheet(cheat_sheet_info: dict) -> CheatSheet:
    new_cheat_sheet: CheatSheet = CheatSheet(
        cheat_sheet_info["title"],
        cheat_sheet_info["author_token"],
        cheat_sheet_info["content"],
        cheat_sheet_info["context"],
    )


    if cheat_sheet_info.get("date"):
        new_cheat_sheet.date = cheat_sheet_info["date"]
    if cheat_sheet_info.get("likes"):
        new_cheat_sheet.likes = cheat_sheet_info["likes"]
    if cheat_sheet_info.get("dislikes"):
        new_cheat_sheet.dislikes = cheat_sheet_info["dislikes"]
    if cheat_sheet_info.get("keywords"):
        new_cheat_sheet.keywords = cheat_sheet_info["keywords"]
    if cheat_sheet_info.get("original_lang"):
        new_cheat_sheet.original_lang = cheat_sheet_info["original_lang"]
    if cheat_sheet_info.get("comments"):
        new_cheat_sheet.comments = cheat_sheet_info["comments"]


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
        self.cheat_sheet = read_cheat_sheet_json()
        cheat_sheet: CheatSheet = self.cheat_sheet.get(token, None)
        return cheat_sheet
    

    def get_cheat_sheet_info(self, token: str) -> dict:
        cheat_sheet: CheatSheet = self.get_cheat_sheet(token)
        if cheat_sheet is None:
            return {}
        return cheat_sheet.get_info()
