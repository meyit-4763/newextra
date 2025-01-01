import random

from pyrogram import filters
from DnsXMusic import app


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "Aşk havada ama biraz kıvılcım gerekiyor.",
                "İyi bir başlangıç ama gelişmeye açık.",
                "Güzel bir şeyin başlangıcı sadece.",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "Güçlü bir bağ var. Onu beslemeye devam et.",
                "İyi bir şansın var. Üzerinde çalış.",
                "Aşk filizleniyor, devam et.",
            ]
        )
    else:
        return random.choice(
            [
                "Vay! Cennette yapılmış bir eşleşme!",
                "Mükemmel eşleşme! Bu bağı değerli kıl.",
                "Birlikte olmak için kaderde var. Tebrikler!",
            ]
        )


@app.on_message(filters.command("love", prefixes="/"))
def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"{name1}💕 + {name2}💕 = {love_percentage}%\n\n{love_message}"
    else:
        response = "Lütfen /love komutundan sonra iki isim girin."
    app.send_message(message.chat.id, response)


__MODULE__ = "𝘼𝙨̧𝙠"
__HELP__ = """
**Aşk Hesaplayıcı:**

• `/love [isim1] [isim2]`: İki kişi arasındaki aşk yüzdesini hesaplar.
"""
