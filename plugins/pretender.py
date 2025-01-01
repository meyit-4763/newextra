from typing import Dict, Union

from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message
from YukkiMusic import app


mongo = MongoCli(MONGO_DB_URI).Rankings

impdb = mongo.pretender


async def usr_data(chat_id: int, user_id: int) -> bool:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(user)


async def get_userdata(chat_id: int, user_id: int) -> Union[Dict[str, str], None]:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return user


async def add_userdata(
    chat_id: int, user_id: int, username: str, first_name: str, last_name: str
):
    await impdb.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )


async def check_pretender(chat_id: int) -> bool:
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)


async def impo_on(chat_id: int) -> None:
    await impdb.insert_one({"chat_id_toggle": chat_id})


async def impo_off(chat_id: int) -> None:
    await impdb.delete_one({"chat_id_toggle": chat_id})


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat or not await check_pretender(chat_id):
        return
    user_id = message.from_user.id
    user_data = await get_userdata(chat_id, user_id)
    if not user_data:
        await add_userdata(
            chat_id,
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        return

    usernamebefore = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    lastname_before = user_data.get("last_name", "")

    msg = f"[{message.from_user.id}](tg://user?id={message.from_user.id})\n"

    changes = []

    if (
        first_name != message.from_user.first_name
        and lastname_before != message.from_user.last_name
    ):
        changes.append(
            f"İsim değişti: {first_name} {lastname_before} -> {message.from_user.first_name} {message.from_user.last_name}\n"
        )
    elif first_name != message.from_user.first_name:
        changes.append(
            f"İsim değişti: {first_name} -> {message.from_user.first_name}\n"
        )
    elif lastname_before != message.from_user.last_name:
        changes.append(
            f"Soyisim değişti: {lastname_before} -> {message.from_user.last_name}\n"
        )

    if usernamebefore != message.from_user.username:
        changes.append(
            f"Kullanıcı adı değişti: @{usernamebefore} -> @{message.from_user.username}\n"
        )

    if changes:
        msg += "".join(changes)
        await message.reply_text(msg)

    await add_userdata(
        chat_id,
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )


@app.on_message(
    filters.group & filters.command("pretender") & ~filters.bot & ~filters.via_bot
)
async def set_mataa(_, message: Message):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if message.from_user.id not in admin_ids:
        return
    if len(message.command) == 1:
        return await message.reply("**Tespit edilen sahte kullanım:\n/pretender on|off**")
    chat_id = message.chat.id
    if message.command[1] == "on":
        cekset = await check_pretender(chat_id)
        if cekset:
            await message.reply(
                f"Sahte kullanım zaten **{message.chat.title}** için etkin."
            )
        else:
            await impo_on(chat_id)
            await message.reply(
                f"Sahte kullanım başarıyla **{message.chat.title}** için etkinleştirildi."
            )
    elif message.command[1] == "off":
        cekset = await check_pretender(chat_id)
        if not cekset:
            await message.reply(
                f"Sahte kullanım zaten **{message.chat.title}** için devre dışı."
            )
        else:
            await impo_off(chat_id)
            await message.reply(
                f"Sahte kullanım başarıyla **{message.chat.title}** için devre dışı bırakıldı."
            )
    else:
        await message.reply("**Tespit edilen sahte kullanım:\n/pretender on|off**")


__MODULE__ = "𝙎𝙖𝙝𝙩𝙚 𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı"
__HELP__ = """
/pretender - [Aç / Kapat] - Sohbetiniz için sahte kullanım özelliğini açmak veya kapatmak için. Eğer herhangi bir kullanıcı adını, ismini veya biyografisini değiştirirse, bot mesajı sohbetinize gönderecektir.
"""
