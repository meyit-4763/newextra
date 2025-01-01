from pyrogram import filters
from TheApi import api
from DnsXMusic import app


@app.on_message(filters.command("tavsiye"))
async def advice(_, message):
    A = await message.reply_text("...")
    res = await api.get_advice()
    await A.edit(res)


__MODULE__ = "𝙏𝙖𝙫𝙨𝙞𝙮𝙚"
__HELP__ = """
/tavsiye - Rastgele tavsiye al"""
