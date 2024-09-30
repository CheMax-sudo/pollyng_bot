import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


authorization = InlineKeyboardButton(text='🔆 Ответить на вопросы 🔆', callback_data='authorization')
keyboard = InlineKeyboardMarkup(inline_keyboard=[[authorization]])

statistics = InlineKeyboardButton(text='🔆 Статистика 🔆', callback_data='statistics')
keyboardSt = InlineKeyboardMarkup(inline_keyboard=[[statistics]])


# Кнопки answer_options
answer_age = [
               [InlineKeyboardButton(text='Младше 23', callback_data='answer1')],
               [InlineKeyboardButton(text='23 или Старше', callback_data='answer2')]
               ]
keyboard2 = InlineKeyboardMarkup(inline_keyboard=answer_age)


answer_question2 = [[InlineKeyboardButton(text='Всё устраивает', callback_data='answer3')]]
keyboard3 = InlineKeyboardMarkup(inline_keyboard=answer_question2)


answer_question3 = [
               [InlineKeyboardButton(text='Да', callback_data='answer5')],
               [InlineKeyboardButton(text='Нет', callback_data='answer6')]
               ]
keyboard4 = InlineKeyboardMarkup(inline_keyboard=answer_question3)


answer_question4 = [
               [InlineKeyboardButton(text='Да', callback_data='answer7')],
               [InlineKeyboardButton(text='Нет', callback_data='answer8')]
               ]
keyboard5 = InlineKeyboardMarkup(inline_keyboard=answer_question4)


answer_question5 = [
               [InlineKeyboardButton(text='Да', callback_data='answer9')],
               [InlineKeyboardButton(text='Нет', callback_data='answer10')],
               [InlineKeyboardButton(text='Не хочу, но боюсь отказаться и потерять в деньгах', callback_data='answer11')]
               ]
keyboard6 = InlineKeyboardMarkup(inline_keyboard=answer_question5)

