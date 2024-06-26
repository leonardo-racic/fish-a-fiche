# Fish a fiche

**FR** : Bonjour à tous ! Bienvenu dans la documentation de notre projet de NSI, visant à créer un site internet permettant de créer des fiches de révisions et les poster en ligne.

**EN** : Hello everyone ! Welcome to the documention of our NSI project, an web-site allowing you to create revision sheet and post them online ! Wonderful isn't it ?

## Introduction

This is the main file for the documentation, linking all the other markdown files. If you are interested in developping this project, you should definitely check it out!

## Project's architecture

This project is very dense, as almost each python script we have written have more than a hundred lines, which may prove to be challenging to handle, when there are a lot of modules to check. As such, we have decided to create a consistent architecture in a scalable paradigm.

### folder "documentation"

A folder containing all the [documentation](/documentation) files to centralize all our documentation files. there a documentation for all the main modules. If you want to know more about one of them, go check the folder !

### folder "index"

A folder acting as a data base : [INDEX](/index), still need some imporvement, but the devs are working on it.

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

A file containing some file names for the github website management tool, so that the bot doesn't take them into account when someone pushes something, because these files change very often.

### Read.me

A file used for the presentation of project on our github page.

### _config.yml

A file containing some information for the github website management tool, so that the bot knows what to modify to customize our site.

### accounts.json

A file contaning the way we stocked all informations about a user, his personal data and his different cheat_sheet created.

### app.py

This file is the MAIN file, the file connecting all the others, essential for the good working of our website. He is importing all the other files, the necessary modules and the main functions.

### cheat_sheet.json

A json containing all the cheat sheet.

### debug.log

A file containing the logs of the website.

### index.html

There is currently nothing in, but will be used for github.

### main.sh

This file is just a dev tool, don't care about it.

### requirement.txt

A file listing all the external modules that need to be imported for the proper functioning of the site.

### singletons.py

A file containing multitasking functions which avoid having to put them back each time in other files.

### terminal_log.py

A file which allows a user encountering a problem with the site to record their errors before sending them to the site's moderation team. Team which will therefore be able to analyze its problem based on the data recorded by the user.

### JS modules

A folder in which js modules are stocked and used to verify the user's input.
