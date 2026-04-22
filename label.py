"""
Module label.py - Gestion du catalogue JSON
Auteur: Groupe SahelSound Records
"""
import json
import os
from datetime import datetime

# === Gestion du fichier JSON ===

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
    """
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# === Gestion de l'historique (extension facultative) ===

def historiser(action, details, log_file="historique.log"):
    """
    Écrit une ligne dans le fichier d'historique.
    Extension facultative.
    """
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action} : {details}\n")


# === Fonctions métier ===

def lister_artistes(catalogue):
    """
    Retourne la liste des artistes avec infos résumées.
    Chaque élément : nom, genre, pays, nombre d'albums.
    """
    resultats = []
    for artiste in catalogue:
        resultats.append({
            "nom":      artiste.get("nom", "Inconnu"),
            "genre":    artiste.get("genre", "Inconnu"),
            "pays":     artiste.get("pays", "Inconnu"),
            "nb_albums": len(artiste.get("albums", []))
        })
    return resultats

def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche des artistes par critère (nom, genre ou id).
    Insensible à la casse.
    Retourne une liste des artistes correspondants.
    """
    if critere not in ("nom", "genre", "id"):
        return []
    resultats = []
    for artiste in catalogue:
        if artiste.get(critere, "").lower() == valeur.lower():
            resultats.append(artiste)
    return resultats

def rechercher_avancee(catalogue, genre=None, pays=None, annee_min=None):
    """
    RECHERCHE AVANCÉE (Extension)
    Filtre les albums selon plusieurs critères :
    - genre : filtrer par genre musical (optionnel)
    - pays : filtrer par pays d'origine (optionnel)
    - annee_min : ne garder que les albums sortis après cette année (optionnel)
    
    Retourne une liste d'albums correspondant aux critères avec infos artiste.
    """
    resultats = []
    
    for artiste in catalogue:
        # Vérifier les critères sur l'artiste
        if genre and artiste.get("genre", "").lower() != genre.lower():
            continue
        if pays and artiste.get("pays", "").lower() != pays.lower():
            continue
        
        # Parcourir les albums
        for album in artiste.get("albums", []):
            if annee_min and album.get("annee", 0) < annee_min:
                continue
            
            resultats.append({
                "artiste": artiste.get("nom"),
                "genre": artiste.get("genre"),
                "pays": artiste.get("pays"),
                "titre": album.get("titre"),
                "annee": album.get("annee"),
                "streams": album.get("streams")
            })
    
    return resultats

def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un artiste après validation de l'identifiant.
    Retourne True si ajout réussi, False si ID déjà existant.
    """
    for a in catalogue:
        if a.get("id") == artiste.get("id"):
            print(f"ERREUR : L'ID {artiste['id']} existe déjà.")
            return False
    catalogue.append(artiste)
    # Extension : historisation
    historiser("AJOUT ARTISTE", f"{artiste['nom']} ({artiste['id']})")
    return True

def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à l'artiste correspondant à id_artiste.
    Retourne True si réussi, False si artiste introuvable.
    """
    for artiste in catalogue:
        if artiste.get("id") == id_artiste:
            artiste.setdefault("albums", []).append(album)
            # Extension : historisation
            historiser("AJOUT ALBUM", f"{album['titre']} -> {artiste['nom']} ({id_artiste})")
            return True
    print(f"ERREUR : Artiste {id_artiste} introuvable.")
    return False