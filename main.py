from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

from kivy.lang import Builder

from kivymd.app import MDApp

#class MyApp(App):
#    def build(self):
#        self.icon = 'myicon.png'


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
        if self.num_rows[x1] == self.num_rows[x2] or self.num_rows[x1] + self.num_rows[x2] == 10:

            # Задаем точки проверки в масиве
            len_x1_x2 = abs(x2 - x1)
            if x2 > x1:
                start_pos = x1
            else:
                start_pos = x2

            # Проверка по вертикали
            if len_x1_x2 % 9 == 0:
                for i in range(9, len_x1_x2, 9):
                    if self.num_rows[start_pos + i] != "*":
                        return 0
                return True

            # Проверка по горизонтали
            for i in range(1, len_x1_x2):
                if self.num_rows[start_pos + i] != "*":
                    return 0
            return True

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
                    self.label_refresh(f'Пока все получается! :)\nОсталось невычеркнутых цифр: {self.win}')
                    self.num_rows[self.two_nums[0]] = "*"
                    self.btn_map[self.two_nums[0]].text = "*"
                    self.btn_map[self.two_nums[0]].disabled = True
                    self.num_rows[self.two_nums[1]] = "*"
                    self.btn_map[self.two_nums[1]].text = "*"
                    self.btn_map[self.two_nums[1]].disabled = True
                else:
                    self.label_refresh('Выбранная пара цифр не может быть вычеркнута, '
                                       'поскольку не соответствует правилам игры :(')
                self.btn_map[self.two_nums[0]].background_color = [1, 1, 1, 1]
                self.btn_map[self.two_nums[1]].background_color = [1, 1, 1, 1]
                self.two_nums = []

    # Обновление игрового поля (исходник)
    '''def btn_map_refresh(self):  # Применять функцию чаще с параметрами начало и конец
        self.btn_map = []
        self.ids.btn_grid.clear_widgets()
        for i in range(len(self.num_rows)):
            btn = Button(text=str(self.num_rows[i]), on_press=lambda inst, x=i: self.num_click(inst, x))  # size_hint=(1, 30), height=80,
            self.btn_map.append(btn)
            # Отключение вычеркнутых кнопок-цифр
            if self.num_rows[i] == '*':
                self.btn_map[i].disabled = True
            self.ids.btn_grid.add_widget(self.btn_map[i])'''

    # Обновление игрового поля (тестовая)
    def btn_map_refresh(self, if_clear, end_point, start_point=0):
        if if_clear == 1:
            self.btn_map = []
            self.ids.btn_grid.clear_widgets()
        for i in range(start_point, end_point):
            btn = Button(text=str(self.num_rows[i]),
                         on_press=lambda inst, x=i: self.num_click(inst, x))  # size_hint=(1, 30), height=80,
            self.btn_map.append(btn)
            # Отключение вычеркнутых кнопок-цифр
            if self.num_rows[i] == '*':
                self.btn_map[i].disabled = True
            self.ids.btn_grid.add_widget(self.btn_map[i])

    # Начало игры (нового раунда)
    def new_round(self):
        self.label_refresh("Игра началась!")
        # Обновление копии списка с цифрами
        self.num_rows = self.first_rows.copy()
        # Обновление игрового поля
        self.btn_map_refresh(if_clear=1, end_point=len(self.first_rows))
        '''self.btn_map = []
        self.ids.btn_grid.clear_widgets()
        for i in range(len(self.first_rows)):
            btn = Button(text=str(self.first_rows[i]), on_press=lambda inst, x=i: self.num_click(inst, x))  # size_hint=(1, 30), height=80,
            self.btn_map.append(btn)
            self.ids.btn_grid.add_widget(self.btn_map[i])'''

        # Счетчик на количество цифр
        self.win = 27
        # Включение игровых кнопок
        self.ids.next_rows_btn.disabled = False
        self.ids.clear_rows_btn.disabled = False

    # Продление рядов цифр
    def next_rows(self, instance):
        temp_rows = []
        for i in self.num_rows:
            if i != "*":
                temp_rows.append(i)
                self.win += 1
        old_len = len(self.num_rows)
        self.num_rows.extend(temp_rows)
        self.btn_map_refresh(if_clear=0, start_point=old_len, end_point=len(self.num_rows))
        '''for i in range(old_len, len(self.num_rows)):
            btn = Button(text=str(self.num_rows[i]), on_press=lambda inst, x=i: self.num_click(inst, x))
            self.btn_map.append(btn)
            self.ids.btn_grid.add_widget(self.btn_map[i])'''
        self.label_refresh(f'Цифр стало в 2 раза больше!\nОсталось цифр до победы: {self.win}')

    # Исключение полностью вычеркнутых рядов
    def clean_rows(self, instance):
        temp_rows = []
        rows = len(self.num_rows) // 9
        for i in range(rows):
            start_idx = 9 * i
            end_idx = start_idx + 9
            k = 0
            for j in range(start_idx, end_idx):
                if self.num_rows[j] == "*":
                    k += 1
                else:
                    break
            if k < 9:
                temp_rows.extend(self.num_rows[start_idx:end_idx])
        for i in range(9 * rows, len(self.num_rows)):
            temp_rows.append(self.num_rows[i])
        if self.num_rows == temp_rows:
            self.label_refresh('Пока нет полностью вычеркнутых рядов! :(')
        else:
            self.num_rows = temp_rows
            self.btn_map_refresh(if_clear=1, end_point=len(self.num_rows))
            self.label_refresh('Игровое поле чуть сократилось! :)')

    # Создание переменных
    num_rows = []  # Список цифр
    btn_map = []  # Список кнопок
    win = -1  # Счетчик победы

    # Стартовые 3 ряда цифр
    first_rows = [i for i in range(1, 10)]
    for i in range(11, 20):
        first_rows.append(i // 10)
        first_rows.append(i % 10)

    # Переменная для проверки пары
    two_nums = []


# Экран с правилами игры
class RulesScreen(Screen):
    pass


class NumbersApp(MDApp):
    def build(self):
        self.icon = 'myicon.png'
        # Создание 2 игровых окон
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RulesScreen(name='rules'))
        return sm


if __name__ == '__main__':
    NumbersApp().run()
