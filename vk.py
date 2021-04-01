import vk_api
import json
import vk
from vk_api import keyboard
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
#from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

import sqlite3
import csv
from static_info import *

vk_session = vk_api.VkApi(token = vk_token)
longpoll = VkLongPoll(vk_session)


def gen_keyboard_button(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color.lower()}"
            }

def generate_keyboard(*buttons):
    keyboard = {
    "one_time" : True,
    "buttons" : [
        ]
    }
    for value in buttons:
        keyboard['buttons'].append(value)
    keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def generate_db():
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (fullname TEXT, choices TEXT, successfull BOOL, webpage TEXT)''')
    con.commit()
    con.close()

def generate_csv(name):
    with open(name,'wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\n')
    return csv_writer

def add_note_to_db(user_data):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.executemany('INSERT INTO users VALUES (?,?,?,?)', user_data)
    con.commit()
    con.close()
    

def write_message(sender, message, key=None):
    vk_session.method('messages.send', {'user_id' : sender, 'message': message, 'random_id' : get_random_id(), 'keyboard' : key})

def get_user_info(user_id):
    return vk_session.method('users.get', {'user_ids': user_id})
# def generate_final(info):
#     info1 = info
# #    if info[0] == ans2[0] and info[1] == ans3[0]:
#     if info[3] == ans4[0]:
#         return '{}, {}'.format(final[1],final[3])
#     if info[3] == ans4[1]:
#         return '{}, {}'.format(final[3],final[4])    
#     if info[3] == ans4[2]:
#         return '{}, {}'.format(final[3],final[5])
#     if info[3] == ans4[3]:
#         return '{}, {}'.format(final[3],final[8])

def main():
    №generate_db()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            received_message = event.text
            sender = event.user_id
            if received_message == 'Начать':
                keyboard = generate_keyboard(
                    [gen_keyboard_button(ans1[0], 'PRIMARY'), gen_keyboard_button(ans1[1], 'PRIMARY')],
                    [gen_keyboard_button(ans1[2], 'PRIMARY')]
                    )
                #//////////////////// говнокод
                user_get=get_user_info(sender)
                user_get=user_get[0]
                first_name=user_get['first_name']
                last_name=user_get['last_name']
                full_name=first_name+" "+last_name
                write_message(sender, q1, keyboard)
            #    data = {sender : []}
                with open("users.csv", mode="a", encoding='utf-8') as w_file:
                    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
                    file_writer.writerow([full_name,"1111","True"])
                #//////////////////// говнокод конец

            elif received_message in ans1.values():
                keyboard = generate_keyboard(
                    [gen_keyboard_button(ans2[0], 'PRIMARY'), gen_keyboard_button(ans2[1], 'PRIMARY')],
                    [gen_keyboard_button(ans2[2], 'PRIMARY')]
                    )
                write_message(sender, q2, keyboard)
                #data[sender].append(received_message)
            elif received_message in ans2.values():
                keyboard = generate_keyboard(
                    [gen_keyboard_button(ans3[0], 'PRIMARY'), gen_keyboard_button(ans3[1], 'PRIMARY')],
                    [gen_keyboard_button(ans3[2], 'PRIMARY')]
                    )
                write_message(sender, q3, keyboard)
                #data[sender].append(received_message)
            elif received_message in ans3.values():
                keyboard = generate_keyboard(
                    [gen_keyboard_button(ans4[0], 'PRIMARY'), gen_keyboard_button(ans4[1], 'PRIMARY')],
                    [gen_keyboard_button(ans4[2], 'PRIMARY'), gen_keyboard_button(ans4[3], 'PRIMARY')]
                    )
                write_message(sender, q4, keyboard)
                #data[sender].append(received_message) 
            elif received_message in ans4.values():
                keyboard = generate_keyboard(
                    [gen_keyboard_button(ans4[0], 'PRIMARY'), gen_keyboard_button(ans4[1], 'PRIMARY')],
                    [gen_keyboard_button(ans4[2], 'PRIMARY'), gen_keyboard_button(ans4[3], 'PRIMARY')]
                    )
                # data[sender].append(received_message) 
                # write_message(sender, q5)
                # final = generate_final(data[sender])
                write_message(sender, "Молодец возьми с полки пирожок")
                #csv.writerow("{},{},{},{}".format(str(sender),"1111","True",str(sender)))
            else:
                write_message(sender, "Удачной дороги, спортсмен")


if __name__ == "__main__":
    main()