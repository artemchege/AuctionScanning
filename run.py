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

def superCombo(autohotpy, event): #действия в бесконечном цикле прерываем флагом
    print("A is pressed, starting endless clicking cycle")

    shutil.rmtree("cash/")
    time.sleep(2)
    os.mkdir("cash")

    coord = make_screen_get_coordinates()  # возможно вынести отдельной функцией и запускать 1 раз в начале
    while myflag is True:

        now = datetime.datetime.now()
        current_time = now.strftime("%D:%H:%M:%S")
        print(current_time, "our data-path")
        #os.mkdir(f"cash/{path}")

        massives = get_data(coord, current_time)
        write_db(massives, current_time)

        buy = position_to_buy(massives)
        print(buy, " это наш массив buy")

        stroke = InterceptionMouseStroke()

        if len(buy)>0:
            for i in buy:
                print("Покупаю шмотку на позиции: ", i)
                x = coord["x"] + 700  # смещаемся вправо на 700 пикселей
                print("Двигаемся к координате X: ", x)
                y = coord["y"] + 20 + i * 50  # смещаемся уть вниз на 20 и потом на порядок шмотки в списке
                print("Двигаемся к координате Y: ", y)

                pyautogui.moveTo(x, y, 2)
                autohotpy.moveMouseToPosition(x,y)


                print("Сместились на кноку покупки КУПИТЬ")
                time.sleep(1)

                stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
                autohotpy.sendToDefaultMouse(stroke)
                stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
                autohotpy.sendToDefaultMouse(stroke)

                print("Нажали КУПИТЬ")
                time.sleep(1)

                pyautogui.moveTo(600, 440, 2)  # смещение на кнопку покупки
                autohotpy.moveMouseToPosition(600, 440)


                print("Сместились на кноку ОК")
                time.sleep(1)

                stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
                autohotpy.sendToDefaultMouse(stroke)
                stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
                autohotpy.sendToDefaultMouse(stroke)

                print("Нажали ОК")
                time.sleep(1)

        pyautogui.moveTo(coord["x"], coord["y"], 2) #двигаемся к началу и обновляем страницу аукцциона
        autohotpy.moveMouseToPosition(coord["x"], coord["y"])

        time.sleep(1)

        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        autohotpy.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        autohotpy.sendToDefaultMouse(stroke)

        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S"))
        time.sleep(15)

if __name__ == "__main__": #инициалихируем 2 потока
    threadOne = threading.Thread(target=do_moovs, name="first thread") #первый поток запускает кликера
    threadTwo = threading.Thread(target=hear_exit, name="second thread") #второй поток запускает слушателя прерываания события
    threadOne.start()
    threadTwo.start()
    threadOne.join()
    threadTwo.join()