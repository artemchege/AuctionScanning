# -*- coding: utf-8 -*-
from AutoHotPy import AutoHotPy  # we need to tell python that we are going to use the library
from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import time
import pyautogui
import threading
import datetime
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
    while myflag is True:

        massives = get_data()
        write_db(massives)
        buy(massives)

        coord = massives[2]

        stroke = InterceptionMouseStroke()
        pyautogui.moveTo(coord["x"], coord["y"], 2)
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