import pyautogui
#from r2auction import *
import sqlite3
from PIL import Image
import datetime
from functions import *


def write_bd(name, price):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    query = "INSERT INTO auction_data (name, price, date, time) VALUES ("+"'"+name+"'"+", "+"'"+price+"'"+", CURRENT_DATE, CURRENT_TIME)"
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()


def delete_spaces(income_list):
    #возможно модернизировать и что бы 000 разделиялись пробелами?
    result = list()
    for i in income_list:
        result.append(i.replace(" ", ""))
    return result



now = datetime.datetime.now()
print(now.strftime("%H:%M:%S"))

