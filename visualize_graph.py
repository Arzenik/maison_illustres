import networkx as nx
import matplotlib.pyplot as plt

# Données fournies
data = {
    "nom": "Musée Clemenceau",
    "pays": "France",
    "region": "Île-de-France",
    "departement": "Paris",
    "commune": "Paris",
    "numero_et_libelle_de_la_voie": "44 Rue Francisque Gay",
    "complement_d_adresse": None,
    "latitude": "48.85287",
    "longitude": "2.343452",
    "types": ["Histoire et politique"],
    "annee_d_obtention": "2012",
    "description": "Homme d’État...",
    "auteur_nom_de_l_illustre": "Georges Clemenceau",
    "date_de_maj": "2022-07-22 10:28:41",
}

# Création du graphe
G = nx.DiGraph()  # Graphe orienté

# Ajouter les relations hiérarchiques géographiques
G.add_edge(data["nom"], data["pays"])
G.add_edge(data["pays"], data["region"])
G.add_edge(data["region"], data["departement"])
G.add_edge(data["departement"], data["commune"])
G.add_edge(data["commune"], data["numero_et_libelle_de_la_voie"] or "N/A")
G.add_edge(
    data["numero_et_libelle_de_la_voie"] or "N/A",
    f"Latitude: {data['latitude']}, Longitude: {data['longitude']}",
)

# Ajouter auteur et description à la hiérarchie
G.add_edge(data["nom"], f"Auteur: {data['auteur_nom_de_l_illustre']}")
G.add_edge(f"Auteur: {data['auteur_nom_de_l_illustre']}", f"Description: {data['description']}")

# Ajouter des relations spécifiques au musée
G.add_edge(data["nom"], f"Types: {', '.join(data['types'])}")
G.add_edge(data["nom"], f"Année d'obtention: {data['annee_d_obtention']}")
G.add_edge(data["nom"], f"Date de mise à jour: {data['date_de_maj']}")

# Dessiner le graphe
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)  # Positionnement automatique

# Dessiner les nœuds et les arêtes
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    font_size=10,
    node_color="lightblue",
    edge_color="gray",
    arrows=True,
    arrowstyle="->",
    arrowsize=20,
)

plt.title("Schéma hiérarchique des données d'un musée avec auteur et description")
plt.show()
