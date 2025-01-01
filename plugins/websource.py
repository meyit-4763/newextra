import requests
from pyrogram import filters
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from DnsXMusic import app


def download_website(url):
    headers = {
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return (
                f"Kaynak kodunu indirmek başarısız oldu. Durum kodu: {response.status_code}"
            )

    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"


# /webdl komutu için web sitesi kaynak kodunu indirme işleyicisi
@app.on_message(filters.command("webdl"))
def web_download(client, message):
    # Komutun yanında bir URL olup olmadığını kontrol et
    if len(message.command) == 1:
        message.reply_text("Lütfen /webdl komutuyla birlikte bir URL girin.")
        return

    # /webdl komutundan sonra URL'yi al
    url = message.command[1]

    source_code = download_website(url)
    if source_code.startswith("Bir hata oluştu") or source_code.startswith(
        "Kaynak kodunu indirmek"
    ):
        message.reply_text(source_code)
    else:
        # Kaynak kodunu bir dosyaya kaydet
        with open("website.txt", "w", encoding="utf-8") as file:
            file.write(source_code)
        message.reply_document(document="website.txt", caption=f"{url} adresinin kaynak kodu.")


__MODULE__ = "𝙒𝙚𝙗𝘿𝙇"
__HELP__ = """
**KOMUT:**

• /webdl - **Web sitesi kaynak kodunu indir.**

**BİLGİ:**

- Bu bot, bir web sitesinin kaynak kodunu indirmek için bir komut sağlar.
- /webdl komutunu bir URL ile kullanarak web sitesinin kaynak kodunu indirin ve sohbete gönderin.

**NOT:**

- Bu komut, web sitesi kaynak kodunu indirmek için kullanılabilir.
- Kaynak kodu bir belge olarak kaydedilecek ve sohbete gönderilecektir.
"""
