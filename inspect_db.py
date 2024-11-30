import sqlite3

# Connexion à la base SQLite
conn = sqlite3.connect("maisons_illustres.db")
cursor = conn.cursor()

# Récupérer la liste des tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables dans la base de données :")
for table in tables:
    print(f"- {table[0]}")

# Afficher les colonnes de chaque table
for table in tables:
    print(f"\nStructure de la table '{table[0]}':")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  - {column[1]} ({column[2]})")

conn.close()

