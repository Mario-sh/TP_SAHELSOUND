import json
def charger_catalogue(chemin) :
    """Fonction pour lire et retourner le json"""

    try:
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)
        return donnees
    except FileNotFoundError :
        return []
    except json.JSONDecodeError :
        return []
    

def sauvegarder_catalogue(donnees, chemin) :
    """Fonction pour écrire dans le json"""

    try:
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
    except IOError :
        print("Erreur : impossible d'écrire le fichier.")
  
def lister_artistes(catalogue) : 
    """Fonction qui parcourt la liste des articles et retourne un résumé"""
    if len(catalogue) == 0:
        return []
    resultats = []
    for artiste in catalogue : 
    
        ligne = f"{artiste['id']} | {artiste['nom']} | {artiste['genre']} | {artiste['pays']} | {len(artiste['albums'])} albums"
        resultats.append(ligne)
    return resultats
        

def rechercher_artiste(catalogue, critere, valeur) : 
    """Fontion qui permet de chercher un ou plusieurs artistes selon un critère"""
    result = []
    for artiste in catalogue :
        if artiste[critere] == valeur : 
            result.append(artiste)
    return result

def ajouter_artiste(catalogue, artiste):
    """Fonction qui ajoute un nouvel artiste à la liste après avoir validé que les données sont correctes"""
    # vérifier les champs
    if "id" in artiste and "nom" in artiste and "genre" in artiste and "pays" in artiste:
        # vérifier l'id
        id_existe = False
        for a in catalogue:
            if a["id"] == artiste["id"]:
                id_existe = True
        # ajouter ou afficher erreur
        if id_existe:
            print("Erreur : ID déjà utilisé.")
        else:
            catalogue.append(artiste)
    else:
        print("Erreur : champs obligatoires manquants.")
    return catalogue

def ajouter_album(catalogue, id_artiste, album):
    """Fonction pour ajouter un album"""
    artiste_trouve = False
    if "annee" in album and "titre" in album and "streams" in album:
        for artiste in catalogue:
            if artiste["id"] == id_artiste:
                artiste_trouve = True
                artiste["albums"].append(album)
    else:
        print("Erreur : champs obligatoires manquants.")
    
    if not artiste_trouve:
        print("Erreur : artiste introuvable.")
    
    return catalogue
            