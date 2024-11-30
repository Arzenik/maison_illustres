import sqlite3
import json

# Connexion SQLite
def create_database():
    conn = sqlite3.connect("maisons_illustres.db")
    cursor = conn.cursor()

    # Création des tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            auteur_nom TEXT,
            annee_obtention INTEGER,
            date_maj TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS localisation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maison_id INTEGER NOT NULL,
            code_postal INTEGER,
            region TEXT,
            departement TEXT,
            pays TEXT,
            commune TEXT,
            adresse TEXT,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (maison_id) REFERENCES maisons (id)
        )
    """)
    conn.commit()
    conn.close()

# Chargement des données JSON
def load_data(json_file):
    conn = sqlite3.connect("maisons_illustres.db")
    cursor = conn.cursor()

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

        for item in data:
            # Insertion dans la table maisons
            cursor.execute("""
                INSERT INTO maisons (nom, description, auteur_nom, annee_obtention, date_maj)
                VALUES (?, ?, ?, ?, ?)
            """, (
                item["nom"], 
                item["description"], 
                item["auteur_nom_de_l_illustre"], 
                item["annee_d_obtention"], 
                item["date_de_maj"]
            ))

            maison_id = cursor.lastrowid

            # Insertion dans la table localisation
            cursor.execute("""
                INSERT INTO localisation (maison_id, code_postal, region, departement, pays, commune, adresse, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                maison_id,
                item["code_postal"],
                item["region"],
                item["departement"],
                item["pays"],
                item["commune"],
                item["numero_et_libelle_de_la_voie"],
                item["latitude"],
                item["longitude"]
            ))

    conn.commit()
    conn.close()

# Exécution
if __name__ == "__main__":
    create_database()
    load_data("illustres.json")
    print("Base de données créée et données chargées avec succès.")
