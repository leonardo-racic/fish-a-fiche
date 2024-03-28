# Fish a fiche !

**FR** :Bonjour à tous ! Bienvenu dans la documentation de notre projet de NSI, visant à créer un site internet permettant de créer des fiches de révisions et les poster en ligne.

**EN** : Hello everyone ! Welcome to the documention of our NSI project, an web-site allowing you to create revision sheet and post them online ! Wonderful isn't it ?

# Documentation

## Introduction

This is the main file for the documentation, linking all the other markdown files. If you are interested in developping this project, you should definitely check it out!

## Project's architecture

This project is very dense, as almost each python script we have written have more than a hundred lines, which may prove to be challenging to handle, when there are a lot of modules to check. As such, we have decided to create a consistent architecture in a scalable paradigm.

### folder "documentation"

A folder containing all the [documentation](/documentation) files to centralize all our documentation files. there a documentation for all the main modules. If you want to know more about one of them, go check the folder !

### folder "index"

A folder containing all the important MAIN files regrouped in a [INDEX](/index), still nid some imporvement, but the devs are working on it.

### folder "modules"

A folder containing all the important [modules](/modules)
	- Accounts are handled by [server_account_manager.py](/modules/server_account_manager.py) thanks to the "Account" class from [account_module.py](/modules/account_module.py)
	- Cheat sheet's are handled by [cheat_sheet_manager.py](/modules/cheat_sheet_manager.py) thanks to the "CheatSheet" class from [cheat_sheet_module.py](/modules/cheat_sheet_module.py)
	- All search motors are run thanks to [sheet_search_engine.py](/modules/sheet_search_engine.py)
	- Specific files handling multiple aspects of the website thanks to the main's file routing

### folder "sheets"

A folder, acting as a database, stocking all the different sheet created by users. Actually there is mostly test sheet but you can take a blink on it in [sheets](/sheets)

### folder "templates"

- A folder containing all the static files that the server handles, called [templates](/templates) (that's how JinJa calls them)

- The main python file that is the first to be executed when flask is run: [app.py](/app.py), that is important, since it is the one routing the URLs to the multiple files handling different situations
- A file containing all account's information : [accounts.json](/accounts.json)
- A file containing all the existing cheat sheet: [cheat_sheet.json](/cheat_sheet.json)

### .gitignore

### Read.me

### _config.yml

### accounts.json

### app.py

### cheat_sheet.json

### debug.log

### index.html

### main.sh

### requirement.txt

### singletons.py

### terminal_log.py
