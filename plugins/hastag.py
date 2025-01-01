from pyrogram import filters
from TheApi import api
from YukkiMusic import app


@app.on_message(filters.command("hastag"))
async def hastag(bot, message):
    try:
        text = message.text.split(" ", 1)[1]  # Kullanıcının girdiği metni al
        res = await api.gen_hashtag(text)  # API'den hashtagleri oluştur
    except IndexError:
        return await message.reply_text("Örnek:\n\n/hastag python")  # Kullanıcıdan örnek isteme

    await message.reply_text(f"İşte sizin hashtag'iniz:\n<pre>{res}</pre>", quote=True)  # Hashtagleri kullanıcıya gönder


__MODULE__ = "Hashtag"
__HELP__ = """
**Hashtag Üretici:**

• `/hashtag [metin]`: Verilen metin için hashtag'ler oluşturur.
"""