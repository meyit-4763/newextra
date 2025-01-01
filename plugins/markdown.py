from pyrogram.enums import ChatType, ParseMode
from pyrogram.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from DnsXMusic import app
from DnsXMusic.utils.functions import MARKDOWN


@app.on_message(command("markdownyardim"))
async def mkdwnyardim(_, m: Message):
    keyb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Buraya Tıklayın!",
                    url=f"http://t.me/{app.username}?start=markdown_yardim",
                )
            ]
        ]
    )
    if m.chat.type != ChatType.PRIVATE:
        await m.reply(
            "Aşağıdaki düğmeye tıklayarak markdown kullanım sözdizimini özel mesajda alın!",
            reply_markup=keyb,
        )
    else:
        await m.reply(
            MARKDOWN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
    return
