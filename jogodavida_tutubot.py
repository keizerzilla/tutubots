import os
from parse import parse
from telebot import TeleBot
from configparser import ConfigParser
from superlib.cellular_automaton import CellularAutomaton

config = ConfigParser()
config.read("bots.ini")

API_TOKEN = config["KEYS"]["JOGODAVIDA"]
IMG_FOLDER = config["FOLDERS"]["VIDA_IMG_OUTPUT"]

os.makedirs(IMG_FOLDER, exist_ok=True)

bot = TeleBot(API_TOKEN)
welcome_message = open("jogodavida_tutubot.txt").read()


@bot.message_handler(commands=["help", "start", "ajuda", "iniciar"])
def send_help(message):
    bot.reply_to(message, welcome_message)


@bot.message_handler(func=lambda message : "geradorvida" in message.text)
def life_command(message):
    params = message.text.split(" ")
    
    if len(params) != 3:
        bot.reply_to(message, f"O comando '{message.text}' foi mal formatado. Use a /ajuda para saber como eu funciono.")
        return
    
    command = params[0].lower()
    rule = params[1].lower()
    iters = int(params[2].lower())
    
    if "b" not in rule or "s" not in rule or iters < 1 or iters > 8:
        bot.reply_to(message, f"O comando '{message.text}' possui parâmetros mal formatados. Use a /ajuda para saber como eu funciono.")
        return
    
    bsp = parse("b{birth}s{survival}", rule).named
    b = [int(x) for x in list(bsp["birth"])]
    s = [int(x) for x in list(bsp["survival"])]
    file_img = f"vida/generic_{message.id}_{message.chat.id}.bmp"
    
    auto = CellularAutomaton()
    auto.generate(birth=b, survival=s, steps=iters)
    auto.draw(file_img, width=256, height=256)
    
    bot.send_photo(chat_id=message.chat.id, photo=open(file_img, "rb"), reply_to_message_id=message.id)


@bot.message_handler(commands=["caverna", "cavern"])
def cavern_command(message):
    b = [5, 6, 7, 8]
    s = [4, 5, 6, 7, 8]
    file_img = f"vida/cavern_{message.id}_{message.chat.id}.bmp"
    
    auto = CellularAutomaton()
    auto.generate(birth=b, survival=s, steps=8)
    auto.draw(file_img, width=256, height=256)
    
    bot.send_photo(chat_id=message.chat.id, photo=open(file_img, "rb"), reply_to_message_id=message.id)


@bot.message_handler(commands=["labirinto", "maze"])
def maze_command(message):
    b = [3]
    s = [1, 2, 3, 4, 5]
    file_img = f"{IMG_FOLDER}/maze_{message.id}_{message.chat.id}.bmp"
    
    auto = CellularAutomaton()
    auto.generate(birth=b, survival=s, steps=8)
    auto.draw(file_img, width=256, height=256)
    
    bot.send_photo(chat_id=message.chat.id, photo=open(file_img, "rb"), reply_to_message_id=message.id)


bot.infinity_polling()

