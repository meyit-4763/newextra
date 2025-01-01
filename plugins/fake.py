import requests
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command(["FAKE", "fake"]))
async def fkadress(_, message):
    query = message.text.split(maxsplit=1)[1].strip()  # Kullanıcının girdiği ülke adını al
    url = f"https://randomuser.me/api/?nat={query}"  # API URL'sini oluştur
    response = requests.get(url)  # API'den veri al
    data = response.json()  # JSON formatında veriyi al

    if "results" in data:  # Eğer sonuç varsa
        fk = data["results"][0]  # İlk sonucu al

        name = f"{fk['name']['title']} {fk['name']['first']} {fk['name']['last']}"  # İsim
        address = (
            f"{fk['location']['street']['number']} {fk['location']['street']['name']}"  # Adres
        )
        city = fk["location"]["city"]  # Şehir
        state = fk["location"]["state"]  # Eyalet
        country = fk["location"]["country"]  # Ülke
        postal = fk["location"]["postcode"]  # Posta kodu
        email = fk["email"]  # E-posta
        phone = fk["phone"]  # Telefon
        picture = fk["picture"]["large"]  # Resim
        gender = fk["gender"]  # Cinsiyet

        fkinfo = f"""
**𝙄̇𝙨𝙞𝙢** ⇢ `{name}`
**𝘾𝙞𝙣𝙨𝙞𝙮𝙚𝙩** ⇢ `{gender}`
**𝘼𝙙𝙧𝙚𝙨** ⇢ `{address}`
**𝙐̈𝙡𝙠𝙚** ⇢ `{country}`
**𝙎̧𝙚𝙝𝙞𝙧** ⇢ `{city}`
**𝙀𝙮𝙖𝙡𝙚𝙩** ⇢ `{state}`
**𝙋𝙤𝙨𝙩𝙖 𝙆𝙤𝙙𝙪** ⇢ `{postal}`
**𝙀-𝙥𝙤𝙨𝙩𝙖** ⇢ `{email}`
**𝙏𝙚𝙡𝙚𝙛𝙤𝙣** ⇢ `{phone}`

        """

        await message.reply_photo(photo=picture, caption=fkinfo)  # Resmi ve bilgileri gönder
    else:
        await message.reply_text("𝙊𝙥𝙥𝙨.. 𝙝𝙚𝙧𝙝𝙖𝙣𝙜𝙞 𝙗𝙞𝙧 𝙖𝙙𝙧𝙚𝙨 𝙗𝙪𝙡𝙪𝙣𝙖𝙢𝙖𝙙ı.\n𝙇𝙜̆𝙩𝙛𝙚𝙣 𝙩𝙚𝙠𝙧𝙖𝙧 𝙙𝙚𝙣𝙚𝙮𝙞𝙣.")  # Hata mesajı


__MODULE__ = "𝙎𝙖𝙝𝙩𝙚"  # Modül adı
__HELP__ = """
/fake [ülke adı] - 𝙍𝙖𝙨𝙩𝙜𝙚𝙡𝙚 𝙨𝙖𝙝𝙩𝙚 𝙖𝙙𝙧𝙚𝙨 𝙖𝙡𝙢𝙖𝙠 𝙞𝙘̧𝙞𝙣 𝙠𝙪𝙡𝙡𝙖𝙣ı𝙡ı𝙧.
"""
