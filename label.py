import json

# Charger le catalogue
def charger_catalogue():
    try:
        with open("catalogue.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fichier introuvable")
        return []


# Sauvegarder le catalogue
def sauvegarder_catalogue(data):
    with open("catalogue.json", "w") as f:
        json.dump(data, f, indent=4)


# Lister les artistes
def lister_artistes(catalogue):
    for artiste in catalogue:
        print(f"{artiste['nom']} | {artiste['genre']} | {artiste['pays']} | {len(artiste['albums'])} albums")


# Rechercher artiste
def rechercher_artiste(catalogue, critere, valeur):
    resultats = []
    for artiste in catalogue:

        if valeur.lower() in artiste[critere].lower():
            resultats.append(artiste)
    return resultats


# Ajouter un artiste
def ajouter_artiste(catalogue, artiste):
    for a in catalogue:
        if a["id"] == artiste["id"]:
            print("ID déjà existant")
            return catalogue

    catalogue.append(artiste)
    print("Artiste ajouté")
    return catalogue


# Ajouter un album
def ajouter_album(catalogue, id_artiste, album):
    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            artiste["albums"].append(album)
            print("Album ajouté")
            return catalogue

    print("Artiste non trouvé")
    return catalogue
