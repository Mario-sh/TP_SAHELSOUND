import json

def charger_catalogue(chemin):
    """
    Charge et retourne le catalogue depuis un fichier JSON.
    Retourne une liste vide si le fichier est introuvable.
    """
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fichier introuvable. Catalogue vide créé.")
        return []
    except json.JSONDecodeError:
        print("Fichier JSON corrompu.")
        return []

def sauvegarder_catalogue(data, chemin):
    """
    Écrit les données dans le fichier JSON.
    Paramètres : data (liste), chemin (str)
    """
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def lister_artistes(catalogue):
    """
    Retourne la liste des artistes avec infos résumées.
    Chaque élément : nom, genre, pays, nombre d'albums.
    """
    resultats = []
    for artiste in catalogue:
        resultats.append({
            "nom":      artiste["nom"],
            "genre":    artiste["genre"],
            "pays":     artiste["pays"],
            "nb_albums": len(artiste["albums"])
        })
    return resultats

def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche des artistes par critère (nom, genre ou id).
    Insensible à la casse pour nom et genre.
    Retourne une liste des artistes correspondants.
    """
    resultats = []
    for artiste in catalogue:
        if artiste[critere].lower() == valeur.lower():
            resultats.append(artiste)
    return resultats

def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un artiste après validation de l'identifiant.
    Retourne True si ajout réussi, False si ID déjà existant.
    """
    for a in catalogue:
        if a["id"] == artiste["id"]:
            print(f"ERREUR : L'ID {artiste['id']} existe déjà.")
            return False
    catalogue.append(artiste)
    return True

def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à l'artiste correspondant à id_artiste.
    Retourne True si réussi, False si artiste introuvable.
    """
    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            artiste["albums"].append(album)
            return True
    print(f"ERREUR : Artiste {id_artiste} introuvable.")
    return False