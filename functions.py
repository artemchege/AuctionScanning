# -*- coding: utf-8 -*-
from typing import Any

from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import pyautogui
import time
import pytesseract
from pytesseract import Output
import sqlite3

"""
Возмжноные доработки:
1. Вынести ресайз отдельной функцией?
2. Сделать каскадный вызов преобразования изображения? Функция сразу передает рехультат другой без сохрана
3. Исправить весь PEP8, добавить в requirements новые модули
4. Возможно модернизировать запись в базу что бы сотни разделиялись пробелами?
5. Пролистать блокнот, там тоже были some suggestions
6. На ПН: все функции готовы, осталось собрать в куч, отрефакторить и протестировать на компе иры
7. Прокомментировать все функции
8. Расставить try except на тонках участках
9. После тестов возможно написать интерфейс? 
"""

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'  # строчка что бы path работала не прописывая

#global_coord = {"x": 420, "y": 220}

def make_screen(name):
    screen = pyautogui.screenshot()
    screen.save(f"{name}.png")


def make_screen_advanced(name, x, y, width, height=410):
    # сделать ее умной и указывать с какого окна брать скрин? иначе выставить тайминг на старт программы
    screen = pyautogui.screenshot(region=(x + 160, y - 14, width, height))  # 160 и 14 поправки относительно точки клика
    screen.save(f"{name}.jpg")


def make_sharpness(img, resize, save_as):
    im = Image.open(img)
    width, height = im.size
    im = im.resize((width * resize, height * resize), 1)
    enhancer = ImageEnhance.Sharpness(im)  # увеличиваем резкость
    enhanced_im = enhancer.enhance(6.0)  # опыт покахал что 6х оптимум
    enhanced_im.save(f"{save_as}.png")


def make_black_white(img, save_as):
    mode = 5  # Считываем номер преобразования.
    image = Image.open(img)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей
    if (mode == 5):
        factor = 0
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 0, 0, 0  # черный
                else:
                    a, b, c = 255, 255, 255  # белый
                draw.point((i, j), (a, b, c))
    image.save(f"{save_as}.jpg", "JPEG")  # сейвим новый рисунок
    del draw  # удаляем кисть


def recognition(img, output="list"):  # передаем финальное изображение тессаракту
    if output == "dictionary":
        text = pytesseract.image_to_data(img, lang="rus", config="get.images", output_type=Output.DICT)  # данный конфиг кинет нам файл того как видит изображение тессеракт после своих обработом tessinput
    else:
        text = pytesseract.image_to_string(img, lang="rus", config="get.images")
    return text


def get_coordinates(list):  # ищем слово предложения и на его основе возвращаем кординаты для кликов
    try:
        length = len(list["level"])
        for i in list:
            for j in range(length - 1):
                if list[i][j] == "Предложения":
                    position = j
        result = dict()
        result["x"] = int((list["left"][position] + (list["width"][
            position]) / 2 + 70) / 2)  # и чуть вправо на 70 пикселей, после делить на 2 что бы привести координаты к стандартному размеру
        result["y"] = int(
            (list["top"][position] + (list["height"][position]) / 2 + 150) / 2)  # и опустимся на 150 пикселей ниже
        return result
    except:
        print("some errors occured doing get_coordinates(list)")


def make_screen_get_coordinates():  # создает скрин и возаращает координаты слова Предложения
    time.sleep(10)  # даем 10 сек что бы успеть переключиться на р2
    make_screen("fullscreen")
    make_sharpness("fullscreen.png", 2, "FirstScreenSt1")
    make_black_white("FirstScreenSt1.png", "FirstScreenSt2")
    coord = get_coordinates(recognition("FirstScreenSt2.jpg", output="dictionary"))
    global_coord = coord
    return coord

def delete_empty_element(income_list):
    result = list()
    for i in income_list:
        if len(i)>0:
            result.append(i)
    return result

def delete_spaces(income_list):
    result = list()
    for i in income_list:
        result.append(i.replace(" ", ""))
    return result

def get_data():
    coord = make_screen_get_coordinates() #возможно вынести отдельной функцией и запускать 1 раз в начале
    make_screen_advanced("EndlessScreenItem", coord["x"], coord["y"], 160)
    make_sharpness("EndlessScreenItem.jpg", 6, "EndlessScreenItemSt1")
    make_black_white("EndlessScreenItemSt1.png", "EndlessScreenItemSt2")
    items = recognition("EndlessScreenItemSt2.jpg").split("\n")
    items = delete_empty_element(items)
    for i in items:
        print(i)
    print()
    make_screen_advanced("EndlessScreenPrices", coord["x"]+235, coord["y"], 140)
    make_sharpness("EndlessScreenPrices.jpg", 6, "EndlessScreenPricesSt1")
    make_black_white("EndlessScreenPricesSt1.png", "EndlessScreenPricesSt2")
    prices = recognition("EndlessScreenPricesSt2.jpg").split("\n")
    prices = delete_spaces(delete_empty_element(prices))
    for i in prices:
        print(i)
    return items, prices, coord

def write_db(data):
    if len(data[0])!=len(data[1]): #проверим что колличество цен совпадает с колличеством предметов
        print("Lenght of incomming massives in write_db() arent equal")
        return "Lenght of incomming massives in write_db() arent equal"
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    for i in range(8):
        name, price = data[0][i], data[1][i]
        query= "INSERT INTO auction_data (name, price, date, time) VALUES (" + "'" + name + "'" + ", " + "'" + price + "'" + ", CURRENT_DATE, CURRENT_TIME)"
        cursor.execute(query)
        conn.commit()
    conn.close()

def buy(data):
    if len(data[0]) != len(data[1]):  # проверим что колличество цен совпадает с колличеством предметов
        print("Lenght of incomming massives in write_db() arent equal")
        return "Lenght of incomming massives in write_db() arent equal"
    for i in range(8):
        name, price = data[0][i], data[1][i]
        if filter(name, price, i):
            print("Тру", i)


def filter(name, price, i):
    try:
        item_to_find="+0 Джамадхары убийцы"
        price_to_find=5000000
        if name==item_to_find:
            if int(price)<price_to_find:
                print(f"Предмет {item_to_find} по цене ниже {price_to_find} был найден")
                print(f"Номер предмета на скрине: {i}")
                return True
    except Exception as e:
        print(f"Возникла ошибка: {e}")
    finally:
        print("Фильтр пройден, совпадений не найдено")

def main():
    pass
    #get_data()
    #massives = get_data()
    #write_db(massives)

# сделать в будущем ресайд до 30 пикселей на букву (если будут ошибки в точности),
# согласно исследованиями максимальная эффективность
# также можно выключить словарь, в оф документации написано конфинг строги для этого
# оф документация здесь https://tesseract-ocr.github.io/tessdoc/ImproveQuality
"""
	#now = datetime.datetime.now()
	#print(now.strftime("%d-%m-%Y %H:%M:%S"), "время до")
	
некоторые прочие полезные ссылки, использовать когда появятся проблемы в распознавании
https://pypi.org/project/pytesseract/ оф страница (почти)
https://overcoder.net/q/502228/%D0%BF%D1%80%D0%B5%D0%B4%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-opencv-%D0%BF%D0%B5%D1%80%D0%B5%D0%B4-%D1%80%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC
https://stackoverflow.com/questions/43705481/pytesser-set-character-whitelist
https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
https://coderoad.ru/28935983/%D0%9F%D1%80%D0%B5%D0%B4%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-Tesseract-OCR-%D1%81-OpenCV
https://stackoverrun.com/ru/q/11985017
https://overcoder.net/q/871809/%D1%80%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%82%D0%B5%D0%BA%D1%81%D1%82-%D1%81-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC-tesseract-ocr-%D0%BB%D1%83%D1%87%D1%88%D0%B5-%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0
"""
