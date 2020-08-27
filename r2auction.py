from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import pyautogui
import time
import datetime
import pytesseract
import sys
from pytesseract import Output
from clicker import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' #строчка что бы path работала не прописывая

def make_screen(name):
	screen = pyautogui.screenshot()
	screen.save(f"{name}.jpg")

def make_screen_advanced(name, x, y, width=340, height=410):
	#сделать ее умной и указывать с какого окна брать скрин? иначе выставить тайминг на старт программы
	screen = pyautogui.screenshot(region=(x+160, y+19, width, height)) #160 и 19 поправки относительно точки клика 
	screen.save(f"{name}.jpg")

def make_sharpness(img):
	im = Image.open(img)
	im = im.resize((2720, 1536), 1) #х2, учесть что дальше по коду координаты делятся на 2 для приведения к нормальному размеру
	enhancer = ImageEnhance.Sharpness(im) #увеличиваем резкость
	enhanced_im = enhancer.enhance(6.0) #опыт покахал что 6х оптимум
	enhanced_im.save("st1.sharpness.resize.png")

def made_black_white(img):
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
					a, b, c = 0, 0, 0 #черный
				else:
					a, b, c = 255, 255, 255 #белый
				draw.point((i, j), (a, b, c))
	image.save("st2.black.white.jpg", "JPEG") #сейвим новый рисунок
	del draw #удаляем кисть

def recognition(img): #передаем финальное изображение тессаракту
	#image_to_string можно также использовать этоЮ более информативно
	text = pytesseract.image_to_data(img, lang="rus", config="get.images", output_type=Output.DICT) #данный конфиг кинет нам файл того как видит изображение тессеракт после своих обработом tessinput
	#print(text)
	return text

def get_coordinates(list): #ищем слово предложения и на его основе возвращаем кординаты для кликов
	try:
		length = len(list["level"])
		for i in list:
			for j in range(length - 1):
				if list[i][j] == "Предложения":
					position = j
		result = dict()
		result["x"]=int((list["left"][position]+(list["width"][position])/2+70)/2) #и чуть вправо на 70 пикселей, после делить на 2 что бы привести координаты к стандартному размеру
		result["y"]=int((list["top"][position]+(list["height"][position])/2+150)/2) #и опустимся на 150 пикселей ниже
		return result
	except:
		print("some errors occured doing get_coordinates(list)")


def make_screen_get_coordinates(): #создает скрин и возаращает координаты слова Предложения
	#make_screen("name") позже связать функцию с последующими, синхронизировать названия, пока для отладки отключено
	make_sharpness("fullscreen.png")
	made_black_white("st1.sharpness.resize.png")
	coord = get_coordinates(recognition("st2.black.white.jpg"))
	make_screen_advanced("after_advanced", coord["x"], coord["y"])


print(make_screen_get_coordinates())


#сделать в будущем ресайд до 30 пикселей на букву (если будут ошибки в точности),
# согласно исследованиями максимальная эффективность
#также можно выключить словарь, в оф документации написано конфинг строги для этого
#оф документация здесь https://tesseract-ocr.github.io/tessdoc/ImproveQuality
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