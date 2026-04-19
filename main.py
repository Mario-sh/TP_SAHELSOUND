from label import *

FICHIER = "catalogue.json"

catalogue = charger_catalogue(FICHIER)

while True:
    print("\n=== MENU ===")
    print("1. Voir artistes")
    print("2. Rechercher artiste")
    print("3. Ajouter artiste")
    print("4. Ajouter album")
    print("5. Quitter")

    choix = input("Choix : ")

    if choix == "1":
        lister_artistes(catalogue)

    elif choix == "2":
        critere = input("nom ou genre : ")
        valeur = input("Recherche : ")
        resultats = rechercher_artiste(catalogue, critere, valeur)
        for a in resultats:
            print(a["nom"], "-", a["genre"])

    elif choix == "3":
        id_artiste = input("ID : ")
        nom = input("Nom : ")
        genre = input("Genre : ")
        pays = input("Pays : ")

        nouvel_artiste = {
            "id": id_artiste,
            "nom": nom,
            "genre": genre,
            "pays": pays,
            "albums": []
        }

        catalogue = ajouter_artiste(catalogue, nouvel_artiste)
        sauvegarder_catalogue(catalogue, FICHIER)

    elif choix == "4":
        id_artiste = input("ID artiste : ")
        titre = input("Titre album : ")
        annee = int(input("Année : "))
        streams = int(input("Streams : "))

        album = {
            "titre": titre,
            "annee": annee,
            "streams": streams
        }

        catalogue = ajouter_album(catalogue, id_artiste, album)
        sauvegarder_catalogue(catalogue, FICHIER)

    elif choix == "5":
        print("Fin du programme")
        break

    else:
        print("Choix invalide")
