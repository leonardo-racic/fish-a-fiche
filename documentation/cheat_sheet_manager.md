# Documentation of the [cheat_sheet_manager](../modules/cheat_sheet_manager.py) file
This a file managing the cheat_sheet of the web-site, their creation, open, stocking.
## converter json en cheat sheet
the file is checking with the function *"json_to_cheat_sheet"* if all the token have been fill by the user and adding the cheat_sheet important information on the public seeing version of the cheat_sheet
## cheat_sheet reader
the function *"read_cheat_sheet_json"* is making check to know if everything is ok, to open the file, and then it's open the file.
## class CheatSheetManager
Here we defined a class named **"CheatSheetManager"**, which could be used in other files.
This class is tool box for our website, with functions such as *"get_cheat_sheet"* which fetch the cheat_sheet required, or *"get_cheat_sheet_info"* wich fetch the info about the cheat_sheet, *"add_cheat_sheet"* wich add a new cheat_sheet to the database. *"create_new_cheat_sheet"* wich is creating a new cheat_sheet. But most of the function name will give you their own utility.
