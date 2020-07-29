import requests
import os
import time
import random
import telebot
import json
import re
from termcolor import colored


def cleanhtml(raw_html):
    import re
    recompile = re.compile('<br>')
    qwe = re.sub(recompile, '\n', raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', qwe)
    return cleantext


def rand_post_from_board(board):
    response = requests.get('https://2ch.hk/' + board + '/threads.json')
    resp_json = response.json()
    board_dict = resp_json.get("threads")
    threads_on_page = []
    for i in range(10):
        threads_on_page.append(board_dict[i])
    for i in range(10):
        print('Название треда: ', threads_on_page[i].get('subject'), threads_on_page[i].get('num'), '№: ', i)

    number = int(input('Какой тред открыть? ', ))
    thread = 'https://2ch.hk/' + board + '/res/' + threads_on_page[number].get('num') + '.json'
    print(thread)
    responce_thread = requests.get(thread)  # выгружаем json самого треда
    responce_thread_json = responce_thread.json()
    thread_dict = responce_thread_json.get('threads')  # добываем из словаря всё, что связано с threads
    posts = thread_dict[0].get('posts')  # т.к без индекса эта штука считается list, добавляем индекс и это уже словарь
    # и из этого словаря уже вытаскиваем всё с ключём posts
    print('количество постов: ', len(posts))
    comments = posts[random.randint(0, len(posts) - 1)].get(
        'comment')  # считаем кол-во комментов - 1, т.к нумерация с 0
   # cleaning_the_post = cleanhtml(comments)  # очищаем пост от html-гадости
    print('Длина поста:', len((cleanhtml(comments))))
    if len(cleanhtml(comments)) <= len(threads_on_page[number].get('num')):  # проверяем, есть ли в посте слова
        print('Пост пустой или с картинкой')
    else:
        print('Случайный пост:', cleanhtml(comments))


def post_with_word(board, word):  # получаем список постов с заданным словом на заданной доске в виде массива
    # from termcolor import colored
    board_list = ['mo', 'mo', 'moba', 'mobi', 'mov', 'mu', 'mus', 'ne', 'news', 'nvr', 'o', 'obr', 'old', 'out', 'p',
                  'pa', 'ph', 'po', 'pok', 'pr', 'psy', 'pvc', 'qtr4', 'r', 'r34', 'ra', 're',
                  'rf', 'rm', 'ro', 'ruvn', 's', 'sad', 'sci', 'se', 'sex', 'sf', 'smo', 'sn', 'soc', 'socionics', 'sp',
                  'spc', 'srv', 'sw', 't', 'td', 'tes', 'to', 'tr', 'trv', 'tv', 'ukr', 'un', 'ussr', 'v',
                  'vape', 'vg', 'vn', 'vr', 'w', 'web', 'wh', 'whn', 'who', 'wm', 'wow', 'wp', 'wr', 'wrk', 'wwe', 'ya',
                  'zog', 'b']
    if board not in board_list:
        return str('Нет такой доски')
    comment_pull = []
    response = requests.get('https://2ch.hk/' + board + '/threads.json')
    resp_json = response.json()
    board_dict = resp_json.get("threads")
    threads_on_page = []
    for i in range(20): # 20 - просто выборка, если что можно поменять
        threads_on_page.append(board_dict[i])
    for i in range(20):
        thread = 'https://2ch.hk/' + board + '/res/' + threads_on_page[i].get('num') + '.json'
        responce_thread = requests.get(thread)
        responce_thread_json = responce_thread.json()
        thread_dict = responce_thread_json.get('threads')
        posts = thread_dict[0].get('posts')
        for j in range(len(posts)):
            comments = posts[j].get('comment')
            cleaning_the_post = cleanhtml(comments)
            # cleaning_the_post = re.sub(word, colored(word, 'red'), cleaning_the_post)
            if word in cleaning_the_post:
                comment_pull.append(cleaning_the_post)
            else:
                continue
    if len(comment_pull) == 0:
        return str('Нет такого слова')
    else:
        to_return = comment_pull
        return to_return  # получили массив постов с заданным словом


def ret_string(list_):  # абсолюно все посты с заданным словом в виде одной строки
    returned_list = list_
    empty = ''
    list_to_string = []
    for i in range(len(returned_list)):
        returned_list[i] = returned_list[i].replace('&quot;', '*')
        returned_list[i] = returned_list[i].replace('&gt;', '>')
        list_to_string.append(returned_list[i] + '\n')
        list_to_string.append('\n' + '____________________' + '\n')
    empty = empty.join(list_to_string)
    return empty


def random_posts(list_):  # рандомный пост с заданным словом
    returned_list = list_
    # returned_list = returned_list.replace('&quot;', '*')
    # returned_list = returned_list.replace('&gt;', '>')
    return returned_list[random.randint(0, len(returned_list) - 1)]


def remove_posted(list_, post):
    index_ = list_.index(post)
    list_.pop(index_)
    return list_


def post_to_porfirevich(input_post):
    response = requests.post("https://models.dobro.ai/gpt2/medium/",
                             data=json.dumps({'prompt': input_post, "length": '40'}))
    response_json = response.json()
    response_result = response_json.get('replies')
    return input_post + response_result[random.randint(0, 2)]
