import random
import time

import requests
from pyrogram import filters
from pyrogram.enums import ChatAction, PollType
from DnsXMusic import app


last_command_time = {}


@app.on_message(filters.command(["test"]))
async def quiz(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text(
            "Lütfen bu komutu tekrar kullanmadan önce 5 saniye bekleyin."
        )
        return

    last_command_time[user_id] = current_time

    categories = [9, 17, 18, 20, 21, 27]
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    response = requests.get(url).json()

    question_data = response["results"][0]
    question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    incorrect_answers = question_data["incorrect_answers"]

    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)

    cid = all_answers.index(correct_answer)
    await app.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=all_answers,
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=cid,
    )


__MODULE__ = "𝙏𝙚𝙨𝙩"
__HELP__ = " /test - Rastgele bir quiz almak için"
