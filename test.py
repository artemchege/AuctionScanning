import pyautogui
#from r2auction import *
import sqlite3
from PIL import Image


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

x = ['4 710 000', '1630 009', '324 223', '324 222', '4 499 000', '2990 008', '2990 000', '2889 999']
print(x, "до")
x = delete_spaces(x)
print(x)

for i in range(8):
    print(i)


