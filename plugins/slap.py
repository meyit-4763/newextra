import nekos
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command("slap"))
async def slap(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(
                nekos.img("slap"),
                caption=f"{message.from_user.mention} tokatladı {message.reply_to_message.from_user.mention}",
            )
        else:
            await message.reply_video(nekos.img("slap"))
    except Exception as e:
        await message.reply_text(f"Hata: {e}")


__HELP__ = """
Kullanılabilir komutlar:
- /slap: Birine tokat atar. Eğer bir yanıt olarak kullanılırsa, yanıt verilen kullanıcıya tokat atar.
"""
__MODULE__ = "𝙏𝙤𝙠𝙖𝙩"
