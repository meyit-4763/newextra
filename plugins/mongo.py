import re

from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app


mongo_url_pattern = re.compile(r"mongodb(?:\+srv)?:\/\/[^\s]+")


@app.on_message(filters.command("mongocheck"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply(
            "Lütfen komuttan sonra MongoDB URL'nizi girin: `/mongocheck your_mongodb_url`"
        )
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            # MongoDB örneğine bağlanmayı dene
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()  # Bağlantı başarısız olursa bir istisna oluşturur
            await message.reply("MongoDB URL'si geçerli ve bağlantı başarılı ✅")
        except Exception as e:
            await message.reply(f"MongoDB'ye bağlanma başarısız: {e}")
    else:
        await message.reply("Ups! MongoDB formatınız geçersiz.")


__MODULE__ = "MongoDB"
__HELP__ = """
**MongoDB Kontrol Aracı:**

• `/mongocheck [mongo_url]`: Bir MongoDB URL'sinin geçerliliğini kontrol eder ve MongoDB örneğine bağlantıyı test eder.
"""