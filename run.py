# -*- coding: utf-8 -*-
from AutoHotPy import AutoHotPy  # we need to tell python that we are going to use the library
#from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import time
import pyautogui
import threading
import datetime
import shutil
from functions import *

"""
Future improvings:
1. Попробовать объединить или сделать так что бы close_endless_cycle автоматом вызывала stop_programm 
2. Отладить цикл нажатий, помнять кнопки мыши с правой на левую
3. Вытсавить корректный time.sleep()
"""

myflag=True

def hear_exit(): #данная функция только слушает, если услышит то делает флаг False
    auto = AutoHotPy()
    auto.registerExit(auto.ESC, close_endless_cycle)
    auto.start()

def do_moovs(): #эта функция двигает
    global myflag
    auto = AutoHotPy()
    auto.registerExit(auto.X, stop_programm)
    auto.registerForKeyDown(auto.A, superCombo)
    auto.start()

def close_endless_cycle(autohotpy, event): #выходит из бесконечного цикла кликера
    global myflag
    myflag=False
    autohotpy.stop()
    print("ESC is pressed, exiting the clicker")

def stop_programm(autohotpy, event): #закрывает программу
    autohotpy.stop()
    print("X is pressed, closing the programm")

def left_click(autohotpy, event):
    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)

def superCombo(autohotpy, event): #действия в бесконечном цикле прерываем флагом
    """
    Бесконечная многозадачная функция, которая:
    1. Получает координаты окна аукциона
    2. Проваливается в бесконечный цикл, где она:
        - Обновляет страницу аукциона
        - Достает дату (предмет, цена) путем создания отдельных скринов
        - Проверяет дату, а после пишет в базу
        - Проверяет дату и после сверяет ее с предметами Х по цене У, если предметы найдены - покупает/пищит
    NOTE: На текущем уровне владения python, функцию невозможно сократить ввиду переданных только сюда autohotpy, event
    """
    print("A is pressed, starting endless clicking cycle")

    #Сперва сотрем старый и создадим пустой кеш, обнулим счетчик
    shutil.rmtree("cash/")
    time.sleep(1)
    os.mkdir("cash")
    count = 0

    #Достанем координаты окна аукциона
    coord = make_screen_get_coordinates()

    #Запускаем бесконечный цикл, прерывваем по флагу, который устанавливает через ESC параллельным тредом
    while myflag is True:
        #создадим текущую дату, которая после передается в функцию записи в базу и создание директорий
        now = datetime.datetime.now()
        current_time = now.strftime("%D:%H:%M:%S")

        #принт служебной информации/лога
        count+=1
        print(f"\n"
              f"Попытка номер: {count}, время: {current_time} ")

        #двигаемся к кнопке обновления ауциона
        #через раз кликаем то на ближнее, то на дальнее оружие
        if count%2==0:
            pyautogui.moveTo(coord["x"], coord["y"], 2) #двигаемся к началу и обновляем страницу аукцциона
            autohotpy.moveMouseToPosition(coord["x"], coord["y"])
            time.sleep(1) #нужен ли он? после убрать
        else:
            pyautogui.moveTo(coord["x"], coord["y"]+30, 2)
            autohotpy.moveMouseToPosition(coord["x"], coord["y"]+30)
            time.sleep(1)

        #делаем щелчок
        left_click(autohotpy, event) #необходимо передавать эти атрбиуты из родительской функции, иначе не работает

        time.sleep(2) #очень важный таймаут, аук обновляется не сразу (0,5 сек), зато скрин делается мгновенно

        #достаем дату с текущей страницы аукциона
        massives = get_data(coord, current_time)

        #пишем результат в базу с текущем временем
        write_db(massives, current_time)

        #достаем позиции к покупке, пишем лог-файл с текущем временем
        buy = position_to_buy(massives, current_time)

        print(buy, " это наш массив buy") #мусор, потом удалить, оставить на этапе отладки

        #если очередь на покупку ненулевая, то покупаем указанные в очереди вещи
        if len(buy)>0:
            for i in buy:
                #print("Покупаю шмотку на позиции: ", i)
                x = coord["x"] + 700  # смещаемся вправо на 700 пикселей
                #print("Двигаемся к координате X: ", x)
                y = coord["y"] + 20 + i * 50  # смещаемся уть вниз на 20 и потом на порядок шмотки в списке
                #print("Двигаемся к координате Y: ", y)

                #совершаем плавное движение, если не сработало то резкое
                pyautogui.moveTo(x, y, 2)
                autohotpy.moveMouseToPosition(x,y)

                print("Сместились на кноку покупки КУПИТЬ")
                time.sleep(1)

                #нажатие
                left_click(autohotpy, event)

                #print("Нажали КУПИТЬ")
                time.sleep(1)

                # смещение на кнопку покупки
                pyautogui.moveTo(600, 440, 2)
                autohotpy.moveMouseToPosition(600, 440)

                #print("Сместились на кноку ОК")
                time.sleep(1)

                #нажатие
                left_click(autohotpy, event)

                #print("Нажали ОК")
                time.sleep(1)

if __name__ == "__main__": #инициалихируем 2 потока
    threadOne = threading.Thread(target=do_moovs, name="first thread") #первый поток запускает кликера
    threadTwo = threading.Thread(target=hear_exit, name="second thread") #второй поток запускает слушателя прерываания события
    threadOne.start()
    threadTwo.start()
    threadOne.join()
    threadTwo.join()