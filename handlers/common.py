import sqlite3
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keybords import keybord as kb
from database.requests import set_user, update_user


router = Router()


def user_has_access(user_id):
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    # Проверка, есть ли ID пользователя в базе данных
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result is not None


class Reg(StatesGroup):
    tg_name = State()
    age = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()


@router.message(Command('test'))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.chat.first_name
    await message.answer(f'{user_id}, {name}')


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.chat.first_name
    if user_has_access(user_id):
        await message.answer(f'Привет, {name}. Если хотите посмотреть статистику по группе?\nНажмите кнопку ниже.', reply_markup=kb.keyboardSt)
    else:
        await set_user(message.from_user.id)
        await message.answer(f'Привет {name}. Я провожу анонимный опрос студентов!\n'
                                   'Поделись своим мнением. Ответь на 5 вопросов и ты увидишь сколько нас '
                                   'и что мы думаем о том как здесь учат.', reply_markup=kb.keyboard)


@router.callback_query(F.data == 'statistics')
async def stati(call: CallbackQuery):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE age == 23;""")
    rows = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE age == 20;""")
    rows2 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question2 == 'Устраивает';""")
    rows3 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question2 != 'Устраивает';""")
    rows4 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question3 == 'Да';""")
    rows5 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question3 == 'Нет';""")
    rows6 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question4 == 'Да';""")
    rows7 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question4 == 'Нет';""")
    rows8 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question5 == 'Да';""")
    rows9 = cursor.fetchall()
    cursor.execute("""SELECT * FROM users WHERE question5 != 'Да';""")
    rows10 = cursor.fetchall()
    await call.message.answer(f'{len(rows2)} чел <<< Младше 23 ВОЗРАСТ Старше 23 >>> {len(rows)} чел\n'
                              f'{len(rows3)} ДА <<< Устраивает качество и формат обучения >>> НЕТ {len(rows4)}\n'
                              f'{len(rows5)} ДА < Соответствует курс тому что было обещано > НЕТ {len(rows6)}\n'
                              f'{len(rows7)} ДА <Устраивает работа куратора и тех.поддержки> НЕТ {len(rows8)}\n'
                              f'{len(rows9)} ДА <<< Хотите продолжать обучение >>> НЕТ {len(rows10)}')
    conn.close()


# Нажатие Кнопки ответить на вопросы.
@router.callback_query(F.data == 'authorization')
async def reg_one(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ваш возраст?", reply_markup=kb.keyboard2)
    await state.update_data(tg_name=call.from_user.first_name)
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.age)


# Ответ кнопкой меньше 23 лет. Вопрос №1
@router.callback_query(Reg.age, F.data == 'answer1')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await state.update_data(age='20')

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Устраивает ли вас качество и формат обучения?\nЕсли не устраивает то нажмите кнопку"
                              " Не устраивает и напишите что именно вас не устраивает.", reply_markup=kb.keyboard3)
    await state.set_state(Reg.question2)


# Ответ кнопкой 23 или больше лет. Вопрос №1
@router.callback_query(Reg.age, F.data == 'answer2')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await state.update_data(age='23')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Устраивает ли вас качество и формат обучения?\nЕсли не устраивает то просто напишите"
                              " что именно вас не устраивает и отправте сообщение.", reply_markup=kb.keyboard3)
    await state.set_state(Reg.question2)


# Ответ Кнопкой "Устраивает" на вопрос №2
@router.callback_query(Reg.question2, F.data == 'answer3')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await state.update_data(question2='Устраивает')
    await call.message.answer("Cоответствует ли обучение тому, что озвучивал менеджер или что было заявлено в рекламе"
                              " при приобретении курса?", reply_markup=kb.keyboard4)
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.question3)


# Ответ ТЕКСТОМ от пользователя на вопрос №2
@router.message(Reg.question2)
async def reg_age(message: Message, state: FSMContext):

    await state.update_data(question2=message.text)
    name = message.chat.first_name

    await message.answer(f'{name} ваш ответ принят!\n\nCоответствует ли обучение тому, что озвучивал менеджер'
                          ' или что было заявлено в рекламе при приобретении курса?', reply_markup=kb.keyboard4)

    await state.set_state(Reg.question3)


# Ответ ДА на вопрос №3
@router.callback_query(Reg.question3, F.data == 'answer5')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Устраивает ли вас работа куратора и технической поддержки?", reply_markup=kb.keyboard5)
    await state.update_data(question3='Да')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.question4)


# Ответ НЕТ на вопрос №3
@router.callback_query(Reg.question3, F.data == 'answer6')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Устраивает ли вас работа куратора и технической поддержки?", reply_markup=kb.keyboard5)
    await state.update_data(question3='Нет')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.question4)


# Ответ ДА на вопрос №4
@router.callback_query(Reg.question4, F.data == 'answer7')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Хотите ли вы продолжать обучение?", reply_markup=kb.keyboard6)
    await state.update_data(question4='Да')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.question5)


# Ответ НЕТ на вопрос №4
@router.callback_query(Reg.question4, F.data == 'answer8')
async def reg_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Хотите ли вы продолжать обучение?", reply_markup=kb.keyboard6)
    await state.update_data(question4='Нет')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Reg.question5)


# Ответ ДА на вопрос №5
@router.callback_query(Reg.question5, F.data == 'answer9')
async def reg_age(call: CallbackQuery, state: FSMContext):
    name = call.message.chat.first_name
    await call.message.answer(f'{name} Благодарим за активность!')
    await state.update_data(question5='Да')
    data = await state.get_data()
    await update_user(call.from_user.id, data['tg_name'], data['age'], data['question2'], data['question3'],
                      data['question4'], data['question5'])
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()


# Ответ НЕТ на вопрос №5
@router.callback_query(Reg.question5, F.data == 'answer10')
async def reg_age(call: CallbackQuery, state: FSMContext):
    name = call.message.chat.first_name
    await call.message.answer(f'{name} Благодарим за активность!')
    await state.update_data(question5='Нет')
    data = await state.get_data()
    await update_user(call.from_user.id, data['tg_name'], data['age'], data['question2'], data['question3'],
                      data['question4'], data['question5'])
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()


# Ответ НЕТ но боюсь отказаться и потерять в деньгах на вопрос №5
@router.callback_query(Reg.question5, F.data == 'answer11')
async def reg_age(call: CallbackQuery, state: FSMContext):
    name = call.message.chat.first_name
    await call.message.answer(f'{name} Благодарим за активность!')
    await state.update_data(question5='Боюсь потерять деньги')
    data = await state.get_data()
    await update_user(call.from_user.id, data['tg_name'], data['age'], data['question2'], data['question3'],
                      data['question4'], data['question5'])
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()




