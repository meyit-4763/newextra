import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from DnsXMusic import app

from utils.permissions import adminsOnly

chatQueue = []

stopProcess = False

@app.on_message(filters.command(["zombies"]))
@adminsOnly("can_restrict_members")
async def remove(client, message):

    global stopProcess
    try:
        try:
            sender = await app.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except BaseException:
            has_permissions = message.sender_chat
        if has_permissions:
            bot = await app.get_chat_member(message.chat.id, "self")
            if bot.status == ChatMemberStatus.MEMBER:
                await message.reply(
                    "➠ | 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥𝙡𝙖𝙧ı 𝙮𝙖𝙡𝙣ı𝙯𝙘𝙖 𝘼𝙙𝙢𝙞𝙣𝙡𝙚𝙧 𝙮𝙖𝙨𝙖𝙠𝙡𝙖𝙮𝙖𝙗𝙞𝙡𝙞𝙩"
                )
            else:
                if len(chatQueue) > 30:
                    await message.reply(
                        "➠ | 𝘽𝙚𝙣 𝙕𝙖𝙩𝙚𝙣 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥𝙡𝙖𝙧ı 𝙔𝙖𝙨𝙖𝙠𝙡𝙖𝙙ı𝙢.."
                    )
                else:
                    if message.chat.id in chatQueue:
                        await message.reply(
                            "➠ | 𝙞𝙨̧𝙡𝙚𝙢𝙞 𝙙𝙪𝙧𝙙𝙪𝙧𝙢𝙖𝙠 𝙞𝙘̧𝙞𝙣 𝙇𝙪̈𝙩𝙛𝙚𝙣 /stop 𝙆𝙤𝙢𝙪𝙩𝙪𝙣𝙪 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙣. "
                        )
                    else:
                        chatQueue.append(message.chat.id)
                        deletedList = []
                        async for member in app.get_chat_members(message.chat.id):
                            if member.user.is_deleted:
                                deletedList.append(member.user)
                        lenDeletedList = len(deletedList)
                        if lenDeletedList == 0:
                            await message.reply("⟳ | 𝘽𝙪 𝙎𝙤𝙝𝙗𝙚𝙩𝙩𝙚 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥 𝙔𝙤𝙠𝙩𝙪𝙧.")
                            chatQueue.remove(message.chat.id)
                        else:
                            k = 0
                            processTime = lenDeletedList * 1
                            temp = await app.send_message(
                                message.chat.id,
                                f"🧭 | 𝙏𝙤𝙥𝙡𝙖𝙢 {lenDeletedList} 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥𝙡𝙖𝙧 𝙆𝙖𝙡𝙙𝙧ı𝙡𝙙ı.\n🥀 | 𝙕𝙖𝙢𝙖𝙣: {processTime}.",
                            )
                            if stopProcess:
                                stopProcess = False
                            while len(deletedList) > 0 and not stopProcess:
                                deletedAccount = deletedList.pop(0)
                                try:
                                    await app.ban_chat_member(
                                        message.chat.id, deletedAccount.id
                                    )
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                                k += 1
                            if k == lenDeletedList:
                                await message.reply(
                                    f"✅ | 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥𝙡𝙖𝙧 𝙔𝙖𝙨𝙖𝙠𝙡𝙖𝙣𝙙ı."
                                )
                                await temp.delete()
                            else:
                                await message.reply(
                                    f"✅ | 𝙎𝙞𝙡𝙞𝙣𝙚𝙣 𝙃𝙚𝙨𝙖𝙥 {k} 𝙔𝙖𝙨𝙖𝙠𝙡𝙖𝙣𝙙ı."
                                )
                                await temp.delete()
                            chatQueue.remove(message.chat.id)
        else:
            await message.reply(
                "👮🏻 | ᴏʟᴍᴀᴅɪ, **𝙎𝙖𝙙𝙚𝙘𝙚 𝙔𝙤̈𝙣𝙚𝙩𝙞𝙘𝙞𝙡𝙚𝙧**"
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)

__MODULE__ = "𝙕𝙤𝙢𝙗𝙞𝙚𝙨"
__HELP__ = """
**komutlar:**
- /zombies: ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ɢʀᴏᴜᴘᴛᴀɴ ᴄᴀᴋᴀʀ.

**bilgi:**
- ᴍᴏᴅᴜʟᴇ ɴᴀᴍᴇ: ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ᴄᴀᴋᴀʀ
- ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ɢʀᴏᴜᴘᴛᴀɴ ᴄᴀᴋᴀʀ.
- ᴄᴏᴍᴍᴀɴᴅs: /zombies
- ᴘᴇʀᴍɪssɪᴏɴs ɴᴇᴇᴅᴇᴅ: ᴄᴀɴ ʀᴇsᴛʀɪᴄᴛ ᴍᴇᴍʙᴇʀs

**not:**
- ᴇɴ ʏᴇᴋᴜɴ ᴇғғᴇᴄᴛ ɪçɪɴ ʙɪʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ ᴋᴜʟʟᴀɴɪɴ. ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.
""" 
