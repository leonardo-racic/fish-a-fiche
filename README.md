# fish-a-fiche

## Deployment

Indeed, our project has been developped enough to be deployed [in this website!](https://greandelephant.pythonanywhere.com/)

## Description

An online website where you can find small cheat-sheets for any subject, theme, or domain you are interested in such as languages' grammar/vocabulary/syntax..., math/physics/chemistry's formula, socio-eco-geopolitical definitions, theorems, proofs, computer science notions, and much more!
This project is realised thanks to GALTIER Maxime, DUCLOS Marc-Antoine, and RAČIĆ Leonardo.

## Tools for the project

- Python language used with the Flask application
- Python modules used in the project *(cf requirements.txt)*
- HTML & CSS (current's project imposed condition) & internal JavaScript

## To-do list

- Handle user authentication by hashing, storing account information, and handling the home page according to the user's account status (logged, not connected yet, etc.). ~~*STATUS WIP*~~ DONE
- Create a HTML website that helps creating cheat-sheets using markdown (or a custom dialect) and that helps previewing the cheat-sheets before publishing. ~~*PREVIEWING WIP*~~ DONE (after publishing your cheat sheet, you can see what it looks like, and can modify it as much as you want, as such previewing is not that useful)
- Handle user profiles with their own cheat-sheets by displaying their username, description, said localisation, pronouns, languages, user icon, cheat-sheets, their favorite cheat-sheets... ~~*ALMOST DONE*~~ DONE (people can like, dislike, save, update their profile... we even created a basic algorithm for the cheat sheet's visibility)
- Create the Cheat-Sheet Market (CSM), a web-page that helps the user find their desired cheat-sheet through a rough categorization of cheat-sheets by their domains and popularity, by a search bar, etc. ~~*WIP*~~ DONE
- Handle Cheat-Sheet Posts (CSP) in which there is the rendered version of the cheat-sheet, that people can eventually like, favorite, comment and discuss under it (or on an extract if possible). ~~*WIP*~~ DONE
- Documentations for each file employed in the project. ~~*WIP*~~ DONE, check it [here](/documentation/documentation.md)
  
## Dependencies

- Flask, and its own dependencies (Jinja...)
- Other Python3 libraries
- cf [requirement.txt](/requirement.txt)
