import random

import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from YukkiMusic import app


@app.on_message(filters.command(["wall", "wallpaper"]))
async def wall(_, message: Message):

    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        text = None
    if not text:
        return await message.reply_text("`Lütfen arama yapmak için bir sorgu verin.`")
    m = await message.reply_text("Aranıyor...")
    try:
        url = requests.get(f"https://api.safone.dev/wall?query={text}").json()[
            "results"
        ]
        ran = random.randint(0, 7)
        await message.reply_photo(
            photo=url[ran]["imageUrl"],
            caption=f"🥀 **İsteyen:** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Bağlantı", url=url[ran]["imageUrl"])],
                ]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit_text(
            f"`Duvar kağıdı bulunamadı: `{text}`",
        )


__MODULE__ = "𝙒𝘼𝙇𝙇"
__HELP__ = """
**KOMUTLAR:**

• /WALL - **Duvar kağıdını indir ve gönder.**

**BİLGİ:**

- Bu bot, duvar kağıdını indirmek ve göndermek için bir komut sağlar.
- Duvar kağıdı aramak ve göndermek için bir metin ile /WALL komutunu kullanın.

**NOT:**

- Bu komut, duvar kağıdını indirmek ve göndermek için kullanılabilir.
"""
