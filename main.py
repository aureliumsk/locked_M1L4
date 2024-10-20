import telebot
from telebot.types import Message
from config import token

from random import choices
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message: Message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        type = choices((Pokemon, Wizard, Fighter), weights=(2, 1, 1))[0]

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
    


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для игры в покемонов, скорее попробуй создать себе покемона, нажимай - /go")


bot.infinity_polling(none_stop=True)

