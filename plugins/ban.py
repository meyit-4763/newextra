import asyncio
from contextlib import suppress
from string import ascii_lowercase
from typing import Dict, Union

from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from DnsXMusic import app
from DnsXMusic.core.mongo import mongodb
from DnsXMusic.misc import SUDOERS
from DnsXMusic.utils.database import save_filter
from DnsXMusic.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from DnsXMusic.utils.keyboard import ikb

from utils.error import capture_err
from utils.permissions import adminsOnly, member_permissions


warnsdb = mongodb.warns

__MODULE__ = "𝘽𝙖𝙣"
__HELP__ = """
/ban - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙮𝙖𝙨𝙖𝙠𝙡𝙖  
/sban - 𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙣ı𝙣 𝙜𝙧𝙪𝙥𝙩𝙖 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙙𝙞𝙜̆𝙞 𝙩𝙪̈𝙢 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı 𝙨𝙞𝙡 𝙫𝙚 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙮𝙖𝙨𝙖𝙠𝙡𝙖 
/tban - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙚𝙡𝙞𝙧𝙡𝙞 𝙗𝙞𝙧 𝙨𝙪̈𝙧𝙚 𝙮𝙖𝙨𝙖𝙠𝙡𝙖  
/unban - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙢𝙖𝙮ı 𝙠𝙖𝙡𝙙ı𝙧  
/warn - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙪𝙮𝙖𝙧  
/swarn - 𝙂𝙧𝙪𝙗𝙪𝙣 𝙞𝙘̧𝙞𝙣𝙙𝙚𝙠𝙞 𝙩𝙪̈𝙢 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı 𝙨𝙞𝙡 𝙫𝙚 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙪𝙮𝙖𝙧  
/rmwarns - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙣ı𝙣 𝙩𝙪̈𝙢 𝙪𝙮𝙖𝙧ı𝙡𝙖𝙧ı𝙣ı 𝙠𝙖𝙡𝙙ı𝙧  
/warns - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙣ı𝙣 𝙪𝙮𝙖𝙧ı𝙡𝙖𝙧ı𝙣ı 𝙜𝙤̈𝙨𝙩𝙚𝙧  
/kick - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙖𝙩  
/skick - 𝙔𝙖𝙣ı𝙩𝙡𝙖𝙣𝙖𝙣 𝙢𝙚𝙨𝙖𝙟ı 𝙨𝙞𝙡𝙚𝙧𝙚𝙠 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙚𝙣𝙞 𝙜𝙧𝙪𝙥𝙩𝙖𝙣 𝙖𝙩
/purge - 𝙎𝙚𝙘̧𝙞𝙡𝙚𝙣 𝙢𝙚𝙨𝙖𝙟𝙙𝙖𝙣 𝙨𝙤𝙣𝙧𝙖𝙠𝙞 𝙈𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı 𝙩𝙚𝙢𝙞𝙯𝙡𝙚 
/purge [n] - 𝙔𝙖𝙣ı𝙩𝙡𝙖𝙣𝙖𝙣 𝙢𝙚𝙨𝙖𝙟𝙙𝙖𝙣 "n" 𝙨𝙖𝙮ı𝙙𝙖 𝙢𝙚𝙨𝙖𝙟ı 𝙩𝙚𝙢𝙞𝙯𝙡𝙚 
/del - 𝙔𝙖𝙣ı𝙩𝙡𝙖𝙣𝙖𝙣 𝙢𝙚𝙨𝙖𝙟ı 𝙨𝙞𝙡  
/promote - 𝘽𝙞𝙧 𝙪̈𝙮𝙚𝙮𝙞 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙞𝙧 
/fullpromote - 𝘽𝙞𝙧 𝙪̈𝙮𝙚𝙮𝙞 𝙩𝙪̈𝙢 𝙝𝙖𝙠𝙡𝙖𝙧ı𝙮𝙡𝙖 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧  
/demote - 𝘽𝙞𝙧 𝙪̈𝙮𝙚𝙮𝙞 𝙜𝙚𝙧𝙞 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧 
/pin - Bir mesajı sabitle  
/unpin - 𝘽𝙞𝙧 𝙢𝙚𝙨𝙖𝙟ı𝙣 𝙨𝙖𝙗𝙞𝙩𝙡𝙞𝙜̆𝙞𝙣𝙞 𝙠𝙖𝙡𝙙ı𝙧 
/unpinall - 𝙏𝙪̈𝙢 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙣𝙢𝙞𝙨̧ 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı𝙣 𝙨𝙖𝙗𝙞𝙩𝙡𝙞𝙜̆𝙞𝙣𝙞 𝙠𝙖𝙡𝙙ı𝙧  
/mute - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙨𝙪𝙨𝙩𝙪𝙧  
/tmute - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙚𝙡𝙞𝙧𝙡𝙞 𝙗𝙞𝙧 𝙨𝙪̈𝙧𝙚 𝙨𝙪𝙨𝙩𝙪𝙧  
/unmute - 𝘽𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙨𝙪𝙨𝙩𝙪𝙧𝙢𝙖𝙮ı kaldır  
/zombies - 𝙎𝙞𝙡𝙞𝙣𝙢𝙞𝙨̧ 𝙝𝙚𝙨𝙖𝙥𝙡𝙖𝙧ı 𝙮𝙖𝙨𝙖𝙠𝙡𝙖  
/report | @admins | @admin - 𝘽𝙞𝙧 𝙢𝙚𝙨𝙖𝙟ı 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙡𝙚𝙧𝙚 𝙗𝙞𝙡𝙙𝙞𝙧 
/link - 𝙂𝙧𝙪𝙗𝙖/𝙨𝙪̈𝙥𝙚𝙧 𝙜𝙧𝙪𝙗𝙖 𝙙𝙖𝙫𝙚𝙩 𝙗𝙖𝙜̆𝙡𝙖𝙣𝙩ı𝙨ı 𝙜𝙤̈𝙣𝙙𝙚𝙧."""


async def int_to_alpha(user_id: int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False


@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙖𝙩𝙖𝙢𝙖𝙢, 𝙞𝙨𝙩𝙚𝙧𝙨𝙚𝙣𝙞𝙯 𝙖𝙮𝙧ı𝙡𝙖𝙗𝙞𝙡𝙞𝙧𝙞𝙢")
    if user_id in SUDOERS:
        return await message.reply_text("𝙔𝙜̆𝙠𝙨𝙚𝙡𝙩𝙞𝙡𝙢𝙞𝙨̧ 𝙤𝙡𝙖𝙣 𝙗𝙞𝙧𝙞𝙣𝙞 𝙖𝙩𝙢𝙖𝙠 𝙢ı 𝙞𝙨𝙩𝙞𝙮𝙤𝙧𝙨𝙪𝙣?")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "𝘽𝙞𝙧 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙮𝙞 𝙖𝙩𝙖𝙢𝙖𝙢, 𝙠𝙪𝙧𝙖𝙡𝙡𝙖𝙧ı 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙨𝙪𝙣, 𝘽𝙪 𝙮𝙪̈𝙯𝙙𝙚𝙣 𝙮𝙖𝙥𝙖𝙢𝙖𝙢."
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**𝙆𝙞𝙘𝙠 𝙖𝙡𝙖𝙣:** {mention}
**𝙆𝙞𝙘𝙠 𝘼𝙩𝙖𝙣:** {message.from_user.mention if message.from_user else '𝘼𝙣𝙤𝙣𝙞𝙢'}
**𝙎𝙚𝙗𝙚𝙥:** {reason or '𝙎𝙚𝙗𝙚𝙥 𝙔𝙤𝙠'}"""
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)


# Ban members


@app.on_message(
    filters.command(["ban", "sban", "tban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙮𝙖𝙢𝙖𝙢,𝙞𝙨𝙩𝙚𝙧𝙨𝙚𝙣𝙞𝙯 𝙖𝙮𝙧ı𝙡𝙖𝙗𝙞𝙡𝙞𝙧𝙞𝙢..")
    if user_id in SUDOERS:
        return await message.reply_text("𝙔𝙜̆𝙠𝙨𝙚𝙡𝙩𝙞𝙡𝙢𝙞𝙨̧ 𝙤𝙡𝙖𝙣 𝙗𝙞𝙧𝙞𝙣𝙞 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙢𝙖𝙠 𝙢ı 𝙞𝙨𝙩𝙞𝙮𝙤𝙧𝙨𝙪𝙣? 𝙔𝙚𝙣𝙞𝙙𝙚𝙣 𝙙𝙪̈𝙨̧𝙪̈𝙣!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "𝘽𝙞𝙧 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙮𝙞 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙮𝙖𝙢𝙖𝙢, 𝙠𝙪𝙧𝙖𝙡𝙡𝙖𝙧ı 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙨𝙪𝙣, 𝙗𝙚𝙣 𝙙𝙚 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙪𝙢."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"**𝘽𝙖𝙣𝙡𝙖𝙣𝙖𝙣:** {mention}\n"
        f"**𝘽𝙖𝙣𝙡𝙖𝙮𝙖𝙣:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**𝘽𝙖𝙣𝙡𝙖𝙣𝙙ı:** {time_value}\n"
        if temp_reason:
            msg += f"**𝙎𝙚𝙗𝙚𝙥:** {temp_reason}"
        with suppress(AttributeError):
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg)
            else:
                await message.reply_text("99'𝙙𝙖𝙣 𝙛𝙖𝙯𝙡𝙖 𝙠𝙪𝙡𝙡𝙖𝙣𝙖𝙢𝙖𝙯𝙨ı𝙣.")
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the user
    # they want to unban is not in the group.
    reply = message.reply_to_message
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("𝘽𝙞𝙧 𝙠𝙖𝙣𝙖𝙡ı𝙣 𝙮𝙖𝙨𝙖𝙜̆ı𝙣ı 𝙠𝙖𝙡𝙙ı𝙧𝙖𝙢𝙖𝙯𝙨ı𝙣ı𝙯")

    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"𝙔𝙖𝙨𝙖𝙠 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙙ı! {umention}")


# Promote Members


@app.on_message(
    filters.command(["promote", "fullpromote"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢..")
        
    bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙚𝙢𝙞𝙮𝙤𝙧𝙪𝙢..")
    if not bot:
        return await message.reply_text("𝙗𝙪 𝙨𝙤𝙝𝙗𝙚𝙩𝙩𝙚 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞 𝙙𝙚𝙜̆𝙞𝙡𝙞𝙢.")
    if not bot.can_promote_members:
        return await message.reply_text("𝙔𝙚𝙩𝙚𝙧𝙡𝙞 𝙞𝙯𝙞𝙣𝙡𝙚𝙧𝙞𝙢 𝙮𝙤𝙠.")

    umention = (await app.get_users(user_id)).mention

    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.can_change_info,
                can_invite_users=bot.can_invite_users,
                can_delete_messages=bot.can_delete_messages,
                can_restrict_members=bot.can_restrict_members,
                can_pin_messages=bot.can_pin_messages,
                can_promote_members=bot.can_promote_members,
                can_manage_chat=bot.can_manage_chat,
                can_manage_video_chats=bot.can_manage_video_chats,
            ),
        )
        return await message.reply_text(f"𝙏𝙖𝙢𝙖𝙢𝙚𝙣 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙞𝙡𝙙𝙞! {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        privileges=ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
    )
    await message.reply_text(f"𝙏𝙚𝙧𝙛𝙞 𝙀𝙩𝙩𝙞𝙧𝙞𝙡𝙙𝙞! {umention}")


# Demote Member


@app.on_message(filters.command("purge") & ~filters.private)
@adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    repliedmsg = message.reply_to_message
    await message.delete()

    if not repliedmsg:
        return await message.reply_text("𝙏𝙚𝙢𝙞𝙯𝙡𝙚𝙢𝙚𝙠 𝙞𝙘̧𝙞𝙣 𝙗𝙞𝙧 𝙢𝙚𝙨𝙖𝙟𝙖 𝙮𝙖𝙣ı𝙩 𝙫𝙚𝙧.")

    cmd = message.command
    if len(cmd) > 1 and cmd[1].isdigit():
        purge_to = repliedmsg.id + int(cmd[1])
        if purge_to > message.id:
            purge_to = message.id
    else:
        purge_to = message.id

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
        repliedmsg.id,
        purge_to,
    ):
        message_ids.append(message_id)

        # Max message deletion limit is 100
        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # For both sides
            )

            # To delete more than 100 messages, start again
            message_ids = []

    # Delete if any messages left
    if len(message_ids) > 0:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


@app.on_message(filters.command("del") & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("𝙎𝙞𝙡𝙢𝙚𝙠 𝙞𝙘̧𝙞𝙣 𝙗𝙞𝙧 𝙢𝙚𝙨𝙖𝙟𝙖 𝙮𝙖𝙣ı𝙩 𝙫𝙚𝙧.")
    await message.reply_to_message.delete()
    await message.delete()


@app.on_message(filters.command("demote") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢..")
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙚𝙢𝙚𝙙𝙞𝙜̆𝙞𝙢 𝙜𝙞𝙗𝙞 𝙧𝙪̈𝙩𝙗𝙚𝙢𝙞 𝙙𝙪̈𝙨̧𝙪̈𝙧𝙚𝙢𝙚𝙢..")
    if user_id in SUDOERS:
        return await message.reply_text(
            "𝙔𝙪̈𝙠𝙨𝙚𝙡𝙩𝙞𝙡𝙢𝙞𝙨̧ 𝙤𝙡𝙖𝙣 𝙗𝙧𝙞𝙞𝙣𝙞 𝙩𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙢𝙧𝙠 𝙢𝙞 𝙞𝙨𝙩𝙞𝙮𝙤𝙧𝙨𝙪𝙣? 𝙔𝙚𝙣𝙞𝙙𝙚𝙣 𝙙𝙪̈𝙨̧𝙪̈𝙣!"
        )
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.chat.promote_member(
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                ),
            )
            umention = (await app.get_users(user_id)).mention
            await message.reply_text(f"𝙏𝙚𝙧𝙛𝙞 𝙚𝙩𝙩𝙞𝙧𝙞𝙡𝙙𝙞! {umention}")
        else:
            await message.reply_text("𝘽𝙖𝙝𝙨𝙚𝙩𝙩𝙞𝙜̆𝙞𝙣𝙞𝙯 𝙠𝙞𝙨̧𝙞 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞 𝙙𝙚𝙜̆𝙞𝙡.") 
        except Exception as e:
        await message.reply_text(e)

# Pin Messages


@app.on_message(filters.command(["unpinall"]) & filters.group & ~BANNED_USERS)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if message.command[0] == "unpinall":
        return await message.reply_text(
            "𝙏𝙪̈𝙢 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı 𝙨𝙖𝙗𝙞𝙩𝙩𝙚𝙣 𝙠𝙖𝙡𝙙ı𝙧𝙢𝙖𝙠 𝙞𝙨𝙩𝙚𝙙𝙞𝙜̆𝙞𝙣𝙞𝙯𝙚 𝙚𝙢𝙞𝙣 𝙢𝙞𝙨𝙞𝙣𝙞𝙯?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝙀𝙫𝙚𝙩", callback_data="unpin_yes"),
                        InlineKeyboardButton(text="𝙃𝙖𝙮ı𝙧", callback_data="unpin_no"),
                    ],
                ]
            ),
    )


@app.on_callback_query(filters.regex(r"unpin_(yes|no)"))
async def callback_query_handler(_, query: CallbackQuery):
    if query.data == "unpin_yes":
        await app.unpin_all_chat_messages(query.message.chat.id)
        return await query.message.edit_text("𝙏𝙪̈𝙢 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙣𝙢𝙞𝙨̧ 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙙ı.")
    elif query.data == "unpin_no":
        return await query.message.edit_text(
            "𝙏𝙪̈𝙢 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙣𝙢𝙞𝙨̧ 𝙢𝙚𝙨𝙖𝙟𝙡𝙖𝙧ı𝙣 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙢𝙖𝙨ı 𝙞𝙥𝙩𝙖𝙡 𝙚𝙙𝙞𝙡𝙙𝙞."
        )



@app.on_message(filters.command(["pin", "unpin"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("𝘽𝙞𝙧 𝙢𝙚𝙨𝙖𝙟𝙖 𝙮𝙖𝙣ı𝙩 𝙫𝙚𝙧𝙚𝙧𝙚𝙠 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙢𝙚𝙠/𝙨̧𝙖𝙗𝙡𝙤𝙣𝙪𝙣𝙪 𝙠𝙖𝙡𝙙ı𝙧𝙢𝙖𝙠 𝙞𝙘̧𝙞𝙣")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"𝘽𝙪 𝙢𝙚𝙨𝙖𝙟ı𝙣 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙢𝙚𝙨𝙞 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙙ı: [this]({r.link}).") 
            disable_web_page_preview=True,
    await r.pin(disable_notification=True)
    await message.reply(
        f"Sabitlenmiş [this]({r.link}) mesaj.") 
        disable_web_page_preview=True,
    msg = "𝙇𝙪̈𝙩𝙛𝙚𝙣 𝙨𝙖𝙗𝙞𝙩𝙡𝙚𝙣𝙢𝙞𝙨̧ 𝙢𝙚𝙨𝙖𝙟ı 𝙠𝙤𝙣𝙩𝙧𝙤𝙡 𝙚�𝙞𝙣: ~ " + f"[𝙆𝙤𝙣𝙩𝙧𝙤𝙡 𝙚𝙩, {r.link}]"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)


# Mute members


@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙨𝙪𝙨𝙩𝙪𝙧𝙖𝙢𝙖𝙢..")
    if user_id in SUDOERS:
        return await message.reply_text("𝙔𝙜̆𝙠𝙨𝙚𝙡𝙩𝙞𝙡𝙢𝙞𝙨̧ 𝙤𝙡𝙖𝙣 𝙗𝙞𝙧𝙞𝙣𝙞 𝙨𝙪𝙨𝙩𝙪𝙧𝙢𝙖𝙠 𝙢ı 𝙞𝙨𝙩𝙞𝙮𝙤𝙧𝙨𝙪𝙣? 𝘽𝙪𝙣𝙪 𝙩𝙚𝙠𝙧𝙖𝙧 𝙙𝙪̈𝙨̧𝙪̈𝙣!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "𝘽𝙞𝙧 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙮𝙞 𝙨𝙪𝙨𝙩𝙪𝙧𝙖𝙢𝙖𝙢, 𝙠𝙪𝙧𝙖𝙡𝙡𝙖𝙧ı 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙨𝙪𝙣, 𝙗𝙚𝙣 𝙙𝙚 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙪𝙢."
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🚨 𝙎𝙪𝙨𝙩𝙪𝙧𝙢𝙖𝙮ı 𝙞𝙥𝙩𝙖𝙡 𝙚𝙩 🚨": f"unmute_{user_id}"})
    msg = (
        f"**𝙎𝙪𝙨𝙩𝙪𝙧𝙪𝙡𝙖𝙣:** {mention}\n"
        f"**𝙎𝙪𝙨𝙩𝙪𝙧𝙖𝙣:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"**𝙎𝙪𝙨𝙩𝙪𝙧𝙪𝙡𝙙𝙪:** {time_value}\n"
        if temp_reason:
            msg += f"**𝙎𝙚𝙗𝙚𝙥:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("99'𝙙𝙖𝙣 𝙛𝙖𝙯𝙡𝙖 𝙠𝙪𝙡𝙡𝙖𝙣𝙖𝙢𝙖𝙯𝙨ı𝙣. ")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**𝙎𝙚𝙗𝙚𝙥:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg, reply_markup=keyboard)


@app.on_message(filters.command("unmute") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢..")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"𝙎𝙪𝙨𝙩𝙪𝙧𝙢𝙖 𝙖𝙘̧ı𝙡𝙙ı! {umention}")


@app.on_message(filters.command(["warn", "swarn"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    if user_id == app.id:
        return await message.reply_text("𝙆𝙚𝙣𝙙𝙞𝙢𝙞 𝙪𝙮𝙖𝙣𝙖𝙢𝙖𝙢, 𝙞𝙨𝙩𝙚𝙧𝙨𝙚𝙣 𝙖𝙮𝙧ı𝙡𝙖𝙗𝙞𝙡𝙞𝙧𝙞𝙢")
    if user_id in SUDOERS:
        return await message.reply_text(
            "𝙆𝙚𝙣𝙙𝙞 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙢𝙞 𝙪𝙮𝙖𝙧𝙖𝙢𝙖𝙢, 𝙘̧𝙪̈𝙣𝙠𝙪̈ 𝙤 𝙗𝙚𝙣𝙞 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙮𝙤𝙧!"
        )
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "𝘽𝙞𝙧 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙮𝙞 𝙪𝙮𝙖𝙧𝙖𝙢𝙖𝙢, 𝙠𝙪𝙧𝙖𝙡𝙡𝙖𝙧ı 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙨𝙪𝙣, 𝙗𝙚𝙣 𝙙𝙚 𝙗𝙞𝙡𝙞𝙮𝙤𝙧𝙪𝙢."
        )
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨  𝙐𝙮𝙖𝙧ı𝙮ı 𝙞𝙥𝙩𝙖𝙡 𝙚𝙩 🚨": f"unwarn_{user_id}"})
    if warns:
        warns = warns["warns"]
    else:
        warns = 0
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"{mention} 𝙞𝙘̧𝙞𝙣 𝙪𝙮𝙖𝙧ı 𝙨𝙖𝙮ı𝙨ı 𝙖𝙨̧ı𝙡𝙙ı, 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙣𝙙ı! ")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**𝙐𝙮𝙖𝙧ı𝙡𝙖𝙣:** {mention}
**𝙐𝙮𝙖𝙧𝙖𝙣:** {message.from_user.mention if message.from_user else '𝘼𝙣𝙤𝙣𝙞𝙢'}
**𝙎𝙚𝙗𝙚𝙥:** {reason or '𝙎𝙚𝙗𝙚𝙥 𝙔𝙤𝙠'}
**𝙐𝙮𝙖𝙧ı𝙡𝙖𝙧:** {warns + 1}/3"""
        replied_message = message.reply_to_message
        if replied_message:
            message = replied_message
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_") & ~BANNED_USERS)
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "𝘽𝙪 𝙚𝙮𝙡𝙚𝙢𝙞 𝙜𝙚𝙧𝙘̧𝙚𝙠𝙡𝙚𝙨̧𝙩𝙞𝙧𝙢𝙚𝙠 𝙞𝙘̧𝙞𝙣 𝙮𝙚𝙩𝙚𝙧𝙡𝙞 𝙞𝙯𝙣𝙞𝙣𝙞𝙯 𝙮𝙤𝙠.\n"
            + f"𝙄̇𝙯𝙞𝙣 𝙜𝙚𝙧𝙚𝙠𝙡𝙞: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙣ı𝙣 𝙪𝙮𝙖𝙧ı𝙨ı 𝙮𝙤𝙠.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"𝙐𝙮𝙖𝙧ı {from_user.mention} 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙙ı."
    await cq.message.edit(text)


@app.on_message(filters.command("rmwarns") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    mention = (await app.get_users(user_id)).mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} 𝙐𝙮𝙖𝙧ı𝙨ı 𝙔𝙤𝙠.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"𝙐𝙮𝙖𝙧ı𝙡𝙖𝙧 {mention} 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙠𝙖𝙡𝙙ı𝙧ı𝙡𝙙ı.")


@app.on_message(filters.command("warns") & ~filters.private & ~BANNED_USERS)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("O 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙮ı 𝙗𝙪𝙡𝙖𝙢ı𝙮𝙤𝙧𝙪𝙢.")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention} 𝙐𝙮𝙖𝙧ı𝙨ı 𝙔𝙤𝙠")
    return await message.reply_text(f"{mention} , {warns}/3 𝙐𝙮𝙖𝙧ı.")


@app.on_message(filters.command("link") & ~BANNED_USERS)
@adminsOnly("can_invite_users")
async def invite(_, message):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        link = (await app.get_chat(message.chat.id)).invite_link
        if not link:
            link = await app.export_chat_invite_link(message.chat.id)
        text = f"𝙄̇𝙨̧𝙩𝙚 𝙜𝙧𝙪𝙗𝙪𝙣 𝙙𝙖𝙫𝙚𝙩 𝙗𝙖𝙜̆𝙡𝙖𝙣𝙩ı𝙨ı\n\n{link}"
        if message.reply_to_message:
            await message.reply_to_message.reply_text(
                text, disable_web_page_preview=True
            )
        else:
            await message.reply_text(text, disable_web_page_preview=True)
