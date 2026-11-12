"""Quiz culture — Occitanie / France / art (réponses à choix multiples)."""

from __future__ import annotations

from typing import TypedDict
import random


class Question(TypedDict):
    q: str
    choices: list[str]  # 4 choix, le premier est toujours la bonne (on shuffle à l'affichage)
    expl: str


QUESTIONS: list[Question] = [
    {
        "q": "Quel est le plus vieux jardin botanique de France ?",
        "choices": [
            "Le Jardin des Plantes de Montpellier",
            "Le Jardin des Tuileries",
            "Le Parc de la Tête d'Or",
            "Les Jardins de Versailles",
        ],
        "expl": "Créé en 1593 sous Henri IV pour la Faculté de Médecine.",
    },
    {
        "q": "Face à quel monument se trouve le Musée de la Romanité à Nîmes ?",
        "choices": [
            "Les Arènes de Nîmes",
            "La Tour Magne",
            "La Maison Carrée",
            "Le Pont du Gard",
        ],
        "expl": "La façade en « drap de verre » d'Elizabeth de Portzamparc dialogue avec les Arènes.",
    },
    {
        "q": "Dans quelle ville se trouve le musée Paul Valéry ?",
        "choices": ["Sète", "Agde", "Béziers", "Narbonne"],
        "expl": "Sur les hauteurs de Sète, avec vue sur la mer et le Mont Saint-Clair.",
    },
    {
        "q": "Que signifie MO.CO. à Montpellier ?",
        "choices": [
            "Montpellier Contemporain",
            "Musée Occitan Communal",
            "Maison des Collections",
            "Montpellier Concerts",
        ],
        "expl": "Réseau d'art contemporain (Panacée, Hôtel des collections, école…).",
    },
    {
        "q": "Où a été découvert le célèbre « Éphèbe d'Agde » ?",
        "choices": [
            "Dans l'Hérault, en fouille sous-marine",
            "Dans les Arènes de Nîmes",
            "Au fond du Jardin des Plantes",
            "Sous la place de la Comédie",
        ],
        "expl": "Statue de bronze grecque découverte dans le fleuve Hérault ; visible au musée de l'Éphèbe.",
    },
    {
        "q": "Quel architecte a signé la façade du Musée de la Romanité ?",
        "choices": [
            "Elizabeth de Portzamparc",
            "Jean Nouvel",
            "Christian de Portzamparc",
            "Norman Foster",
        ],
        "expl": "Façade en lames de verre évoquant une toge drapée.",
    },
    {
        "q": "La place de la Comédie à Montpellier doit son nom à…",
        "choices": [
            "L'Opéra Comédie",
            "Une comédie de Molière jouée en 1700",
            "Un ancien cirque romain",
            "La fontaine des Trois Grâces uniquement",
        ],
        "expl": "L'opéra (salle de comédie) a donné son nom à la place emblématique.",
    },
    {
        "q": "Dans quel département se trouve Lodève ?",
        "choices": ["Hérault (34)", "Gard (30)", "Aude (11)", "Aveyron (12)"],
        "expl": "Lodève, au nord de l'Hérault, connue pour son musée et la Savonnerie.",
    },
    {
        "q": "Quel type d'œuvre produit encore la Manufacture de la Savonnerie à Lodève ?",
        "choices": [
            "Des tapis d'apparat",
            "Du savon de Marseille",
            "Des céramiques",
            "Des vitraux",
        ],
        "expl": "Antenne de la Savonnerie nationale : tapis pour les palais de la République.",
    },
    {
        "q": "Le Pic Saint-Loup est surtout connu pour…",
        "choices": [
            "Sa silhouette et ses vins AOC",
            "Un château fort intact",
            "Une station de ski",
            "Un aéroport international",
        ],
        "expl": "Sommet emblématique au nord de Montpellier, rando + vignoble.",
    },
    {
        "q": "Quelle ligne de tram mène facilement à la place de la Comédie ?",
        "choices": [
            "Lignes 1 et 2 (arrêt Comédie)",
            "Uniquement la ligne 4",
            "Le métro ligne A",
            "Aucune, c'est piéton uniquement",
        ],
        "expl": "Tram 1 et 2 desservent l'arrêt Comédie, cœur de Montpellier.",
    },
    {
        "q": "« Culture et mobilité » est un projet porté notamment par…",
        "choices": [
            "APIJE Mobilité, IFAD et Parcours Santé Mieux Être",
            "Uniquement la mairie de Montpellier",
            "Le Louvre",
            "La SNCF seule",
        ],
        "expl": "Projet transversal d'accès à la culture avec mobilité accompagnée.",
    },
]


def tire_question() -> tuple[Question, list[str], int]:
    """
    Retourne (question, choix_mélangés, index_de_la_bonne_réponse).
    """
    q = random.choice(QUESTIONS)
    correct = q["choices"][0]
    shuffled = q["choices"][:]
    random.shuffle(shuffled)
    idx = shuffled.index(correct)
    return q, shuffled, idx
