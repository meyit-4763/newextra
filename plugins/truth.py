import requests
from pyrogram import filters
from YukkiMusic import app


truth_api_url = "https://api.truthordarebot.xyz/v1/truth"
dare_api_url = "https://api.truthordarebot.xyz/v1/dare"


@app.on_message(filters.command("truth"))
def get_truth(client, message):
    try:
        response = requests.get(truth_api_url)
        if response.status_code == 200:
            truth_question = response.json()["question"]
            message.reply_text(f"Doğruluk sorusu:\n\n{truth_question}")
        else:
            message.reply_text(
                "Bir doğruluk sorusu alınamadı. Lütfen daha sonra tekrar deneyin."
            )
    except Exception as e:
        message.reply_text(
            "Bir doğruluk sorusu alınırken hata oluştu. Lütfen daha sonra tekrar deneyin."
        )


@app.on_message(filters.command("dare"))
def get_dare(client, message):
    try:
        response = requests.get(dare_api_url)
        if response.status_code == 200:
            dare_question = response.json()["question"]
            message.reply_text(f"Cesaret sorusu:\n\n{dare_question}")
        else:
            message.reply_text(
                "Bir cesaret sorusu alınamadı. Lütfen daha sonra tekrar deneyin."
            )
    except Exception as e:
        message.reply_text(
            "Bir cesaret sorusu alınırken hata oluştu. Lütfen daha sonra tekrar deneyin."
        )


__HELP__ = """
**Doğruluk veya Cesaret Botu Komutları**

Bu komutları kullanarak doğruluk veya cesaret oyunu oynayabilirsiniz:

- `/truth`: Rastgele bir doğruluk sorusu alın. Cevabınızı dürüstçe verin!
- `/dare`: Rastgele bir cesaret meydan okuması alın. Cesaret ederseniz tamamlayın!

**Örnekler:**
- `/truth`: "En utanç verici anınız nedir?"
- `/dare`: "10 şınav çekin."

**Not:**
Eğer soruları alırken herhangi bir sorunla karşılaşırsanız, lütfen daha sonra tekrar deneyin.
"""

__MODULE__ = "Dᴏɢʀᴜʟᴜᴋ"