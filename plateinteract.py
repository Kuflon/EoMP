import plotly.graph_objects as go
import numpy as np


class Plate:
    '''
    Класс интерактивных действий с пластиной(мембраной)
    Возможные действия:
    1. Колебание при имеющемся нажатии
    2. Прогрев пластины при заданной температуре
    '''

    def __init__(self):
        self.scale_min = 0 # Диапазон варьируемых значений
        self.scale_max = 0 #


    def deflection(self, l_1, l0, l1,  a, s, h, times=50):
        '''
        Колебания мембраны.
        Параметры:
        l_1, l0, l1 - массивы состояний мембраны, l1 - конечное состояние
        a - скорость распространения колебаний
        s - шаг времени
        h - шаг разбиения сетки
        times - количество итераций(кол-во фреймов анимации)

        Сохраняет массив фреймов для анимации
        '''

        def step(l_1, l0, l1):
            '''
            Функция шага уравнения колебания
            Возвращает обновленное состояние пластины
            '''

            #Обновление текущего состояния на основе предыдущих
            n = len(l0)
            m = len(l0[0])
            for i in range(1, n-1):
                for j in range(1, m-1):
                    l1[i][j] = a**2 * s**2 / h**2 * \
                    (l0[i+1][j] + l0[i-1][j] + l0[i][j+1] + l0[i][j-1] - 4*l0[i][j]) + \
                    2* l0[i][j] - l_1[i][j]

            #Обновление предыдущих двух состояний
            for i in range(1, n-1):
                for j in range(1, m-1):
                    l_1[i][j] = l0[i][j]
                    l0[i][j] = l1[i][j]

            #Поиск минимального и максимального z для корректного масштабирования анимации
            if self.scale_min > np.amin(l_1): self.scale_min = np.amin(l_1) - 1
            if self.scale_max < np.amax(l1): self.scale_max = np.amax(l1) + 1

            return l_1, l0, l1


        l_1 = np.array(l_1)
        l0 = np.array(l0)
        l1 = np.array(l1) # Текущее состояние пластины
        self.start_frame = l1 # Стартовый фрейм анимации

        # Заполение массива фреймов
        frames=[]
        for i in range(times):
            l_1, l0, l1 = step(l_1, l0, l1)
            frames.append(go.Frame(data=[go.Surface(z=l1)]))

        self.frames = frames


    def warm(self, l0, l1, c, p, l, u, h, s, a, times = 20):
        '''
        Прогрев мембраны.
        Предполагается, что внутренних источников тепла нет
        Параметры:
        l0, l1 - массивы состояний мембраны, l1 - конечное состояние
        с - удельная теплоёмкость материала
        p - плотность материала
        l - коэффициент теплопроводности
        u - температура греющей среды
        h - шаг разбиения сетки
        s - шаг времени
        a - скорость распространения
        times - количество итераций(кол-во фреймов анимации)

        Сохраняет массив фреймов для анимации
        '''

        def step(l0, l1):
            '''
            Функция шага уравнения прогрева
            Возвращает обновленное состояние температуры пластины
            '''

            #Обновление текущего состояния на основе предыдущего в центре
            n = len(l0) - 1
            for i in range(1, n):
                for j in range(1, n):
                    l1[i][j] = (l*s)/(c*p*h**2)* \
                    (l0[i+1][j] + l0[i-1][j] + l0[i][j+1] + l0[i][j-1] - 4*l0[i][j]) + l0[i][j]

            #Обновление текущего состояния на основе предыдущего по бокам
            for i in range(n+1):
                l1[0][i] = (a*h/l*u+l1[1][i]) / (1+a*h/l)
                l1[n][i] = (a*h/l*u+l1[n-1][i]) / (1+a*h/l)
                l1[i][0] = (a*h/l*u+l1[i][1]) / (1+a*h/l)
                l1[i][n] = (a*h/l*u+l1[i][n-1]) / (1+a*h/l)

            l0 = np.copy(l1)
            #Поиск минимального и максимального z для корректного масштабирования анимации
            if self.scale_min > np.amin(l0): self.scale_min = np.amin(l0) - 1
            if self.scale_max < np.amax(l1): self.scale_max = np.amax(l1) + 1

            return l0, l1

        l0 = np.array(l0)
        l1 = np.array(l1)# Текущее состояние температуры
        self.start_frame = np.copy(l1) # Стартовый фрейм анимации

        # Заполение массива фреймов
        frames=[]
        for i in range(times):
            l0, l1 = step(l0, l1)
            frames.append(go.Frame(data=[go.Surface(z=l1)]))

        self.frames = frames


    def show_result(self):
        '''
        Анимация.
        '''

        fig = go.Figure(data=[go.Surface(z=self.start_frame)], frames = self.frames,
        layout=dict(legend_orientation="h",
                                    legend=dict(x=.5, xanchor="center"),
                                    updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None] ) ])],
                                    margin=dict(l=0, r=0, t=0, b=0)))
        fig.update_layout(title='Graph', autosize=False, scene = dict(zaxis = dict(nticks=4, range=[self.scale_min, self.scale_max])),
                          width=700, height=700,
                          margin=dict(l=65, r=50, b=65, t=90))
        fig.show()
