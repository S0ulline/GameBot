import sqlite3


class dbworker:
    def __init__(self, database_file):
        """ Констуктор """
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """ Проверка есть ли юзер в бд """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE userid = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, userid, fullname, username, balance):
        """Добавляем нового юзера"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (userid, fullname, username, balance) VALUES(?, ?, ?, ?)",
                                       (userid, fullname, username, balance))

    def get_window_status(self, user_id):
        """ Статус окна Активно """
        with self.connection:
            result = self.cursor.execute('SELECT `window_activity` FROM `users` WHERE userid = ?',
                                         (user_id,)).fetchall()
            return result

    def set_window_status(self, user_id, window_activity):
        """ Изменение статуса окна """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `window_activity` = ? WHERE userid = ?', (window_activity, user_id))

    def get_window_id(self, user_id):
        """ Статус окна Активно """
        with self.connection:
            result = self.cursor.execute('SELECT `window_id` FROM `users` WHERE userid = ?',
                                         (user_id,)).fetchall()
            return result

    def set_window_id(self, user_id, window_id):
        """ Изменение id окна """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `window_id` = ? WHERE userid = ?', (window_id, user_id))

    def set_reset_win(self, user_id, reset_win):
        """ Изменение статуса окна сброса """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `reset_win` = ? WHERE userid = ?', (reset_win, user_id))

    def get_reset_win(self, user_id):
        """ Получение статуса окна сброса """
        with self.connection:
            result = self.cursor.execute('SELECT `reset_win` FROM `users` WHERE userid = ?',
                                         (user_id,)).fetchall()
            return result

    def user_exists_to_dice(self, user_id):
        """ Проверка есть ли юзер в бд Кости"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `dice` WHERE userid = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user_to_dice(self, userid):
        """Добавляем нового юзера в Кости"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `dice` (userid) VALUES(?)", (userid,))

    def get_balance(self, user_id):
        """ Получение баланса игрока """
        with self.connection:
            result = self.cursor.execute('SELECT `balance` FROM `users` WHERE userid = ?', (user_id,)).fetchall()
            return result

    def change_balance(self, user_id, balance):
        """ Изменение баланса игрока """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `balance` = ? WHERE userid = ?', (balance, user_id))

    def get_dice_bet(self, user_id):
        """ Получение ставки игрока в игре Кости """
        with self.connection:
            result = self.cursor.execute('SELECT `bet` FROM `dice` WHERE userid = ?', (user_id,)).fetchall()
            return result

    def change_dice_bet(self, user_id, bet):
        """ Изменение ставки игрока в игре Кости """
        with self.connection:
            self.cursor.execute('UPDATE `dice` SET `bet` = ? WHERE userid = ?', (bet, user_id))
