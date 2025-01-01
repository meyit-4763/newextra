from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User
from DnsXMusic import app
from datetime import datetime


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "[{full_name}](tg://user?id={user_id})\n\n"
    " ➻ 𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙞𝙛: `{user_id}`\n"
    " ➻ 𝙞𝙨𝙞𝙢: `{first_name}`\n"
    " ➻ 𝙨𝙤𝙮𝙞𝙨𝙞𝙢: `{last_name}`\n"
    " ➻ 𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙖𝙙ı: `@{username}`\n"
    " ➻ 𝙎𝙤𝙣 𝙂𝙤̈𝙧𝙪̈𝙡𝙢𝙚: `{last_online}`"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "ʀᴇᴄᴇɴᴛʟʏ"
    elif user.status == "within_week":
        return "ᴡɪᴛʜɪɴ ᴛʜᴇ ʟᴀsᴛ ᴡᴇᴇᴋ"
    elif user.status == "within_month":
        return "ᴡɪᴛʜɪɴ ᴛʜᴇ ʟᴀsᴛ ᴍᴏɴᴛʜ"
    elif user.status == "long_time_ago":
        return "ᴀ ʟᴏɴɢ ᴛɪᴍᴇ ᴀɢᴏ :("
    elif user.status == "online":
        return "ᴄᴜʀʀᴇɴᴛʟʏ ᴏɴʟɪɴᴇ"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command("whois"))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("Bu kullanıcıyı tanımıyorum.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
        infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            user_dc=user.dc_id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=LastOnline(user),
            bio=desc if desc else "ᴇᴍᴩᴛʏ.",
        ),
        disable_web_page_preview=True,
    )


__HELP__ = """
**ᴄᴏᴍᴍᴀɴᴅ:**

• /whois - **ᴋᴜsᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴄʜᴇᴄᴋ ᴇᴛ.**

**ɪɴғᴏ:**

- ᴛʜɪs ʙᴏᴛ ᴘʀᴏᴠɪᴅᴇs ᴀ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄʜᴇᴄᴋ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
- ᴜsᴇ /whois ᴄᴏᴍᴍᴀɴᴅ ғᴏʟʟᴏᴡᴇᴅ ʙʏ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴜsᴇʀ.

**ɴᴏᴛᴇ:**

- ᴛʜᴇ /whois ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜsᴇʀ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.
- ᴛʜᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ɪɴᴄʟᴜᴅᴇs ᴜsᴇʀ ɪᴅ, ғɪʀsᴛ ɴᴀᴍᴇ, ʟᴀsᴛ ɴᴀᴍᴇ, ᴜsᴇʀɴᴀᴍᴇ, ᴀɴᴅ ʟᴀsᴛ sᴇᴇɴ sᴛᴀᴛᴜs.
"""

__MODULE__ = "𝙆𝙞𝙢𝙙𝙞𝙧"
