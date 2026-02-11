import os
import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- 1. ТОКЕН ---
TOKEN = os.getenv("8332132764:AAFIw6WhDGZtjiAaZbjkKM2bv-ddLakjItE")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Environment на Render")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. КАРТЫ ---
RARITIES = {
    "Common": {"chance": 60, "folder": "cards/common"},
    "Rare": {"chance": 25, "folder": "cards/rare"},
    "Epic": {"chance": 10, "folder": "cards/epic"},
    "Legendary": {"chance": 5, "folder": "cards/legendary"},
}

def get_random_rarity():
    roll = random.randint(1, 100)
    current = 0
    for rarity, data in RARITIES.items():
        current += data["chance"]
        if roll <= current:
            return rarity
    return "Common"

def get_random_card(rarity):
    folder = RARITIES[rarity]["folder"]
    
    # Проверка на существование папки
    if not os.path.exists(folder):
        logging.warning(f"⚠️ Папка {folder} не найдена")
        return None
    
    files = os.listdir(folder)
    if not files:
        logging.warning(f"⚠️ В папке {folder} нет файлов")
        return None
        
    return os.path.join(folder, random.choice(files))

# --- 3. КОМАНДЫ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎴 Добро пожаловать в Femboy Card Game!\nНапиши /card чтобы получить карточку!")

@dp.message(Command("card"))
async def card(message: types.Message):
    rarity = get_random_rarity()
    card_path = get_random_card(rarity)

    if card_path and os.path.exists(card_path):
        photo = types.FSInputFile(card_path)
        await message.answer_photo(photo, caption=f"✨ Тебе выпала карта!\n⭐ Редкость: {rarity}")
    else:
        await message.answer(f"🎴 Тебе выпала карта!\n⭐ Редкость: {rarity}\n(🖼️ Изображение временно недоступно)")

# --- 4. ДЕРЖИМ ВКЛЮЧЕННЫМ ---
async def keep_alive():
    while True:
        await asyncio.sleep(300)  # 5 минут
        logging.info("🤖 Бот работает")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Бот запускается...", flush=True)
    
    # Фоновая задача, чтобы Render не усыпил
    asyncio.create_task(keep_alive())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
