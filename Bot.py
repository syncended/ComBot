import os
import cv2
import time
import ctypes
import Config
import telebot
import logging
import subprocess
from telebot import apihelper
from telebot import types
from functools import wraps
from Process import kill, get_processes
from desktopmagic.screengrab_win32 import getScreenAsImage

# Init logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Setting
apihelper.proxy = {'https': Config.__PROXY__}
bot = telebot.TeleBot(Config.__TOKEN__)

cmd_status = False
process_select = False

# Init folders
try:
    os.mkdir("res")
except IOError:
    # Nothing
    print()

# Create default keyboard
keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
keyboard.add(
    types.KeyboardButton('/webcam'),
    types.KeyboardButton('/screen'),
    types.KeyboardButton('/process'),
    types.KeyboardButton('/cmd'),
    types.KeyboardButton('/system')
)

# Create
system_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
system_keyboard.add(
    types.KeyboardButton('/shutdown'),
    types.KeyboardButton('/lock'),
    types.KeyboardButton('/home')
)


# White list checking
def in_white_list(func):
    @wraps(func)
    def decorator(message):
        logger.info(message)
        if message.from_user.id in Config.__WHITE_LIST__:
            return func(message)

    return decorator


@bot.message_handler(commands=['kb', 'keyboard'])
@in_white_list
def open_keyboard(message):
    bot.send_message(message.chat.id, 'Keyboard open', reply_markup=keyboard)


@bot.message_handler(commands=['cmd'])
@in_white_list
def cmd_command(message):
    bot.send_message(message.chat.id, 'Console mode started, send <exit> to disable it')
    global cmd_status
    cmd_status = True


@bot.message_handler(commands=['process'])
@in_white_list
def process_command(message):
    processes = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    proc_list = get_processes()
    for proc in proc_list:
        item = types.KeyboardButton(proc)
        processes.row(item)

    item = types.KeyboardButton("/home")
    processes.row(item)
    bot.send_message(message.chat.id, 'Select process to kill', reply_markup=processes)
    global process_select
    process_select = True


@bot.message_handler(commands=['home'])
@in_white_list
def home(message):
    bot.send_message(message.chat.id, 'Return to main keyboard', reply_markup=keyboard)
    global process_select
    process_select = False


@bot.message_handler(commands=['system'])
@in_white_list
def system_command(message):
    bot.send_message(message.chat.id, 'System commands opened', reply_markup=system_keyboard)
    global cmd_status
    cmd_status = True


@bot.message_handler(commands=['shutdown'])
@in_white_list
def cmd_command(message):
    bot.send_message(message.chat.id, 'Shutting down', reply_markup=keyboard)
    os.system("shutdown /s /t 1")


@bot.message_handler(commands=['lock'])
@in_white_list
def cmd_command(message):
    bot.send_message(message.chat.id, 'PC locked', reply_markup=keyboard)
    user32 = ctypes.cdll.LoadLibrary("user32.dll")
    user32.LockWorkStation()


@bot.message_handler(commands=['screen'])
@in_white_list
def take_screenshot(message):
    file_name = 'res/' + time.time().__str__() + '.png'
    screen = getScreenAsImage()
    screen.save(file_name, format='png')
    photo = open(file_name, 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()


@bot.message_handler(commands=['webcam'])
@in_white_list
def take_screenshot(message):
    cam = cv2.VideoCapture(0)
    ret_val, frame = cam.read()
    file_name = 'res/' + time.time().__str__() + '.png'
    cv2.imwrite(file_name, img=frame)
    photo = open(file_name, 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True)
@in_white_list
def default_message(message):
    global cmd_status, process_select
    if cmd_status:
        if message.text == '<exit>':
            cmd_status = False
            bot.send_message(message.chat.id, 'Cmd mode disabled')
            return
        else:
            output = subprocess.Popen(message.text, stdout=subprocess.PIPE, shell=True)
            (result, err) = output.communicate()
            try:
                text = result.decode('cp866')
                bot.send_message(message.chat.id, text)
            except:
                bot.send_message(message.chat.id, 'Probably command is wrong')
    elif process_select:
        kill(message.text)
        process_select = False
        bot.send_message(message.chat.id, 'Process killed', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Unsupported command')


bot.polling()
