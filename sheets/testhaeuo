# Documentation
---

## Organisation des fichiers

Les conversions sont effectuées par 3 fichiers : 
- [ConvertToBin.py](../ConvertToBin.py)
- [ConvertToDec.py](../ConvertToDec.py)
- [ConvertToHex.py](../ConvertToHex.py)

L'IHM est assurée par le fichier :
- [ParseInput.py](../ParseInput.py)

Utilisant les fichiers :

- [AsciiArt.py](../AsciiArt.py)
- [AsciiArtFont.txt](../AsciiArtFont.txt)

Afin de générer le titre.

La mise en relation des différentes parties du programme est effectuée par le fichier :

- [main.py](../main.py)

## Les principales fonctions

### Dans ConvertToDec.py

- `convert_to_dec (n, base)` est une fonction qui transforme n'importe quelle chaîne de caractères `n` associée à une base disponible appelée `base` en un nombre décimal.
Cette fonction utilise les fonctions :

- `convert_hex_to_dec (h)` convertissant un hexadecimal `h` en décimal

- `convert_bin_to_dec (b)` convertissant un binaire `b` en décimal

### Dans ConvertToHex.py

- `convert_to_hex (n, base)` transformant n'importe quelle chaîne de caractères `n` associée à une base disponible appelée `base` en un nombre hexadécimal.
elle utilise les fonctions :

- `convert_dec_to_hex (n)` convertissant un décimal `n` en hexadécimal

- `convert_bin_to_hex (b)` convertissant un binaire `b` en un hexadécimal, en le convertissant d'abord en décimal via `convert_to_dec` puis en hexadécimal via `convert_dec_to_hex`.

### Dans ConvertToBin.py

- `convert_to_bin (n, base)` transformant n'importe quelle chaîne de caractères `n` associée a une base disponible appelée `base` en un nombre binaire.
elle utilise les fonctions :

- `convert_dec_to_bin (n)` convertissant un décimal `n` en binaire

- `convert_hex_to_bin (h)` convertissant un hexadécimal `h` en un binaire, en le convertissant d'abord en décimal via `convert_to_dec` puis en binaire via `convert_dec_to_bin`.

### Dans ParseInput.py

- `output_result (n, initial_base, final_base)` est une fonction affichant le résultat de la conversion de l'entier naturel `n` en base `initial_base` à la base `final_base`. Cette fonction prend en arguments trois strings et ne retourne rien.

- `get_inputs ()` est une fonction permettant de recueillir les entrées de l'utilisateur (étant le nombre entier à convertir, sa base, ainsi que la base dans laquelle on veut convertir l'entier naturel). Par conséquence, cette fonction ne prend aucun argument, mais renvoie trois strings.

- `wait_for_input (text, error_text, *possible_inputs)` est une fonction permettant d'obtenir une entrée de l'utilisateur après avoir afficher le string `texte`. Si l'entrée donnée n'est pas dans les différents `*possible_inputs`, alors on affiche `error_text` et on redemande à l'utilisateur d'entrer une information jusqu'à ce qu'elle soit validée.

### Dans AsciiArt.py

- `print_with_font (text)` est une fonction qui premièrement importe l'équivalent de chaque lettre à l'aide de la fonction `get_font`. Elle utilise ces équivalences pour écrire un texte donné en argument avec la police choisie.

- `get_font ()` est une fonction qui retourne un dictionnaire comprenant pour chaque lettre une liste correspondant à chaque ligne de la police.

### Dans main.py

- `introduce_program ()` écrit les informations d'utilisation du programme ainsi que le titre à l'aide de la fonction `print_with_font ()` importée depuis [AsciiArt.py](../AsciiArt.py) .

- `get_str_list_conversions (conversions)` est une fonction prenant une liste de dictionnaires (`conversions`) et renvoie une liste de textes telle que chaque texte résume une conversion, dans l'ordre dans lequel les conversions ont été réalisées.

- `display_conversions ()` écrit en sortie toutes les conversions qui ont été faites depuis le lancement du programme, à l'aide de la fonction `get_str_list_conversions`.

- `update_txt_file (conversions)` est une fonction prenant une liste de dictionnaires (`conversions`) et écrit à la suite du fichier `conversions.txt` les conversions, à l'aide de la fonction `get_str_list_conversions`.

- La dernière partie n'est exécutée que si le programme est executé directement. Elle appelle la fonction `introduce_program ()`, réalisant les conversions de l'utilisateur et les affichant après que l'utilisateur n'ait plus envie de réaliser des conversions. 

## Utilisation

Chaque fichier peut être utilisé indépendemment des autres, mis à part [ConvertToBin.py](../ConvertToBin.py)et [ConvertToHex.py](../ConvertToHex.py) qui emploient [ConvertToDec.py](../ConvertToDec.py), en l'important a l'aide du keyword `import`.
