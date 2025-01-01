from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api
from DnsXMusic import app


@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "𝙊̈𝙧𝙣𝙚𝙠:\n\n`/ai 𝙗𝙖𝙨𝙞𝙩 𝙗𝙞𝙧 𝙬𝙚𝙗 𝙨𝙞𝙩𝙚𝙨𝙞 𝙠𝙤𝙙𝙪 𝙮𝙖𝙯 𝙝𝙩𝙢𝙡 𝙘𝙨𝙨, 𝙟𝙨 𝙠𝙪𝙡𝙡𝙖𝙣𝙖𝙧𝙖𝙠?`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text  # Yanıtlanan mesajın metnini al
    else:
        user_input = " ".join(message.command[1:])  # Komutun geri kalanını birleştir

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)  # Yazma eylemi gönder
    results = await api.chatgpt(user_input)  # API'den yanıt al
    await message.reply_text(results)  # Yanıtı gönder


__MODULE__ = "𝙂𝙗𝙩"  # Modül adı
__HELP__ = """
/advice - 𝘽𝙤𝙩 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙧𝙖𝙨𝙩𝙜𝙚𝙡𝙚 𝙩𝙖𝙫𝙨𝙞𝙮𝙚 𝙖𝙡ı𝙣
/ai [soru] - 𝘾𝙝𝙖𝙩𝙂𝙋𝙏'𝙣𝙞𝙣 𝘼𝙄 𝙨𝙤𝙧𝙪𝙣𝙪 𝙨𝙤𝙧
/gemini [soru] - 𝙂𝙤𝙤𝙜𝙡𝙚 𝙂𝙚𝙢𝙞𝙣𝙞 𝘼𝙄 𝙨𝙤𝙧𝙪𝙣𝙪 𝙨𝙤𝙧
"""
