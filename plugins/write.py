from pyrogram import filters
from TheApi import api
from YukkiMusic import app


@app.on_message(filters.command(["write"]))
async def write(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        txt = message.reply_to_message.text
    elif len(message.command) > 1:
        txt = message.text.split(None, 1)[1]
    else:
        return await message.reply(
            "Lütfen bir mesaja yanıt verin veya komuttan sonra yazmak için bir metin yazın."
        )
    nan = await message.reply_text("İşleniyor...")
    try:
        img = await api.write(txt)
        await message.reply_photo(img)
        await nan.delete()
    except Exception as e:
        await nan.edit(str(e))


__MODULE__ = "Yaz"
__HELP__ = """
**KOMUTLAR**:
- /write: ᴡʀɪᴛᴇ ᴛᴇxᴛ ᴏɴ ᴀɴ ᴄʟᴏᴜᴅ ᴀɴᴅ ɢᴇᴛ ᴀɴ ᴇᴅɪᴛᴇᴅ ᴘʜᴏᴛᴏ.

**BİLGİ**:
- ᴍᴏᴅᴜʟᴇ ɴᴀᴍᴇ: ᴡʀɪᴛᴇ
- ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴡʀɪᴛᴇ ᴛᴇxᴛ ᴏɴ ᴀɴ ᴄʟᴏᴜᴅ ᴀɴᴅ ɢᴇᴛ ᴀɴ ᴇᴅɪᴛᴇᴅ ᴘʜᴏᴛᴏ.
- ᴄᴏᴍᴍᴀɴᴅs: /write
- ᴘᴇʀᴍɪssɪᴏɴs ɴᴇᴇᴅᴇᴅ: ʏᴏᴋ

**NOT**:
- En iyi sonuçlar için benimle bir grup sohbetinde doğrudan kullanın.