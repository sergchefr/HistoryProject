import telebot

bot = telebot.TeleBot("8190916259:AAEsF_m4TwjVHr_vLbu6I4W1YzfOaU2BXEo")

@bot.message_handler(commands=['start'])
def start(message):
    text = f'''
    ⚡️ Привет, {message.from_user.first_name}! Я бот "ДатаГрад", и я помогу вам освежить или проверить ваши знания о ключевых датах и событиях XX века.
Вас ждет увлекательная викторина! 
    
▶️ Чтобы начать, используйте команду /quiz.
❓ Для получения списка команд, введите /help.'''
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['test'])
def test(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('a')
    itembtn2 = types.InlineKeyboardButton('v')
    itembtn3 = types.InlineKeyboardButtonButton('d')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, f"Выбери, {message.from_user.first_name}:", reply_markup=markup)

@bot.message_handler()
def echo(message):
    bot.send_message(message.chat.id, f"К сожалению, я понимаю только команды, а «{message.text}» не является командой.", parse_mode="html")

bot.polling(none_stop=True)
