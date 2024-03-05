from uuid import uuid4 as get_uuid
from json import dumps as dict_to_json
from datetime import datetime
import os.path
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
        keywords: list[str] = [],
        token: str = str(get_uuid()),
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
            "comments": self.comments,
        }

    def store_to_index(self):
        ix = index.open_dir("index")
        writer = ix.writer()

        writer.add_document(title=self.title,
                            author_token=self.author_token,
                            date = self.date,
                            lang = self.original_lang,
                            subject = self.sgebdbf,#add this to the class
                            keyword = self.keywords,
                            description = self.context,
                            views=0,
                            likes=0,
                            dislikes=self.dislikes,
                            comments = self.comments,
                            comments_counter = 0, #add this to the class
                            path = str(self.author_token,"/",self.title))

        writer.commit()

        

    def update_document():


    def to_json(self) -> str:
        info: dict = self.get_info()
        json_str: str = dict_to_json(info, indent=4)
        return json_str
    


if __name__ == "__main__":
    cs: CheatSheet = CheatSheet("Volumic mass", "Ado's token", "p=m/V", "for science stuff")
    print(cs.to_json())
        


            
        