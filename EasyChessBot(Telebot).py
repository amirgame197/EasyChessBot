#This one is some old ass not working typa shit i've been on, Ignore for your own sanity.

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import apihelper
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot("7191127389:AAE9Ot7ZM8GZ0wRe52dFU__tySF8KTnkYVc") # I dont even remember this token lol

apihelper.proxy = {
    'http': 'socks5h://127.0.0.1:10808',
    'https': 'socks5h://127.0.0.1:10808'
}
apihelper.SESSION_TIME_TO_LIVE = 60 * 5

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("♜", callback_data="1"),
        InlineKeyboardButton("♞", callback_data="2"),
        InlineKeyboardButton("♝", callback_data="3"),
        InlineKeyboardButton("♚", callback_data="4"),
        InlineKeyboardButton("♛", callback_data="5"),
        InlineKeyboardButton("♝", callback_data="6"),
        InlineKeyboardButton("♞", callback_data="7"),
        InlineKeyboardButton("♜", callback_data="8")
    )
    keyboard.row(
        InlineKeyboardButton("♟", callback_data="9"),
        InlineKeyboardButton("♟", callback_data="10"),
        InlineKeyboardButton("♟", callback_data="11"),
        InlineKeyboardButton("♟", callback_data="12"),
        InlineKeyboardButton("♟", callback_data="13"),
        InlineKeyboardButton("♟", callback_data="14"),
        InlineKeyboardButton("♟", callback_data="15"),
        InlineKeyboardButton("♟", callback_data="16")
    )
    keyboard.row(
        InlineKeyboardButton("🏻", callback_data="17"),
        InlineKeyboardButton("🏻", callback_data="18"),
        InlineKeyboardButton("🏻", callback_data="19"),
        InlineKeyboardButton("🏻", callback_data="20"),
        InlineKeyboardButton("🏻", callback_data="21"),
        InlineKeyboardButton("🏻", callback_data="22"),
        InlineKeyboardButton("🏻", callback_data="23"),
        InlineKeyboardButton("🏻", callback_data="24")
    )
    keyboard.row(
        InlineKeyboardButton("🏻", callback_data="25"),
        InlineKeyboardButton("🏻", callback_data="26"),
        InlineKeyboardButton("🏻", callback_data="27"),
        InlineKeyboardButton("🏻", callback_data="28"),
        InlineKeyboardButton("🏻", callback_data="29"),
        InlineKeyboardButton("🏻", callback_data="30"),
        InlineKeyboardButton("🏻", callback_data="31"),
        InlineKeyboardButton("🏻", callback_data="32")
    )
    keyboard.row(
        InlineKeyboardButton("🏻", callback_data="33"),
        InlineKeyboardButton("🏻", callback_data="34"),
        InlineKeyboardButton("🏻", callback_data="35"),
        InlineKeyboardButton("🏻", callback_data="36"),
        InlineKeyboardButton("🏻", callback_data="37"),
        InlineKeyboardButton("🏻", callback_data="38"),
        InlineKeyboardButton("🏻", callback_data="39"),
        InlineKeyboardButton("🏻", callback_data="40")
    )
    keyboard.row(
        InlineKeyboardButton("🏻", callback_data="41"),
        InlineKeyboardButton("🏻", callback_data="42"),
        InlineKeyboardButton("🏻", callback_data="43"),
        InlineKeyboardButton("🏻", callback_data="44"),
        InlineKeyboardButton("🏻", callback_data="45"),
        InlineKeyboardButton("🏻", callback_data="46"),
        InlineKeyboardButton("🏻", callback_data="47"),
        InlineKeyboardButton("🏻", callback_data="48")
    )
    keyboard.row(
        InlineKeyboardButton("♙", callback_data="49"),
        InlineKeyboardButton("♙", callback_data="50"),
        InlineKeyboardButton("♙", callback_data="51"),
        InlineKeyboardButton("♙", callback_data="52"),
        InlineKeyboardButton("♙", callback_data="53"),
        InlineKeyboardButton("♙", callback_data="54"),
        InlineKeyboardButton("♙", callback_data="55"),
        InlineKeyboardButton("♙", callback_data="56")
    )
    keyboard.row(
        InlineKeyboardButton("♖", callback_data="57"),
        InlineKeyboardButton("♘", callback_data="58"),
        InlineKeyboardButton("♗", callback_data="59"),
        InlineKeyboardButton("♔", callback_data="60"),
        InlineKeyboardButton("♕", callback_data="61"),
        InlineKeyboardButton("♗", callback_data="62"),
        InlineKeyboardButton("♘", callback_data="63"),
        InlineKeyboardButton("♖", callback_data="64")
    )
    bot.send_message(message.chat.id, "Choose a piece:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, text="Selected option: {}".format(call.data))

bot.infinity_polling(timeout=90, long_polling_timeout=30)
