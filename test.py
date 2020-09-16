from functions import *
import time
import datetime

#time.sleep(5)
#make_screen("fullscreen")
#скрин сделан, можно работать дальше

def make_screen_get_coordinates():  # создает скрин и возаращает координаты слова Предложения
    #time.sleep(10)  # даем 10 сек что бы успеть переключиться на р2
    #make_screen("fullscreen")
    #make_sharpness("fullscreen.png", 2, "FirstScreenSt1")
    #make_black_white("FirstScreenSt1.png", "FirstScreenSt2")
    coord = get_coordinates(recognition("FirstScreenSt2.jpg", output="dictionary"))
    #global_coord = coord
    return coord

def get_data(coord, time):

    path  = time.replace("/","_").replace(":",".")
    os.mkdir(f"cash/{path}")

    make_screen_advanced("common_view", coord["x"], coord["y"], 610, data_path=path)

    make_screen_advanced("EndlessScreenItem", coord["x"], coord["y"], 160, data_path=path)
    make_sharpness("EndlessScreenItem.jpg", 6, "EndlessScreenItemSt1", data_path=path)
    make_black_white("EndlessScreenItemSt1.png", "EndlessScreenItemSt2", data_path=path)
    items = recognition("EndlessScreenItemSt2.jpg", data_path=path).split("\n")
    items = delete_empty_element(items)
    for i in items:
        print(i)
    print()
    make_screen_advanced("EndlessScreenPrices", coord["x"]+235, coord["y"], 140, data_path=path)
    make_sharpness("EndlessScreenPrices.jpg", 6, "EndlessScreenPricesSt1", data_path=path)
    make_black_white("EndlessScreenPricesSt1.png", "EndlessScreenPricesSt2", data_path=path)
    prices = recognition("EndlessScreenPricesSt2.jpg", data_path=path).split("\n")
    prices = delete_spaces(delete_empty_element(prices)).replace("\n\x0c", "") #попробовать т возможно применить к айтемам тоже
    for i in prices:
        print(i)
    return items, prices

def test_get_data(coord, time):
    path = time.replace("/","_").replace(":",".")
    os.mkdir(f"cash/{path}")

    items = list()
    prices = list()

    for i in range(8):

        make_screen_advanced(f"Item-{i}", coord["x"], coord["y"]+52*i, 160, data_path=path, height=50)
        make_sharpness(f"Item-{i}.jpg", 6, f"ItemSt1-{i}", data_path=path)
        make_black_white(f"ItemSt1-{i}.png", f"ItemSt2-{i}", data_path=path)
        item = recognition(f"ItemSt2-{i}.jpg", data_path=path)
        items.append(item)
        print(item)

        make_screen_advanced(f"Price-{i}", coord["x"]+235, coord["y"]+52*i, 140, data_path=path, height=50)
        make_sharpness(f"Price-{i}.jpg", 6, f"PriceSt1-{i}", data_path=path)
        make_black_white(f"PriceSt1-{i}.png", f"PriceSt2-{i}", data_path=path)
        item = recognition(f"PriceSt2-{i}.jpg", data_path=path)
        prices.append(item)
        print(item)

    return items, delete_spaces(prices)
    #возмонжо удалить delete_spaces() и в базу писать строку с пробелами, удалять на эатапе фильтра и сранения чисел


print(make_screen_get_coordinates())
coord = make_screen_get_coordinates()

now = datetime.datetime.now()
current_time = now.strftime("%D:%H:%M:%S")
print(current_time)

time.sleep(5)
print(test_get_data(coord, current_time))