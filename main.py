import asyncio
import random
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

load_dotenv()

# --- CONFIG ---
API_TOKEN = os.getenv("API_TOKEN")
MY_ID = int(os.getenv("MY_ID", "133724864"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Temporary storage for student progress
user_data = {}

IDIOMS = [
    {"phrase": "Piece of cake", "translation": "Проще пареной репы", "example": "This exam was a piece of cake!"},
    {"phrase": "Break a leg", "translation": "Ни пуха, ни пера", "example": "Go out there and break a leg!"},
    {"phrase": "Under the weather", "translation": "Плохо себя чувствовать", "example": "I'm feeling a bit under the weather today."},
    {"phrase": "Call it a day", "translation": "Закругляться", "example": "We've worked 10 hours. Let's call it a day!"},
    {"phrase": "Spill the beans", "translation": "Выболтать секрет", "example": "Don't spill the beans about the surprise party!"},
    {"phrase": "Cut to the chase", "translation": "Перейти сразу к делу", "example": "Stop talking about the weather and cut to the chase."},
    {"phrase": "Beat around the bush", "translation": "Ходить вокруг да около", "example": "Don't beat around the bush and tell me what happened."},
    {"phrase": "Hit the nail on the head", "translation": "Попасть в точку", "example": "You hit the nail on the head with that analysis."},
    {"phrase": "Once in a blue moon", "translation": "Очень редко", "example": "I only see him once in a blue moon."},
    {"phrase": "The elephant in the room", "translation": "Очевидная проблема", "example": "We need to talk about the elephant in the room: our budget."},
    {"phrase": "Back to the drawing board", "translation": "Начать всё сначала", "example": "The project failed, so it's back to the drawing board."},
    {"phrase": "Bite the bullet", "translation": "Стиснуть зубы / решиться", "example": "I hate the dentist, but I'll just have to bite the bullet."},
    {"phrase": "Best of both worlds", "translation": "Лучшее из двух миров", "example": "Working from home gives her the best of both worlds."},
    {"phrase": "Barking up the wrong tree", "translation": "Искать не там / ошибаться", "example": "If you think I stole it, you're barking up the wrong tree."},
    {"phrase": "Blessing in disguise", "translation": "Не было бы счастья, да несчастье помогло", "example": "Losing that job was a blessing in disguise."},
    {"phrase": "Cold shoulder", "translation": "Оказать холодный прием", "example": "After our fight, she gave me the cold shoulder."},
    {"phrase": "Get out of hand", "translation": "Выйти из-под контроля", "example": "The party got a bit out of hand last night."},
    {"phrase": "Hang in there", "translation": "Держись! (поддержка)", "example": "I know it's tough, but hang in there!"},
    {"phrase": "Look before you leap", "translation": "Семь раз отмерь — один отрежь", "example": "It's a big investment. Look before you leap."},
    {"phrase": "See eye to eye", "translation": "Сходиться во взглядах", "example": "My boss and I don't always see eye to eye."}
]

# --- KEYBOARDS ---
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="New Idiom 🎲")]],
    resize_keyboard=True
)

check_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Check my sentence ✅", callback_data="check_me")]]
)

# --- HANDLERS ---
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        f"Hi! I'm your English mentor bot. 🇺🇸\nReady to learn some cool American idioms?\nClick the button below!",
        reply_markup=main_kb
    )

@dp.message(F.text == "New Idiom 🎲")
async def send_idiom(message: types.Message):
    user_id = message.from_user.id
    idiom = random.choice(IDIOMS)
    
    if user_id not in user_data:
        user_data[user_id] = {"streak": 1, "current_idiom": idiom['phrase']}
    else:
        user_data[user_id]["streak"] += 1
        user_data[user_id]["current_idiom"] = idiom['phrase']

    response = (
        f"🔥 Your streak: {user_data[user_id]['streak']} idioms\n\n"
        f"<b>{idiom['phrase']}</b> — {idiom['translation']}\n"
        f"Example: <i>{idiom['example']}</i>\n\n"
        "Now, write your own sentence and I'll send it to Maria!"
    )
    await message.answer(response, parse_mode="HTML", reply_markup=check_kb)

@dp.callback_query(F.data == "check_me")
async def process_callback_check(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Waiting for your sentence... ✍️")

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_sentences(message: types.Message):
    user_info = f"Student @{message.from_user.username or message.from_user.first_name}"
    current_idiom = user_data.get(message.from_user.id, {}).get("current_idiom", "Unknown")
    
    report = f"📬 <b>New Sentence!</b>\n\n{user_info}\nIdiom: {current_idiom}\nSentence: {message.text}"
    await bot.send_message(MY_ID, report, parse_mode="HTML")
    
    await message.answer("Got it! Maria will check it soon. Keep it up! ✨")

async def main():
    print("STUDENT BOT STARTED WITH SAFE CONFIG")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
