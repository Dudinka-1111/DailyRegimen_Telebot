import telebot
from telebot import types

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем встроенную клавиатуру с кнопками
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Доброе утро!", callback_data="good_morning")
    button2 = types.InlineKeyboardButton("Я проспала.", callback_data="overslept")
    markup.add(button1, button2)

    # Отправляем сообщение с клавиатурой
    bot.send_message(
        message.chat.id,
        "Игра началась!\nПоставь будильник на 7.40 и просыпайся вовремя!",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["good_morning", "overslept"])
def handle_response(call):
    if call.data == "good_morning":
        response = "Доброе утро! Хорошего дня!\nТы заработала 5 баллов!"
    elif call.data == "overslept":
        response = "О нет! Попробуйте завтра встать вовремя."

    # Отправляем новое сообщение с ответом на первый выбор
    bot.send_message(call.message.chat.id, response)

    # Создаем клавиатуру для задания №1
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Готово", callback_data="task1_done")
    button2 = types.InlineKeyboardButton("Не успела заправить кровать", callback_data="task1_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №1
    bot.send_message(call.message.chat.id,
                     "Задание №1:\n 1. Выпей стакан воды.\n 2. Сделай зарядку.\n 3. Умойся.\n 4. Заправь кровать.\n 5. Оденься и иди завтракать.",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task1_done", "task1_not_done"])
def handle_task1_response(call):
    if call.data == "task1_done":
        response = "Отличная работа! Ты заработала еще 25 баллов!"
    elif call.data == "task1_not_done":
        response = "Не переживай, в следующий раз все успеешь!"

    # Отправляем новое сообщение с ответом на задание №1
    bot.send_message(call.message.chat.id, response)

    # Создаем клавиатуру для задания №2
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Готово", callback_data="task2_done")
    button2 = types.InlineKeyboardButton("Не ходила", callback_data="task2_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №2
    bot.send_message(call.message.chat.id, "Задание №2:\nЗанятие хореографией в театре \"Фуете\".", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task2_done", "task2_not_done"])
def handle_task2_response(call):
    if call.data == "task2_done":
        response = "Молодец! Ты получила еще 10 баллов!"
    elif call.data == "task2_not_done":
        response = "Вероятно ты плохо себя чувствуешь. Поправляйся!"

    # Отправляем новое сообщение с ответом на задание №2
    bot.send_message(call.message.chat.id, response)

    # Создаем клавиатуру для задания №3
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Готово", callback_data="task3_done")
    button2 = types.InlineKeyboardButton("Не ходила", callback_data="task3_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №3
    bot.send_message(call.message.chat.id,
                     "Задание №3:\n 1. Переодевайся в школьную форму.\n 2. Иди обедать.\n 3. Урок по Английскому.",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task3_done", "task3_not_done"])
def handle_task3_response(call):
    if call.data == "task3_done":
        response = "Отлично! Ты заработала еще 15 баллов!"
    elif call.data == "task3_not_done":
        response = "Надеюсь, ты разберешь новый материал самостоятельно и сможешь выполнить домашнее задание."

    # Отправляем новое сообщение с ответом на задание №3
    bot.send_message(call.message.chat.id, response)

    # Создаем клавиатуру для задания №4
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Выполнено", callback_data="task4_done")
    button2 = types.InlineKeyboardButton("Не ходила", callback_data="task4_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №4
    bot.send_message(call.message.chat.id,
                     "Задание №4:\nА теперь тебя ждут уроки в школе.",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task4_done", "task4_not_done"])
def handle_task4_response(call):
    if call.data == "task4_done":
        bot.send_message(call.message.chat.id, "Отлично! Сколько оценок \"5\" и \"4\" ты получила? (введи значения через пробел)")
        bot.register_next_step_handler(call.message, handle_grades_input)
    elif call.data == "task4_not_done":
        response = "Тогда попроси у одноклассников фото классных работ, чтобы лучше усвоить материал уроков."
        bot.send_message(call.message.chat.id, response)

        # Переходим к заданию №5 сразу после сообщения
        send_task5_message(call.message.chat.id)

# Обработка ввода количества оценок
def handle_grades_input(message):
    try:
        # Разделяем ввод пользователя по пробелам
        grades = message.text.split()
        fives = int(grades[0])
        fours = int(grades[1])

        # Вычисляем итоговые баллы
        if fives == 0 and fours == 0:
            total_points = 30  # Начисляем 30 баллов, если нет пятёрок и четвёрок
        else:
            total_points = fives * 50 + fours * 40

        # Отправляем сообщение с итоговыми баллами
        bot.send_message(message.chat.id, f"Ты заработала еще {total_points} баллов!")
    except (IndexError, ValueError):
        # Если ввод некорректен, отправляем сообщение об ошибке и просим повторить попытку
        bot.send_message(message.chat.id, "Пожалуйста, введи два числа, разделенных пробелом (например, '3 2').")
        bot.register_next_step_handler(message, handle_grades_input)
        return

    # Переходим к заданию №5
    send_task5_message(message.chat.id)

def send_task5_message(chat_id):
    # Создаем клавиатуру для задания №5
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Спасибо!", callback_data="task5_done")
    button2 = types.InlineKeyboardButton("Не хочу ужинать.", callback_data="task5_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №5
    bot.send_message(chat_id, "Задание 5:\n 1. Прогулка.\n 2. Наряжайся к ужину.\n 3. Семейный ужин.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task5_done", "task5_not_done"])
def handle_task5_response(call):
    if call.data == "task5_done":
        response = "На здоровье, котенок! Ты заработала еще 15 баллов!"
    elif call.data == "task5_not_done":
        response = "Съешь конфетку!."

    # Отправляем сообщение с ответом на задание №5
    bot.send_message(call.message.chat.id, response)

    # Переходим к заданию №6
    send_task6_message(call.message.chat.id)

def send_task6_message(chat_id):
    # Создаем клавиатуру для задания №6
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Готово", callback_data="task6_done")
    button2 = types.InlineKeyboardButton("А можно завтра закончить", callback_data="task6_not_done")
    markup.add(button1, button2)

    # Отправляем сообщение с заданием №6
    bot.send_message(chat_id, "Задание №6:\n1. Уроки.\n2. Занятие музыкой.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task6_done", "task6_not_done"])
def handle_task6_response(call):
    if call.data == "task6_done":
        response = "Молодец! Ты заработала еще 20 баллов."
    elif call.data == "task6_not_done":
        response = "Давай, я помогу тебе."

    # Отправляем сообщение с ответом на задание №6
    bot.send_message(call.message.chat.id, response)

    # Переходим к заданию №7
    send_task7_message(call.message.chat.id)

def send_task7_message(chat_id):
        # Создаем клавиатуру для задания №7
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Спокойной ночи!", callback_data="task7_done")
        button2 = types.InlineKeyboardButton("Я хочу еще почитать.", callback_data="task7_not_done")
        markup.add(button1, button2)

        # Отправляем сообщение с заданием №7
        bot.send_message(chat_id, "Задание №7:\n1. Прими душ.\n2. Почитай книгу.\n3. Ложись спать в 22:00.",
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["task7_done", "task7_not_done"])
def handle_task7_response(call):
        if call.data == "task7_done":
            response = "Ты заработала еще 15 баллов. Спокойной ночи!"
        elif call.data == "task7_not_done":
            response = "Спокойной ночи."

        # Отправляем сообщение с ответом на задание №7
        bot.send_message(call.message.chat.id, response)

        # Переходим к финальному сообщению или завершаем день
        send_final_message(call.message.chat.id)

def send_final_message(chat_id):
    # Финальное сообщение
    bot.send_message(chat_id,
                             "Вот и закончился твой день! Надеюсь, ты отлично провела время и заработала много баллов! До завтра!")


# Запуск бота
bot.polling(none_stop=True)