#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors.exceptions.bad_request_400 import UserAlreadyParticipant
from pyrogram.types import ChatJoinRequest
from DnsXMusic import app
from DnsXMusic.core.mongo import mongodb
from DnsXMusic.misc import SUDOERS
from DnsXMusic.utils.keyboard import ikb

from utils.permissions import adminsOnly, member_permissions


approvaldb = mongodb.autoapprove


def smallcap(text):
    trans_table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ0𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    )
    return text.translate(trans_table)


@app.on_message(filters.command("otoonay") & filters.group)
@adminsOnly("can_change_info")
async def approval_command(client, message):
    chat_id = message.chat.id
    chat = await approvaldb.find_one({"chat_id": chat_id})
    if chat:
        mode = chat.get("mode", "")
        if not mode:
            mode = "manual"
            await approvaldb.update_one(
                {"chat_id": chat_id},
                {"$set": {"mode": mode}},
                upsert=True,
            )
        if mode == "automatic":
            switch = "manual"
            mdbutton = "𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠"
        else:
            switch = "automatic"
            mdbutton = "𝙈𝙖𝙣𝙪𝙚𝙡"
        buttons = {
            "𝙆𝙖𝙥𝙖𝙡ı": "approval_off",
            f"{mdbutton}": f"approval_{switch}",
        }
        keyboard = ikb(buttons, 1)
        await message.reply(
            "**𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙊𝙣𝙖𝙮 𝘽𝙪 𝙨𝙤𝙝𝙗𝙚𝙩 𝙞𝙘̧𝙞𝙣: 𝙀𝙩𝙠𝙞𝙣.**", reply_markup=keyboard
        )
    else:
        buttons = {"𝘼𝙘̧ı𝙠 ": "approval_on"}
        keyboard = ikb(buttons, 1)
        await message.reply(
            "**𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙊𝙣𝙖𝙮 𝘽𝙪 𝙨𝙤𝙝𝙗𝙚𝙩 𝙞𝙘̧𝙞𝙣: 𝘿𝙚𝙫𝙧𝙚 𝘿ı𝙨̧ı.**", reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("approval(.*)"))
async def approval_cb(client, cb):
    chat_id = cb.message.chat.id
    from_user = cb.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        if from_user.id not in SUDOERS:
            return await cb.answer(
                f"𝙂𝙚𝙧𝙚𝙠𝙡𝙞 𝙞𝙯𝙣𝙚 𝙨𝙖𝙝𝙞𝙥 𝙙𝙚𝙜̆𝙞𝙡𝙨𝙞𝙣𝙞𝙯\n 𝙄̇𝙯𝙞𝙣: {permission}",
                show_alert=True,
            )
    command_parts = cb.data.split("_", 1)
    option = command_parts[1]
    if option == "off":
        if await approvaldb.count_documents({"chat_id": chat_id}) > 0:
            approvaldb.delete_one({"chat_id": chat_id})
            buttons = {"ᴛᴜʀɴ ᴏɴ": "approval_on"}
            keyboard = ikb(buttons, 1)
            return await cb.edit_message_text(
                "**𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙤𝙣𝙖𝙮 𝙗𝙪 𝙨𝙤𝙝𝙗𝙚𝙩 𝙞𝙘̧𝙞𝙣: 𝘿𝙚𝙫𝙧𝙚 𝘿ı𝙨̧ı**",
                reply_markup=keyboard,
            )
    if option == "on":
        switch = "manual"
        mode = "automatic"
    if option == "automatic":
        switch = "manual"
        mode = option
    if option == "manual":
        switch = "automatic"
        mode = option
    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )
    chat = await approvaldb.find_one({"chat_id": chat_id})
    mode = smallcap(chat["mode"])
    buttons = {"𝙆𝙖𝙥𝙖𝙡ı": "approval_off", f"{mode}": f"approval_{switch}"}
    keyboard = ikb(buttons, 1)
    await cb.edit_message_text(
        "**𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙊𝙣𝙖𝙮 𝘽𝙪 𝙨𝙤𝙝𝙗𝙚𝙩 𝙞𝙘̧𝙞𝙣: 𝙀𝙩𝙠𝙞𝙣.**", reply_markup=keyboard
    )


@app.on_message(filters.command("fullonay") & filters.group)
@adminsOnly("can_restrict_members")
async def clear_pending_command(client, message):
    a = await message.reply_text("𝘽𝙚𝙠𝙡𝙚𝙮𝙞𝙣....")
    chat_id = message.chat.id
    await app.approve_all_chat_join_requests(chat_id)
    await a.edit("𝙀𝙜̆𝙚𝙧 𝙝𝙚𝙧𝙝𝙖𝙣𝙜𝙞 𝙗𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙤𝙣𝙖𝙮 𝙗𝙚𝙠𝙡𝙞𝙮𝙤𝙧𝙨𝙖, 𝙗𝙚𝙣 𝙤𝙣𝙪̈ 𝙤𝙣𝙖𝙮𝙡ı𝙮𝙤𝙧𝙪𝙢.")
    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"pending_users": []}},
    )


@app.on_message(filters.command("onaysil") & filters.group)
@adminsOnly("can_restrict_members")
async def clear_pending_command(client, message):
    chat_id = message.chat.id
    result = await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"pending_users": []}},
    )
    if result.modified_count > 0:
        await message.reply_text("𝘽𝙚𝙠𝙡𝙚𝙮𝙚𝙣 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙡𝙖𝙧 𝙩𝙚𝙢𝙞𝙯𝙡𝙚𝙣𝙙𝙞.")
    else:
        await message.reply_text("𝙏𝙚𝙢𝙞𝙯𝙡𝙚𝙣𝙚𝙘𝙚𝙠 𝙗𝙚𝙠𝙡𝙚𝙮𝙚𝙣 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙮𝙤𝙠.")


@app.on_chat_join_request(filters.group)
async def accept(client, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    chat_id = await approvaldb.find_one({"chat_id": chat.id})
    if chat_id:
        mode = chat_id["mode"]
        if mode == "automatic":
            await app.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
            return
        if mode == "manual":
            is_user_in_pending = await approvaldb.count_documents(
                {"chat_id": chat.id, "pending_users": int(user.id)}
            )
            if is_user_in_pending == 0:
                await approvaldb.update_one(
                    {"chat_id": chat.id},
                    {"$addToSet": {"pending_users": int(user.id)}},
                    upsert=True,
                )
                buttons = {
                    "𝙆𝙖𝙗𝙪𝙡 𝙚𝙩": f"manual_approve_{user.id}",
                    "𝙍𝙚𝙙𝙙𝙚𝙩": f"manual_decline_{user.id}",
                }
                keyboard = ikb(buttons, int(2))
                text = f"**𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı: {user.mention} 𝙜𝙧𝙪𝙗𝙪𝙢𝙪𝙯𝙖 𝙠𝙖𝙩ı𝙡𝙢𝙖𝙠 𝙞𝙘̧𝙞𝙣 𝙗𝙞𝙧 𝙞𝙨𝙩𝙚𝙠 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙙𝙞 𝙃𝙚𝙧𝙝𝙖𝙣𝙜𝙞 𝙗𝙞𝙧 𝙮𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞 𝙗𝙪𝙣𝙪 𝙠𝙖𝙗𝙪𝙡 𝙚𝙙𝙚𝙗𝙞𝙡𝙞𝙧 𝙫𝙚𝙮𝙖 𝙧𝙚𝙙𝙙𝙚𝙙𝙞𝙡𝙚𝙗𝙞𝙡𝙞𝙧.**"
                admin_data = [
                    i
                    async for i in app.get_chat_members(
                        chat_id=message.chat.id,
                        filter=ChatMembersFilter.ADMINISTRATORS,
                    )
                ]
                for admin in admin_data:
                    if admin.user.is_bot or admin.user.is_deleted:
                        continue
                    text += f"[\u2063](tg://user?id={admin.user.id})"
                return await app.send_message(chat.id, text, reply_markup=keyboard)


@app.on_callback_query(filters.regex("manual_(.*)"))
async def manual(app, cb):
    chat = cb.message.chat
    from_user = cb.from_user
    permissions = await member_permissions(chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        if from_user.id not in SUDOERS:
            return await cb.answer(
                f"𝙂𝙚𝙧𝙚𝙠𝙡𝙞 𝙞𝙯𝙣𝙚 𝙨𝙖𝙝𝙞𝙥 𝙙𝙚𝙜̆𝙞𝙡𝙨𝙞𝙣𝙞𝙯.\n 𝙄̇𝙯𝙞𝙣: {permission}",
                show_alert=True,
            )
    datas = cb.data.split("_", 2)
    dis = datas[1]
    id = datas[2]
    if dis == "approve":
        try:
            await app.approve_chat_join_request(chat_id=chat.id, user_id=id)
        except UserAlreadyParticipant:
            await cb.answer(
                "𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı, 𝙜𝙧𝙪𝙗𝙪𝙣𝙪𝙯𝙙𝙖 𝙝𝙚𝙧𝙝𝙖𝙣𝙜𝙞 𝙗𝙞𝙧𝙞 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙤𝙣𝙖𝙮𝙡𝙖𝙣𝙙ı.",
                show_alert=True,
            )
            return await cb.message.delete()

    if dis == "decline":
        try:
            await app.decline_chat_join_request(chat_id=chat.id, user_id=id)
        except Exception as e:
            if "messages.HideChatJoinRequest" in str(e):
                await cb.answer(
                    "𝙆𝙪𝙡𝙡𝙖𝙣ı𝙘ı, 𝙜𝙧𝙪𝙗𝙪𝙣𝙪𝙯𝙙𝙖 𝙝𝙚𝙧𝙝𝙖𝙣𝙜𝙞 𝙗𝙞𝙧𝙞 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙤𝙣𝙖𝙮𝙡𝙖𝙣𝙙ı.",
                    show_alert=True,
                )

    await approvaldb.update_one(
        {"chat_id": chat.id},
        {"$pull": {"pending_users": int(id)}},
    )
    return await cb.message.delete()


__MODULE__ = "𝙊𝙣𝙖𝙮"
__HELP__ = """
𝙆𝙤𝙢𝙪𝙩: /otoonay

𝘽𝙪 𝙢𝙤𝙙𝙪̈𝙡, 𝙗𝙞𝙧 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı 𝙩𝙖𝙧𝙖𝙛ı𝙣𝙙𝙖𝙣 𝙜𝙧𝙪𝙗𝙪𝙣𝙪𝙯𝙪𝙣 𝙙𝙖𝙫𝙚𝙩 𝙗𝙖𝙜̆𝙡𝙖𝙣𝙩ı𝙨ı 𝙖𝙧𝙖𝙘ı𝙡ı𝙜̆ı𝙮𝙡𝙖 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙞𝙡𝙚𝙣 𝙨𝙤𝙝𝙗𝙚𝙩 𝙠𝙖𝙩ı𝙡𝙢𝙖 𝙞𝙨𝙩𝙚𝙠𝙡𝙚𝙧𝙞𝙣𝙞 𝙤𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙤𝙡𝙖𝙧𝙖𝙠 𝙠𝙖𝙗𝙪𝙡 𝙚𝙩𝙢𝙚𝙮𝙚 𝙮𝙖𝙧𝙙ı𝙢𝙘ı 𝙤𝙡𝙪𝙧.

𝙈𝙤𝙙𝙡𝙖𝙧: /otoonay 𝙠𝙤𝙢𝙪𝙩𝙪𝙣𝙪 𝙜𝙧𝙪𝙗𝙪𝙣𝙪𝙯𝙙𝙖 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙙𝙞𝙜̆𝙞𝙣𝙞𝙯𝙙𝙚, 𝙤𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙤𝙣𝙖𝙮 𝙚𝙩𝙠𝙞𝙣 𝙙𝙚𝙜̆𝙞𝙡𝙨𝙚 "𝙖𝙘̧" 𝙢𝙚𝙨𝙖𝙟ı𝙣ı 𝙜𝙤̈𝙧𝙚𝙘𝙚𝙠𝙨𝙞𝙣𝙞𝙯. 𝙀𝙜̆𝙚𝙧 𝙯𝙖𝙩𝙚𝙣 𝙚𝙩𝙠𝙞𝙣𝙨𝙚, 𝙖𝙨̧𝙖𝙜̆ı𝙙𝙖 𝙗𝙚𝙡𝙞𝙧𝙩𝙞𝙡𝙚𝙣 𝙞𝙠𝙞 𝙢𝙤𝙙𝙙𝙖𝙣 𝙗𝙞𝙧𝙞𝙣𝙞 𝙜𝙤̈𝙧𝙚𝙘𝙚𝙠𝙨𝙞𝙣𝙞𝙯 𝙫𝙚 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙢ı 𝙝𝙖𝙠𝙠ı𝙣𝙙𝙖 𝙗𝙞𝙡𝙜𝙞 𝙖𝙡𝙖𝙘𝙖𝙠𝙨ı𝙣ı𝙯.

¤ 𝙊𝙩𝙤𝙢𝙖𝙩𝙞𝙠 - 𝙎𝙤𝙝𝙗𝙚𝙩 𝙠𝙖𝙩ı𝙡𝙢𝙖 𝙞𝙨𝙩𝙚𝙠𝙡𝙚𝙧𝙞𝙣𝙞 𝙤𝙩𝙤𝙢𝙖𝙩𝙞𝙠 𝙤𝙡𝙖𝙧𝙖𝙠 𝙠𝙖𝙗𝙪𝙡 𝙚𝙙𝙚𝙧.

¤ 𝙈𝙖𝙣𝙪𝙚𝙡 - 𝙔𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙡𝙚𝙧𝙞 𝙚𝙩𝙞𝙠𝙚𝙩𝙡𝙚𝙮𝙚𝙧𝙚𝙠 𝙨𝙤𝙝𝙗𝙚𝙩𝙚 𝙗𝙞𝙧 𝙢𝙚𝙨𝙖𝙟 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙞𝙡𝙚𝙘𝙚𝙠𝙩𝙞𝙧. 𝙔𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙡𝙚𝙧, 𝙞𝙨𝙩𝙚𝙠𝙡𝙚𝙧𝙞 𝙠𝙖𝙗𝙪𝙡 𝙚𝙙𝙚𝙗𝙞𝙡𝙞𝙧 𝙫𝙚𝙮𝙖 𝙧𝙚𝙙𝙙𝙚𝙙𝙚𝙗𝙞𝙡𝙞𝙧.

𝙆𝙪𝙡𝙡𝙖𝙣ı𝙢: /onaysil 𝙠𝙤𝙢𝙪𝙩𝙪𝙣𝙪 𝙠𝙪𝙡𝙡𝙖𝙣𝙖𝙧𝙖𝙠 𝙩𝙪̈𝙢 𝙗𝙚𝙠𝙡𝙚𝙮𝙚𝙣 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙡𝙖𝙧ı 𝙫𝙚𝙧𝙞𝙩𝙖𝙗𝙖𝙣ı𝙣𝙙𝙖𝙣 𝙠𝙖𝙡𝙙ı𝙧𝙖𝙗𝙞𝙡𝙞𝙧𝙨𝙞𝙣𝙞𝙯. 𝘽𝙪, 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙘ı𝙣ı𝙣 𝙩𝙚𝙠𝙧𝙖𝙧 𝙞𝙨𝙩𝙚𝙠 𝙜𝙤̈𝙣𝙙𝙚𝙧𝙢𝙚𝙨𝙞𝙣𝙚 𝙤𝙡𝙖𝙣𝙖𝙠 𝙩𝙖𝙣ı𝙧.
"""
