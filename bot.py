import telebot
import config
import reve

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def generate_img(message):
    bot.send_chat_action(message.chat.id, 'typing')

    image_path = reve.generate_reve_image(message.text)

    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Ошибка при генерации изображения")

bot.infinity_polling()
