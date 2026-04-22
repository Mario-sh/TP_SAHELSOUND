"""
Module analyse.py - Statistiques avec Pandas
Auteur: Groupe SahelSound Records
"""
import pandas as pd

def construire_dataframe(catalogue):
    """
    Convertit le catalogue en DataFrame Pandas.
    Aplatit la liste des albums avec une boucle (une ligne par album).
    """
    rows = []
    for artiste in catalogue:
        for album in artiste.get("albums", []):
            rows.append({
                "artiste": artiste.get("nom", "Inconnu"),
                "genre":   artiste.get("genre", "Inconnu"),
                "pays":    artiste.get("pays", "Inconnu"),
                "titre":   album.get("titre", "Inconnu"),
                "annee":   album.get("annee", 0),
                "streams": album.get("streams", 0)
            })
    return pd.DataFrame(rows)

def top5_artistes(catalogue):
    """
    Retourne le top 5 des artistes par nombre total de streams.
    """
    df = construire_dataframe(catalogue)
    if df.empty:
        return []
    top = (
        df.groupby("artiste")["streams"]
          .sum()
          .sort_values(ascending=False)
          .head(5)
          .reset_index()
    )
    return list(zip(top["artiste"], top["streams"]))

def moyenne_streams_par_genre(catalogue):
    """
    Retourne la moyenne des streams par genre musical.
    """
    df = construire_dataframe(catalogue)
    if df.empty:
        return {}
    moy = (
        df.groupby("genre")["streams"]
          .mean()
          .sort_values(ascending=False)
          .round(0)
    )
    return moy.to_dict()

def albums_par_annee(catalogue):
    """
    Retourne le nombre d'albums sortis par année.
    Filtre les années > 2000 avec un masque booléen.
    """
    df = construire_dataframe(catalogue)
    if df.empty:
        return {}
    masque = df["annee"] > 2000
    df_filtre = df[masque]
    par_annee = (
        df_filtre.groupby("annee")["titre"]
                 .count()
                 .sort_index()
    )
    return par_annee.to_dict()

def exporter_rapport(catalogue):
    """
    Exporte le rapport complet dans rapport.csv avec un formatage professionnel.
    Le fichier contient :
    - Synthèse par artiste (streams totaux, nb albums)
    - Classement top 5
    - Moyennes par genre
    - Albums par année
    """
    df = construire_dataframe(catalogue)
    
    if df.empty:
        print("Aucune donnée à exporter.")
        return
    
    # === 1. Synthèse par artiste ===
    synthese = df.groupby(["artiste", "genre", "pays"]).agg({
        "streams": "sum",
        "titre": "count"
    }).rename(columns={"streams": "streams_totaux", "titre": "nb_albums"}).reset_index()
    
    # Trier par streams décroissants
    synthese = synthese.sort_values("streams_totaux", ascending=False)
    
    # Ajouter une colonne avec streams formatés (pour la lisibilité)
    synthese["streams_formate"] = synthese["streams_totaux"].apply(lambda x: f"{x:,}")
    
    # === 2. Top 5 ===
    top5 = synthese.head(5)[["artiste", "streams_totaux"]].copy()
    top5["classement"] = range(1, len(top5) + 1)
    top5["streams_formate"] = top5["streams_totaux"].apply(lambda x: f"{x:,}")
    
    # === 3. Moyennes par genre ===
    moy_genre = df.groupby("genre")["streams"].mean().round(0).reset_index()
    moy_genre = moy_genre.sort_values("streams", ascending=False)
    moy_genre["streams_formate"] = moy_genre["streams"].apply(lambda x: f"{x:,}")
    
    # === 4. Albums par année ===
    masque = df["annee"] > 2000
    albums_annee = df[masque].groupby("annee")["titre"].count().reset_index()
    albums_annee = albums_annee.sort_values("annee")
    albums_annee.columns = ["annee", "nb_albums"]
    
    # === 5. Statistiques générales ===
    stats = pd.DataFrame({
        "indicateur": [
            "Nombre total d'artistes",
            "Nombre total d'albums",
            "Nombre de genres différents",
            "Total des streams (tous albums)",
            "Streams moyens par album",
            "Année la plus productive",
            "Genre le plus streamé"
        ],
        "valeur": [
            df["artiste"].nunique(),
            len(df),
            df["genre"].nunique(),
            f"{df['streams'].sum():,}",
            f"{df['streams'].mean():,.0f}",
            albums_annee.loc[albums_annee["nb_albums"].idxmax(), "annee"] if not albums_annee.empty else "N/A",
            moy_genre.iloc[0]["genre"] if not moy_genre.empty else "N/A"
        ]
    })
    
    # === 6. Export vers CSV avec séparateur point-virgule (meilleur pour Excel français) ===
    with open("rapport.csv", "w", encoding="utf-8-sig") as f:
        # En-tête principal
        f.write("=" * 80 + "\n")
        f.write("RAPPORT SAHELSOUND RECORDS\n")
        f.write(f"Généré le : {pd.Timestamp.now().strftime('%d/%m/%Y à %H:%M')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Section 1 : Synthèse par artiste
        f.write("1. SYNTHÈSE PAR ARTISTE (triés par streams totaux)\n")
        f.write("-" * 80 + "\n")
        synthese.to_csv(f, index=False, sep=";", columns=["artiste", "genre", "pays", "streams_formate", "nb_albums"])
        f.write("\n")
        
        # Section 2 : Top 5
        f.write("2. TOP 5 DES ARTISTES\n")
        f.write("-" * 80 + "\n")
        top5.to_csv(f, index=False, sep=";", columns=["classement", "artiste", "streams_formate"])
        f.write("\n")
        
        # Section 3 : Moyennes par genre
        f.write("3. MOYENNE DES STREAMS PAR GENRE\n")
        f.write("-" * 80 + "\n")
        moy_genre.to_csv(f, index=False, sep=";", columns=["genre", "streams_formate"])
        f.write("\n")
        
        # Section 4 : Albums par année
        f.write("4. NOMBRE D'ALBUMS SORTIS PAR ANNÉE (après 2000)\n")
        f.write("-" * 80 + "\n")
        albums_annee.to_csv(f, index=False, sep=";")
        f.write("\n")
        
        # Section 5 : Statistiques générales
        f.write("5. STATISTIQUES GÉNÉRALES\n")
        f.write("-" * 80 + "\n")
        stats.to_csv(f, index=False, sep=";")
        f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("FIN DU RAPPORT\n")
        f.write("=" * 80 + "\n")
    
    print("✅ rapport.csv généré avec succès (formaté et lisible)")