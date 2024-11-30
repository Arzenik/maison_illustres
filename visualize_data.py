import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Étape 1 : Récupérer les données depuis l'API
response = requests.get("http://127.0.0.1:8000/maisons")
maisons = response.json()

# Étape 2 : Transformer les données en DataFrame pandas
df = pd.DataFrame(maisons)

# Étape 3 : Diagramme 1 - Répartition par région
plt.figure(figsize=(10, 6))
region_counts = df['region'].value_counts()
region_counts.plot(kind='bar', color='skyblue')
plt.title("Répartition des Maisons par Région")
plt.xlabel("Région")
plt.ylabel("Nombre de Maisons")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Étape 4 : Diagramme 2 - Histogramme des années d'obtention
plt.figure(figsize=(10, 6))
sns.histplot(df['annee_obtention'], bins=20, kde=True, color='orange')
plt.title("Distribution des Années d'Obtention")
plt.xlabel("Année d'Obtention")
plt.ylabel("Nombre de Maisons")
plt.tight_layout()
plt.show()

# Étape 5 : Carte avec Folium
map = folium.Map(location=[48.8566, 2.3522], zoom_start=6)  # Centre sur la France
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['nom']} ({row['commune']})"
    ).add_to(map)
map.save("map.html")
print("Carte enregistrée sous 'map.html'. Ouvrez ce fichier pour visualiser les points.")
