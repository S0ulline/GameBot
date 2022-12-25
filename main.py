import contextlib
from aiogram.utils.exceptions import MessageNotModified
from decimal import Decimal
import inline_keyboards as kb
from aiogram import types
from persistance.sqlalchemy_orm import User, UserDiceInfo
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from startup import bot_api, db

bot = Bot(token=bot_api)
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
        return

    user = db.user_repository.get(message.from_user.id)
    if user:
        win_status = user.window_activity
        if win_status:
            reset_win_status = user.reset_win
            if reset_win_status:
                await message.answer(text="Не балуйся❗\nЯ уже дал тебе все что нужно.")
            else:
                user.reset_win = True
                db.save_changes()
                await message.answer(text="ВНИМАНИЕ❗❗❗\nОкно игр уже запущено выше🙄\n"
                                          "Если у вас возникла ошибка нажмите кнопку ниже⬇",
                                     reply_markup=kb.keyboard_reset)
            return
        window_id = await message.answer(text=f'Привет, я LYbot👋"\n'
                                              f'Со мной ты можешь сыграть в азартные мини-игры🎰\n'
                                              f'Тут нет подкруток, нет реальных денег, все зависит только от твоей удачи🍀\n'
                                              f'\n\nВаш баланс на текущий момент: <b>{user.balance}</b>\n'
                                              f'Играй, смотри все не проиграй😄\nУспехов✊',
                                         reply_markup=kb.keyboard_info_games, parse_mode='HTML')
    else:
        user = User(id=message.from_user.id,
                    fullname=message.from_user.full_name,
                    username=message.from_user.username,
                    balance=5000)
        db.user_repository.add(user)
        window_id = await message.answer(text=f'Привет, я LYbot👋"\n'
                                              f'Со мной ты можешь сыграть в азартные мини-игры🎰 (Количество игр будут меняться и добавляться с каждым обновлением)\n'
                                              f'Тут нет подкруток, нет реальных денег, все зависит только от твоей удачи🍀\n'
                                              f'\n\nВаш баланс на текущий момент: <b>{user.balance}</b>\n'
                                              f'Играй, смотри все не проиграй😄\nУспехов✊',
                                         reply_markup=kb.keyboard_info_games, parse_mode='HTML')
    user.window_id = window_id.message_id
    user.window_activity = True
    db.save_changes()


@dp.callback_query_handler(text="dice_game")  # Правила игры в кости
async def dice_game(call: types.CallbackQuery):
    await call.message.edit_text(text='Добро пожаловать в игру "Кости🎲🎲🎲"\n'
                                      'В этой мини-игре вам предстоит угадать сумму кубиков\n'
                                      '(Это начальная версия мини-игры которая будет со временем улучшаться)\n\n'
                                      'ПРАВИЛА❗\n'
                                      '1) Сделал ставку\n'
                                      '2) Угадываешь сумму выпавшую на 3-х кубиках\n'
                                      '3) Выигрываешь в 10 раз больше. Все просто😏',
                                 reply_markup=kb.keyboard_info_dice)


@dp.callback_query_handler(text="back")  # Начальное сообщение вызываемое через кнопку
async def back(call: types.CallbackQuery):
    user = db.user_repository.get(call.message.from_user.id)
    await call.message.edit_text(text=f'Привет, я LYbot👋"\n'
                                      f'Со мной ты можешь сыграть в азартные мини-игры🎰 (Количество игр будут меняться и добавляться с каждым обновлением)\n'
                                      f'Тут нет подкруток, нет реальных денег, все зависит только от твоей удачи🍀\n'
                                      f'\n\nВаш баланс на текущий момент: <b>{user.balance}</b>\n'
                                      f'Играй, смотри все не проиграй😄\nУспехов✊',
                                 reply_markup=kb.keyboard_info_games, parse_mode='HTML')


@dp.callback_query_handler(text="dice_game_start")  # Начало игры в кости
async def dice_game_start(call: types.CallbackQuery):
    user_dice = db.user_dice_info_repository.get(call.message.chat.id)
    if user_dice is None:
        user_dice = UserDiceInfo(id=call.message.chat.id)
        db.user_dice_info_repository.add(user_dice)
    user = db.user_repository.get(call.message.chat.id)
    user_dice = db.user_dice_info_repository.get(call.message.chat.id)
    bet = user_dice.bet
    balance = user.balance
    with contextlib.suppress(MessageNotModified):
        await call.message.edit_text(text=f'Начало игры в кости🎲\nВаша ставка: <b>{bet}</b>\nБаланс: <b>{balance}</b>',
                                     reply_markup=kb.keyboard_dice, parse_mode='HTML')
    db.save_changes()


@dp.callback_query_handler(text="change_the_bet")  # Выбор ставки
async def dice_change_the_bet(call: types.CallbackQuery):
    await call.message.edit_text("Выберите ставку:", reply_markup=kb.keyboard_dice_bet)


@dp.callback_query_handler(lambda call: call.data in dice_bet)  # Выбрана ставка
async def dice_bet_selected(call: types.CallbackQuery):
    bet_request = dice_bet[call.data]
    user = db.user_repository.get(call.message.chat.id)
    balance = user.balance
    user_dice = db.user_dice_info_repository.get(call.message.chat.id)
    if bet_request == 'all_in':
        user_dice.bet = balance
    else:
        if Decimal(bet_request) > balance:
            await call.answer(text="Ставка не может быть больше баланса😐", show_alert=True)
        else:
            user_dice.bet = Decimal(bet_request)
    db.save_changes()
    await dice_game_start(call)


@dp.callback_query_handler(text="choose_a_number")  # Выбор числа
async def dice_choose_a_number(call: types.CallbackQuery):
    user = db.user_repository.get(call.message.chat.id)
    user_dice = db.user_dice_info_repository.get(call.message.chat.id)
    bet = user_dice.bet
    balance = user.balance
    if bet > balance:
        await call.answer(text="Пожалуйста измените ставку😐", show_alert=True)
        db.save_changes()
        await dice_game_start(call)
    else:
        if bet <= 0:
            await call.answer(text="Ставка не может быть меньше или равняться нулю😐", show_alert=True)
            db.save_changes()
            await dice_game_start(call)
        else:
            await call.message.edit_text(text="⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
            user.balance -= bet
            window_id = await call.message.answer(text="Ставки сделаны\nВыберите число",
                                                  reply_markup=kb.keyboard_choose_number)
            user.window_id = window_id.message_id
            db.save_changes()


@dp.callback_query_handler(lambda call: call.data in throwing_the_dice_array)  # Выбрано число
async def number_selected(call: types.CallbackQuery):
    user = db.user_repository.get(call.message.chat.id)
    await user.plays_dice_bet(db, call)


@dp.callback_query_handler(text="close_window")  # Закрытие окна
async def close_window(call: types.CallbackQuery):
    user = db.user_repository.get(call.message.chat.id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=user.window_id)
    user.window_activity = False
    user.window_id = 0
    db.save_changes()


@dp.callback_query_handler(text="reset_window")  # Сброс окна
async def reset_window(call: types.CallbackQuery):
    user = db.user_repository.get(call.message.chat.id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=user.window_id)
    await call.message.delete()
    user.window_activity = False
    user.window_id = 0
    user.reset_win = False
    db.save_changes()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
