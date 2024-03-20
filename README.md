# fish-a-fiche

An online website where you can find small cheat-sheets for any subject, theme, or domain you are interested in such as languages' grammar/vocabulary/syntax..., math/physics/chemistry's formula, eco-socio-geopolitical definitions, theorems, proofs, computer science notions!
This project is realised thanks to GALTIER Maxime, DUCLOS Marc-Antoine, and RAČIĆ Leonardo.

## Tools for the project

(Check out the venv/virtual environment in order to get the exact version of each module and interpreter)
- Python language used with the Flask application
- HTML & CSS (current's project imposed condition)

## To-do list

- Handle user authentication by hashing, storing account information, and handling the home page according to the user's account status (logged, not connected yet, etc.)
- Create a HTML website that helps creating cheat-sheets using markdown (or a custom dialect) and that helps previewing the cheat-sheets before publishing
- Handle user profiles with their own cheat-sheets by displaying their username, description, said localisation, pronouns, languages, user icon, cheat-sheets, their favorite cheat-sheets...
- Create the Cheat-Sheet Market (CSM), a web-page that helps the user find their desired cheat-sheet through a rough categorization of cheat-sheets by their domains and popularity, by a search bar, etc.
- Handle Cheat-Sheet Posts (CSP) in which there is the rendered version of the cheat-sheet, that people can eventually like, favorite, comment and discuss under it (or on an extract if possible).
- Documentations for each file employed in the project
  
  

## Dependencies

- Flask, and its own dependencies (Jinja...)
- Python 3, including venv

 ## bug fixing

when you save your profile, you are redirected to /profile/username instead of /profile/usertoken