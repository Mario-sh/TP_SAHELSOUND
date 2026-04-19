import pandas as pd
import json


# Charger et transformer le JSON en DataFrame
def charger_dataframe():
    try:
        with open("catalogue.json", "r") as f:
            data = json.load(f)

        # Transformer les données imbriquées (albums) en tableau plat
        df = pd.json_normalize(
            data,
            "albums",
            ["nom", "genre", "pays"]
        )

        return df

    except FileNotFoundError:
        print("Fichier introuvable")
        return pd.DataFrame()


# Top 5 artistes par total de streams
def top_artistes(df):
    if df.empty:
        print("Aucune donnée disponible")
        return

    top = (
        df.groupby("nom")["streams"]
        .sum()
        .head(5)
    )

    print("\n=== TOP 5 ARTISTES ===")
    print(top)


# Moyenne des streams par genre
def moyenne_par_genre(df):
    if df.empty:
        print("Aucune donnée disponible")
        return

    moyenne = df.groupby("genre")["streams"].mean()

    print("\n=== MOYENNE DES STREAMS PAR GENRE ===")
    print(moyenne)


# Nombre d'albums par année
def albums_par_annee(df):
    if df.empty:
        print("Aucune donnée disponible")
        return

    nb = df.groupby("annee")["titre"].count()

    print("\n=== NOMBRE D'ALBUMS PAR ANNEE ===")
    print(nb)


# Export du rapport CSV
def exporter_csv(df, chemin_sortie="rapport.csv"):
    if df.empty:
        print("Aucune donnée à exporter")
        return

    df.to_csv(chemin_sortie, index=False, encoding="utf-8-sig")
    print(f"Rapport exporté dans {chemin_sortie}")


# (OPTION BONUS) Filtrer les albums à partir d'une année
def filtrer_par_annee(df, annee_min):
    if df.empty:
        print("Aucune donnée disponible")
        return

    filtre = df[df["annee"] >= annee_min]

    print(f"\n=== ALBUMS APRES {annee_min} ===")
    print(filtre)


# Test direct du module
if __name__ == "__main__":
    df = charger_dataframe()

    top_artistes(df)
    moyenne_par_genre(df)
    albums_par_annee(df)
    filtrer_par_annee(df, 2020)
    exporter_csv(df)
