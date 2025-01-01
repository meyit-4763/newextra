import io

from gtts import gTTS
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command("tts"))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Lütfen sesli konuşmaya dönüştürmek için bir metin sağlayın."
        )

    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang="hi")
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    audio_file = io.BytesIO(audio_data.read())
    audio_file.name = "audio.mp3"
    await message.reply_audio(audio_file)


__HELP__ = """
**Metin Sesli Konuşma Botu Komutları**

`/tts` komutunu kullanarak metni sesli konuşmaya dönüştürebilirsiniz.

- `/tts <metin>`: Verilen metni Hintçe sesli konuşmaya dönüştürür.

**Örnek:**
- `/tts Namaste Duniya`

**Not:**
`/tts` komutundan sonra bir metin sağladığınızdan emin olun.
"""

__MODULE__ = "Tᴛs"