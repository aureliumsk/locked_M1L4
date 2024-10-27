import telebot
from telebot.types import Message
from config import token

from random import choices
from logic import Pokemon, Wizard, Fighter
from time import time

bot = telebot.TeleBot(token, threaded=False) 

@bot.message_handler(commands=['go'])
def go(message: Message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        type = choices((Pokemon, Wizard, Fighter), weights=(4.0, 1.0, 1.0))[0]

        pokemon = type(message.from_user.username)
        
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack(message: Message):
    if message.reply_to_message is None:
        bot.reply_to(message, "Необходимо ответить на сообщение противника!")
        return
    owner_pokemon = Pokemon.pokemons.get(message.from_user.username, None)
    enemy_pokemon = Pokemon.pokemons.get(message.reply_to_message.from_user.username, None)
    if owner_pokemon is None:
        bot.reply_to(message, "У вас нет покемона!")
        return
    if enemy_pokemon is None:
        bot.reply_to(message, "У противника нет покемона!")
        return
    bot.reply_to(message, owner_pokemon.attack(enemy_pokemon))
    

recharges = {}

@bot.message_handler(commands=['rest'])
def rest(message: Message):
    owner_pokemon = Pokemon.pokemons.get(message.from_user.username, None)
    if owner_pokemon.hp == owner_pokemon.max_hp:
        bot.reply_to(message, f"Ваш покемон полностью здоров!")
        return
    recharge_time = recharges.get(owner_pokemon, 0)
    current_time = time()
    if recharge_time > current_time:
        bot.reply_to(message, f"Подождите ещё {recharge_time - current_time:.2f} секунд!")
        return
    if owner_pokemon is None:
        bot.reply_to(message, "У вас нет покемона!")
        return
    owner_pokemon.hp = owner_pokemon.max_hp
    recharges[owner_pokemon] = current_time + 30.0
    bot.reply_to(message, "Жизни вашего покемона были восстановлены!")


@bot.message_handler(commands=['info'])
def info(message: Message):
    owner_pokemon = Pokemon.pokemons.get(message.from_user.username, None)
    if owner_pokemon is None:
        bot.reply_to(message, "У вас нет покемона!")
        return
    bot.send_message(message.chat.id, owner_pokemon.info())

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для игры в покемонов, скорее попробуй создать себе покемона, нажимай - /go")


bot.infinity_polling()

