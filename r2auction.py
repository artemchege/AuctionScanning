from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import pyautogui
import time
import pytesseract
import sys
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' #строчка что бы path работала не прописывая


def make_sharpness():
	im = Image.open("x.jpg")
	im = im.resize((1359, 1236), 1)
	enhancer = ImageEnhance.Sharpness(im) #увеличиваем резкость
	enhanced_im = enhancer.enhance(6.0) #опыт покахал что 6х оптимум
	enhanced_im.save("b.png")

def made_black_white():
	mode = 5  # Считываем номер преобразования.
	image = Image.open("b.png")  # Открываем изображение.
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
	image.save("c.jpg", "JPEG") #сейвим новый рисунок
	del draw #удаляем кисть

def recognition(): #передаем финальное изображение тессаракту
	text = pytesseract.image_to_data("c.jpg", lang="rus", config="get.images") #данный конфиг кинет нам файл того как видит изображение тессеракт после своих обработом tessinput
	print(text)
	return text

def main():
	make_sharpness()
	made_black_white()
	recognition()

main()


#сделать в будущем ресайд до 30 пикселей на букву (если будут ошибки в точности),
# согласно исследованиями максимальная иффективность
#также можно выключить словарь, в оф документации написано конфинг строги для этого
#оф документация здесь https://tesseract-ocr.github.io/tessdoc/ImproveQuality
"""
некоторые прочие полезные ссылки, использовать когда появятся проблемы в распознавании
https://pypi.org/project/pytesseract/ оф страница (почти)
https://overcoder.net/q/502228/%D0%BF%D1%80%D0%B5%D0%B4%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-opencv-%D0%BF%D0%B5%D1%80%D0%B5%D0%B4-%D1%80%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC
https://stackoverflow.com/questions/43705481/pytesser-set-character-whitelist
https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
https://coderoad.ru/28935983/%D0%9F%D1%80%D0%B5%D0%B4%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-Tesseract-OCR-%D1%81-OpenCV
https://stackoverrun.com/ru/q/11985017
https://overcoder.net/q/871809/%D1%80%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%82%D0%B5%D0%BA%D1%81%D1%82-%D1%81-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC-tesseract-ocr-%D0%BB%D1%83%D1%87%D1%88%D0%B5-%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0
"""