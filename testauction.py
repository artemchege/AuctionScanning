# -*- coding: utf-8 -*-

# The example starts here
from AutoHotPy import AutoHotPy  # we need to tell python that we are going to use the library
from AutoHotPy import Key
from InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import time
import pyautogui


# The following function is called when you press ESC.
# autohotpy is the instance that controlls the library, you should do everything through it.
def exitAutoHotKey(autohotpy, event):
    #print(autohotpy, "   autohotpy ESC")
    #print(event, "   event ESC")
    """
    exit the program when you press ESC
    """
    print("Провалились в exitAutoHotKey")
    autohotpy.stop()  # makes the program finish successfully. Thisis the right way to stop it


def superCombo(autohotpy, event):
    #while True:
        try:
            #print(autohotpy, "   autohotpy supercombo()")
            #print(event, "   event autohotpy()")
            stroke = InterceptionMouseStroke()  # I highly suggest you to open InterceptionWrapper to read which attributes this class has
            # To simulate a mouse click we manually have to press down, and release the buttons we want.
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
            #autohotpy.stop()
            time.sleep(5)
        except KeyboardInterrupt:
            print("Было прервано через клаву из superCombo")
            autohotpy.stop()

"""def pressA(autohotpy, event):
    autohotpy.A.press()"""

# THIS IS WERE THE PROGRAM STARTS EXECUTING!!!!!!!!
if __name__ == "__main__":
    #while True:
    i=0
    while i<5:
        print(i)
        try:
            auto = AutoHotPy()  # Initialize the library
            #autohotpy = Key()
            auto.registerExit(auto.ESC, exitAutoHotKey)  # Registering an end key is mandatory to be able to stop the program gracefully
            #autohotpy.A.press()
            auto.registerForKeyDown(auto.A, superCombo)  # This method lets you say: "when I press A in the keyboard, then execute "superCombo"
            #autohotpy.A.press()
            #auto.myregister(superCombo)
            auto.start()  # Now that everything is registered we should start runnin the program
            #auto.stop()
            print("Мы в конце блока try")
        except KeyboardInterrupt:
            print("Было прервано через клаву из KeyboardInterrupt")
            #auto.stop()
            #auto2 = AutoHotPy()
            #auto2.registerExit(auto.ESC, exitAutoHotKey)
            #auto2.start()
            #i=10
            break
        i+=1

#python testauction.py

"""from AutoHotPy import *
from InterceptionWrapper import *

def exitAutoHotKey():
    print("yes")

auto = AutoHotPy()
autohotpy = AutoHotPy()

def get_mouse_position():
    pos = autohotpy.getMousePosition()
    print({'x': pos[0], 'y': pos[1]})
    autohotpy.registerExit(auto.ESC,exitAutoHotKey)"""

"""    stroke = InterceptionMouseStroke()
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)"""

"""def dofuckingclick():
    autohotpy = AutoHotPy()
    stroke = InterceptionMouseStroke()  # I highly suggest you to open InterceptionWrapper to read which attributes this class has
    # To simulate a mouse click we manually have to press down, and release the buttons we want.
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)
    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)"""