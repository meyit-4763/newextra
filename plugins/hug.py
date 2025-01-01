import nekos
from pyrogram import filters
from DnsXMusic import app


@app.on_message(filters.command("hug"))
async def huggg(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(
                nekos.img("hug"),
                caption=f"{message.from_user.mention} {message.reply_to_message.from_user.mention} kişisine sarıldı.",
            )
        else:
            await message.reply_video(nekos.img("hug"))
    except Exception as e:
        await message.reply_text(f"Hata: {e}")


__MODULE__ = "𝘼𝙣𝙞𝙢𝙖𝙨𝙮𝙤𝙣"
__HELP__ = """
Bu bot aşağıdaki komutlara yanıt verir:

- /hug: Sarılma animasyonu gönderir.

**Komutlar**

- /hug: Sarılma animasyonu gönderir. Başka bir mesaja yanıt olarak kullanıldığında, göndereni ve sarılanı belirtir.

**Nasıl Kullanılır**

- Sarılma animasyonu göndermek için /hug kullanın.
- /hug ile bir mesaja yanıt vererek, göndereni ve sarılanı belirten bir sarılma animasyonu gönderin.

**Notlar**

- Botun video/sticker göndermesine izin veren sohbet ayarlarını kontrol edin, böylece tam işlevsellik sağlanır.
"""
