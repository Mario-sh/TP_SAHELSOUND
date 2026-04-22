"""
Module main.py - Point d'entrée de l'application
Auteur: Groupe SahelSound Records
"""

import label
import analyse

CHEMIN = "catalogue.json"


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
            liste = label.lister_artistes(catalogue)
            if not liste:
                print("Aucun artiste dans le catalogue.")
            else:
                print(f"\n{'NOM':<20} {'GENRE':<15} {'PAYS':<12} ALBUMS")
                print("-" * 55)
                for a in liste:
                    print(
                        f"{a['nom']:<20} {a['genre']:<15} {a['pays']:<12} {a['nb_albums']}"
                    )

        elif choix == "b":
            critere = input("Rechercher par nom ou genre ? ").strip().lower()
            if critere not in ("nom", "genre"):
                print("Critère invalide. Tapez 'nom' ou 'genre'.")
                continue
            valeur = input("Valeur : ").strip()
            resultats = label.rechercher_artiste(catalogue, critere, valeur)
            if resultats:
                for a in resultats:
                    print(f"  → {a['nom']} | {a['genre']} | {a['pays']}")
            else:
                print("Aucun résultat.")

        elif choix == "c":
            id_art = input("ID de l'artiste (ex: ART-001) : ").strip().upper()
            resultats = label.rechercher_artiste(catalogue, "id", id_art)
            if resultats:
                a = resultats[0]
                print(f"\n{a['nom']} | {a['genre']} | {a['pays']}")
                print(f"{'TITRE':<25} {'ANNEE':<8} STREAMS")
                print("-" * 42)
                for alb in a.get("albums", []):
                    print(
                        f"{alb['titre']:<25} {alb['annee']:<8} {alb['streams']:,}"
                    )
            else:
                print("Artiste introuvable.")

        elif choix == "r":
            break
        else:
            print("Choix invalide.")


def menu_ajouter_artiste(catalogue):
    """Sous-menu pour ajouter un nouvel artiste."""
    print("\n-- Ajouter un artiste --")
    id_art = input("ID (ex: ART-013) : ").strip().upper()
    nom = input("Nom de scène : ").strip()
    genre = input("Genre musical : ").strip()
    pays = input("Pays d'origine : ").strip()

    nouvel_artiste = {
        "id": id_art,
        "nom": nom,
        "genre": genre,
        "pays": pays,
        "albums": [],
    }
    if label.ajouter_artiste(catalogue, nouvel_artiste):
        label.sauvegarder_catalogue(catalogue, CHEMIN)
        print(f"Artiste '{nom}' ajouté et sauvegardé.")


def menu_ajouter_album(catalogue):
    """Sous-menu pour ajouter un album à un artiste existant."""
    print("\n-- Ajouter un album --")
    id_art = input("ID de l'artiste : ").strip().upper()

    # Vérifier que l'artiste existe avant de saisir l'album
    artiste = label.rechercher_artiste(catalogue, "id", id_art)
    if not artiste:
        print("Artiste introuvable.")
        return

    titre = input("Titre de l'album : ").strip()

    while True:
        try:
            annee = int(input("Année de sortie : ").strip())
            break
        except ValueError:
            print("Entrez une année valide.")

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


def menu_statistiques(catalogue):
    """Sous-menu pour afficher les statistiques et exporter."""
    if not catalogue:
        print("Catalogue vide. Impossible d'afficher les statistiques.")
        return

    while True:
        print("\n" + "=" * 50)
        print("   📊 STATISTIQUES ET RAPPORT")
        print("=" * 50)
        print("  a. Top 5 artistes par streams")
        print("  b. Moyenne des streams par genre")
        print("  c. Nombre d'albums par année")
        print("  d. Exporter rapport complet")
        print("  r. Retour au menu principal")
        print("-" * 50)
        choix = input("Votre choix : ").strip().lower()

        if choix == "a":
            top = analyse.top5_artistes(catalogue)
            if not top:
                print("Aucune donnée disponible.")
            else:
                print("\n" + "=" * 45)
                print("   🏆 TOP 5 DES ARTISTES PAR STREAMS")
                print("=" * 45)
                print(f"{'#' :<3} {'ARTISTE':<22} {'STREAMS TOTAUX':>18}")
                print("-" * 45)
                for i, (nom, streams) in enumerate(top, 1):
                    # Formater avec séparateurs de milliers
                    streams_formate = f"{streams:,}".replace(",", " ")
                    print(f"{i:<3} {nom:<22} {streams_formate:>18}")
                print("=" * 45)

        elif choix == "b":
            moy = analyse.moyenne_streams_par_genre(catalogue)
            if not moy:
                print("Aucune donnée disponible.")
            else:
                print("\n" + "=" * 45)
                print("   📈 MOYENNE DES STREAMS PAR GENRE")
                print("=" * 45)
                print(f"{'GENRE':<22} {'STREAMS MOYENS':>21}")
                print("-" * 45)
                for genre, val in moy.items():
                    # Formater avec séparateurs de milliers
                    val_formate = f"{val:,.0f}".replace(",", " ")
                    print(f"{genre:<22} {val_formate:>21}")
                print("=" * 45)

        elif choix == "c":
            par_annee = analyse.albums_par_annee(catalogue)
            if not par_annee:
                print("Aucune donnée disponible.")
            else:
                print("\n" + "=" * 45)
                print("   📅 NOMBRE D'ALBUMS SORTIS PAR ANNÉE")
                print("=" * 45)
                print(f"{'ANNÉE':<10} {'NB ALBUMS':>15}")
                print("-" * 45)
                total_albums = 0
                for annee, nb in par_annee.items():
                    print(f"{annee:<10} {nb:>15}")
                    total_albums += nb
                print("-" * 45)
                print(f"{'TOTAL':<10} {total_albums:>15}")
                print("=" * 45)

        elif choix == "d":
            print("\n📁 Export du rapport en cours...")
            analyse.exporter_rapport(catalogue)  # Version améliorée
            # Si tu préfères garder la version simple (CSV uniquement) :
            # analyse.exporter_rapport_simple(catalogue)

        elif choix == "r":
            break
        else:
            print("❌ Choix invalide.")


def main():
    """Point d'entrée de l'application."""
    print("=" * 40)
    print("   SahelSound Records — Catalogue")
    print("=" * 40)

    catalogue = label.charger_catalogue(CHEMIN)

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Consulter le catalogue")
        print("2. Ajouter un artiste")
        print("3. Ajouter un album")
        print("4. Statistiques et rapport")
        print("5. Quitter")

        choix = input("Ton choix : ").strip()

        if choix == "1":
            menu_consulter(catalogue)
        elif choix == "2":
            menu_ajouter_artiste(catalogue)
        elif choix == "3":
            menu_ajouter_album(catalogue)
        elif choix == "4":
            menu_statistiques(catalogue)
        elif choix == "5":
            print("À bientôt !")
            break
        else:
            print("Choix invalide. Entre un chiffre entre 1 et 5.")


if __name__ == "__main__":
    main()
