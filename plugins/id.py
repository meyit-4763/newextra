from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command("id"))
async def get_id(client, message):
    try:
        if not message.reply_to_message and message.chat:
            await message.reply(
                f"Kullanıcı <b>{message.from_user.first_name}'ın</b> ID'si <code>{message.from_user.id}</code>.\nBu sohbetin ID'si: <code>{message.chat.id}</code>."
            )
        elif not message.reply_to_message.sticker or message.reply_to_message is None:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"İletilen {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} ID'si <code>{message.reply_to_message.forward_from_chat.id}</code>."
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"İletilen kullanıcı, {message.reply_to_message.forward_from.first_name} ID'si <code>{message.reply_to_message.forward_from.id}</code>."
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "Üzgünüm, o kullanıcının mesajını hiç görmedim veya ID'yi almakta başarısız oldum."
                )
            else:
                await message.reply(
                    f"Kullanıcı {message.reply_to_message.from_user.first_name}'ın ID'si <code>{message.reply_to_message.from_user.id}</code>."
                )
        elif message.reply_to_message.sticker:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"İletilen {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} ID'si <code>{message.reply_to_message.forward_from_chat.id}</code> \nVe yanıtlanan sticker ID'si <code>{message.reply_to_message.sticker.file_id}</code>."
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"İletilen kullanıcı, {message.reply_to_message.forward_from.first_name} ID'si <code>{message.reply_to_message.forward_from.id}</code> \nVe yanıtlanan sticker ID'si <code>{message.reply_to_message.sticker.file_id}</code>."
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "Üzgünüm, o kullanıcının mesajını hiç görmedim veya ID'yi almakta başarısız oldum."
                )

            else:
                await message.reply(
                    f"Kullanıcı {message.reply_to_message.from_user.first_name}'ın ID'si <code>{message.reply_to_message.from_user.id}</code>\nVe yanıtlanan sticker ID'si <code>{message.reply_to_message.sticker.file_id}</code>."
                )
        else:
            await message.reply(
                f"Kullanıcı {message.reply_to_message.from_user.first_name}'ın kullanıcı ID'si <code>{message.reply_to_message.from_user.id}</code>."
            )
    except Exception as r:
        await message.reply(f"ID'yi alırken bir hata oluştu. {r}")


__MODULE__ = "Kullanıcı ID"
__HELP__ = """
**ID Alıcı:**

• `/id`: Kullanıcı ve sohbet ID'lerini alır.
"""