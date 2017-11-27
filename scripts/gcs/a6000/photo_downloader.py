import calendar
import time
import requests
import shutil

number = 0
while true:

    url1 = 'http://odroid@INPUT_PORT/get/imgs'
    response = requests.get(url1)
    list = response.content
    if (str(number) == list[list.index(str(number):list.index(str(number)+1]):
        imgName = list[list.index(number)+5:list.index(number)+19]
        url2 = 'http://odroid@INPUT_PORT/get/imgs/' + imgName
        response = requests.get(url2, stream=True)
        with open('img-'+number+ '.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        number = number + 1

    sleep 4
