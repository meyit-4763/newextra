import asyncio

from pyrogram import enums, filters
from pyrogram.errors import FloodWait
from YukkiMusic import app


@app.on_message(filters.command("bots") & filters.group)
async def bots(client, message):
    try:
        botList = []  # Botların listesini tutmak için boş bir liste oluştur
        async for bot in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.BOTS
        ):
            botList.append(bot.user)  # Botları listeye ekle
        lenBotList = len(botList)  # Bot sayısını al
        text3 = f"**𝘽𝙤𝙩 𝙇𝙞𝙨𝙩𝙚𝙨𝙞 - {message.chat.title}**\n\n🤖 𝘽𝙤𝙩𝙡𝙖𝙧\n"
        while len(botList) > 1:  # Liste 1'den fazla bot içeriyorsa
            bot = botList.pop(0)  # İlk botu çıkar
            text3 += f"├ @{bot.username}\n"  # Botun kullanıcı adını ekle
        else:  # Liste 1 bot içeriyorsa
            bot = botList.pop(0)  # Son botu çıkar
            text3 += f"└ @{bot.username}\n\n"  # Botun kullanıcı adını ekle
            text3 += f"**𝙏𝙤𝙥𝙡𝙖𝙢 𝘽𝙤𝙩 𝙎𝙖𝙮ı𝙨ı**: {lenBotList}**"  # Toplam bot sayısını ekle
            await app.send_message(message.chat.id, text3)  # Mesajı gönder
    except FloodWait as e:  # FloodWait hatası alırsak
        await asyncio.sleep(e.value)  # Belirtilen süre kadar bekle


__MODULE__ = "𝘽𝙤𝙩𝙨"  # Modül adı
__HELP__ = """
**𝘽𝙤𝙩𝙡𝙖𝙧**

• /bots - 𝙂𝙧𝙪𝙗𝙪𝙣 𝙞𝙘̧𝙞𝙣𝙙𝙚𝙠𝙞 𝙗𝙤𝙩𝙡𝙖𝙧ı𝙣 𝙡𝙞𝙨𝙩𝙚𝙨𝙞𝙣𝙞 𝙜𝙤̈𝙨𝙩𝙚𝙧𝙞𝙧.
"""
