from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import *
import sys, json, copy
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import patches
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class CustomDialog(QDialog):
    def __init__(self, parent=None, mess=None, title=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(270, 90)
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(mess)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MySpinBox(QDoubleSpinBox):
    def __init__(self, ind, params=dict()):
        super().__init__(**params)
        self.ind = ind

class OpenWindow(QMainWindow):
    __data = {
        'robotype': 'Декарт',
        'movetype': 'Позиционное',
        'param_dec': [10.0, 6.0, 0.002],
        'coord_dec': [0.0, 1.0, 0.0, 1.0],
        'param_cil': [1.5, 0.1, 0.6, 0.2, 10.0, 6.0],
        'coord_cil': [-1.5, 1.5, 0.0, 0.7],
        'param_scr': [1.5, 0.1, 0.6, 0.4, 0.2, 10.0, 6.0],
        'coord_scr': [-1.5, 1.5, -2.5, 2.5],
        'param_col': [1.5, 0.1, 0.4, 0.2, 10.0, 6.0],
        'coord_col': [0.0, 0.7, -1.5, 1.5],
        'engine': [0.001, 0.001, 100.0, 250.0, 26.0, 26.0, 0.002, 0.002, 0.0, 0.0],
        'reg': [200.0, 200.0, 0.0, 0.0, 30.0, 30.0],
        'calc': [16.0, 0.008, 0.016, 0.016],
        'line': [0.0, 1.0, 0.0, 1.0, 1.0],
        'circle': [0.5, 0.5, 0.5, 0.5],
        'line_or_circle': 'line',
        'ciclogram': [np.linspace(0.5, 8, 16),
                      [0.4, 0.35, 0.2, 0.1, 0.2, 0.3, 0.35, 0.35, 0.45, 0.45, 0.5, 0.6, 0.7, 0.6, 0.45, 0.4],
                      [0.1, 0.2, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.2, 0.1]]
    }
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Моделирование роботов")
        self.setMinimumSize(535, 400)
        menu = self.menuBar()

        self.path_to_file = None
        self.data = copy.deepcopy(self.__data)

        #СПРАВОЧНАЯ ИНФОРМАЦИЯ------------------------------------------------------------------------------------------
        menu1 = menu.addMenu("Справочная информация")

        action1_about = QAction("About", self)
        action1_about.triggered.connect(self.show1_about_window)
        action1_robot_img = QAction("Схема робота", self)
        action1_robot_img.triggered.connect(self.show1_robot_img_window)
        action1_help = QAction("Помощь", self)
        action1_help.triggered.connect(self.show1_help_window)

        menu1.addAction(action1_about)
        menu1.addAction(action1_robot_img)
        menu1.addAction(action1_help)

        #СОХРАНЕНИЯ-----------------------------------------------------------------------------------------------------
        menu2 = menu.addMenu("Сохранения")

        action2_new = QAction("Новый", self)
        action2_new.triggered.connect(self.show2_new_window)
        action2_load = QAction("Загрузить", self)
        action2_load.triggered.connect(self.show2_load_window)
        action2_save = QAction("Сохранить", self)
        action2_save.triggered.connect(self.show2_save_window)
        action2_save_as = QAction("Сохранить как", self)
        action2_save_as.triggered.connect(self.show2_saveas_window)

        menu2.addAction(action2_new)
        menu2.addAction(action2_load)
        menu2.addAction(action2_save)
        menu2.addAction(action2_save_as)

        #РЕЖИМ РАБОТЫ---------------------------------------------------------------------------------------------------
        menu3 = menu.addMenu("Режим работы")

        action3_rob = QAction("Тип робота", self)
        action3_rob.triggered.connect(self.show3_select_robotype)
        action3_mov = QAction("Тип движения", self)
        action3_mov.triggered.connect(self.show3_select_movetype)

        menu3.addAction(action3_rob)
        menu3.addAction(action3_mov)

        #НАСТРОЙКА ПАРАМЕТРОВ-------------------------------------------------------------------------------------------
        menu4 = menu.addMenu("Настройка параметров")

        action4_param_dec = QAction("Конструктивные параметры", self)
        action4_param_dec.triggered.connect(self.show4_select_param_dec)
        action4_coord_dec = QAction("Ограничение по координатам", self)
        action4_coord_dec.triggered.connect(self.show4_select_coord_dec)

        action4_param_cil = QAction("Конструктивные параметры", self)
        action4_param_cil.triggered.connect(self.show4_select_param_cil)
        action4_coord_cil = QAction("Ограничение по координатам", self)
        action4_coord_cil.triggered.connect(self.show4_select_coord_cil)

        action4_param_scr = QAction("Конструктивные параметры", self)
        action4_param_scr.triggered.connect(self.show4_select_param_scr)
        action4_coord_scr = QAction("Ограничение по координатам", self)
        action4_coord_scr.triggered.connect(self.show4_select_coord_scr)

        action4_param_col = QAction("Конструктивные параметры", self)
        action4_param_col.triggered.connect(self.show4_select_param_col)
        action4_coord_col = QAction("Ограничение по координатам", self)
        action4_coord_col.triggered.connect(self.show4_select_coord_col)

        menu4_1 = menu4.addMenu("Робот")
        menu4_1_dec = menu4_1.addMenu("Декарт")
        menu4_1_dec.addAction(action4_param_dec)
        menu4_1_dec.addAction(action4_coord_dec)

        menu4_1_cil = menu4_1.addMenu("Цилиндр")
        menu4_1_cil.addAction(action4_param_cil)
        menu4_1_cil.addAction(action4_coord_cil)

        menu4_1_scr = menu4_1.addMenu("Скара")
        menu4_1_scr.addAction(action4_param_scr)
        menu4_1_scr.addAction(action4_coord_scr)

        menu4_1_col = menu4_1.addMenu("Колер")
        menu4_1_col.addAction(action4_param_col)
        menu4_1_col.addAction(action4_coord_col)

        action4_engine = QAction("Параметры двигателей", self)
        action4_engine.triggered.connect(self.show4_select_engine)
        action4_reg = QAction("Параметры регуляторов", self)
        action4_reg.triggered.connect(self.show4_select_reg)

        menu4_2 = menu4.addMenu("Система управления")
        menu4_2.addAction(action4_engine)
        menu4_2.addAction(action4_reg)

        action4_calc = QAction("Вычислитель", self)
        action4_calc.triggered.connect(self.show4_select_calc)
        menu4_3 = menu4.addAction(action4_calc)

        action4_pos_move = QAction("Позиционное", self)
        action4_pos_move.triggered.connect(self.show4_select_pos_move)
        action4_cont_line = QAction("Прямая", self)
        action4_cont_line.triggered.connect(self.show4_select_cont_line)
        action4_cont_circle = QAction("Окружность", self)
        action4_cont_circle.triggered.connect(self.show4_select_cont_circle)

        menu4_4 = menu4.addMenu("Движение")
        menu4_4.addAction(action4_pos_move)
        menu4_4_cont = menu4_4.addMenu("Контурное")
        menu4_4_line = menu4_4_cont.addAction(action4_cont_line)
        menu4_4_circle = menu4_4_cont.addAction(action4_cont_circle)

        #РАСЧЁТ---------------------------------------------------------------------------------------------------------
        menu5 = menu.addMenu("Расчёт")

        action5_show_area = QAction("Рабочая область", self)
        action5_show_area.triggered.connect(self.show5_graph)
        action5_plot = QAction("График", self)
        action5_plot.triggered.connect(lambda: self.show5_graph(with_graph=True))

        menu5.addAction(action5_show_area)
        menu5.addAction(action5_plot)

    #СПРАВОЧНАЯ ИНФОРМАЦИЯ ФУНКЦИИ--------------------------------------------------------------------------------------
    def show1_about_window(self, checked):
        self.w1_about = QWidget()
        self.w1_about.setFixedSize(360, 100)

        about = QLabel("Моделирование манипуляционных двухзвенных роботов\n "
                       "Декарт, Цилиндр, Скара, Колер\n Дипломный проект 2022-2023")
        about.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay1_about = QGridLayout()
        lay1_about.addWidget(about)

        self.w1_about.setLayout(lay1_about)
        self.w1_about.setWindowTitle("About")
        self.w1_about.show()

    def show1_robot_img_window(self, checked):
        self.w1_robot_img = QWidget()
        self.w1_robot_img.setFixedSize(500, 400)

        if self.data['robotype'] == 'Декарт':
            pixmap = QPixmap("Декарт.png")
        elif self.data['robotype'] == 'Цилиндр':
            pixmap = QPixmap("Цилиндр.png")
        elif self.data['robotype'] == 'Скара':
            pixmap = QPixmap("Скара.png")
        elif self.data['robotype'] == 'Колер':
            pixmap = QPixmap("Колер.png")

        pixmap = pixmap.scaled(500, 400)
        label = QLabel(self.w1_robot_img)
        label.setPixmap(pixmap)

        self.w1_robot_img.setWindowTitle(f'Схема робота {self.data["robotype"]}')
        self.w1_robot_img.show()

    def show1_help_window(self, checked):
        self.w1_help = QWidget()
        self.w1_help.setFixedSize(690, 520)
        help1 = QLabel("ПАКЕТ ПРИКЛАДНЫХ ПРОГРАММ\n «МОДЕЛИРОВАНИЕ РОБОТОВ»\n")
        help_text_file = open('help.txt', encoding='utf-8')
        help_text = help_text_file.read()
        help2 = QLabel(help_text)
        help_text_file.close()

        help1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay1_help = QGridLayout()
        lay1_help.addWidget(help1)
        lay1_help.addWidget(help2)

        self.w1_help.setLayout(lay1_help)
        self.w1_help.setWindowTitle("Помощь")
        self.w1_help.show()

    #СОХРАНЕНИЯ ФУНКЦИИ-------------------------------------------------------------------------------------------------
    def show2_new_window(self, checked):
        dig = CustomDialog(self, "Вы уверены, что хотите сбросить\n все настройки и начать заново?", "Внимание!")
        if dig.exec():
            self.path_to_file = None
            self.data = copy.deepcopy(self.__data)

    def show2_load_window(self, checked):
        load_file_name = QFileDialog.getOpenFileName(self, 'Выберите файл для загрузки')
        load_file_path = load_file_name[0]
        if load_file_path:
            with open(load_file_path, 'r', encoding='utf-8') as load_file:
                self.data = json.load(load_file)
            self.path_to_file = load_file_path

    def show2_save_window(self, checked):
        if self.path_to_file:
            with open(self.path_to_file, 'w', encoding='utf-8') as save_file:
                json.dump(self.data, save_file)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Выберите файл для сохранения')
            file_path = file_name[0] + '.json'
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.data, save_file)
                self.path_to_file = file_path

    def show2_saveas_window(self, checked):
        saveas_file_name = QFileDialog.getSaveFileName(self, 'Выберите файл для сохранения')
        saveas_file_path = saveas_file_name[0]
        if saveas_file_path:
            with open(saveas_file_path + '.json', 'w', encoding='utf-8') as save_file:
                json.dump(self.data, save_file)
            self.path_to_file = saveas_file_path

    #РЕЖИМ РАБОТЫ ФУНКЦИИ-----------------------------------------------------------------------------------------------
    def show3_select_robotype(self, checked):
        self.w3_robot = QWidget()
        self.w3_robot.setFixedSize(300, 120)

        check_robot1 = QCheckBox('Декарт')
        check_robot2 = QCheckBox('Цилиндр')
        check_robot3 = QCheckBox('Скара')
        check_robot4 = QCheckBox('Колер')

        self.rob_dict = {
            'Декарт': check_robot1,
            'Цилиндр': check_robot2,
            'Скара': check_robot3,
            'Колер': check_robot4
        }

        self.rob_dict[self.data['robotype']].setChecked(True)

        check_robot1.stateChanged.connect(self.show3_uncheck1)
        check_robot2.stateChanged.connect(self.show3_uncheck1)
        check_robot3.stateChanged.connect(self.show3_uncheck1)
        check_robot4.stateChanged.connect(self.show3_uncheck1)

        lay3_robot = QGridLayout()
        lay3_robot.addWidget(check_robot1)
        lay3_robot.addWidget(check_robot2)
        lay3_robot.addWidget(check_robot3)
        lay3_robot.addWidget(check_robot4)

        self.w3_robot.setLayout(lay3_robot)
        self.w3_robot.setWindowTitle("Тип робота")
        self.w3_robot.show()

    def show3_uncheck1(self, state):
        if state:
            if self.sender() == self.rob_dict['Декарт']:
                self.rob_dict['Цилиндр'].setChecked(False)
                self.rob_dict['Скара'].setChecked(False)
                self.rob_dict['Колер'].setChecked(False)
                self.data['robotype'] = 'Декарт'

            elif self.sender() == self.rob_dict['Цилиндр']:
                self.rob_dict['Декарт'].setChecked(False)
                self.rob_dict['Скара'].setChecked(False)
                self.rob_dict['Колер'].setChecked(False)
                self.data['robotype'] = 'Цилиндр'

            elif self.sender() == self.rob_dict['Скара']:
                self.rob_dict['Декарт'].setChecked(False)
                self.rob_dict['Цилиндр'].setChecked(False)
                self.rob_dict['Колер'].setChecked(False)
                self.data['robotype'] = 'Скара'

            elif self.sender() == self.rob_dict['Колер']:
                self.rob_dict['Декарт'].setChecked(False)
                self.rob_dict['Цилиндр'].setChecked(False)
                self.rob_dict['Скара'].setChecked(False)
                self.data['robotype'] = 'Колер'

    def show3_select_movetype(self, checked):
        self.w3_move = QWidget()
        self.w3_move.setFixedSize(300, 120)

        check_move1 = QCheckBox('Позиционное')
        check_move2 = QCheckBox('Контурное')

        self.move_dict = {
            'Позиционное': check_move1,
            'Контурное': check_move2,
        }

        self.move_dict[self.data['movetype']].setChecked(True)

        check_move1.stateChanged.connect(self.show3_uncheck2)
        check_move2.stateChanged.connect(self.show3_uncheck2)

        lay3_move = QGridLayout()
        lay3_move.addWidget(check_move1)
        lay3_move.addWidget(check_move2)

        self.w3_move.setLayout(lay3_move)
        self.w3_move.setWindowTitle("Тип движения")
        self.w3_move.show()

    def show3_uncheck2(self, state):
        if state:
            if self.sender() == self.move_dict['Позиционное']:
                self.move_dict['Контурное'].setChecked(False)
                self.data['movetype'] = 'Позиционное'

            elif self.sender() == self.move_dict['Контурное']:
                self.move_dict['Позиционное'].setChecked(False)
                self.data['movetype'] = 'Контурное'

    #НАСТРОЙКА ПАРАМЕТРОВ ФУНКЦИИ---------------------------------------------------------------------------------------
    #ДЕКАРТ ПАРАМЕТРЫ И ОГРАНИЧЕНИЯ-------------------------------------------------------------------------------------
    def show4_select_param_dec(self, checked):
        self.w4_param_dec = QWidget()
        self.w4_param_dec.setFixedSize(400, 80)

        label1_param_dec = QLabel('Масса 1-го звена')
        label2_param_dec = QLabel('Масса 2-го звена')
        label3_param_dec = QLabel('Момент инерции')

        param_dec = self.data['param_dec']
        input1_param_dec = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_dec[0])
        input1_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 0))
        input2_param_dec = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_dec[1])
        input2_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 1))
        input3_param_dec = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0,value = param_dec[2])
        input3_param_dec.valueChanged.connect(lambda change: self.show4_change_param_dec(change, 2))

        grid4_param_dec = QGridLayout()
        grid4_param_dec.addWidget(label1_param_dec, 0, 0)
        grid4_param_dec.addWidget(label2_param_dec, 0, 1)
        grid4_param_dec.addWidget(label3_param_dec, 0, 2)
        grid4_param_dec.addWidget(input1_param_dec, 1, 0)
        grid4_param_dec.addWidget(input2_param_dec, 1, 1)
        grid4_param_dec.addWidget(input3_param_dec, 1, 2)

        self.w4_param_dec.setLayout(grid4_param_dec)
        self.w4_param_dec.setWindowTitle("Конструктивные параметры Декарт")
        self.w4_param_dec.show()

    def show4_change_param_dec(self, change, key):
        self.data['param_dec'][key] = change

    def show4_select_coord_dec(self, checked):
        self.w4_coord_dec = QWidget()
        self.w4_coord_dec.setFixedSize(500, 80)

        label1_coord_dec = QLabel('Xmin')
        label2_coord_dec = QLabel('Xmax')
        label3_coord_dec = QLabel('Ymin')
        label4_coord_dec = QLabel('Ymax')

        coord_dec = self.data['coord_dec']
        input1_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[0])
        input1_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 0))
        input2_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[1])
        input2_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 1))
        input3_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[2])
        input3_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 2))
        input4_coord_dec = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_dec[3])
        input4_coord_dec.valueChanged.connect(lambda change: self.show4_change_coord_dec(change, 3))

        grid4_coord_dec = QGridLayout()
        grid4_coord_dec.addWidget(label1_coord_dec, 0, 0)
        grid4_coord_dec.addWidget(label2_coord_dec, 0, 1)
        grid4_coord_dec.addWidget(label3_coord_dec, 0, 2)
        grid4_coord_dec.addWidget(label4_coord_dec, 0, 3)
        grid4_coord_dec.addWidget(input1_coord_dec, 1, 0)
        grid4_coord_dec.addWidget(input2_coord_dec, 1, 1)
        grid4_coord_dec.addWidget(input3_coord_dec, 1, 2)
        grid4_coord_dec.addWidget(input4_coord_dec, 1, 3)

        self.w4_coord_dec.setLayout(grid4_coord_dec)
        self.w4_coord_dec.setWindowTitle("Ограничение по координатам Декарт")
        self.w4_coord_dec.show()

    def show4_change_coord_dec(self, change, key):
        self.data['coord_dec'][key] = change

    #ЦИЛИНДР ПАРАМЕТРЫ И ОГРАНИЧЕНИЯ------------------------------------------------------------------------------------
    def show4_select_param_cil(self, checked):
        self.w4_param_cil = QWidget()
        self.w4_param_cil.setFixedSize(400, 180)

        label1_param_cil = QLabel('Момент 1-го звена')
        label2_param_cil = QLabel('Момент 2-го звена')
        label3_param_cil = QLabel('Длина 1-го звена')
        label4_param_cil = QLabel('Расстояние')
        label5_param_cil = QLabel('Масса 1-го звена')
        label6_param_cil = QLabel('Масса 2-го звена')

        param_cil = self.data['param_cil']
        input1_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[0])
        input1_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 0))
        input2_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[1])
        input2_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 1))
        input3_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[2])
        input3_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 2))
        input4_param_cil = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_cil[3])
        input4_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 3))
        input5_param_cil = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_cil[4])
        input5_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 4))
        input6_param_cil = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_cil[5])
        input6_param_cil.valueChanged.connect(lambda change: self.show4_change_param_cil(change, 5))

        grid4_param_cil = QGridLayout()
        grid4_param_cil.addWidget(label1_param_cil, 0, 0)
        grid4_param_cil.addWidget(label2_param_cil, 0, 1)
        grid4_param_cil.addWidget(label3_param_cil, 0, 2)
        grid4_param_cil.addWidget(input1_param_cil, 1, 0)
        grid4_param_cil.addWidget(input2_param_cil, 1, 1)
        grid4_param_cil.addWidget(input3_param_cil, 1, 2)
        grid4_param_cil.addWidget(label4_param_cil, 2, 0)
        grid4_param_cil.addWidget(label5_param_cil, 2, 1)
        grid4_param_cil.addWidget(label6_param_cil, 2, 2)
        grid4_param_cil.addWidget(input4_param_cil, 3, 0)
        grid4_param_cil.addWidget(input5_param_cil, 3, 1)
        grid4_param_cil.addWidget(input6_param_cil, 3, 2)

        self.w4_param_cil.setLayout(grid4_param_cil)
        self.w4_param_cil.setWindowTitle("Конструктивные параметры Цилиндр")
        self.w4_param_cil.show()

    def show4_change_param_cil(self, change, key):
        self.data['param_cil'][key] = change

    def show4_select_coord_cil(self, checked):
        self.w4_coord_cil = QWidget()
        self.w4_coord_cil.setFixedSize(500, 80)

        label1_coord_cil = QLabel('A1min')
        label2_coord_cil = QLabel('A1max')
        label3_coord_cil = QLabel('Q2min')
        label4_coord_cil = QLabel('Q2max')

        coord_cil = self.data['coord_cil']
        input1_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[0])
        input1_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 0))
        input2_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_cil[1])
        input2_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 1))
        input3_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_cil[2])
        input3_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 2))
        input4_coord_cil = QDoubleSpinBox(decimals=3, singleStep=0.001,  maximum=1, minimum=0, value=coord_cil[3])
        input4_coord_cil.valueChanged.connect(lambda change: self.show4_change_coord_cil(change, 3))

        grid4_coord_cil = QGridLayout()
        grid4_coord_cil.addWidget(label1_coord_cil, 0, 0)
        grid4_coord_cil.addWidget(label2_coord_cil, 0, 1)
        grid4_coord_cil.addWidget(label3_coord_cil, 0, 2)
        grid4_coord_cil.addWidget(label4_coord_cil, 0, 3)
        grid4_coord_cil.addWidget(input1_coord_cil, 1, 0)
        grid4_coord_cil.addWidget(input2_coord_cil, 1, 1)
        grid4_coord_cil.addWidget(input3_coord_cil, 1, 2)
        grid4_coord_cil.addWidget(input4_coord_cil, 1, 3)

        self.w4_coord_cil.setLayout(grid4_coord_cil)
        self.w4_coord_cil.setWindowTitle("Ограничение по координатам Цилиндр")
        self.w4_coord_cil.show()

    def show4_change_coord_cil(self, change, key):
        self.data['coord_cil'][key] = change

    #СКАРА ПАРАМЕТРЫ И ОГРАНИЧЕНИЯ--------------------------------------------------------------------------------------
    def show4_select_param_scr(self, checked):
        self.w4_param_scr = QWidget()
        self.w4_param_scr.setFixedSize(500, 180)

        label1_param_scr = QLabel('Момент 1-го звена')
        label2_param_scr = QLabel('Момент 2-го звена')
        label3_param_scr = QLabel('Длина 1-го звена')
        label4_param_scr = QLabel('Длина 2-го звена')
        label5_param_scr = QLabel('Расстояние')
        label6_param_scr = QLabel('Масса 1-го звена')
        label7_param_scr = QLabel('Масса 2-го звена')

        param_scr = self.data['param_scr']
        input1_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[0])
        input1_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 0))
        input2_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[1])
        input2_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 1))
        input3_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[2])
        input3_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 2))
        input4_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[3])
        input4_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 3))
        input5_param_scr = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_scr[4])
        input5_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 4))
        input6_param_scr = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_scr[5])
        input6_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 5))
        input7_param_scr = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_scr[6])
        input7_param_scr.valueChanged.connect(lambda change: self.show4_change_param_scr(change, 6))

        grid4_param_scr = QGridLayout()
        grid4_param_scr.addWidget(label1_param_scr, 0, 0)
        grid4_param_scr.addWidget(label2_param_scr, 0, 1)
        grid4_param_scr.addWidget(label3_param_scr, 0, 2)
        grid4_param_scr.addWidget(label4_param_scr, 0, 3)
        grid4_param_scr.addWidget(input1_param_scr, 1, 0)
        grid4_param_scr.addWidget(input2_param_scr, 1, 1)
        grid4_param_scr.addWidget(input3_param_scr, 1, 2)
        grid4_param_scr.addWidget(input4_param_scr, 1, 3)

        grid4_param_scr.addWidget(label5_param_scr, 2, 0)
        grid4_param_scr.addWidget(label6_param_scr, 2, 1)
        grid4_param_scr.addWidget(label7_param_scr, 2, 2)
        grid4_param_scr.addWidget(input5_param_scr, 3, 0)
        grid4_param_scr.addWidget(input6_param_scr, 3, 1)
        grid4_param_scr.addWidget(input7_param_scr, 3, 2)

        self.w4_param_scr.setLayout(grid4_param_scr)
        self.w4_param_scr.setWindowTitle("Конструктивные параметры Скара")
        self.w4_param_scr.show()

    def show4_change_param_scr(self, change, key):
        self.data['param_scr'][key] = change

    def show4_select_coord_scr(self, checked):
        self.w4_coord_scr = QWidget()
        self.w4_coord_scr.setFixedSize(500, 80)

        label1_coord_scr = QLabel('Q1min')
        label2_coord_scr = QLabel('Q1max')
        label3_coord_scr = QLabel('Q2min')
        label4_coord_scr = QLabel('Q2max')

        coord_scr = self.data['coord_scr']
        input1_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[0])
        input1_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 0))
        input2_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[1])
        input2_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 1))
        input3_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[2])
        input3_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 2))
        input4_coord_scr = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_scr[3])
        input4_coord_scr.valueChanged.connect(lambda change: self.show4_change_coord_scr(change, 3))

        grid4_coord_scr = QGridLayout()
        grid4_coord_scr.addWidget(label1_coord_scr, 0, 0)
        grid4_coord_scr.addWidget(label2_coord_scr, 0, 1)
        grid4_coord_scr.addWidget(label3_coord_scr, 0, 2)
        grid4_coord_scr.addWidget(label4_coord_scr, 0, 3)
        grid4_coord_scr.addWidget(input1_coord_scr, 1, 0)
        grid4_coord_scr.addWidget(input2_coord_scr, 1, 1)
        grid4_coord_scr.addWidget(input3_coord_scr, 1, 2)
        grid4_coord_scr.addWidget(input4_coord_scr, 1, 3)

        self.w4_coord_scr.setLayout(grid4_coord_scr)
        self.w4_coord_scr.setWindowTitle("Ограничение по координатам Скара")
        self.w4_coord_scr.show()

    def show4_change_coord_scr(self, change, key):
        self.data['coord_scr'][key] = change

    #КОЛЕР ПАРАМЕТРЫ И ОГРАНИЧЕНИЯ--------------------------------------------------------------------------------------
    def show4_select_param_col(self, checked):
        self.w4_param_col = QWidget()
        self.w4_param_col.setFixedSize(400, 180)

        label1_param_col = QLabel('Момент 1-го звена')
        label2_param_col = QLabel('Момент 2-го звена')
        label3_param_col = QLabel('Длина 2-го звена')
        label4_param_col = QLabel('Расстояние')
        label5_param_col = QLabel('Масса 1-го звена')
        label6_param_col = QLabel('Масса 2-го звена')

        param_col = self.data['param_col']
        input1_param_col = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_col[0])
        input1_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 0))
        input2_param_col = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_col[1])
        input2_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 1))
        input3_param_col = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_col[2])
        input3_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 2))
        input4_param_col = QDoubleSpinBox(singleStep = 0.1, maximum = 1, minimum = 0, value = param_col[3])
        input4_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 3))
        input5_param_col = QDoubleSpinBox(maximum = 20, minimum = 0, value = param_col[4])
        input5_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 4))
        input6_param_col = QDoubleSpinBox(maximum = 20, minimum = 0,value = param_col[5])
        input6_param_col.valueChanged.connect(lambda change: self.show4_change_param_col(change, 5))

        grid4_param_col = QGridLayout()
        grid4_param_col.addWidget(label1_param_col, 0, 0)
        grid4_param_col.addWidget(label2_param_col, 0, 1)
        grid4_param_col.addWidget(label3_param_col, 0, 2)
        grid4_param_col.addWidget(input1_param_col, 1, 0)
        grid4_param_col.addWidget(input2_param_col, 1, 1)
        grid4_param_col.addWidget(input3_param_col, 1, 2)
        grid4_param_col.addWidget(label4_param_col, 2, 0)
        grid4_param_col.addWidget(label5_param_col, 2, 1)
        grid4_param_col.addWidget(label6_param_col, 2, 2)
        grid4_param_col.addWidget(input4_param_col, 3, 0)
        grid4_param_col.addWidget(input5_param_col, 3, 1)
        grid4_param_col.addWidget(input6_param_col, 3, 2)

        self.w4_param_col.setLayout(grid4_param_col)
        self.w4_param_col.setWindowTitle("Конструктивные параметры Колер")
        self.w4_param_col.show()

    def show4_change_param_col(self, change, key):
        self.data['param_col'][key] = change

    def show4_select_coord_col(self, checked):
        self.w4_coord_col = QWidget()
        self.w4_coord_col.setFixedSize(500, 80)

        label1_coord_col = QLabel('Q1min')
        label2_coord_col = QLabel('Q1max')
        label3_coord_col = QLabel('A2min')
        label4_coord_col = QLabel('A2max')

        coord_col = self.data['coord_col']
        input1_coord_col = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_col[0])
        input1_coord_col.valueChanged.connect(lambda change: self.show4_change_coord_col(change, 0))
        input2_coord_col = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=coord_col[1])
        input2_coord_col.valueChanged.connect(lambda change: self.show4_change_coord_col(change, 1))
        input3_coord_col = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=3.124, minimum=-3.124, value=coord_col[2])
        input3_coord_col.valueChanged.connect(lambda change: self.show4_change_coord_col(change, 2))
        input4_coord_col = QDoubleSpinBox(decimals=3, singleStep=0.001,  maximum=3.124, minimum=-3.124, value=coord_col[3])
        input4_coord_col.valueChanged.connect(lambda change: self.show4_change_coord_col(change, 3))

        grid4_coord_col = QGridLayout()
        grid4_coord_col.addWidget(label1_coord_col, 0, 0)
        grid4_coord_col.addWidget(label2_coord_col, 0, 1)
        grid4_coord_col.addWidget(label3_coord_col, 0, 2)
        grid4_coord_col.addWidget(label4_coord_col, 0, 3)
        grid4_coord_col.addWidget(input1_coord_col, 1, 0)
        grid4_coord_col.addWidget(input2_coord_col, 1, 1)
        grid4_coord_col.addWidget(input3_coord_col, 1, 2)
        grid4_coord_col.addWidget(input4_coord_col, 1, 3)

        self.w4_coord_col.setLayout(grid4_coord_col)
        self.w4_coord_col.setWindowTitle("Ограничение по координатам Колер")
        self.w4_coord_col.show()

    def show4_change_coord_col(self, change, key):
        self.data['coord_col'][key] = change

    #ПАРАМЕТРЫ ДВИГАТЕЛЕЙ-----------------------------------------------------------------------------------------------
    def show4_select_engine(self, checked):
        self.w4_engine = QWidget()
        self.w4_engine.setFixedSize(300, 260)

        label1_eng = QLabel('J1')
        label2_eng = QLabel('J2')
        label3_eng = QLabel('n1')
        label4_eng = QLabel('n2')
        label5_eng = QLabel('U1max')
        label6_eng = QLabel('U2max')
        label7_eng = QLabel('Ku1')
        label8_eng = QLabel('Ku2')
        label9_eng = QLabel('Kq1')
        label10_eng = QLabel('Kq2')

        eng = self.data['engine']
        input1_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[0])
        input1_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 0))
        input2_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=1, minimum=0, value=eng[1])
        input2_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 1))
        input3_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[2])
        input3_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 2))
        input4_eng = QDoubleSpinBox(maximum=500, minimum=0, value=eng[3])
        input4_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 3))
        input5_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[4])
        input5_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 4))
        input6_eng = QDoubleSpinBox(maximum=40, minimum=0, value=eng[5])
        input6_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 5))
        input7_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[6])
        input7_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 6))
        input8_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[7])
        input8_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 7))
        input9_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[8])
        input9_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 8))
        input10_eng = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=0.1, minimum=0, value=eng[9])
        input10_eng.valueChanged.connect(lambda change: self.show4_change_eng(change, 9))

        grid4_eng = QGridLayout()
        grid4_eng.addWidget(label1_eng, 0, 0)
        grid4_eng.addWidget(label2_eng, 0, 1)
        grid4_eng.addWidget(input1_eng, 1, 0)
        grid4_eng.addWidget(input2_eng, 1, 1)

        grid4_eng.addWidget(label3_eng, 2, 0)
        grid4_eng.addWidget(label4_eng, 2, 1)
        grid4_eng.addWidget(input3_eng, 3, 0)
        grid4_eng.addWidget(input4_eng, 3, 1)

        grid4_eng.addWidget(label5_eng, 4, 0)
        grid4_eng.addWidget(label6_eng, 4, 1)
        grid4_eng.addWidget(input5_eng, 5, 0)
        grid4_eng.addWidget(input6_eng, 5, 1)

        grid4_eng.addWidget(label7_eng, 6, 0)
        grid4_eng.addWidget(label8_eng, 6, 1)
        grid4_eng.addWidget(input7_eng, 7, 0)
        grid4_eng.addWidget(input8_eng, 7, 1)

        grid4_eng.addWidget(label9_eng, 8, 0)
        grid4_eng.addWidget(label10_eng, 8, 1)
        grid4_eng.addWidget(input9_eng, 9, 0)
        grid4_eng.addWidget(input10_eng, 9, 1)

        self.w4_engine.setLayout(grid4_eng)
        self.w4_engine.setWindowTitle("Параметры двигателей")
        self.w4_engine.show()

    def show4_change_eng(self, change, key):
        self.data['engine'][key] = change

    #ПАРАМЕТРЫ РЕГУЛЯТОРОВ----------------------------------------------------------------------------------------------
    def show4_select_reg(self, checked):
        self.w4_reg = QWidget()
        self.w4_reg.setFixedSize(310, 200)

        label1_reg = QLabel('Кп1')
        label2_reg = QLabel('Кп2')
        label3_reg = QLabel('Ки1')
        label4_reg = QLabel('Ки2')
        label5_reg = QLabel('Кд1')
        label6_reg = QLabel('Кд2')

        reg = self.data['reg']
        input1_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[0])
        input1_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 0))
        input2_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[1])
        input2_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 1))
        input3_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[2])
        input3_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 2))
        input4_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[3])
        input4_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 3))
        input5_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[4])
        input5_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 4))
        input6_reg = QDoubleSpinBox(decimals=3, singleStep=0.001, maximum=500, minimum=0, value=reg[5])
        input6_reg.valueChanged.connect(lambda change: self.show4_change_reg(change, 5))

        grid4_reg = QGridLayout()
        grid4_reg.addWidget(label1_reg, 0, 0)
        grid4_reg.addWidget(label2_reg, 0, 1)
        grid4_reg.addWidget(input1_reg, 1, 0)
        grid4_reg.addWidget(input2_reg, 1, 1)
        grid4_reg.addWidget(label3_reg, 2, 0)
        grid4_reg.addWidget(label4_reg, 2, 1)
        grid4_reg.addWidget(input3_reg, 3, 0)
        grid4_reg.addWidget(input4_reg, 3, 1)
        grid4_reg.addWidget(label5_reg, 4, 0)
        grid4_reg.addWidget(label6_reg, 4, 1)
        grid4_reg.addWidget(input5_reg, 5, 0)
        grid4_reg.addWidget(input6_reg, 5, 1)

        self.w4_reg.setLayout(grid4_reg)
        self.w4_reg.setWindowTitle("Параметры регуляторов")
        self.w4_reg.show()

    def show4_change_reg(self, change, key):
        self.data['reg'][key] = change

    #ПАРАМЕТРЫ ВЫЧИСЛИТЕЛЯ----------------------------------------------------------------------------------------------
    def show4_select_calc(self, checked):
        self.w4_calc = QWidget()
        self.w4_calc.setFixedSize(500, 100)

        label1_calc = QLabel('Разрядность')
        label2_calc = QLabel('Такт управления')
        label3_calc = QLabel('Такт обмена')
        label4_calc = QLabel('Постоянная фильтра')

        calc = self.data['calc']
        input1_calc = QDoubleSpinBox(maximum = 32, minimum = 2, value = calc[0])
        input1_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 0))
        input2_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[1])
        input2_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 1))
        input3_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[2])
        input3_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 2))
        input4_calc = QDoubleSpinBox(decimals = 3, singleStep = 0.001, maximum = 1, minimum = 0, value = calc[3])
        input4_calc.valueChanged.connect(lambda change: self.show4_change_calc(change, 3))

        grid4_calc = QGridLayout()
        grid4_calc.addWidget(label1_calc, 0, 0)
        grid4_calc.addWidget(label2_calc, 0, 1)
        grid4_calc.addWidget(label3_calc, 0, 2)
        grid4_calc.addWidget(label4_calc, 0, 3)
        grid4_calc.addWidget(input1_calc, 1, 0)
        grid4_calc.addWidget(input2_calc, 1, 1)
        grid4_calc.addWidget(input3_calc, 1, 2)
        grid4_calc.addWidget(input4_calc, 1, 3)

        self.w4_calc.setLayout(grid4_calc)
        self.w4_calc.setWindowTitle("Параметры вычислителей")
        self.w4_calc.show()

    def show4_change_calc(self, change, key):
        self.data['calc'][key] = change

    #ПОЗИЦИОННОЕ ДВИЖЕНИЕ(ЦИКЛОГРАММА)----------------------------------------------------------------------------------
    def show4_select_pos_move(self, checked):
        self.w4_pos_move = QWidget()
        self.w4_pos_move.setFixedSize(1000, 180)

        labels = ['t', 'q1', 'q2']
        pos_move_dict = {
            't': 100,
            'q1': 300,
            'q2': 300}

        grid4_pos_move = QGridLayout()
        for row, label in enumerate(labels):
            value_label = QLabel(label)
            grid4_pos_move.addWidget(value_label, row, 0)
            for col in range(16):
                params = {
                    'decimals': 2,
                    'value': self.data['ciclogram'][row][col],
                    'minimum': -pos_move_dict[label],
                    'maximum': pos_move_dict[label]
                }
                sp_box = MySpinBox([row, col], params)
                sp_box.valueChanged.connect(self.show4_get_pos_values)
                grid4_pos_move.addWidget(sp_box, row, col + 1)

        self.w4_pos_move.setLayout(grid4_pos_move)
        self.w4_pos_move.setWindowTitle('Циклограмма')
        self.w4_pos_move.show()

    def show4_get_pos_values(self, change):
        row, col = self.sender().ind
        self.data['ciclogram'][row][col] = change

    #КОНТУРНОЕ ДВИЖЕНИЕ(ПРЯМАЯ)-----------------------------------------------------------------------------------------
    def show4_select_cont_line(self, checked):
        self.w4_cont_line = QWidget()
        self.w4_cont_line.setFixedSize(500, 100)
        show_graph_line = QPushButton('Показать')
        show_graph_line.clicked.connect(self.show5_graph)

        label1_cont_line = QLabel('x1')
        label2_cont_line = QLabel('x2')
        label3_cont_line = QLabel('y1')
        label4_cont_line = QLabel('y2')
        label5_cont_line = QLabel('Скорость')

        self.data['line_or_circle'] = 'line'
        line = self.data['line']
        input1_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[0])
        input1_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 0))
        input2_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[1])
        input2_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 1))
        input3_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[2])
        input3_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 2))
        input4_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[3])
        input4_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 3))
        input5_cont_line = QDoubleSpinBox(maximum=10, minimum=0, value=line[4])
        input5_cont_line.valueChanged.connect(lambda change: self.show4_change_line(change, 4))

        grid4_cont_line = QGridLayout()
        grid4_cont_line.addWidget(label1_cont_line, 0, 0)
        grid4_cont_line.addWidget(label2_cont_line, 0, 1)
        grid4_cont_line.addWidget(label3_cont_line, 0, 2)
        grid4_cont_line.addWidget(label4_cont_line, 0, 3)
        grid4_cont_line.addWidget(label5_cont_line, 0, 4)
        grid4_cont_line.addWidget(input1_cont_line, 1, 0)
        grid4_cont_line.addWidget(input2_cont_line, 1, 1)
        grid4_cont_line.addWidget(input3_cont_line, 1, 2)
        grid4_cont_line.addWidget(input4_cont_line, 1, 3)
        grid4_cont_line.addWidget(input5_cont_line, 1, 4)
        grid4_cont_line.addWidget(show_graph_line, 2, 4)

        self.w4_cont_line.setLayout(grid4_cont_line)
        self.w4_cont_line.setWindowTitle("Прямая")
        self.w4_cont_line.show()

    def show4_change_line(self, change, key):
        self.data['line'][key] = change

    #КОНТУРНОЕ ДВИЖЕНИЕ(ОКРУЖНОСТЬ)-------------------------------------------------------------------------------------
    def show4_select_cont_circle(self, checked):
        self.w4_cont_circle = QWidget()
        self.w4_cont_circle.setFixedSize(400, 100)
        show_graph_circle = QPushButton('Показать')
        show_graph_circle.clicked.connect(self.show5_graph)

        label1_cont_circle = QLabel('x')
        label2_cont_circle = QLabel('y')
        label3_cont_circle = QLabel('r')
        label4_cont_circle = QLabel('Скорость')

        self.data['line_or_circle'] = 'circle'
        circle = self.data['circle']
        input1_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[0])
        input1_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 0))
        input2_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[1])
        input2_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 1))
        input3_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[2])
        input3_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 2))
        input4_cont_circle = QDoubleSpinBox(maximum=1000, minimum=0, value=circle[3])
        input4_cont_circle.valueChanged.connect(lambda change: self.show4_change_circle(change, 3))

        grid4_cont_circle = QGridLayout()
        grid4_cont_circle.addWidget(label1_cont_circle, 0, 0)
        grid4_cont_circle.addWidget(label2_cont_circle, 0, 1)
        grid4_cont_circle.addWidget(label3_cont_circle, 0, 2)
        grid4_cont_circle.addWidget(label4_cont_circle, 0, 3)
        grid4_cont_circle.addWidget(input1_cont_circle, 1, 0)
        grid4_cont_circle.addWidget(input2_cont_circle, 1, 1)
        grid4_cont_circle.addWidget(input3_cont_circle, 1, 2)
        grid4_cont_circle.addWidget(input4_cont_circle, 1, 3)
        grid4_cont_circle.addWidget(show_graph_circle, 2, 3)

        self.w4_cont_circle.setLayout(grid4_cont_circle)
        self.w4_cont_circle.setWindowTitle("Окружность")
        self.w4_cont_circle.show()

    def show4_change_circle(self, change, key):
        self.data['circle'][key] = change

    #РАСЧЁТ РАБОЧЕЙ ОБЛАСТИ---------------------------------------------------------------------------------------------
    def show5_graph(self, with_graph=False):
        self.workspace_plot = QWidget()
        self.workspace_plot.setFixedSize(700, 700)
        if with_graph:
            self.workspace_plot.setWindowTitle(f'Построение контура: {self.data["robotype"]}')
        else:
            self.workspace_plot.setWindowTitle(f'Рабочая область: {self.data["robotype"]}')

        layout = QVBoxLayout(self.workspace_plot)
        x_ticks = np.linspace(-1, 1, 11)
        y_ticks = np.linspace(0, 2, 11)

        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        sns.set_style('whitegrid')

        self._static_ax = self.fig.subplots()
        self._static_ax.plot()
        self._static_ax.set_xlim([-1, 1])
        self._static_ax.set_ylim([0, 2])
        self._static_ax.set_xticks(x_ticks)
        self._static_ax.set_yticks(y_ticks)

    #РАБОЧАЯ ОБЛАСТЬ ДЕКАРТ---------------------------------------------------------------------------------------------
        if self.data['robotype'] == 'Декарт':
            x_ax = self.data['coord_dec'][0:2]
            y_min, y_max = self.data['coord_dec'][2:4]
            self._static_ax.fill_between(x_ax, [y_min, y_min], [y_max, y_max], color='C0', alpha=0.3)
    #РАБОЧАЯ ОБЛАСТЬ ЦИЛИНДР--------------------------------------------------------------------------------------------
        elif self.data['robotype'] == 'Цилиндр':
            edge_len = self.data['param_cil'][2]
            a_min, a_max = self.data['coord_cil'][0:2]
            q_min, q_max = self.data['coord_cil'][2:4]
            q_min = edge_len + q_min
            q_max = edge_len + q_max

            wedge = patches.Wedge(
                (0, 0),
                q_max,
                np.degrees(a_min) + 90,
                np.degrees(a_max) + 90,
                color = 'C0',
                alpha = 0.3,
                width = q_max - q_min
            )

            self._static_ax.add_artist(wedge)

        #РАБОЧАЯ ОБЛАСТЬ СКАРА------------------------------------------------------------------------------------------
        elif self.data['robotype'] == 'Скара':
            pass

        #РАБОЧАЯ ОБЛАСТЬ КОЛЕР------------------------------------------------------------------------------------------
        elif self.data['robotype'] == 'Колер':
            edge_len = self.data['param_col'][2]
            q_min, q_max = self.data['coord_col'][0:2]
            a_min, a_max = self.data['coord_col'][2:4]
            q_min = edge_len + q_min
            q_max = edge_len + q_max + 0.05
            ymin = np.arange(-q_min - 0.001, q_min + 0.001, 0.001)
            ymax = ymin + (q_max - q_min)
            xmin = (q_min ** 2 - ymin ** 2) ** 0.5
            xmax = (q_min ** 2 - (ymax - (q_max - q_min)) ** 2) ** 0.5

            pos_x_max = xmax
            neg_x_max = -xmax[::-1]
            neg_x_min = -xmin
            pos_x_min = xmin[::-1]

            pos_y_max = ymax
            neg_y_max = ymax[::-1]
            neg_y_min = ymin
            pos_y_min = ymin[::-1]

            pos_ratio = -(a_min / np.pi)
            pos_x_max = pos_x_max[int(pos_x_max.shape[0] * (1 - pos_ratio)):]
            pos_y_max = pos_y_max[int(pos_y_max.shape[0] * (1 - pos_ratio)):]
            pos_x_min = pos_x_min[:int(pos_x_min.shape[0] * pos_ratio)]
            pos_y_min = pos_y_min[:int(pos_y_min.shape[0] * pos_ratio)]

            neg_ratio = (a_max / np.pi)
            neg_x_max = neg_x_max[:int(neg_x_max.shape[0] * neg_ratio)]
            neg_y_max = neg_y_max[:int(neg_y_max.shape[0] * neg_ratio)]
            neg_x_min = neg_x_min[int(neg_x_min.shape[0] * (1 - neg_ratio)):]
            neg_y_min = neg_y_min[int(neg_y_min.shape[0] * (1 - neg_ratio)):]

            circle__x_array = np.nan_to_num(
                np.concatenate((pos_x_max, neg_x_max, neg_x_min, pos_x_min))
            )
            circle__y_array = np.nan_to_num(
                np.concatenate((pos_y_max, neg_y_max, neg_y_min, pos_y_min))
            )

            circle__y_array = circle__y_array[(circle__x_array < 0.57) & (circle__x_array > -0.57)]
            circle__x_array = circle__x_array[(circle__x_array < 0.57) & (circle__x_array > -0.57)]

            self._static_ax.fill(circle__x_array, circle__y_array, color='C0', alpha=0.3)

        #ПОКАЗАТЬ КОНТУР------------------------------------------------------------------------------------------------
        if self.data['movetype'] == 'Контурное':
            if self.data['line_or_circle'] == 'circle':
                x, y, r = self.data['circle'][:3]
                circle = patches.Circle((x, y), r, fill=False, edgecolor='green')
                self._static_ax.add_patch(circle)
            elif self.data['line_or_circle'] == 'line':
                x1, x2, y1, y2 = self.data['line'][:4]
                self._static_ax.plot([x1, x2], [y1, y2], color='green')

        #ОТРИСОВКА------------------------------------------------------------------------------------------------------
        if with_graph:
            q1_array = [] if self.data['robotype'] != 'Декарт' else self.data['ciclogram'][1]
            q2_array = [] if self.data['robotype'] != 'Декарт' else self.data['ciclogram'][2]
            if self.data['robotype'] == 'Цилиндр':
                for i in range(16):
                    q1 = (self.data['param_cil'][2] + self.data['ciclogram'][2][i]) * np.sin(self.data['ciclogram'][1][i])
                    #q1 = -(np.arctan(self.data['ciclogram'][1][i]/self.data['ciclogram'][2][i]))
                    q2 = (self.data['param_cil'][2] + self.data['ciclogram'][2][i]) * np.cos(self.data['ciclogram'][1][i])
                    #q2 = (np.sqrt(self.data['ciclogram'][1][i]**2 + self.data['ciclogram'][2][i]**2) - self.data['param_cil'][2])
                    q1_array.append(q1)
                    q2_array.append(q2)
            elif self.data['robotype'] == 'Скара':
                for i in range(16):
                    q1 = (self.data['param_scr'][2] * np.sin(self.data['ciclogram'][1][i]) +
                          self.data['param_scr'][3] * np.sin(np.sin(self.data['ciclogram'][1][i] + self.data['ciclogram'][2][i])))
                    #q1 = q1 * (self.data['param_scr'][0] + self.data['engine'][0]*self.data['engine'][2]*self.data['engine'][2] +
                    #           self.data['param_scr'][6]*self.data['param_scr'][2]*self.data['param_scr'][2] +
                    #           self.data['param_scr'][6]*self.data['param_scr'][4]*self.data['param_scr'][4] +
                    #           self.data['param_scr'][1]*(self.data['param_scr'][2]*self.data['param_scr'][2] +
                    #                                      self.data['param_scr'][3]*self.data['param_scr'][3]))

                    q2 = (self.data['param_scr'][2] * np.cos(self.data['ciclogram'][1][i]) +
                          self.data['param_scr'][3] * np.cos(np.cos(self.data['ciclogram'][1][i] + self.data['ciclogram'][2][i])))
                    #q2 = q2 * (2*self.data['param_scr'][6]*self.data['param_scr'][2]*self.data['param_scr'][4]+
                    #           2*self.data['param_scr'][2]*self.data['param_scr'][3])

                    q1_array.append(q1)
                    q2_array.append(q2)
            elif self.data['robotype'] == 'Колер':
                for i in range(16):
                    q1 = (self.data['param_col'][2] * np.sin(self.data['ciclogram'][2][i]))
                    #q1 = (self.data['ciclogram'][2][i] - np.sqrt(self.data['param_col'][2]**2 - self.data['ciclogram'][1][i]**2))
                    q2 = (self.data['ciclogram'][1][i] + self.data['param_col'][2] * np.cos(self.data['ciclogram'][2][i]))
                    #q2 = (np.arcsin(-self.data['ciclogram'][1][i]/self.data['param_col'][2]))
                    q1_array.append(q1)
                    q2_array.append(q2)
            self.q1 = q1_array
            self.q2 = q2_array

            self.graph_animation = anim.FuncAnimation(self.fig, self.show5_anim,
                                                      frames=len(self.data['ciclogram'][1]),
                                                      interval=100 * self.data['ciclogram'][0][-1], repeat=False)

        self.workspace_plot.show()

    def show5_anim(self, i):
        if i >= 1:
            self._static_ax.plot((self.q1[i - 1], self.q1[i]),
                                 (self.q2[i - 1], self.q2[i]),
                                 lw=1, color='red')
        self._static_ax.scatter(self.q1[i], self.q2[i],
                                 s=15, color='red')

app = QApplication(sys.argv)
window = OpenWindow()
window.show()
app.exec() 