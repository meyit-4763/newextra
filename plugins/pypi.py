import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app


def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        if response.status_code == 200:
            pypi_info = response.json()
            return pypi_info
        else:
            return None
    except Exception as e:
        print(f"PyPI bilgileri alınırken hata: {e}")
        return None


@app.on_message(filters.command("pypi", prefixes="/"))
async def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        pypi_info = get_pypi_info(package_name)

        if pypi_info:
            info_message = (
                f"Sevgili {message.from_user.mention} \n "
                f"İşte paket detaylarınız \n\n "
                f"Paket Adı ➪ {pypi_info['info']['name']}\n\n"
                f"Son Versiyon ➪ {pypi_info['info']['version']}\n\n"
                f"Açıklama ➪ {pypi_info['info']['summary']}\n\n"
                f"Proje URL'si ➪ {pypi_info['info']['project_urls']['Homepage']}"
            )
            close_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="〆 Kapat 〆", callback_data="close")]]
            )
            await message.reply_text(info_message, reply_markup=close_markup)
        else:
            await message.reply_text(
                f"Paket '{package_name}' bulunamadı. Lütfen daha sonra tekrar deneyin."
            )

    except IndexError:
        await message.reply_text(
            "Lütfen /pypi komutundan sonra bir paket adı girin."
        )


__MODULE__ = "Pʏᴘɪ"
__HELP__ = """
**Komutlar:**
• /pypi <paket_adı>: Belirtilen Python paketinin PyPI'den detaylarını alın.

**Bilgi:**
Bu modül, kullanıcıların PyPI'den Python paketleri hakkında bilgi almasına olanak tanır; paket adı, son versiyon, açıklama ve proje URL'si dahil.

**Not:**
Lütfen `/pypi` komutundan sonra geçerli bir paket adı sağlayın, böylece paket detaylarını alabilirsiniz.
"""