import telebot
import config
import os
from services.leonardo_service import LeonardoService

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
leonardo = LeonardoService(config.LEONARDO_API_KEY)


# 1️⃣ START / HELP
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "👋 Привет!\n\n"
        "Я бот для генерации изображений через Leonardo AI.\n\n"
        "Просто отправь текстовое описание,\n"
        "и я создам для тебя картинку 🎨"
    )
    bot.send_message(message.chat.id, text)


# 2️⃣ Обработка текста
@bot.message_handler(content_types=['text'])
def handle_prompt(message):

    # 4️⃣ Сообщение о генерации
    status_msg = bot.send_message(
        message.chat.id,
        "⏳ Генерирую картинку..."
    )

    # 2️⃣ Имитация печати
    bot.send_chat_action(message.chat.id, "typing")

    image_path = leonardo.generate_image(message.text)

    if image_path:

        # Отправляем картинку
        with open(image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)

        # 4️⃣ Удаляем сообщение "Генерирую..."
        bot.delete_message(message.chat.id, status_msg.message_id)

        # 3️⃣ Удаляем файл с диска
        try:
            os.remove(image_path)
            print(f"Deleted file: {image_path}")
        except Exception as e:
            print("Failed to delete file:", e)

    else:
        bot.edit_message_text(
            "❌ Ошибка генерации изображения.",
            message.chat.id,
            status_msg.message_id
        )


bot.infinity_polling()
