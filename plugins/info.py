import os

from pyrogram import enums, filters
from pyrogram.types import Message
from DnsXMusic import app
from DnsXMusic.misc import SUDOERS
from DnsXMusic.utils.database import is_gbanned_user


n = "\n"
w = " "


def bold(x):
    return f"**{x}:** "


def bold_ul(x):
    return f"**--{x}:**-- "


def mono(x):
    return f"`{x}`{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        if value is not None:
            text += (
                indent * w
                + bold(key)
                + (
                    (value[0] + n)
                    if isinstance(value, list) and isinstance(value[0], str)
                    else mono(value)
                )
            )
    return text


async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "Son zamanlarda."
        elif x == enums.UserStatus.LAST_WEEK:
            return "Geçen hafta."
        elif x == enums.UserStatus.LONG_AGO:
            return "Uzun zaman önce."
        elif x == enums.UserStatus.OFFLINE:
            return "Çevrimdışı."
        elif x == enums.UserStatus.ONLINE:
            return "Çevrimiçi."
    except BaseException:
        return "**Bir şeyler yanlış gitti!**"


async def get_user_info(user, already=False):
    if not already:
        user = await app.get_users(user)
    if not user.first_name:
        return ["Silinmiş hesap", None]
    user_id = user.id
    online = await userstatus(user_id)
    username = user.username
    first_name = user.first_name
    mention = user.mention("Bağlantı")
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_gbanned = await is_gbanned_user(user_id)
    is_sudo = user_id in SUDOERS
    is_premium = user.is_premium
    body = {
        "İsim": [first_name],
        "Kullanıcı Adı": [("@" + username) if username else "Yok"],
        "ID": user_id,
        "DC ID": dc_id,
        "Bahsetme": [mention],
        "Premium": is_premium,
        "Son Görülme": online,
    }
    caption = section("Kullanıcı Bilgisi", body)
    return [caption, photo_id]


async def get_chat_info(chat):
    chat = await app.get_chat(chat)
    username = chat.username
    link = f"[Bağlantı](t.me/{username})" if username else "Yok"
    photo_id = chat.photo.big_file_id if chat.photo else None
    info = f"""
❅─────✧❅✦❅✧─────❅
             ✦ Sohbet Bilgisi ✦

➻ Sohbet ID ‣ {chat.id}
➻ İsim ‣ {chat.title}
➻ Kullanıcı Adı ‣ {chat.username}
➻ DC ID ‣ {chat.dc_id}
➻ Açıklama ‣ {chat.description}
➻ Sohbet Türü ‣ {chat.type}
➻ Doğrulandı mı ‣ {chat.is_verified}
➻ Kısıtlı mı ‣ {chat.is_restricted}
➻ Oluşturucu mu ‣ {chat.is_creator}
➻ Dolandırıcı mı ‣ {chat.is_scam}
➻ Sahte mi ‣ {chat.is_fake}
➻ Üye Sayısı ‣ {chat.members_count}
➻ Bağlantı ‣ {link}


❅─────✧❅✦❅✧─────❅"""

    return info, photo_id


@app.on_message(filters.command("info"))
async def info_func(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
        user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_input = message.text.split(None, 1)[1]
        if user_input.isdigit():
            user = int(user_input)
        elif user_input.startswith("@"):
            user = user_input
        else:
            return await message.reply_text(
                "Lütfen bir kullanıcının kullanıcı ID'sini veya kullanıcı adını sağlayın ya da bir kullanıcıya yanıt verin."
            )

    m = await message.reply_text("İşleniyor...")

    try:
        info_caption, photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(info_caption, disable_web_page_preview=True)
    photo = await app.download_media(photo_id)

    await message.reply_photo(photo, caption=info_caption, quote=False)
    await m.delete()
    os.remove(photo)


@app.on_message(filters.command("chatinfo"))
async def chat_info_func(_, message: Message):
    splited = message.text.split()
    if len(splited) == 1:
        chat = message.chat.id
        if chat == message.from_user.id:
            return await message.reply_text("**Kullanım:** /chatinfo [KULLANICI_ADI|ID]")
    else:
        chat = splited[1]
    try:
        m = await message.reply_text("İşleniyor...")

        info_caption, photo_id = await get_chat_info(chat)
        if not photo_id:
            return await m.edit(info_caption, disable_web_page_preview=True)

        photo = await app.download_media(photo_id)
        await message.reply_photo(photo, caption=info_caption, quote=False)

        await m.delete()
        os.remove(photo)
    except Exception as e:
        await m.edit(e)


__MODULE__ = "𝘽𝙞𝙡𝙜𝙞"
__HELP__ = """
**Kullanıcı & Sohbet Bilgisi:**

• `/info`: Kullanıcı hakkında bilgi al. Kullanıcı adı, ID ve daha fazlası.
• `/chatinfo [KULLANICI_ADI|ID]`: Sohbet hakkında bilgi al. Üye sayısı, doğrulandı mı, davet bağlantısı ve daha fazlası.
"""
