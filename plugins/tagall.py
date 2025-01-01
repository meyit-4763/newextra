import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from YukkiMusic import app


SPAM_CHATS = []


async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if user_id in admin_ids:
        return True
    return False


@app.on_message(
    filters.command(["all", "allmention", "mentionall", "tagall"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "Etiketleme işlemi zaten devam ediyor. Durdurmak istiyorsanız /cancel kullanın."
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "**Tüm kullanıcıları etiketlemek için bir metin verin, örneğin »** `@all Merhaba Arkadaşlar`"
        )
        return
    if replied:
        usernum = 0
        usertxt = ""
        try:
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(message.chat.id):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(1)
                    usernum = 0
                    usertxt = ""

            if usernum != 0:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        try:
            usernum = 0
            usertxt = ""
            text = message.text.split(None, 1)[1]
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(message.chat.id):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await app.send_message(
                        message.chat.id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(2)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


async def tag_all_admins(_, message):
    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "Etiketleme işlemi zaten devam ediyor. Durdurmak istiyorsanız /cancel kullanın."
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "**Tüm yöneticileri etiketlemek için bir metin verin, örneğin »** `@admins Merhaba Arkadaşlar`"
        )
        return
    if replied:
        usernum = 0
        usertxt = ""
        try:
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(
                message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(1)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        usernum = 0
        usertxt = ""
        try:
            text = message.text.split(None, 1)[1]
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(
                message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await app.send_message(
                        message.chat.id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(2)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


@app.on_message(
    filters.command(["admin", "admins", "report"], prefixes=["/", "@"]) & filters.group
)
async def admintag_with_reporting(client, message):
    if not message.from_user:
        return
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    admins = [
        admin.user.id
        async for admin in client.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if message.command[0] == "report":
        if from_user_id in admins:
            return await message.reply_text(
                "Oops! Görünüşe göre bir yöneticisiniz!\nYönetici olan bir kullanıcıyı raporlayamazsınız."
            )

    if from_user_id in admins:
        return await tag_all_admins(client, message)

    if len(message.text.split()) <= 1 and not message.reply_to_message:
        return await message.reply_text("Raporlamak istediğiniz kullanıcıya yanıt verin.")

    reply = message.reply_to_message or message
    reply_user_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    linked_chat = (await client.get_chat(chat_id)).linked_chat
    if reply_user_id == app.id:
        return await message.reply_text("Kendimi neden raporlayayım?")
    if (
        reply_user_id in admins
        or reply_user_id == chat_id
        or (linked_chat and reply_user_id == linked_chat.id)
    ):
        return await message.reply_text(
            "Yanıt verdiğiniz kullanıcının bir yönetici olduğunu biliyor musunuz?"
        )

    user_mention = reply.from_user.mention if reply.from_user else "kullanıcı"
    text = f"Yöneticilere {user_mention} rapor edildi!."

    for admin in admins:
        admin_member = await client.get_chat_member(chat_id, admin)
        if not admin_member.user.is_bot and not admin_member.user.is_deleted:
            text += f"[\u2063](tg://user?id={admin})"

    await reply.reply_text(text)


@app.on_message(
    filters.command(
        [
            "stopmention",
            "cancel",
            "cancelmention",
            "offmention",
            "mentionoff",
            "cancelall",
        ],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text("**Etiketleme işlemi başarıyla durduruldu!**")

    else:
        await message.reply_text("**Devam eden bir işlem yok!**")
        return


__MODULE__ = "Tᴀɢᴀʟʟ"
__HELP__ = """

@all veya /all | /tagall veya @tagall | /mentionall veya @mentionall [metin] veya [bir mesaja yanıt vererek] tüm kullanıcıları etiketlemek için kullanın.

/admins veya @admins | /report [metin] veya [bir mesaja yanıt vererek] tüm yöneticileri etiketlemek için kullanın.

/cancel veya @cancel | /offmention veya @offmention | /mentionoff veya @mentionoff | /cancelall veya @cancelall - Devam eden herhangi bir etiketleme işlemini durdurmak için kullanın.

**__NOT__** Bu komut yalnızca sohbetin yöneticileri tarafından kullanılabilir ve botun ve asistanın grup içinde bir yönetici olduğundan emin olun.
"""