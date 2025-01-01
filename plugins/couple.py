import os
import random
from datetime import datetime, timedelta

import pytz
import requests
from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TheApi import api
from DnsXMusic import app

from utils import get_couple, get_image, save_couple


# Mevcut tarihi GMT+5:30 saat diliminde al
def get_today_date():
    timezone = pytz.timezone("Europe/istanbul")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")


# Yarın tarihini GMT+5:30 saat diliminde al
def get_todmorrow_date():
    timezone = pytz.timezone("Europe/istanbul")
    tomorrow = datetime.now(timezone) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")


# URL'den resim indir
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path


# Tarihler
tomorrow = get_todmorrow_date()
today = get_today_date()


@app.on_message(filters.command(["asıklar", "couples"]))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("𝘽𝙪 𝙠𝙤𝙢𝙪𝙩 𝙮𝙖𝙡𝙣ı𝙯𝙘𝙖 𝙜𝙧𝙪𝙥𝙡𝙖𝙧𝙙𝙖 𝙘̧𝙖𝙡ı𝙨̧ı𝙧.")

    p1_path = "downloads/pfp.png"
    p2_path = "downloads/pfp1.png"
    test_image_path = f"downloads/test_{cid}.png"
    cppic_path = "downloads/cppic.png"

    try:
        is_selected = await get_couple(cid, today)
        if not is_selected:
            msg = await message.reply_text("❣️")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot and not i.user.is_deleted:
                    list_of_users.append(i.user.id)

            c1_id = random.choice(list_of_users)  # İlk kullanıcıyı rastgele seç
            c2_id = random.choice(list_of_users)  # İkinci kullanıcıyı rastgele seç
            while c1_id == c2_id:  # İki kullanıcı aynı olmamalı
                c1_id = random.choice(list_of_users)

            photo1 = (await app.get_chat(c1_id)).photo
            photo2 = (await app.get_chat(c2_id)).photo

            N1 = (await app.get_users(c1_id)).mention
            N2 = (await app.get_users(c2_id)).mention

            try:
                p1 = await app.download_media(photo1.big_file_id, file_name=p1_path)
            except Exception:
                p1 = download_image(
                    "https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path
                )
            try:
                p2 = await app.download_media(photo2.big_file_id, file_name=p2_path)
            except Exception:
                p2 = download_image(
                    "https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path
                )

            img1 = Image.open(p1)
            img2 = Image.open(p2)

            background_image_path = download_image(
                "https://telegra.ph/file/96f36504f149e5680741a.jpg", cppic_path
            )
            img = Image.open(background_image_path)

            img1 = img1.resize((437, 437))
            img2 = img2.resize((437, 437))

            mask = Image.new("L", img1.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + img1.size, fill=255)

            mask1 = Image.new("L", img2.size, 0)
            draw = ImageDraw.Draw(mask1)
            draw.ellipse((0, 0) + img2.size, fill=255)

            img1.putalpha(mask)
            img2.putalpha(mask1)

            draw = ImageDraw.Draw(img)

            img.paste(img1, (116, 160), img1)
            img.paste(img2, (789, 160), img2)

            img.save(test_image_path)

            TXT = f"""
**𝘽𝙪𝙜𝙪̈𝙣𝙪̈𝙣 𝘾̧𝙞𝙛𝙩𝙞:

{N1} + {N2} = 💚

𝙎𝙤𝙣𝙧𝙖𝙠𝙞 𝙘̧𝙞𝙛𝙩𝙡𝙚𝙧 {tomorrow} 𝙩𝙖𝙧𝙞𝙝𝙞𝙣𝙙𝙚 𝙨𝙚𝙘̧𝙞𝙡𝙚𝙘𝙚𝙠𝙩𝙞𝙧!!**
            """
            await message.reply_photo(
                test_image_path,
                caption=TXT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝘽𝙚𝙣𝙞 𝙂𝙧𝙪𝙗𝙪𝙣𝙖 𝙀𝙠𝙡𝙚 🌋",
                                url=f"https://t.me/{app.username}?startgroup=true",
                            )
                        ]
                    ]
                ),
            )

            await msg.delete()  # Önceki mesajı sil
            img_url = await api.upload_image(test_image_path)  # Resmi API'ye yükle
            couple = {"c1_id": c1_id, "c2_id": c2_id}  # Çift bilgilerini oluştur
            await save_couple(cid, today, couple, img_url)  # Çifti kaydet

        else:
            msg = await message.reply_text("❣️")
            b = await get_image(cid)  # Daha önce kaydedilen çifti al
            c1_id = int(is_selected["c1_id"])  # İlk kullanıcının ID'sini al
            c2_id = int(is_selected["c2_id"])  # İkinci kullanıcının ID'sini al
            c1_name = (await app.get_users(c1_id)).first_name  # İlk kullanıcının ismini al
            c2_name = (await app.get_users(c2_id)).first_name  # İkinci kullanıcının ismini al

            TXT = f"""
**𝘽𝙪𝙜𝙪̈𝙣𝙪̈𝙣 𝘾̧𝙞𝙛𝙩𝙞 🎉:

[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❣️

𝙎𝙤𝙣𝙧𝙖𝙠𝙞 𝙘̧𝙞𝙛𝙩𝙡𝙚𝙧 {tomorrow} 𝙩𝙖𝙧𝙞𝙝𝙞𝙣𝙙𝙚 𝙨𝙚𝙘̧𝙞𝙡𝙚𝙘𝙚𝙠𝙩𝙞𝙧!!**
            """
            await message.reply_photo(
                b,
                caption=TXT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝘽𝙚𝙣𝙞 𝙂𝙧𝙪𝙗𝙪𝙣𝙖 𝙀𝙠𝙡𝙚🌋",
                                url=f"https://t.me/{app.username}?startgroup=true",
                            )
                        ]
                    ]
                ),
            )
            await msg.delete()  # Önceki mesajı sil

    except Exception:
        pass  # Hata durumunda hiçbir şey yapma
    finally:
        try:
            os.remove(p1_path)  # Geçici dosyaları sil
            os.remove(p2_path)
            os.remove(test_image_path)
            os.remove(cppic_path)
        except Exception:
            pass  # Silme işlemi sırasında hata olursa hiçbir şey yapma
