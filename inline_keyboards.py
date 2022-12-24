from aiogram import types

INFO_GAMES_BTN_GROUP = [types.InlineKeyboardButton(text="Кости🎲", callback_data="dice_game"),
                        types.InlineKeyboardButton(text="Закрыть❌", callback_data="close_window")]
keyboard_info_games = types.InlineKeyboardMarkup(row_width=1)
keyboard_info_games.add(*INFO_GAMES_BTN_GROUP)

RESET_BTN = [types.InlineKeyboardButton(text="Сброс🔄", callback_data="reset_window")]
keyboard_reset = types.InlineKeyboardMarkup(row_width=1)
keyboard_reset.add(*RESET_BTN)

INFO_DICE_BTN_GROUP = [types.InlineKeyboardButton(text="Играть🎲", callback_data="dice_game_start"),
                       types.InlineKeyboardButton(text="Назад◀", callback_data="back")]
keyboard_info_dice = types.InlineKeyboardMarkup(row_width=1)
keyboard_info_dice.add(*INFO_DICE_BTN_GROUP)

DICE_BTN_GROUP = [types.InlineKeyboardButton(text="⚪100", callback_data="dice_bet_100"),
                  types.InlineKeyboardButton(text="🔴500", callback_data="dice_bet_500"),
                  types.InlineKeyboardButton(text="🔵1000", callback_data="dice_bet_1000"),
                  types.InlineKeyboardButton(text="🟢2500", callback_data="dice_bet_2500"),
                  types.InlineKeyboardButton(text="🟡5000", callback_data="dice_bet_5000"),
                  types.InlineKeyboardButton(text="🟤10000", callback_data="dice_bet_10000"),
                  types.InlineKeyboardButton(text="🟠50000", callback_data="dice_bet_50000"),
                  types.InlineKeyboardButton(text="⚫100000", callback_data="dice_bet_100000"),
                  types.InlineKeyboardButton(text="🟣Поставить всё", callback_data="dice_bet_all_in")]
keyboard_dice_bet = types.InlineKeyboardMarkup(row_width=2)
keyboard_dice_bet.add(*DICE_BTN_GROUP)

DICE_BET_BTN_GROUP = [types.InlineKeyboardButton(text="Выбрать число☝", callback_data="choose_a_number"),
                      types.InlineKeyboardButton(text="Изменить ставку✏", callback_data="change_the_bet"),
                      types.InlineKeyboardButton(text="Главное меню🏠", callback_data="back")]
keyboard_dice = types.InlineKeyboardMarkup(row_width=1)
keyboard_dice.add(*DICE_BET_BTN_GROUP)

CHOOSE_NUMBER_BTN_GROUP = [types.InlineKeyboardButton(text="3", callback_data="3", ),
                           types.InlineKeyboardButton(text="4", callback_data="4"),
                           types.InlineKeyboardButton(text="5", callback_data="5"),
                           types.InlineKeyboardButton(text="6", callback_data="6"),
                           types.InlineKeyboardButton(text="7", callback_data="7"),
                           types.InlineKeyboardButton(text="8", callback_data="8"),
                           types.InlineKeyboardButton(text="9", callback_data="9"),
                           types.InlineKeyboardButton(text="10", callback_data="10"),
                           types.InlineKeyboardButton(text="11", callback_data="11"),
                           types.InlineKeyboardButton(text="12", callback_data="12"),
                           types.InlineKeyboardButton(text="13", callback_data="13"),
                           types.InlineKeyboardButton(text="14", callback_data="14"),
                           types.InlineKeyboardButton(text="15", callback_data="15"),
                           types.InlineKeyboardButton(text="16", callback_data="16"),
                           types.InlineKeyboardButton(text="17", callback_data="17"),
                           types.InlineKeyboardButton(text="18", callback_data="18")]
keyboard_choose_number = types.InlineKeyboardMarkup(row_width=4)
keyboard_choose_number.add(*CHOOSE_NUMBER_BTN_GROUP)

ROLL_THE_DICE_BTN_GROUP = [types.InlineKeyboardButton(text="Играть еще🎲", callback_data="dice_game_start"),
                           types.InlineKeyboardButton(text="Главное меню🏠", callback_data="back")]
keyboard_roll_the_dice = types.InlineKeyboardMarkup(row_width=1)
keyboard_roll_the_dice.add(*ROLL_THE_DICE_BTN_GROUP)
