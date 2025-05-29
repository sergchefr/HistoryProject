import telebot
from telebot import types
import random
from randYearGenerator import random_year
import xml.etree.ElementTree as ET

# Инициализация
bot = telebot.TeleBot("8190916259:AAEsF_m4TwjVHr_vLbu6I4W1YzfOaU2BXEo")
user_data = {}
questions = {}
quiz_list = []
highest_score = 10

tree = ET.parse('database.xml')
root = tree.getroot()

# Парсинг
for elem in root.findall('quiz_element'):
    quiz_item = {
        'question': elem.findtext('question', default='').strip(),
        'options': random_year(elem.findtext('year', default='').strip()),
        'year': elem.findtext('year', default='').strip(),
        'description': elem.findtext('description', default='').strip()
    }
    quiz_list.append(quiz_item)

# Теперь quiz_list — список словарей, каждый словарь — один quiz_element

# def get_random_quiz():
#     return list(random.sample(questions, k=min(10, len(questions))))

def get_random_quiz_element():
    quiz = random.choice(quiz_list)
    return quiz['question'], quiz['options'], quiz['year'], quiz['description']

def get_random_quiz():
    quiz_elements=[]

    while len(set(quiz_elements)) < 10:
        quiz_elements.append(get_random_quiz_element())
    return quiz_elements

# Вспомогательные функции

# Принимает правильный ответ и тот, что написал пользователь. Возвращает количество полученных очков
def count_score(correct_year, answer):
    if 10>=abs(answer-correct_year)>=5: return 1
    if 5>abs(answer-correct_year)>2: return 2
    if 2>=abs(answer-correct_year)>=1: return 4
    if abs(answer-correct_year)==0: return 8
    return 0


# Функции
@bot.message_handler(commands=['start'])
def start(message):
    text = f'''
    ⚡️ Привет, {message.from_user.first_name}! Я бот "ДатаГрад", и я помогу вам освежить или проверить ваши знания о ключевых датах и событиях XX века.
    Вас ждет увлекательная викторина! 

    ▶️ Чтобы начать, нажмите "Quiz".
    ❓ Для получения своей статистики нажмите "Stats".'''
    user_data[message.chat.id] = {
        "score": 0,
        "hardmode_score": 0,
        "current": 0,
        "quiz": get_random_quiz()
    }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    quiz_button = types.KeyboardButton("Quiz")
    stats_button = types.KeyboardButton("Stats")
    markup.add(quiz_button, stats_button)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "Quiz")
def ask_question(message):
    user = user_data[message.chat.id]
    if user["current"] >= highest_score:
        text = '''
        👀 Хотите сыграть снова? Нажмите "Quiz".
        📖 Для просмотра статистики нажмите "Stats"
        '''
        bot.send_message(message.chat.id, f"Викторина завершена!\nВы набрали {user['score']} из {highest_score} баллов.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quiz_button = types.KeyboardButton("Quiz")
        stats_button = types.KeyboardButton("Stats")
        markup.add(quiz_button, stats_button)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        return

    q = user["quiz"][user["current"]]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in q["options"]:
        markup.add(types.KeyboardButton(opt))
    bot.send_message(message.chat.id, f"Вопрос {user['current'] + 1}: {q['question']}", reply_markup=markup)


@bot.message_handler(func=lambda m: True)
def handle_answer(message):
    user = user_data.get(message.chat.id)
    if not user or user["current"] >= 10:
        return

    q = user["quiz"][user["current"]]
    correct = q["correct"]

    user["hardmode_score"] += count_score(correct, q["answer"])

    if message.text == correct:
        user["score"] += 1
        response = f"✅ Верно! {q['info']}"
    elif message.text in q["options"]:
        response = f"❌ Неверно. Правильный ответ: {correct}.\n Вот краткое описание этого исторического события: {q['info']}"
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите вариант ответа с кнопок🥺")
        return

    user["current"] += 1
    bot.send_message(message.chat.id, response)
    ask_question(message)


# @bot.message_handler(commands=['test'])
# def test(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     itembtn1 = types.KeyboardButton('1945')
#     itembtn2 = types.KeyboardButton('1917')
#     itembtn3 = types.KeyboardButton('1983')
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(message.chat.id, f"Выбери, {message.from_user.first_name}:", reply_markup=markup)
#

@bot.message_handler()
def echo(message):
    bot.send_message(message.chat.id, f"К сожалению, я понимаю только команды, а «{message.text}» не является командой.", parse_mode="html")


bot.polling(none_stop=True)