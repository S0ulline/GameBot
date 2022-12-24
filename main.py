import asyncio
import contextlib

from aiogram.utils.exceptions import MessageNotModified

import config
import inline_keyboards as kb
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import dbworker

db = dbworker('mydatabase.db')

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

throwing_the_dice_array = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
dice_bet = {'dice_bet_100': '100', 'dice_bet_500': '500', 'dice_bet_1000': '1000', 'dice_bet_2500': '2500',
            'dice_bet_5000': '5000', 'dice_bet_10000': '10000', 'dice_bet_50000': '50000', 'dice_bet_100000': '100000',
            'dice_bet_all_in': 'all_in'}


@dp.message_handler(commands=['games', 'start'])  # Начальное сообщение
async def start_msg(message: types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        await message.answer(text="Азартные игры запрещены в группах и каналах❌\n"
                                  "Для игры перейдите в личный чат с ботом❗")
    else:
        win_status = db.get_window_status(message.from_user.id)[0][0]
        if win_status:
            reset_win_status = db.get_reset_win(message.from_user.id)[0][0]
            if reset_win_status:
                await message.answer(text="Не балуйся❗")
            else:
                db.set_reset_win(message.from_user.id, True)
                await message.answer(text="Окно игр уже запущенно\n"
                                          "Если у вас возникла ошибка нажмите кнопку ниже⬇",
                                     reply_markup=kb.keyboard_reset)
        else:
            if db.user_exists(message.from_user.id):
                window_id = await message.answer(text="Начальное сообщение", reply_markup=kb.keyboard_info_games)
            else:
                db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username, 5000)
                window_id = await message.answer(text="Начальное сообщение\nДобро пожаловать\n"
                                                      f"Баланс {5000}", reply_markup=kb.keyboard_info_games)
            db.set_window_id(message.from_user.id, window_id.message_id)
            db.set_window_status(message.from_user.id, True)


@dp.callback_query_handler(text="dice_game")  # Правила игры в кости
async def dice_game(call: types.CallbackQuery):
    await call.message.edit_text(text="Правила игры в кости", reply_markup=kb.keyboard_info_dice)


@dp.callback_query_handler(text="back")  # Начальное сообщение вызываемое через кнопку
async def back(call: types.CallbackQuery):
    await call.message.edit_text(text="Начальное сообщение", reply_markup=kb.keyboard_info_games)


@dp.callback_query_handler(text="dice_game_start")  # Начало игры в кости
async def dice_game_start(call: types.CallbackQuery):
    if not db.user_exists_to_dice(call.message.chat.id):
        db.add_user_to_dice(call.message.chat.id)
    bet = db.get_dice_bet(call.message.chat.id)[0][0]
    balance = db.get_balance(call.message.chat.id)[0][0]
    with contextlib.suppress(MessageNotModified):
        await call.message.edit_text(text=f'Начало игры в кости\nСтавка: {bet}\nБаланс: {balance}',
                                     reply_markup=kb.keyboard_dice)


@dp.callback_query_handler(text="change_the_bet")  # Выбор ставки
async def dice_change_the_bet(call: types.CallbackQuery):
    await call.message.edit_text("Выберите ставку:", reply_markup=kb.keyboard_dice_bet)


@dp.callback_query_handler(lambda call: call.data in dice_bet)  # Выбрана ставка
async def dice_bet_selected(call: types.CallbackQuery):
    bet_request = dice_bet[call.data]
    balance = db.get_balance(call.message.chat.id)[0][0]
    if bet_request == 'all_in':
        bet = balance
        db.change_dice_bet(call.message.chat.id, bet)
    else:
        if float(bet_request) > balance:
            await call.answer(text="Ставка не может быть больше баланса", show_alert=True)
        else:
            bet = float(bet_request)
            db.change_dice_bet(call.message.chat.id, bet)
    await dice_game_start(call)


@dp.callback_query_handler(text="choose_a_number")  # Выбор числа
async def dice_choose_a_number(call: types.CallbackQuery):
    bet = db.get_dice_bet(call.message.chat.id)[0][0]
    balance = db.get_balance(call.message.chat.id)[0][0]
    if bet > balance:
        await call.answer(text="Пожалуйста измените ставку", show_alert=True)
        await dice_game_start(call)
    else:
        if bet <= 0:
            await call.answer(text="Вы бедный, у вас нет деняк", show_alert=True)
            await dice_game_start(call)
        else:
            await call.message.edit_text(text="⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
            balance -= bet
            db.change_balance(call.message.chat.id, balance)
            window_id = await call.message.answer(text="Ставки сделаны\nВыберите число",
                                                  reply_markup=kb.keyboard_choose_number)
            db.set_window_id(call.message.chat.id, window_id.message_id)


@dp.callback_query_handler(lambda call: call.data in throwing_the_dice_array)  # Выбрано число
async def number_selected(call: types.CallbackQuery):
    bet = db.get_dice_bet(call.message.chat.id)[0][0]
    balance = db.get_balance(call.message.chat.id)[0][0]
    number = call.data
    await call.message.edit_text(text=f'Выбрано число: {number}\nЗапускаем процесс броска...')
    await asyncio.sleep(2)
    await call.message.delete()
    dice_1 = await call.message.answer_dice(emoji='🎲')
    dice_2 = await call.message.answer_dice(emoji='🎲')
    dice_3 = await call.message.answer_dice(emoji='🎲')
    result = dice_1.dice.value + dice_2.dice.value + dice_3.dice.value
    if result == int(number):
        balance += bet * 2
        db.change_balance(call.message.chat.id, balance)
        await asyncio.sleep(4)
        window_id = await call.message.answer(text=f'Вы угадали🟢\n'
                                                   f'Вы поставили: {bet}\n'
                                                   f'Вы выйграли: {bet * 2}\n\n'
                                                   f'Вы выбрали число: {number}\n'
                                                   f'Сумма кубиков: {result}\n\n'
                                                   f'Ваш баланс: {balance}',
                                              reply_markup=kb.keyboard_roll_the_dice)
    else:
        await asyncio.sleep(4)
        window_id = await call.message.answer(text=f'Вы не угадали🔴\n'
                                                   f'Вы поставили: {bet}\n'
                                                   f'Вы ничего не выйграли\n\n'
                                                   f'Вы выбрали число: {number}\n'
                                                   f'Сумма кубиков: {result}\n\n'
                                                   f'Ваш баланс: {balance}',
                                              reply_markup=kb.keyboard_roll_the_dice)
    db.set_window_id(call.message.chat.id, window_id.message_id)


@dp.message_handler(commands=['reset'])  # Начальное сообщение
async def reset(message: types.Message):
    win_status = db.get_window_status(message.from_user.id)
    if not win_status:
        await message.answer(text="Все окна закрыты, дополнительных действий не требуется\n"
                                  "Для вызова нового окна введите команду /start")
    else:
        await message.answer(text="Для сброса нажмите кнопку ниже", reply_markup=kb.keyboard_reset)


@dp.callback_query_handler(text="close_window")  # Закрытие окна
async def close_window(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=db.get_window_id(call.message.chat.id)[0][0])
    db.set_window_status(call.message.chat.id, False)
    db.set_window_id(call.message.chat.id, 0)


@dp.callback_query_handler(text="reset_window")  # Сброс окна
async def reset_window(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=db.get_window_id(call.message.chat.id)[0][0])
    await call.message.delete()
    db.set_window_status(call.message.chat.id, False)
    db.set_window_id(call.message.chat.id, 0)
    db.set_reset_win(call.message.chat.id, False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
