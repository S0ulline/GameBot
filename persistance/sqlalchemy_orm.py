import asyncio

from aiogram import types
from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
import inline_keyboards as kb

Base = declarative_base()


class Entity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True)


class User(Entity):
    __tablename__ = "users"
    fullname = Column(String)
    username = Column(String)
    balance = Column(Numeric)
    window_activity = Column(Boolean, default=False)
    window_id = Column(Integer, default=0)
    reset_win = Column(Boolean, default=False)

    async def plays_dice_bet(self, db, call: types.CallbackQuery):
        user_dice = db.user_dice_info_repository.get(self.id)
        bet = user_dice.bet
        number = call.data
        await call.message.edit_text(text=f'Выбрано число: <b>{number}</b>\nЗапускаем процесс броска...', parse_mode='HTML')
        await asyncio.sleep(2)
        await call.message.delete()
        dice_1 = await call.message.answer_dice(emoji='🎲')
        dice_2 = await call.message.answer_dice(emoji='🎲')
        dice_3 = await call.message.answer_dice(emoji='🎲')
        result = dice_1.dice.value + dice_2.dice.value + dice_3.dice.value
        if result == int(number):
            self.balance += bet * 10
            await asyncio.sleep(4)
            window_id = await call.message.answer(text=f'Вы угадали🟢\n'
                                                       f'Вы поставили: {bet}\n'
                                                       f'Вы выйграли: {bet * 10}\n\n'
                                                       f'Вы выбрали число: {number}\n'
                                                       f'Сумма кубиков: {result}\n\n'
                                                       f'Ваш баланс: {self.balance}',
                                                  reply_markup=kb.keyboard_roll_the_dice)
        else:
            await asyncio.sleep(4)
            window_id = await call.message.answer(text=f'Вы не угадали🔴\n'
                                                       f'Вы поставили: {bet}\n'
                                                       f'Вы ничего не выйграли\n\n'
                                                       f'Вы выбрали число: {number}\n'
                                                       f'Сумма кубиков: {result}\n\n'
                                                       f'Ваш баланс: {self.balance}',
                                                  reply_markup=kb.keyboard_roll_the_dice)
        self.window_id = window_id.message_id
        db.save_changes()

    def __repr__(self):
        return f"User(id={self.id!r}," \
               f"fullname={self.fullname!r}," \
               f"username={self.username}," \
               f"balance={self.balance}," \
               f"window_activity={self.window_activity}," \
               f"window_id={self.window_id}," \
               f"reset_win={self.reset_win})"


class UserDiceInfo(Entity):
    __tablename__ = "users_dice_info"
    id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True)
    bet = Column(Numeric, default=0)
    luck = Column(Integer, default=0)
    failure = Column(Integer, default=0)

    def __repr__(self):
        return f"UserDice(id={self.id!r}," \
               f"bet={self.bet!r}," \
               f"luck={self.luck}," \
               f"failure={self.failure})"

#
# class Address(Base):
#     __tablename__ = "address"
#     id = Column(Integer, primary_key=True)
#     email_address = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
#     user = relationship("User", back_populates="addresses")
#
#     def __repr__(self):
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
