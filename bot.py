import json
from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("👋 Salom! Bu bot orqali siz hisobingizni va jarimalarni kuzatishingiz mumkin.")

@dp.message_handler(commands=["hisob"])
async def check_balance(message: types.Message):
    data = load_data()
    await message.reply(f"💰 Hisobingizda: {data['balance']} so‘m")

@dp.message_handler(commands=["jarimalar"])
async def list_penalties(message: types.Message):
    data = load_data()
    if not data["penalties"]:
        await message.reply("✅ Hech qanday jarima mavjud emas.")
    else:
        msg = "📉 Jarimalar:\n"
        for p in data["penalties"]:
            msg += f"- {p['date']} | {p['amount']} so‘m | {p['reason']}\n"
        await message.reply(msg)

@dp.message_handler(commands=["e'tiroz"])
async def appeal(message: types.Message):
    await message.reply("✉️ E’tirozingizni yozib yuboring. Admin ko‘rib chiqadi.")

@dp.message_handler(lambda msg: msg.chat.id != ADMIN_ID)
async def handle_appeals(message: types.Message):
    await bot.send_message(ADMIN_ID, f"📩 E’tiroz:\n{message.text}\n👤 From: {message.from_user.full_name}")

