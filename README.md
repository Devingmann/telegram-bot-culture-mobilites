# Bot Telegram — Culture & Mobilités

Bot pour le groupe **Culture et mobilité** (Montpellier & alentours).

## Fonctionnalités

| Commande / bouton | Rôle |
|-------------------|------|
| `/start` | Menu principal |
| `/sorties` | Lieux culturels dans un **rayon de ~50 km** (Montpellier, Sète, Nîmes, Lodève, Agde, Ganges…) |
| Filtres | Tous · Gratuits · Musées · Expos · Spectacles · Patrimoine · Nature |
| `/blague` | Blague légère orientée culture / patrimoine |
| `/quiz` | Quiz culture (Occitanie, art, lieux du groupe) |
| `/aide` | Liste des commandes |

Les distances sont calculées à vol d’oiseau depuis la place de la Comédie (Montpellier).

## Installation rapide

```bash
cd telegram-bot-culture-mobilites
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

1. Ouvre Telegram → **@BotFather** → `/newbot` → choisis un nom → copie le **token**.
2. Colle-le dans `.env` :
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   RADIUS_KM=50
   ```
3. Lance :
   ```bash
   python -m bot.main
   ```
4. Dans Telegram, cherche ton bot et envoie `/start`.

## Structure

```
telegram-bot-culture-mobilites/
├── bot/main.py          # Bot (handlers Telegram)
├── data/
│   ├── lieux.py         # Catalogue + distance haversine
│   ├── blagues.py       # Blagues
│   └── quiz.py          # Questions culture
├── .env.example
├── requirements.txt
└── README.md
```

## Étendre

- **Ajouter un lieu** : édite `data/lieux.py` (nom, ville, lat/lon, type, gratuit…).
- **Ajouter une blague** : `data/blagues.py`.
- **Ajouter une question** : `data/quiz.py` (la *première* réponse de `choices` est toujours la bonne ; le bot mélange à l’affichage).
- **OpenAgenda** : une clé `OPENAGENDA_API_KEY` est prévue dans `.env` pour brancher plus tard l’API live d’événements.

## Déploiement 24/7 (idées simples)

- **Raspberry Pi** / petit VPS : `screen` ou `systemd` + `python -m bot.main`
- **Railway / Render / Fly.io** : service worker qui lance `python -m bot.main`
- Ne committe **jamais** le fichier `.env` (token secret).

## Lien avec le site

Site du groupe : https://cultures-mobilite.vercel.app

Encourage les membres à proposer des idées de sorties ici **et** sur le groupe Telegram.
