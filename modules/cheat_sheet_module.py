from uuid import uuid4 as get_uuid
from json import dumps as dict_to_json
from datetime import datetime
from typing import List
from whoosh.index import create_in
import whoosh.index as index


def get_current_date() -> str:
    now: datetime = datetime.now()
    date_str: str = now.strftime("%d/%m/%Y - %H:%M")
    return date_str


class CheatSheet:
    def __init__(
        self,
        title: str,
        author_token: str,
        content: str,
        context: str,
        date: str = get_current_date(),
        original_lang: str = "EN",
        comments: dict = {},
        likes: int = 0,
        dislikes: int = 0,
        keywords: List[str] = [],
        token: str = str(get_uuid())
    ) -> None:
        self.token: str = token
        self.title: str = title
        self.author_token: str = author_token
        self.content: str = content
        self.date: str = date
        self.original_lang: str = original_lang
        self.context: str = context
        self.comments: dict = comments
        self.keywords: list[str] = keywords
        self.likes: int = likes
        self.dislikes: int = dislikes
    

    def __repr__(self) -> str:
        return f"CheatSheet({self.token})"


    def get_info(self) -> dict:
        return {
            "token": self.token,
            "title": self.title,
            "author_token": self.author_token,
            "content": self.content,
            "context": self.context,
            "date": self.date,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "original_lang": self.original_lang,
            "keywords": self.keywords,
            "comments": self.comments
        }


    def store_to_index(self):
        ix = index.open_dir("index")
        writer = ix.writer()
        writer.add_document(title=self.title,
                            author_token=self.author_token,
                            date = datetime.now(),
                            lang = self.original_lang,
                            keyword = " ".join(self.keywords),
                            description = self.context,
                            likes = self.likes,
                            dislikes=self.dislikes,
                            comments = self.comments,
                            comments_counter = len(self.comments),
                            path = str(self.author_token+"/"+self.title),
                        )

        writer.commit()

        

    def update_document():
        pass


    def to_json(self) -> str:
        info: dict = self.get_info()
        json_str: str = dict_to_json(info, indent=4)
        return json_str
    
    def create_file(self):
        f = open("test.json", "w")
        f.write(self.to_json())


def check_then_update(cs: CheatSheet, json_dict: dict, data: str) -> None:
    if json_dict.get(data):
        cs.__dict__[data] = json_dict.get(data)


def json_to_cheat_sheet(json_dict: dict) -> CheatSheet:
    new_cs = CheatSheet(
        json_dict["title"],
        json_dict["author_token"],
        json_dict["content"],
        json_dict["context"],
        json_dict["date"],
        json_dict["original_lang"],
        json_dict["comments"],
        json_dict["likes"],
        json_dict["dislikes"],
        json_dict["keywords"],
        json_dict["token"],
    )
    return new_cs


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

if __name__ == "__main__":
    cs: CheatSheet = CheatSheet("Volumic mass", "Ado's token", "p=m/V", "for science stuff")
    cs.create_file()
        


            
        