#!/usr/bin/env python3
"""Bot Telegram Culture & Mobilités — sorties (~50 km), blagues, quiz."""

from __future__ import annotations

import logging
import os
import random
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

ROOT = Path(__file__).resolve().parent.parent
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.blagues import BLAGUES
from data.lieux import filtrer_par_type, lieux_dans_rayon
from data.quiz import tire_question

load_dotenv(ROOT / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
RADIUS_KM = float(os.getenv("RADIUS_KM", "50"))

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("culture-bot")

QUIZ_STATE: dict[int, dict] = {}


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📅 Sorties / lieux", callback_data="menu_sorties"),
                InlineKeyboardButton("🎲 Blague", callback_data="menu_blague"),
            ],
            [
                InlineKeyboardButton("🧠 Quiz culture", callback_data="menu_quiz"),
                InlineKeyboardButton("ℹ️ Aide", callback_data="menu_aide"),
            ],
        ]
    )


def sorties_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Tous les lieux", callback_data="lieux_all"),
                InlineKeyboardButton("Gratuits", callback_data="lieux_gratuit"),
            ],
            [
                InlineKeyboardButton("Musées", callback_data="lieux_musee"),
                InlineKeyboardButton("Expos", callback_data="lieux_expo"),
            ],
            [
                InlineKeyboardButton("Spectacles", callback_data="lieux_spectacle"),
                InlineKeyboardButton("Patrimoine", callback_data="lieux_patrimoine"),
            ],
            [
                InlineKeyboardButton("Nature", callback_data="lieux_nature"),
                InlineKeyboardButton("← Menu", callback_data="menu_home"),
            ],
        ]
    )


def format_lieu(lieu: dict, dist: float) -> str:
    gratuit = " · 🆓 gratuit" if lieu.get("gratuit") else ""
    return (
        f"📍 *{lieu['nom']}* ({lieu['ville']}) — {dist} km{gratuit}\n"
        f"   _{lieu['type']}_ · {lieu['adresse']}\n"
        f"   {lieu['note']}"
    )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    prenom = user.first_name if user else "toi"
    text = (
        f"Salut {prenom} ! 👋\n\n"
        "Je suis le bot *Culture & Mobilités* — rayon ~50 km autour de Montpellier "
        "(Sète, Nîmes, Lodève, Agde, Ganges…).\n\n"
        "Je peux te proposer des *lieux culturels*, te raconter une *blague*, "
        "ou lancer un *quiz culture*.\n\n"
        "Utilise les boutons ou les commandes :\n"
        "/sorties · /blague · /quiz · /aide"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=menu_keyboard())


async def cmd_aide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "*Commandes*\n"
        "/start — menu principal\n"
        "/sorties — lieux culturels (filtre par type)\n"
        "/blague — une blague culture / patrimoine\n"
        "/quiz — question de culture (Occitanie & art)\n"
        "/aide — ce message\n\n"
        "*Astuce* : propose aussi tes idées de sorties sur le groupe Telegram "
        "du projet Culture et mobilité !"
    )
    target = update.callback_query.message if update.callback_query else update.message
    if update.callback_query:
        await update.callback_query.answer()
        await target.reply_text(text, parse_mode="Markdown", reply_markup=menu_keyboard())
    else:
        await target.reply_text(text, parse_mode="Markdown", reply_markup=menu_keyboard())


async def cmd_blague(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    blague = random.choice(BLAGUES)
    text = f"🎭 *Blague du jour*\n\n{blague}"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode="Markdown", reply_markup=menu_keyboard()
        )
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=menu_keyboard())


async def cmd_sorties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"🗺️ *Lieux culturels* dans un rayon de *{int(RADIUS_KM)} km* "
        "autour de Montpellier.\n\nChoisis un filtre :"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode="Markdown", reply_markup=sorties_keyboard()
        )
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=sorties_keyboard())


async def send_lieux_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    items: list,
    titre: str,
) -> None:
    if not items:
        msg = "Aucun lieu trouvé pour ce filtre dans le rayon."
    else:
        lines = [f"*{titre}* ({len(items)} résultats)\n"]
        for lieu, dist in items[:12]:
            lines.append(format_lieu(lieu, dist))
            lines.append("")
        if len(items) > 12:
            lines.append(f"_… et {len(items) - 12} autres._")
        msg = "\n".join(lines)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            msg, parse_mode="Markdown", reply_markup=sorties_keyboard()
        )
    else:
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=sorties_keyboard())


async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q, shuffled, correct_idx = tire_question()
    user_id = update.effective_user.id
    QUIZ_STATE[user_id] = {
        "choices": shuffled,
        "correct_idx": correct_idx,
        "expl": q["expl"],
        "q": q["q"],
    }

    letters = "ABCD"
    buttons = [
        [InlineKeyboardButton(f"{letters[i]}. {shuffled[i]}", callback_data=f"quiz_{i}")]
        for i in range(4)
    ]
    buttons.append([InlineKeyboardButton("← Menu", callback_data="menu_home")])
    kb = InlineKeyboardMarkup(buttons)

    text = f"🧠 *Quiz culture*\n\n{q['q']}"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data or ""
    user_id = update.effective_user.id

    if data == "menu_home":
        await query.answer()
        await query.message.reply_text("Menu principal 👇", reply_markup=menu_keyboard())
        return

    if data == "menu_aide":
        await cmd_aide(update, context)
        return

    if data == "menu_blague":
        await cmd_blague(update, context)
        return

    if data == "menu_sorties":
        await cmd_sorties(update, context)
        return

    if data == "menu_quiz":
        await cmd_quiz(update, context)
        return

    if data.startswith("lieux_"):
        kind = data.replace("lieux_", "")
        if kind == "all":
            items = lieux_dans_rayon(RADIUS_KM)
            await send_lieux_list(update, context, items, "Tous les lieux")
        elif kind == "gratuit":
            items = [(l, d) for l, d in lieux_dans_rayon(RADIUS_KM) if l.get("gratuit")]
            await send_lieux_list(update, context, items, "Lieux gratuits")
        else:
            items = filtrer_par_type(kind, RADIUS_KM)
            await send_lieux_list(update, context, items, f"Filtre : {kind}")
        return

    if data.startswith("quiz_"):
        await query.answer()
        state = QUIZ_STATE.get(user_id)
        if not state:
            await query.message.reply_text(
                "Quiz expiré — relance /quiz", reply_markup=menu_keyboard()
            )
            return
        try:
            chosen = int(data.split("_")[1])
        except (IndexError, ValueError):
            return
        correct = state["correct_idx"]
        if chosen == correct:
            text = (
                f"✅ *Bravo !*\n\nBonne réponse : *{state['choices'][correct]}*\n\n"
                f"💡 {state['expl']}"
            )
        else:
            text = (
                f"❌ Raté…\n\nLa bonne réponse était : *{state['choices'][correct]}*\n\n"
                f"💡 {state['expl']}"
            )
        QUIZ_STATE.pop(user_id, None)
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Encore un quiz", callback_data="menu_quiz"),
                    InlineKeyboardButton("← Menu", callback_data="menu_home"),
                ]
            ]
        )
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    await query.answer()


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    t = (update.message.text or "").lower()
    if any(w in t for w in ("blague", "joke", "mdr", "humour")):
        await cmd_blague(update, context)
    elif any(w in t for w in ("quiz", "question", "culture")):
        await cmd_quiz(update, context)
    elif any(w in t for w in ("sortie", "lieu", "musée", "expo", "où")):
        await cmd_sorties(update, context)
    else:
        await update.message.reply_text(
            "Dis-moi : *sorties*, *blague* ou *quiz* — ou utilise /start",
            parse_mode="Markdown",
            reply_markup=menu_keyboard(),
        )


def main() -> None:
    if not TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN manquant.\n"
            "1. Ouvre Telegram → @BotFather → /newbot\n"
            "2. Copie le token dans .env (voir .env.example)"
        )

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("aide", cmd_aide))
    app.add_handler(CommandHandler("help", cmd_aide))
    app.add_handler(CommandHandler("blague", cmd_blague))
    app.add_handler(CommandHandler("sorties", cmd_sorties))
    app.add_handler(CommandHandler("lieux", cmd_sorties))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    log.info("Bot Culture & Mobilités démarré (rayon %s km)", RADIUS_KM)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
