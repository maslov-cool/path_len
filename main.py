import os
import sys

import pygame
import requests


def main(geocode):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    # Готовим запрос.
    geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"].split()
        # Печатаем извлечённые из ответа поля:
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


s = 0
A = []
for i in ['Россия, Москва, Бородинский мост',
          'Россия, Москва, улица Киевская',
          'Россия, Москва, Киевский вокзал',
          'Россия, Москва, Бородинский мост',
          'Россия, Москва, ул. Льва Толстого',
          'Россия, Москва, ул. Льва Толстого, 16'
          ]:
    A.append(main(i))
for i in range(1, len(A)):
    s += ((float(A[i][0]) - float(A[i - 1][0])) ** 2 + (float(A[i][1]) - float(A[i - 1][1])) ** 2) ** 0.5 * 111
print(f'путь от киевского вокзала до офиса яндекса составляет {s} км')

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
ll_spn = f'll={','.join(A[0])}&spn=0.022,0.022'

# Готовим запрос.

map_request = f"{server_address}{ll_spn}&apikey={api_key}&pl="
for i in A[1:]:
    map_request += f"{i[0]},{i[1]}"
    if i != A[-1]:
        map_request += ','
map_request += '&pt='
map_request += f"{A[0][0]},{A[0][1]},comma"
response = requests.get(map_request)
print(map_request)
if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
