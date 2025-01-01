from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command(["qr"]))
async def write_text(client, message):
    if len(message.command) < 2:
        await message.reply_text("**Kullanım**: `/qr https://t.me/vivekkumar07089`")
        return
    text = " ".join(message.command[1:])
    photo_url = "https://apis.xditya.me/qr/gen?text=" + text
    await app.send_photo(
        chat_id=message.chat.id, photo=photo_url, caption="İşte QR kodunuz"
    )


__MODULE__ = "Qʀɢᴇɴ"

__HELP__ = """
Bu modül QR kodları oluşturur. `/qr` komutunu takip eden metin veya URL ile kodlamak istediğiniz içeriği sağlayın. Örneğin, `/qr https://t.me/vivekkumar07089`. Bot, sağlanan girdi için bir QR kodu oluşturacaktır. URL'ler için protokolü (http:// veya https://) dahil etmeyi unutmayın. QR kodları oluşturmanın keyfini çıkarın!
"""