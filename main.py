import asyncio
import logging
import os
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup,
)

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
MY_ID = int(os.environ.get("MY_TELEGRAM_ID", "0"))

idioms = [
    {"phrase": "Piece of cake", "translation": "Проще пареной репы", ...},
    {"phrase": "Break a leg", "translation": "Ни пуха, ни пера", ...},
    # ... 20 idioms total
]

@dp.message(Command("start"))
async def send_welcome(message):
    # Shows welcome text + "New Idiom 🎲" button

@dp.message(F.text == "New Idiom 🎲")
async def send_idiom(message):
    # Tracks streak, picks random idiom, shows "Check my sentence ✅" button

@dp.callback_query(F.data == "check_me")
async def process_callback_check(callback_query):
    # Prompts user to write a sentence

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_sentences(message):
    # Forwards student's sentence to MY_ID (Maria)
    # Replies: "Got it! Sent to Maria. Жди фидбек! ✨"
