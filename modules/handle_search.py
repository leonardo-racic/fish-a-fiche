import json

#def handle_search(server_account_manager,cheat_sheet_manager, name):

def check(t):


    # Open the existing JSON file for loading into a variable
with open('cheat_sheet.json') as jsondata:
    data: dict = json.loads(jsondata.read())
    print(data)
# Search data based on key and value using filter and list method
print(list(filter(check, list(data.items()))))