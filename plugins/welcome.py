import datetime
from re import findall

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import (
    Chat,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from DnsXMusic import app
from DnsXMusic.misc import SUDOERS
from DnsXMusic.utils.database import is_gbanned_user
from DnsXMusic.utils.functions import check_format, extract_text_and_keyb
from DnsXMusic.utils.keyboard import ikb

from utils import del_welcome, get_welcome, set_welcome
from utils.error import capture_err
from utils.permissions import adminsOnly

from .notes import extract_urls


async def handle_new_member(member, chat):

    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} global olarak yasaklandı ve çıkarıldı,"
                + " eğer bunun yanlış bir yasak olduğunu düşünüyorsanız,"
                + " destek sohbetinde itiraz edebilirsiniz.",
            )
            return
        if member.is_bot:
            return
        return await send_welcome_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_chat_member_updated(filters.group, group=6)
@capture_err
async def welcome(_, user: ChatMemberUpdated):
    if not (
        user.new_chat_member
        and user.new_chat_member.status not in {CMS.RESTRICTED}
        and not user.old_chat_member
    ):
        return

    member = user.new_chat_member.user if user.new_chat_member else user.from_user
    chat = user.chat
    return await handle_new_member(member, chat)


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    welcome, raw_text, file_id = await get_welcome(chat.id)

    if not raw_text:
        return
    text = raw_text
    keyb = None
    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)
    u = await app.get_users(user_id)
    if "{GROUPNAME}" in text:
        text = text.replace("{GROUPNAME}", chat.title)
    if "{NAME}" in text:
        text = text.replace("{NAME}", u.mention)
    if "{ID}" in text:
        text = text.replace("{ID}", f"`{user_id}`")
    if "{FIRSTNAME}" in text:
        text = text.replace("{FIRSTNAME}", u.first_name)
    if "{SURNAME}" in text:
        sname = u.last_name or "Yok"
        text = text.replace("{SURNAME}", sname)
    if "{USERNAME}" in text:
        susername = u.username or "Yok"
        text = text.replace("{USERNAME}", susername)
    if "{DATE}" in text:
        DATE = datetime.datetime.now().strftime("%Y-%m-%d")
        text = text.replace("{DATE}", DATE)
    if "{WEEKDAY}" in text:
        WEEKDAY = datetime.datetime.now().strftime("%A")
        text = text.replace("{WEEKDAY}", WEEKDAY)
    if "{TIME}" in text:
        TIME = datetime.datetime.now().strftime("%H:%M:%S")
        text = text.replace("{TIME}", f"{TIME} UTC")

    if welcome == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif welcome == "Photo":
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


@app.on_message(filters.command("setwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    usage = "Selamlaşma mesajı olarak ayarlamak için bir metne, gif'e veya fotoğrafa yanıt vermeniz gerekiyor.\n\nNotlar: gif ve fotoğraf için başlık gereklidir."
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
            welcome = "Animasyon"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            welcome = "Fotoğraf"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            welcome = "Metin"
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
            await set_welcome(chat_id, welcome, raw_text, file_id)
            return await message.reply_text(
                "Selamlaşma mesajı başarıyla ayarlandı."
            )
        else:
            return await message.reply_text(
                "Yanlış format, yardım bölümünü kontrol edin.\n\n**Kullanım:**\nMetin: `Metin`\nMetin + Butonlar: `Metin ~ Butonlar`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**Sadece Metin, Gif ve Fotoğraf selamlaşma mesajları desteklenmektedir.**"
        )


@app.on_message(filters.command(["delwelcome", "deletewelcome"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id
    await del_welcome(chat_id)
    await message.reply_text("Selamlaşma mesajı silindi.")


@app.on_message(filters.command("getwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return await message.reply_text("Hiç selamlaşma mesajı ayarlanmamış.")
    if not message.from_user:
        return await message.reply_text("Anonimsiniz, selamlaşma mesajı gönderemem.")

    await send_welcome_message(chat, message.from_user.id)

    await message.reply_text(
        f'Selamlaşma: {welcome}\n\nFile_id: `{file_id}`\n\n`{raw_text.replace("`", "")}`'
    )


__MODULE__ = "𝙃𝙤𝙨̧ 𝙂𝙚𝙡𝙙𝙞𝙣"
__HELP__ = """
/setwelcome - Bu komutu bir mesaja yanıt olarak gönderin, selamlaşma mesajı için doğru formatı kontrol edin, bu mesajın sonuna bakın.

/delwelcome - Selamlaşma mesajını silin.
/getwelcome - Selamlaşma mesajını alın.

**SET_WELCOME ->**

**Bir fotoğraf veya gif'i selamlaşma mesajı olarak ayarlamak için, selamlaşma mesajınızı fotoğraf veya gif'in başlığı olarak ekleyin. Başlık aşağıda verilen formatta olmalıdır.**

Metin selamlaşma mesajı için sadece metni gönderin. Sonra komut ile yanıt verin.

Format aşağıdaki gibi olmalıdır.

**Merhaba** {NAME} [{ID}] {GROUPNAME}'ye hoş geldiniz.

~ #Bu ayırıcı (~) metin ve butonlar arasında olmalıdır, bu yorumu kaldırın.

Buton=[Örnek, https://ornek.com]
Buton2=[GitHub, https://github.com]
**NOTLAR ->**

Daha fazla bilgi için /markdownhelp komutunu kontrol edin.
"""
