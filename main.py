from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button


# Игровой экран
class GameScreen(Screen):
    # Конец игры
    def end_round(self):
        self.ids.btn_grid.clear_widgets()
        self.label_refresh("Это удивительно, но игру можно пройти! :)\n"
                           "ПОБЕДА!!!")
        # Выключение игровых кнопок
        self.ids.next_rows_btn.disabled = True
        self.ids.clear_rows_btn.disabled = True

    # Обновление поля событий
    def label_refresh(self, text):
        self.ids.label.text = str(text)
        return self.ids.label

    # Проверка выбранной пары цифр
    def check_nums(self, x1, x2):
        if self.digits[x1] == self.digits[x2] or \
                self.digits[x1] + self.digits[x2] == 10:

            if abs(x1 - x2) % 9 == 0:
                step = 9
            else:
                step = 1

            start = min(x1, x2) + step
            end = max(x1, x2)

            for i in range(start, end, step):
                if self.digits[i] != "*":
                    return False
            return True
        return False

    def num_click(self, instance, x):
        self.label_refresh("Выбери верную пару к цифре =>")

        if instance.background_color != [1, 1, 1, 1]:
            instance.background_color = [1, 1, 1, 1]
            self.two_nums = []
        else:
            instance.background_color = '#F62C3F'
            if x not in self.two_nums:
                self.two_nums.append(x)
            if len(self.two_nums) == 2:
                if self.check_nums(self.two_nums[0], self.two_nums[1]):
                    self.win -= 2
                    if self.win <= 0:
                        self.end_round()
                    self.label_refresh(f'Пока все получается! :)\n'
                                       f'Осталось невычеркнутых цифр: {self.win}')
                    self.digits[self.two_nums[0]] = "*"
                    self.buttons[self.two_nums[0]].text = "*"
                    self.buttons[self.two_nums[0]].disabled = True
                    self.digits[self.two_nums[1]] = "*"
                    self.buttons[self.two_nums[1]].text = "*"
                    self.buttons[self.two_nums[1]].disabled = True
                else:
                    self.label_refresh('Выбранная пара цифр не может быть вычеркнута, '
                                       'поскольку не соответствует правилам игры :(')
                self.buttons[self.two_nums[0]].background_color = [1, 1, 1, 1]
                self.buttons[self.two_nums[1]].background_color = [1, 1, 1, 1]
                self.two_nums = []

    # Обновление игрового поля (тестовая)
    def buttons_refresh(self, if_clear, end_point, start_point=0):
        if if_clear == 1:
            self.buttons = []
            self.ids.btn_grid.clear_widgets()
        for i in range(start_point, end_point):
            btn = Button(text=str(self.digits[i]),
                         on_press=lambda inst, x=i: self.num_click(inst, x))  # size_hint=(1, 30), height=80,
            self.buttons.append(btn)
            # Отключение вычеркнутых кнопок-цифр
            if self.digits[i] == '*':
                self.buttons[i].disabled = True
            self.ids.btn_grid.add_widget(self.buttons[i])

    # Начало игры (нового раунда)
    def new_round(self):
        self.label_refresh("Игра началась!")
        # Обновление игрового поля
        self.digits = self.initial_digits.copy()  # Обновление копии списка с цифрами
        self.buttons = []
        self.two_nums = []
        self.win = 27  # Счетчик на количество цифр
        self.buttons_refresh(if_clear=1, end_point=len(self.initial_digits))
        # Включение игровых кнопок
        self.ids.next_rows_btn.disabled = False
        self.ids.clear_rows_btn.disabled = False

    # Продление рядов цифр
    def next_rows(self, instance):
        temp_rows = []
        for i in self.digits:
            if i != "*":
                temp_rows.append(i)
                self.win += 1
        old_len = len(self.digits)
        self.digits.extend(temp_rows)
        self.buttons_refresh(if_clear=0, start_point=old_len, end_point=len(self.digits))
        self.label_refresh(f'Цифр стало в 2 раза больше!\n'
                           f'Осталось цифр до победы: {self.win}')

    # Исключение полностью вычеркнутых рядов
    def clean_rows(self, instance):
        temp_rows = []
        rows = len(self.digits) // 9
        for i in range(rows):
            start_idx = 9 * i
            end_idx = start_idx + 9
            k = 0
            for j in range(start_idx, end_idx):
                if self.digits[j] == "*":
                    k += 1
                else:
                    break
            if k < 9:
                temp_rows.extend(self.digits[start_idx:end_idx])
        for i in range(9 * rows, len(self.digits)):
            temp_rows.append(self.digits[i])
        if self.digits == temp_rows:
            self.label_refresh('Пока нет полностью вычеркнутых рядов! :(')
        else:
            self.digits = temp_rows
            self.buttons_refresh(if_clear=1, end_point=len(self.digits))
            self.label_refresh('Игровое поле чуть сократилось! :)')

    # Создание переменных
    digits = []  # Список цифр
    buttons = []  # Список кнопок
    win = -1  # Счетчик победы

    # Стартовые 3 ряда цифр
    initial_digits = [i for i in range(1, 10)]
    for i in range(11, 20):
        initial_digits.append(i // 10)
        initial_digits.append(i % 10)

    # Переменная для проверки пары
    two_nums = []


# Экран с правилами игры
class RulesScreen(Screen):
    pass


class NumbersApp(App):
    def build(self):
        self.icon = 'assets\myicon.png'
        # Создание 2 игровых окон
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RulesScreen(name='rules'))
        return sm


if __name__ == '__main__':
    NumbersApp().run()
