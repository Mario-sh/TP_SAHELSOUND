import label
import analyse

CHEMIN = "catalogue.json"

# ── SOUS-MENU 1 ─────────────────────────────
def menu_consulter(catalogue):
    """Sous-menu pour consulter le catalogue."""
    while True:
        print("\n-- Consulter le catalogue --")
        print("  a. Afficher tous les artistes")
        print("  b. Rechercher par nom ou genre")
        print("  c. Détail d'un artiste")
        print("  r. Retour au menu principal")
        choix = input("Choix : ").strip().lower()

        if choix == "a":
            # option a : lister tous les artistes
            liste = label.lister_artistes(catalogue)
            print(f"\n{'NOM':<20} {'GENRE':<15} {'PAYS':<12} ALBUMS")
            print("-" * 55)
            for a in liste:
                print(f"{a['nom']:<20} {a['genre']:<15} {a['pays']:<12} {a['nb_albums']}")

        elif choix == "b":
            # option b : rechercher par nom ou genre
            critere = input("Rechercher par nom ou genre ? ").strip().lower()
            if critere not in ("nom", "genre"):
                print("Critère invalide. Tapez 'nom' ou 'genre'.")
                continue
            valeur = input(f"Valeur : ").strip()
            resultats = label.rechercher_artiste(catalogue, critere, valeur)
            if resultats:
                for a in resultats:
                    print(f"  → {a['nom']} | {a['genre']} | {a['pays']}")
            else:
                print("Aucun résultat.")

        elif choix == "c":
            # option c : détail complet d'un artiste
            id_art = input("ID de l'artiste (ex: ART-001) : ").strip().upper()
            resultats = label.rechercher_artiste(catalogue, "id", id_art)
            if resultats:
                a = resultats[0]
                print(f"\n{a['nom']} | {a['genre']} | {a['pays']}")
                print(f"{'TITRE':<25} {'ANNEE':<8} STREAMS")
                print("-" * 42)
                for alb in a["albums"]:
                    print(f"{alb['titre']:<25} {alb['annee']:<8} {alb['streams']:,}")
            else:
                print("Artiste introuvable.")

        elif choix == "r":
            break
        else:
            print("Choix invalide.")

# ── SOUS-MENU 2 ─────────────────────────────
def menu_ajouter_artiste(catalogue):
    """Sous-menu pour ajouter un nouvel artiste."""
    print("\n-- Ajouter un artiste --")
    print("  a. Saisir les informations")
    print("  r. Retour")
    choix = input("Choix : ").strip().lower()

    if choix == "a":
        id_art = input("ID (ex: ART-004) : ").strip().upper()
        nom    = input("Nom de scène : ").strip()
        genre  = input("Genre musical : ").strip()
        pays   = input("Pays d'origine : ").strip()

        nouvel_artiste = {
            "id":     id_art,
            "nom":    nom,
            "genre":  genre,
            "pays":   pays,
            "albums": []
        }
        if label.ajouter_artiste(catalogue, nouvel_artiste):
            label.sauvegarder_catalogue(catalogue, CHEMIN)
            print(f"Artiste '{nom}' ajouté et sauvegardé.")

# ── SOUS-MENU 3 ─────────────────────────────
def menu_ajouter_album(catalogue):
    """Sous-menu pour ajouter un album à un artiste existant."""
    print("\n-- Ajouter un album --")
    print("  a. Saisir les informations de l'album")
    print("  r. Retour")
    choix = input("Choix : ").strip().lower()

    if choix == "a":
        id_art = input("ID de l'artiste : ").strip().upper()
        titre  = input("Titre de l'album : ").strip()

        # saisie sécurisée année
        while True:
            try:
                annee = int(input("Année de sortie : ").strip())
                break
            except ValueError:
                print("Entrez une année valide.")

        # saisie sécurisée streams
        while True:
            try:
                streams = int(input("Nombre de streams : ").strip())
                if streams < 0:
                    print("Valeur négative non acceptée.")
                    continue
                break
            except ValueError:
                print("Entrez un entier valide.")

        album = {"titre": titre, "annee": annee, "streams": streams}

        if label.ajouter_album(catalogue, id_art, album):
            label.sauvegarder_catalogue(catalogue, CHEMIN)
            print(f"Album '{titre}' ajouté et sauvegardé.")

# ── SOUS-MENU 4 ─────────────────────────────
def menu_statistiques(catalogue):
    """Sous-menu pour afficher les statistiques et exporter."""
    while True:
        print("\n-- Statistiques et rapport --")
        print("  a. Top 5 artistes par streams")
        print("  b. Moyenne des streams par genre")
        print("  c. Nombre d'albums par année")
        print("  d. Exporter rapport.csv")
        print("  r. Retour")
        choix = input("Choix : ").strip().lower()

        if choix == "a":
            top = analyse.top5_artistes(catalogue)
            print(f"\n{'ARTISTE':<20} STREAMS TOTAUX")
            print("-" * 35)
            for nom, streams in top:
                print(f"{nom:<20} {streams:,}")

        elif choix == "b":
            moy = analyse.moyenne_streams_par_genre(catalogue)
            print(f"\n{'GENRE':<18} MOYENNE")
            print("-" * 30)
            for genre, val in moy.items():
                print(f"{genre:<18} {val:,.0f}")

        elif choix == "c":
            par_annee = analyse.albums_par_annee(catalogue)
            print(f"\n{'ANNEE':<8} NB ALBUMS")
            print("-" * 18)
            for annee, nb in sorted(par_annee.items()):
                print(f"{annee:<8} {nb}")

        elif choix == "d":
            analyse.exporter_rapport(catalogue)
            print("rapport.csv généré avec succès.")

        elif choix == "r":
            break
        else:
            print("Choix invalide.")

# ── MENU PRINCIPAL ───────────────────────────
def main():
    """Point d'entrée de l'application."""
    print("=" * 40)
    print("   SahelSound Records — Catalogue")
    print("=" * 40)

    # chargement unique au démarrage
    catalogue = label.charger_catalogue(CHEMIN)

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Consulter le catalogue")
        print("2. Ajouter un artiste")
        print("3. Ajouter un album")
        print("4. Statistiques et rapport")
        print("5. Quitter")

        choix = input("Ton choix : ").strip()

        if   choix == "1": menu_consulter(catalogue)
        elif choix == "2": menu_ajouter_artiste(catalogue)
        elif choix == "3": menu_ajouter_album(catalogue)
        elif choix == "4": menu_statistiques(catalogue)
        elif choix == "5":
            print("À bientôt !")
            break
        else:
            print("Choix invalide. Entre un chiffre entre 1 et 5.")

if __name__ == "__main__":
    main()