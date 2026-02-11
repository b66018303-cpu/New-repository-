import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")  # токен берётся из переменной окружения

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

def get_random_card(rarity):
    folder = RARITIES[rarity]["folder"]
    files = os.listdir(folder)
    return os.path.join(folder, random.choice(files))

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎴 Добро пожаловать в Femboy Card Game!\nНапиши /card чтобы получить карточку!")

@dp.message(Command("card"))
async def card(message: types.Message):
    rarity = get_random_rarity()
    card_path = get_random_card(rarity)

    caption = f"✨ Тебе выпала карта!\n⭐ Редкость: {rarity}"

    photo = types.FSInputFile(card_path)
    await message.answer_photo(photo, caption=caption)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
