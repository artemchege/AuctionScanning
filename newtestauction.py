# -*- coding: utf-8 -*-
from AutoHotPy import AutoHotPy  # we need to tell python that we are going to use the library
from AutoHotPy import Key
from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import time
import pyautogui
import threading

x = True
myflag=True

def AHP():
    auto = AutoHotPy()
    auto.registerExit(auto.ESC, exitAutoHotKey)
    #auto.registerForKeyDown(auto.A, superCombo)
    auto.start()
    print("Мы в конце блока try")

def print_i(y): #функция которая печатает i через 5 секунд
    for i in range(y):
        if myflag is True:
            print (i, myflag)
            time.sleep(5)

def exitAutoHotKey(autohotpy, event):
    global myflag
    print("Провалились в exitAutoHotKey")
    myflag=False
    autohotpy.stop()


def superCombo(autohotpy, event):
        try:
            stroke = InterceptionMouseStroke()
            pyautogui.moveTo(680, 560, 2)
            stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
            autohotpy.sendToDefaultMouse(stroke)
            stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
            autohotpy.sendToDefaultMouse(stroke)
            pyautogui.moveTo(880, 560, 2)
            stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
            autohotpy.sendToDefaultMouse(stroke)
            stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
            autohotpy.sendToDefaultMouse(stroke)
            time.sleep(5)
        except KeyboardInterrupt:
            print("Было прервано через клаву из superCombo")
            autohotpy.stop()

if __name__ == "__main__":
    try:
        threadOne = threading.Thread(target=print_i, args=(10,), name="first thread")
        threadTwo = threading.Thread(target=AHP, name="second thread")
        threadOne.start()
        threadTwo.start()
        threadOne.join()
        threadTwo.join()
    except KeyboardInterrupt:
        print("Было прервано через клаву из KeyboardInterrupt")