import json

#def handle_search(server_account_manager,cheat_sheet_manager, name):

def check(name):
    return t[1]["title"] == name


def filter_title(name):
    with open('cheat_sheet.json') as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]

    return list(filter(lambda x:x[1]["title"] == name, list(data.items())))

print(filter_title('test'))