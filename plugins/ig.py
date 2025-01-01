import re
import requests
from config import LOG_GROUP_ID
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "Lütfen komuttan sonra Instagram reel URL'sini sağlayın."
        )
        return
    url = message.text.split()[1]
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "Sağlanan URL geçerli bir Instagram URL'si değil😅😅"
        )
    a = await message.reply_text("İşleniyor...")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        f = f"Hata:\n{e}"
        try:
            await a.edit(f)
        except Exception:
            await message.reply_text(f)
            return await app.send_message(LOG_GROUP_ID, f)
        return await app.send_message(LOG_GROUP_ID, f)
    
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        type = data["extension"]
        size = data["formattedSize"]
        caption = f"**Süre:** {duration}\n**Kalite:** {quality}\n**Tür:** {type}\n**Boyut:** {size}"
        await a.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            return await a.edit("Reel indirilirken başarısız olundu.")
        except Exception:
            return await message.reply_text("Reel indirilirken başarısız olundu.")


__MODULE__ = "𝙄̇𝙣𝙨𝙩𝙖"
__HELP__ = """
**Instagram Reel İndirici:**

• `/ig [URL]`: Instagram reel'lerini indirin. Komuttan sonra Instagram reel URL'sini sağlayın.
• `/instagram [URL]`: Instagram reel'lerini indirin. Komuttan sonra Instagram reel URL'sini sağlayın.
• `/reel [URL]`: Instagram reel'lerini indirin. Komuttan sonra Instagram reel URL'sini sağlayın.
"""
