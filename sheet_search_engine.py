import whoosh

sheet_folder = "sheets"

def generate_sheet_path(user , sheet_name, local_path = ""):
    """
    Generate the path to a specific sheet file.

    Parameters
    ----------
    user : str
        The username of the user who owns the sheet.
    sheet_name : str
        The name of the sheet file.
    local_path : str, optional
        The local path to the folder where the sheets are stored, by default "".

    Returns
    -------
    str
        The full path to the sheet file.

    """
    #might need a function to tell where is the folder relativeto where you are
    sheet_path = local_path + "/" + sheet_folder + "/" + user + "/" + sheet_name
    return sheet_path


def search_sheet(subject):
    """
    Search for a specific subject in the database.

    Parameters
    ----------
    subject : str
        The subject to search for.

    Returns
    -------
    list
        A list of all the documents that match the subject.

    """
    index = whoosh.filedb.FileStorage(generate_sheet_path(subject))
    searcher = whoosh.index.Index(index)
    query = searcher.query(whoosh.qparser.MultifieldParser("subject", [whoosh.fields.TEXT(stored=True)]))
    results = query.all()
    return results