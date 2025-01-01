import datetime
from re import findall

from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from DnsXMusic import app
from DnsXMusic.misc import SUDOERS
from DnsXMusic.utils.database import is_gbanned_user
from DnsXMusic.utils.functions import check_format, extract_text_and_keyb
from DnsXMusic.utils.keyboard import ikb

from utils import (
    del_goodbye,
    get_goodbye,
    is_greetings_on,
    set_goodbye,
    set_greetings_off,
    set_greetings_on,
)
from utils.error import capture_err
from utils.permissions import adminsOnly

from .notes import extract_urls


async def handle_left_member(member, chat):
    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} küresel olarak yasaklandı ve çıkarıldı. "
                + "Eğer bunun yanlış bir yasak olduğunu düşünüyorsanız, "
                + "destek sohbetinde itiraz edebilirsiniz.",
            )
            return
        if member.is_bot:
            return
        return await send_left_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_message(filters.left_chat_member & filters.group, group=6)
@capture_err
async def goodbye(_, m: Message):
    if m.from_user:
        member = await app.get_users(m.from_user.id)
        chat = m.chat
        return await handle_left_member(member, chat)


async def send_left_message(chat: Chat, user_id: int, delete: bool = False):
    is_on = await is_greetings_on(chat.id, "goodbye")

    if not is_on:
        return

    goodbye, raw_text, file_id = await get_goodbye(chat.id)

    if not raw_text:
        return

    text = raw_text
    keyb = None

    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    u = await app.get_users(user_id)

    replacements = {
        "{NAME}": u.mention,
        "{ID}": f"`{user_id}`",
        "{FIRSTNAME}": u.first_name,
        "{GROUPNAME}": chat.title,
        "{SURNAME}": u.last_name or "Yok",
        "{USERNAME}": u.username or "Yok",
        "{DATE}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{WEEKDAY}": datetime.datetime.now().strftime("%A"),
        "{TIME}": datetime.datetime.now().strftime("%H:%M:%S") + " UTC",
    }

    for placeholder, value in replacements.items():
        if placeholder in text:
            text = text.replace(placeholder, value)

    if goodbye == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif goodbye == "Photo":
        m = await app.send_photo(
            chat.id,
            photo=file_id,
            caption=text,
            reply_markup=keyb,
        )
    else:
        m = await app.send_animation(
            chat.id,
            animation=file_id,
            caption=text,
            reply_markup=keyb,
        )


@app.on_message(filters.command("setgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def set_goodbye_func(_, message):
    usage = "Bir metne yanıt vermeniz gerekiyor, GIF veya fotoğraf ile bunu iyi bir veda mesajı olarak ayarlamak için.\n\nNot: GIF ve fotoğraf için başlık gereklidir."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Daha Fazla Yardım",
                    url=f"t.me/{app.username}?start=greetings",
                )
            ],
        ]
    )
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    try:
        if not replied_message:
            await message.reply_text(usage, reply_markup=key)
            return
        if replied_message.animation:
            goodbye = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            goodbye = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            goodbye = "Text"
            file_id = None
            text = replied_message.text
            raw_text = text.markdown
        if replied_message.reply_markup and not findall(r"\[.+\,.+\]", raw_text):
            urls = extract_urls(replied_message.reply_markup)
            if urls:
                response = "\n".join(
                    [f"{name}=[{text}, {url}]" for name, text, url in urls]
                )
                raw_text = raw_text + response
        raw_text = await check_format(ikb, raw_text)
        if raw_text:
            await set_goodbye(chat_id, goodbye, raw_text, file_id)
            return await message.reply_text(
                "Veda mesajı başarıyla ayarlandı."
            )
        else:
            return await message.reply_text(
                "Yanlış biçimlendirme, lütfen yardım bölümünü kontrol edin.\n\n**Kullanım:**\nMetin: `Text`\nMetin + Butonlar: `Text ~ Butonlar`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**Sadece Metin, GIF ve Fotoğraf veda mesajı olarak desteklenmektedir.**"
        )


@app.on_message(filters.command(["delgoodbye", "deletegoodbye"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_goodbye_func(_, message):
    chat_id = message.chat.id
    await del_goodbye(chat_id)
    await message.reply_text("Veda mesajı başarıyla silindi.")


@app.on_message(filters.command("goodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def goodbye(client, message: Message):
    command = message.text.split()

    if len(command) == 1:
        return await get_goodbye_func(client, message)

    if len(command) == 2:
        action = command[1].lower()
        if action in ["on", "enable", "y", "yes", "true", "t"]:
            success = await set_greetings_on(message.chat.id, "goodbye")
            if success:
                await message.reply_text(
                    "Artık ayrılanlara veda edeceğim!"
                )
            else:
                await message.reply_text("Veda mesajını etkinleştirmede başarısız olundu.")

        elif action in ["off", "disable", "n", "no", "false", "f"]:
            success = await set_greetings_off(message.chat.id, "goodbye")
            if success:
                await message.reply_text("Artık ayrılanlara veda etmeyeceğim.")
            else:
                await message.reply_text("Veda mesajını devre dışı bırakmada başarısız olundu.")

        else:
            await message.reply_text(
                "Geçersiz komut. Lütfen kullanın:\n"
                "/goodbye - Veda mesajınızı almak için\n"
                "/goodbye [on, y, true, enable, t] - Veda mesajlarını etkinleştirmek için\n"
                "/goodbye [off, n, false, disable, f, no] - Veda mesajlarını devre dışı bırakmak için\n"
                "/delgoodbye veya /deletegoodbye - Veda mesajını silmek ve veda mesajlarını devre dışı bırakmak için"
            )
    else:
        await message.reply_text(
            "Geçersiz komut. Lütfen kullanın:\n"
            "/goodbye - Veda mesajınızı almak için\n"
            "/goodbye [on, y, true, enable, t] - Veda mesajlarını etkinleştirmek için\n"
            "/goodbye [off, n, false, disable, f, no] - Veda mesajlarını devre dışı bırakmak için\n"
            "/delgoodbye veya /deletegoodbye - Veda mesajını silmek ve veda mesajlarını devre dışı bırakmak için"
        )


async def get_goodbye_func(_, message):
    chat = message.chat
    goodbye, raw_text, file_id = await get_goodbye(chat.id)
    if not raw_text:
        return await message.reply_text(
            "Henüz bir veda mesajı ayarlamadınız."
        )
    if not message.from_user:
        return await message.reply_text("Anonim olduğunuz için veda mesajı gönderemem.")

    await send_left_message(chat, message.from_user.id)
    is_grt = await is_greetings_on(chat.id, "goodbye")
    text = None
    if is_grt:
        text = "Açık"
    else:
        text = "Kapalı"

    await message.reply_text(
        f"Şu anda ayrılanlara veda mesajı gönderiyorum: {text}\n"
        f"Veda Mesajı: {goodbye}\n\n"
        f"Dosya ID: `{file_id}`\n\n"
        f"`{raw_text.replace('`', '')}`"
    )


__MODULE__ = "𝙑𝙀𝘿𝘼"
__HELP__ = """
**Veda Mesajı Yönetimi:**

/setgoodbye - Bir mesaja yanıt vererek veda mesajını ayarlayın. GIF veya fotoğraf ile ayarlamak için başlık gereklidir.
/goodbye - Veda mesajınızı almak için kullanın.
/goodbye [on, y, true, enable, t] - Veda mesajlarını etkinleştirmek için kullanın.
/goodbye [off, n, false, disable, f, no] - Veda mesajlarını devre dışı bırakmak için kullanın.
/delgoodbye veya /deletegoodbye - Veda mesajını silmek ve veda mesajlarını devre dışı bırakmak için kullanın.

**Not:** Veda mesajı ayarlamak için metin, GIF veya fotoğraf kullanabilirsiniz. Başlık, GIF ve fotoğraf için gereklidir.
"""
