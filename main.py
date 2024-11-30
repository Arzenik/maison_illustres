from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Modèle Pydantic
class Maison(BaseModel):
    nom: str
    description: str
    auteur_nom: str
    annee_obtention: int
    date_maj: str
    code_postal: int
    region: str
    departement: str
    pays: str
    commune: str
    adresse: str
    latitude: float
    longitude: float

# Connexion SQLite
def get_db_connection():
    conn = sqlite3.connect("maisons_illustres.db")
    conn.row_factory = sqlite3.Row
    return conn

# Routes API
@app.get("/maisons")
def get_maisons():
    conn = get_db_connection()
    maisons = conn.execute("""
        SELECT maisons.*, localisation.* 
        FROM maisons
        INNER JOIN localisation ON maisons.id = localisation.maison_id
    """).fetchall()
    conn.close()
    return [dict(maison) for maison in maisons]

@app.get("/maisons/{id}")
def get_maison(id: int):
    conn = get_db_connection()
    maison = conn.execute("""
        SELECT maisons.*, localisation.* 
        FROM maisons
        INNER JOIN localisation ON maisons.id = localisation.maison_id
        WHERE maisons.id = ?
    """, (id,)).fetchone()
    conn.close()
    if maison is None:
        raise HTTPException(status_code=404, detail="Maison non trouvée")
    return dict(maison)

@app.post("/maisons")
def create_maison(maison: Maison):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO maisons (nom, description, auteur_nom, annee_obtention, date_maj)
        VALUES (?, ?, ?, ?, ?)
    """, (maison.nom, maison.description, maison.auteur_nom, maison.annee_obtention, maison.date_maj))
    maison_id = cursor.lastrowid
    cursor.execute("""
        INSERT INTO localisation (maison_id, code_postal, region, departement, pays, commune, adresse, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (maison_id, maison.code_postal, maison.region, maison.departement, maison.pays, maison.commune, maison.adresse, maison.latitude, maison.longitude))
    conn.commit()
    conn.close()
    return {"message": "Maison ajoutée avec succès"}

@app.put("/maisons/{id}")
def update_maison(id: int, maison: Maison):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE maisons
        SET nom = ?, description = ?, auteur_nom = ?, annee_obtention = ?, date_maj = ?
        WHERE id = ?
    """, (maison.nom, maison.description, maison.auteur_nom, maison.annee_obtention, maison.date_maj, id))
    cursor.execute("""
        UPDATE localisation
        SET code_postal = ?, region = ?, departement = ?, pays = ?, commune = ?, adresse = ?, latitude = ?, longitude = ?
        WHERE maison_id = ?
    """, (maison.code_postal, maison.region, maison.departement, maison.pays, maison.commune, maison.adresse, maison.latitude, maison.longitude, id))
    conn.commit()
    conn.close()
    return {"message": "Maison mise à jour avec succès"}

@app.delete("/maisons/{id}")
def delete_maison(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM localisation WHERE maison_id = ?", (id,))
    cursor.execute("DELETE FROM maisons WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Maison supprimée avec succès"}

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API Maisons des Illustres!"}


