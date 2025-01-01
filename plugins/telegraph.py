import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TheApi import api
from YukkiMusic import app


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Lütfen bir medya dosyasına yanıt verin, böylece Telegraphta yükleyebilirim."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 15 * 1024 * 1024:
        return await message.reply_text("Lütfen 15MB'den küçük bir medya dosyası sağlayın.")

    try:
        text = await message.reply("İşleniyor...")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 İndiriliyor... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 Telegrapha yükleniyor...")

            upload_path = await api.upload_image(local_path)

            await text.edit_text(
                f"🌐 | [Yüklenen Bağlantı]({upload_path})",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yüklenen Dosya",
                                url=upload_path,
                            )
                        ]
                    ]
                ),
            )

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ Dosya yükleme başarısız oldu\n\n<i>Sebep: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass


__HELP__ = """
**Telegraph Yükleme Botu Komutları**

Bu komutları kullanarak medya dosyalarını Telegrapha yükleyebilirsiniz:

- `/tgm`: Yanıt verilen medya dosyasını Telegrapha yükler.
- `/tgt`: `/tgm` ile aynı.
- `/telegraph`: `/tgm` ile aynı.
- `/tl`: `/tgm` ile aynı.

**Örnek:**
- Bir fotoğraf veya videoya yanıt vererek `/tgm` kullanarak yükleyin.

**Not:**
Yükleme işleminin çalışabilmesi için bir medya dosyasına yanıt vermeniz gerekmektedir.
"""

__MODULE__ = "𝙏-𝙂𝙧𝙖𝙥𝙝"
