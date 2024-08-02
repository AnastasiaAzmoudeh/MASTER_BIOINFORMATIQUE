Pour Lancer le projet: python3 GUI_FINAL.py 

(Les fonctions pour lire le fichier sont importer dans le fichier GUI_FINAL.py)

GUI_FINAL.py
La classe AAZ_GUI crée l’interface graphique et les fonctions nécessaires aux analyses


-creerInterface : Crée l’interface, les comboboxes, l’entry box, les curseurs et les boutons nécessaires afin de lancer les fonctions.

-search_org : permet en recherchant le nom précis d’un organisme d’obtenir son assembly

sort_with_prefixe et update_list : permet de trier la liste pour que lorsque l’on cherche un organisme dans la combobox on puisse le trouver plus rapide

-analysis

Lorsqu'on choisit l’assembly d’une séquence query et l’assembly d’une séquence subject via les combobox on récupère ces valeurs et puis on regarde si elles sont présentes dans la table gène. 
Ensuite, nous effectuons plusieurs conditions selon ces résultats. Si query et subject sont présent dans la table gène, nous testons si leur combinaison est la table Blast. Si leur combinaison est présente dans la table Blast alors on récupère les résultats dans la table Blast qui sont nécessaires afin de tracer le dotplot. C'est-à-dire le couple de deux gènes avec leur e-value. 
On récupère également des données de la table de Gène pour les séquences query et subject. On récupère le nom du gène et sa position. Grâce à ces données on peut tracer le dotplot.
Si cette combinaison n’est pas dans la table Blast, il faut lancer la commande blast dans le terminal grâce à subprocess.run et on rentre ces données dans la table Blast.

Si une ou les deux séquences ne sont pas dans la table Gène alors il faut les télécharger grâce au lien web conservé dans la table Organisme. Grâce à subprocess.run et la commande wget on peut 
télécharger les fichiers et entrer les données dans la table Gène. On pourra ensuite lancer la commande blast et entrer les données dans la table Blast.

get_infos: donne des informations sur le dotplot en général

Fichier FctLireFiles.py

lire_fichier(fichier) Prend un fichier fasta en entrée et stocke les noms des séquences dans un dictionnaire en clé et en valeur la position et la longueur de la séquence. 
Cette fonction sert à remplir la table Gène.

lire_blast(fichier) prend en entrée un fichier blast.out et sert à récupérer dans un dictionnaire dont la clé est le tuple de query et subject avec en valeur e-value correspondante.

lire_blast_remplir(fichier) prend un fichier blast.out en entrée et récupère tout les lignes afin de les entrer dans une table blastinterm. 
Si plusieurs lignes ont le même couple de gène, alors on sélectionne celui avec le hit le plus significatif.

etape0(fichier): prend un fichier.txt avec toutes les lignes de  données de assembly par exemple ou tous les noms des organismes et les mets dans une liste

make_drop(fichie): prend un fichier appelle etape0 et puis rempli la liste drop qui sert de liste pour les combobox 

BASE DE DONNEES:

-Table organisme
-Table gène
-Table blast 
-Table blastinterm

Autres tables présentes dans le dump ont aide pour la première phase de remplissage des tables




