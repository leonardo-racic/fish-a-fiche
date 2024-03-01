import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT , KEYWORD , DATETIME , NUMERIC , STORED
from whoosh.query import *
import whoosh.index as index

schema = Schema(title=TEXT(stored=True),
                author=TEXT(stored=True) ,
                date=DATETIME(stored=True),
                lang=KEYWORD(stored=True) ,
                subject=TEXT(stored=True),
                keyword=KEYWORD(stored=True),
                description=TEXT(stored=True),
                likes=NUMERIC(stored=True),
                dislikes=NUMERIC(stored=True),
                comments=NUMERIC(stored=True),
                views=NUMERIC(stored=True),
                path=STORED
                )





if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)

ix = index.open_dir("index")

writer = ix.writer()

writer.add_document(title=u"physique", author=u"maxime",
                    path=u"/a", views=3, likes=8)
writer.add_document(title=u"math", author=u"maxime",
                    path=u"/b", views=5, likes=9)
writer.add_document(title=u"franc", author=u"lonardo",
                    path=u"/c", views=98, likes=45)
writer.commit()

with ix.searcher() as searcher:
    
    myquery = Term("author", u"maxime")
    results = searcher.search(myquery)
    print(results[0])