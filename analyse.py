import json
import pandas as pd

def construire_dataframe(catalogue):
    """
    Convertit le catalogue en DataFrame Pandas.
    Aplatit la liste des albums avec une boucle (une ligne par album).
    """
    rows = []
    for artiste in catalogue:
        for album in artiste["albums"]:
            rows.append({
                "artiste": artiste["nom"],
                "genre":   artiste["genre"],
                "pays":    artiste["pays"],
                "titre":   album["titre"],
                "annee":   album["annee"],
                "streams": album["streams"]
            })
    return pd.DataFrame(rows)

def top5_artistes(catalogue):
    """
    Retourne le top 5 des artistes par nombre total de streams.
    Utilise groupby() et sort_values() de Pandas.
    """
    df = construire_dataframe(catalogue)
    top = (
        df.groupby("artiste")["streams"]   # grouper par artiste
          .sum()                            # additionner les streams
          .sort_values(ascending=False)     # trier du plus grand au plus petit
          .head(5)                          # garder les 5 premiers
          .reset_index()                    # remettre artiste en colonne normale
    )
    # retourner une liste de tuples (nom, streams)
    return list(zip(top["artiste"], top["streams"]))

def moyenne_streams_par_genre(catalogue):
    """
    Retourne la moyenne des streams par genre musical.
    Utilise groupby() et mean() de Pandas.
    """
    df = construire_dataframe(catalogue)
    moy = (
        df.groupby("genre")["streams"]
          .mean()
          .sort_values(ascending=False)
    )
    # retourner un dict  { genre: moyenne }
    return moy.to_dict()

def albums_par_annee(catalogue):
    """
    Retourne le nombre d'albums sortis par année.
    Utilise groupby() et count() de Pandas.
    Filtre les années > 2000 avec un masque booléen.
    """
    df = construire_dataframe(catalogue)

    # masque booléen : True pour chaque ligne dont l'année > 2000
    masque = df["annee"] > 2000
    df_filtre = df[masque]   # on applique le masque = filtre les lignes

    par_annee = (
        df_filtre.groupby("annee")["titre"]
                 .count()
                 .sort_values(ascending=False)
    )
    return par_annee.to_dict()

def exporter_rapport(catalogue):
    """
    Exporte le rapport complet dans rapport.csv.
    Utilise encoding='utf-8-sig' pour conserver les accents.
    """
    df = construire_dataframe(catalogue)
    df.to_csv("rapport.csv", index=False, encoding="utf-8-sig")