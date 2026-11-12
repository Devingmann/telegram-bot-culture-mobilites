"""Lieux culturels dans un rayon ~40–50 km de Montpellier (43.6108, 3.8767)."""

from __future__ import annotations

from math import radians, cos, sin, asin, sqrt
from typing import TypedDict

MONTPELLIER = (43.6108, 3.8767)


class Lieu(TypedDict):
    nom: str
    ville: str
    type: str
    lat: float
    lon: float
    adresse: str
    note: str
    gratuit: bool


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(a))


LIEUX: list[Lieu] = [
    {"nom": "Musée Fabre", "ville": "Montpellier", "type": "musée", "lat": 43.6112, "lon": 3.8805, "adresse": "39 Bd Bonne Nouvelle", "note": "Peinture, sculpture, design — collections majeures.", "gratuit": False},
    {"nom": "Centre d'Art La Fenêtre", "ville": "Montpellier", "type": "expo", "lat": 43.6084, "lon": 3.8794, "adresse": "Aile droite Opéra Comédie, Place de la Comédie", "note": "Architecture, design graphique, espace urbain. Souvent gratuit.", "gratuit": True},
    {"nom": "MO.CO. Panacée", "ville": "Montpellier", "type": "expo", "lat": 43.6125, "lon": 3.8740, "adresse": "14 Rue de l'École de Pharmacie", "note": "Art contemporain, grande verrière, café dans la cour.", "gratuit": True},
    {"nom": "Pavillon Populaire", "ville": "Montpellier", "type": "expo", "lat": 43.6105, "lon": 3.8820, "adresse": "Esplanade Charles de Gaulle", "note": "Photographie — expos temporaires souvent gratuites.", "gratuit": True},
    {"nom": "Carré Sainte-Anne", "ville": "Montpellier", "type": "expo", "lat": 43.6089, "lon": 3.8756, "adresse": "2 Rue Sainte-Anne", "note": "Ancienne église, installations monumentales.", "gratuit": True},
    {"nom": "Jardin des Plantes", "ville": "Montpellier", "type": "nature", "lat": 43.6147, "lon": 3.8715, "adresse": "Boulevard Henri IV", "note": "Plus vieux jardin botanique de France (1593). Idéal pique-nique & dessin.", "gratuit": True},
    {"nom": "Opéra Comédie", "ville": "Montpellier", "type": "spectacle", "lat": 43.6082, "lon": 3.8790, "adresse": "Place de la Comédie", "note": "Opéra, danse, concerts — programme saisonnier.", "gratuit": False},
    {"nom": "Musée de la Romanité", "ville": "Nîmes", "type": "musée", "lat": 43.8345, "lon": 4.3600, "adresse": "16 Bd des Arènes, 30000 Nîmes", "note": "Antiquité, mosaïques, façade de verre face aux Arènes.", "gratuit": False},
    {"nom": "Arènes de Nîmes", "ville": "Nîmes", "type": "patrimoine", "lat": 43.8347, "lon": 4.3594, "adresse": "Boulevard des Arènes", "note": "Amphithéâtre romain exceptionnellement bien conservé.", "gratuit": False},
    {"nom": "Musée de Lodève", "ville": "Lodève", "type": "musée", "lat": 43.7330, "lon": 3.3160, "adresse": "Square Georges Auric", "note": "Art contemporain + géologie dans l'Hôtel du Cardinal de Fleury.", "gratuit": False},
    {"nom": "Savonnerie Nationale (Manufacture)", "ville": "Lodève", "type": "patrimoine", "lat": 43.7325, "lon": 3.3170, "adresse": "Lodève", "note": "Atelier de tapis d'apparat — visites sur réservation.", "gratuit": False},
    {"nom": "Musée Paul Valéry", "ville": "Sète", "type": "musée", "lat": 43.3970, "lon": 3.6860, "adresse": "Rue François Desnoyer, Sète", "note": "Art moderne & contemporain, vue sur la mer.", "gratuit": False},
    {"nom": "Théâtre de la Mer / Théâtre Jean-Vilar", "ville": "Sète", "type": "spectacle", "lat": 43.4035, "lon": 3.6950, "adresse": "Sète", "note": "Spectacles, festivals d'été (Jazz à Sète, etc.).", "gratuit": False},
    {"nom": "Musée de l'Éphèbe", "ville": "Agde", "type": "musée", "lat": 43.3100, "lon": 3.4750, "adresse": "Mas de la Clape, Cap d'Agde", "note": "Archéologie sous-marine — célèbre Éphèbe d'Agde.", "gratuit": False},
    {"nom": "Abbaye de Valmagne", "ville": "Villeveyrac", "type": "patrimoine", "lat": 43.4180, "lon": 3.4870, "adresse": "Route de Montagnac", "note": "Abbaye cistercienne, vignoble, concerts d'été.", "gratuit": False},
    {"nom": "Site archéologique de Lattara (Musée Henri Prades)", "ville": "Lattes", "type": "musée", "lat": 43.5680, "lon": 3.9050, "adresse": "390 Av. de Montpellier, Lattes", "note": "Fouilles gauloises et romaines au bord de l'étang.", "gratuit": False},
    {"nom": "Château de Castries", "ville": "Castries", "type": "patrimoine", "lat": 43.6580, "lon": 3.9880, "adresse": "Castries", "note": "Château Renaissance, jardins à la française.", "gratuit": False},
    {"nom": "Pic Saint-Loup / Saint-Mathieu-de-Tréviers", "ville": "Saint-Mathieu-de-Tréviers", "type": "nature", "lat": 43.7680, "lon": 3.8580, "adresse": "Autour du Pic Saint-Loup", "note": "Rando, vues, caves — cadre pour sortie nature + culture locale.", "gratuit": True},
    {"nom": "Ganges — Maison des Services / centre-ville", "ville": "Ganges", "type": "patrimoine", "lat": 43.9330, "lon": 3.7080, "adresse": "Ganges", "note": "Point de départ fréquent du groupe Culture et mobilité.", "gratuit": True},
]


def lieux_dans_rayon(radius_km: float = 40.0) -> list[tuple[Lieu, float]]:
    out: list[tuple[Lieu, float]] = []
    for lieu in LIEUX:
        d = haversine_km(MONTPELLIER[0], MONTPELLIER[1], lieu["lat"], lieu["lon"])
        if d <= radius_km:
            out.append((lieu, round(d, 1)))
    out.sort(key=lambda x: x[1])
    return out


def filtrer_par_type(type_lieu: str, radius_km: float = 40.0) -> list[tuple[Lieu, float]]:
    t = type_lieu.lower().strip()
    return [(l, d) for l, d in lieux_dans_rayon(radius_km) if t in l["type"].lower() or t in l["nom"].lower()]
