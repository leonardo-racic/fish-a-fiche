# Documentation

## Introduction

This is the main file for the documentation, linking all the other markdown files. If you are interested in developping this project, you should definitely check it out!

## Project's architecture

This project is very dense, as almost each python script we have written have more than a hundred lines, which may prove to be challenging to handle, when there are a lot of modules to check. As such, we have decided to create a consistent architecture in a scalable paradigm.
- A folder containing all the important [modules](/modules)
	- Accounts are handled by [server_account_manager.py](/modules/server_account_manager.py) thanks to the "Account" class from [account_module.py](/modules/account_module.py)
	- Cheat sheet's are handled by [cheat_sheet_manager.py](/modules/cheat_sheet_manager.py) thanks to the "CheatSheet" class from [cheat_sheet_module.py](/modules/cheat_sheet_module.py)
	- All search motors are run thanks to [sheet_search_engine.py](/modules/sheet_search_engine.py)
	- Specific files handling multiple aspects of the website thanks to the main's file routing
- A folder containing all the static files that the server handles, called [templates](/templates) (that's how JinJa calls them)
- A folder containing all files' [documentation](/documentation)
- The main python file that is the first to be executed when flask is run: [app.py](/app.py), that is important, since it is the one routing the URLs to the multiple files handling different situations
- A file containing all account's information : [accounts.json](/accounts.json)
- A file containing all the existing cheat sheet: [cheat_sheet.json](/cheat_sheet.json)
