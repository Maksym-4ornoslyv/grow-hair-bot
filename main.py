import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
from telebot import types
import random
import time
import socket
import sys

def check_internet():
    try:
        # Перевіряємо доступність серверу google.com за допомогою порту 80
        socket.create_connection(("www.google.com", 80), timeout=1)
        return True
    except socket.error:
        return False

if check_internet():
    print("Інтернет-з'єднання є")
else:
    print("Інтернет-з'єднання відсутнє")

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['hair'])
def start_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username
    current_time = int(time.time())

    scores_dict = read_scores_from_file()

    if user_id in scores_dict and current_time - scores_dict[user_id]["last_play_time"] < 86400:
        # Executes if the user played less than 24 hours ago
        bot.reply_to(message, f"Ти вже грав\n \n У тебе {scores_dict[user_id]['score']} сантиметрів волосся")
    else:
        # Executes if the user can play
        score = random.randint(-20, 20)
        if user_id in scores_dict:
            scores_dict[user_id]["score"] += score
            scores_dict[user_id]["last_play_time"] = current_time
        else:
            scores_dict[user_id] = {"username": username, "score": score, "last_play_time": current_time}

        write_scores_to_file(scores_dict)

        if score < 0:
            bot.reply_to(message, f"У тебе відрізали {abs(score)} сантиметрів волосся\n \n Тепер у тебе {scores_dict[user_id]['score']} сантиметрів")
        elif score > 0:
            bot.reply_to(message, f"У тебе вирісло {score} сантиметрів волосся\n \n Тепер у тебе {scores_dict[user_id]['score']} сантиметрів")
        else:
            bot.reply_to(message, f"В тебе виросло 0 сантиметрів\n \n У тебе залишилось {scores_dict[user_id]['score']} сантиметрів")



@bot.message_handler(commands=['toph', 'tophair'])
def top_handler(message):
    scores_dict = read_scores_from_file()
    top_list = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)[:10]

    top_message = "Топ-10 гравців:\n \n"
    for i, player in enumerate(top_list):
        top_message += f"{i + 1}. {player['username']}: {player['score']} сантиметрів\n \n"

    bot.reply_to(message, top_message)


def read_scores_from_file():
    scores_dict = {}
    with open('scores.txt', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            user_id = int(data[0])
            username = data[1]
            score = int(data[2])
            last_play_time = int(data[3])
            scores_dict[user_id] = {"username": username, "score": score, "last_play_time": last_play_time}
    return scores_dict


def write_scores_to_file(scores_dict):
    with open('scores.txt', 'w') as f:
        for user_id, data in scores_dict.items():
            f.write(f"{user_id},{data['username']},{data['score']},{data['last_play_time']}\n")

@bot.message_handler(commands=['helph', 'helphair'])
def help_handler(message):
    bot.reply_to(message, "👋 @grow_hair_bot  -  бот, за допомогою якого ви можете ростити своє волосся на ногах і підніматися сходинками топу.\n \n 💻Цей бот був розроблений  @Ya_devat_let_dombyl_bambas \n \n 🦵Для того щоб ростити волосся на ногах пропишіть команду /hair і ваше волосся збільшиться або зменшиться на певну кількість сантиметрів. Ростити волосся можна один раз на добу. \n \n 🥇Щоб подивитися топ гравців вашого чату, пропишіть /toph або /tophair \n \n Сподіваюся ця інформація була корисна для вас.👍")

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("Polling failed:", e)
        time.sleep(5)
        continue
