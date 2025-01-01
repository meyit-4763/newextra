import asyncio
from random import choice

import pyfiglet
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from YukkiMusic import app


# Verilen metni figlet formatında döndür ve bir klavye oluştur
def figle(text):
    x = pyfiglet.FigletFont.getFonts()  # Mevcut fontları al
    font = choice(x)  # Rastgele bir font seç
    figled = str(pyfiglet.figlet_format(text, font=font))  # Metni figlet formatında oluştur
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="〆 𝙁𝙤𝙣𝙩 𝘿𝙚𝙜̆𝙞𝙨̧𝙩𝙞𝙧 〆", callback_data="figlet"),  # Font değiştirme butonu
                InlineKeyboardButton(text="〆 𝙆𝙖𝙥𝙖𝙩 〆", callback_data="close_reply"),  # Kapatma butonu
            ]
        ]
    )
    return figled, keyboard  # Figlet metni ve klavye döndür


@app.on_message(filters.command("figlet"))
async def echo(bot, message):
    global text
    try:
        text = message.text.split(" ", 1)[1]  # Kullanıcının girdiği metni al
    except IndexError:
        return await message.reply_text("𝙊̈𝙧𝙣𝙚𝙠:\n\n`/figlet 𝙈𝙮𝙩 `")  # Hata mesajı
    kul_text, keyboard = figle(text)  # Figlet metnini oluştur
    await message.reply_text(
        f"𝙄̇𝙨̧𝙩𝙚 𝙛𝙞𝙜𝙡𝙚𝙩:\n<pre>{kul_text}</pre>",
        quote=True,
        reply_markup=keyboard,  # Klavye ile birlikte mesajı gönder
    )


@app.on_callback_query(filters.regex("figlet"))
async def figlet_handler(Client, query: CallbackQuery):
    try:
        kul_text, keyboard = figle(text)  # Figlet metnini yeniden oluştur
        await query.message.edit_text(
            f"𝙄̇𝙨̧𝙩𝙚 𝙛𝙞𝙜𝙡𝙚𝙩:\n<pre>{kul_text}</pre>", reply_markup=keyboard  # Mesajı güncelle
        ) 
    except FloodWait as e:
        await asyncio.sleep(e.value)  # FloodWait hatası durumunda bekle

    except Exception as e:
        return await query.answer(e, show_alert=True)  # Hata durumunda kullanıcıya mesaj göster


__MODULE__ = "𝙎̧𝙚𝙠𝙞𝙡"  # Modül adı
__HELP__ = """
**𝙎̧𝙚𝙠𝙞𝙡𝙡𝙞 𝙔𝙖𝙯ı**

• /figlet <metin> - 𝙑𝙚𝙧𝙞𝙡𝙚𝙣 𝙢𝙚𝙩𝙣𝙞𝙣 𝙛𝙞𝙜𝙡𝙚𝙩 𝙛𝙤𝙧𝙢𝙖𝙩ı𝙣𝙙𝙖 𝙤𝙡𝙪𝙨̧𝙩𝙪𝙧𝙪𝙡𝙢𝙖𝙨ı𝙣ı 𝙨𝙖𝙜̆𝙡𝙖𝙧.
"""
