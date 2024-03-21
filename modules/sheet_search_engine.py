"""
This code creates a Whoosh index schema for the cheat-sheet dataset.

The schema defines the fields of the index, including the comment text, author, date, language, subject, and other metadata.

The code creates the index directory if it does not already exist, and then creates the index in the directory using the Schema object.

The code includes a commented-out example of how to search the index using a term query.

Note that this is a simplified version of the actual code, and may not include all possible features or functionality.
"""

import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, NUMERIC, STORED, ID
from whoosh.query import *

# Define the index schema
schema = Schema(
    title=TEXT(stored=True),
    author_token=TEXT(stored=True),  # Tokenized version of the author field
    date=DATETIME(stored=True),
    lang=KEYWORD(stored=True),  # Language of the cheat-sheet
    subject=TEXT(stored=True),
    keyword=KEYWORD(stored=True),
    description=TEXT(stored=True),
    likes=NUMERIC(stored=True),
    dislikes=NUMERIC(stored=True),
    comments_counter=NUMERIC(stored=True),
    comments=STORED,  # Full list of the comments
    views=NUMERIC(stored=True),
    path=ID(unique=True, stored=True)
)


# Create the index directory if it does not already exist
if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)


# Example of how to search the index using a term query
# with ix.searcher() as searcher:
#
#     myquery = Term("author", u"maxime")
#     results = searcher.search(myquery)
#     print(results[0])