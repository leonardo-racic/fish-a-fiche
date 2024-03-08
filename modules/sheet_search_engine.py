import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT , KEYWORD , DATETIME , NUMERIC , STORED , ID
from whoosh.query import *
import whoosh.index as index

schema = Schema(title=TEXT(stored=True),
                author_token=TEXT(stored=True) ,
                date=DATETIME(stored=True),
                lang=KEYWORD(stored=True) ,
                subject=TEXT(stored=True),
                keyword=KEYWORD(stored=True),
                description=TEXT(stored=True),
                likes=NUMERIC(stored=True),
                dislikes=NUMERIC(stored=True),
                comments_counter=NUMERIC(stored=True),
                comments=STORED,
                views=NUMERIC(stored=True),
                path=ID(unique=True,stored=True)
                )





if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)



'''
with ix.searcher() as searcher:
    
    myquery = Term("author", u"maxime")
    results = searcher.search(myquery)
    print(results[0])
    
'''