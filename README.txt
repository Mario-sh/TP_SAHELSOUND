================================================================================
PROJET SAHELSOUND RECORDS - Groupe 
================================================================================

MEMBRES DU GROUPE (tout le monde a codé) :
--------------------------------------------------------------------------------
- [Nom1 Prénom1] : label.py (charger_catalogue, sauvegarder_catalogue, lister_artistes)
- [Nom2 Prénom2] : label.py (rechercher_artiste, ajouter_artiste)
- [Nom3 Prénom3] : label.py (ajouter_album, historiser, rechercher_avancee)
- [Nom4 Prénom4] : analyse.py (construire_dataframe, top5_artistes, moyenne_streams_par_genre)
- [Nom5 Prénom5] : analyse.py (albums_par_annee, exporter_rapport) + main.py

EXTENSION CHOISIE :
--------------------------------------------------------------------------------
🔍 RECHERCHE AVANCÉE (Option 1.d dans le menu Consulter)
   - Filtrage combiné : genre + pays + année minimum
   - Permet de trouver des albums selon plusieurs critères simultanément
   - Chaque critère est optionnel (laisser vide pour ignorer)

FONCTIONNALITÉS IMPLÉMENTÉES :
--------------------------------------------------------------------------------
✅ 1. Consulter le catalogue
   - 1a. Afficher tous les artistes (nom, genre, pays, nb albums)
   - 1b. Rechercher par nom ou genre
   - 1c. Afficher le détail d'un artiste (albums + streams)
   - 1d. Recherche avancée (EXTENSION)

✅ 2. Ajouter un artiste
   - Vérification d'unicité de l'ID
   - Sauvegarde immédiate dans catalogue.json

✅ 3. Ajouter un album
   - Vérification de l'existence de l'artiste
   - Validation des saisies (année, streams non négatifs)

✅ 4. Statistiques et rapport
   - 4a. Top 5 des artistes par streams totaux
   - 4b. Moyenne des streams par genre
   - 4c. Nombre d'albums par année (filtre > 2000)
   - 4d. Exporter rapport complet dans rapport.csv (formaté)

✅ 5. Quitter l'application

CONTRAINTES RESPECTÉES :
--------------------------------------------------------------------------------
- Mode console uniquement
- Persistance JSON (catalogue conservé entre exécutions)
- Modularité stricte (3 modules indépendants)
- Gestion des exceptions (fichier manquant, saisies invalides, ID inexistant)
- Docstrings sur chaque fonction
- Aucune variable globale

COMMENT LANCER L'APPLICATION :
--------------------------------------------------------------------------------
1. Installer pandas : pip install pandas
2. Exécuter : python main.py

FICHIERS FOURNIS :
--------------------------------------------------------------------------------
- main.py          : Point d'entrée et menus
- label.py         : Logique métier (JSON, recherche, historique)
- analyse.py       : Statistiques Pandas et export CSV
- catalogue.json   : Base de données (12 artistes)
- rapport.csv      : Généré par l'option 4d
- historique.log   : Généré automatiquement (historique des modifications)
- README.txt       : Ce fichier

================================================================================