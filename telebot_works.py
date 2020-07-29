import requests

import telebot
import bot_commands as dvch

bot = telebot.TeleBot('token')

board_ = ''
word_ = ''
post = []
rand_post = []


@bot.message_handler(commands=['start'])
def greet_start(message):
    bot.send_message(message.from_user.id, "Sample text")
    bot.register_next_step_handler(message, greetings)


@bot.message_handler(content_types=['text'])
def greetings(message):
    bot.send_message(message.from_user.id, "Напиши название доски")
    bot.register_next_step_handler(message, get_board)


def get_board(message):
    board = message.text
    board = board.lower()
    bot.send_message(message.from_user.id, 'Какое слово ищем??')
    bot.register_next_step_handler(message, get_word, board)


def get_word(message, board):
    global post
    global rand_post
    word = message.text
    bot.send_message(message.from_user.id, 'Процессинг......')
    bot.send_message(message.from_user.id, 'Ищем слово ' + word + ' на доске ' + board)
    post = dvch.post_with_word(board, word)
    get_random_post = str(dvch.random_posts(post).replace('&quot;', '*').replace('&gt;', '>'))
    print(len(post))
    if post == 'Нет такой доски' or post == 'Нет такого слова':
        bot.send_message(message.from_user.id, post)
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text='Новую выборку?', callback_data='new_one'))
        bot.send_message(message.chat.id, 'Что делаем дальше?', reply_markup=keyboard)
    else:
        rand_post = get_random_post.replace('&quot;', '*').replace('&gt;', '>')
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text='Ещё пост?', callback_data='one_more'),
            telebot.types.InlineKeyboardButton(text='Новую выборку?', callback_data='new_one'),
            telebot.types.InlineKeyboardButton(text='ПОРФИРЬЕВИЧ?', callback_data='porf'))
        bot.send_message(message.from_user.id, get_random_post, reply_markup=keyboard)
    post = list(post)
    post = dvch.remove_posted(post, get_random_post)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    global rand_post
    global post
    if call.data == 'one_more':
        print(len(post))
        print(post)
        if len(post) < 1:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(text='Новая выборка', callback_data='new_one'))
            bot.send_message(call.message.chat.id, 'Посты с данным словом кончились', reply_markup=keyboard)
        elif len(post) >= 1:
            raw_post = dvch.random_posts(post)
            rand_post = str(raw_post).replace('&quot;', '*').replace('&gt;', '>')
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(text='Ещё пост?', callback_data='one_more'),
                telebot.types.InlineKeyboardButton(text='Новую выборку?', callback_data='new_one'),
                telebot.types.InlineKeyboardButton(text='ПОРФИРЬЕВИЧ?', callback_data='porf'))
            bot.send_message(call.message.chat.id, rand_post, reply_markup=keyboard)
            post = dvch.remove_posted(post, raw_post)
    if call.data == 'new_one':
        bot.send_message(call.message.chat.id, "Напиши название доски")
        bot.register_next_step_handler(call.message, get_board)
    if call.data == 'porf':
        rand_post = dvch.post_to_porfirevich(rand_post)
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text='Ещё пост?', callback_data='one_more'),
            telebot.types.InlineKeyboardButton(text='Новую выборку?', callback_data='new_one'),
            telebot.types.InlineKeyboardButton(text='ПОРФИРЬЕВИЧ ЕЩЁ7?7?', callback_data='porf'))
        bot.send_message(call.message.chat.id, rand_post, reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)
