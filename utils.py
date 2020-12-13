# coding: utf8


import re
import sys
import urllib

from trans import trans


def trr(string):  # делает транслитерацию
    stt = trans(
        string.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '').replace('"', '').replace('.',
                                                                                                             '').replace(
            '/', '_').replace('$', '').replace('«', '').replace('»', '').replace('?', '').replace('!', '').lower())
    return stt


def term(text):
    # Перевод срока поставщика в срок на сайте +3 дня
    days = (re.findall(r'\d+', text))
    if days != []:
        if int(days[0]) >= 3:
            for x in days:
                days_new = str(int(x) + 2)
                text = text.replace(x, days_new)
                # print (text)

    if text == '3-4 дня':
        text = 'до 6-ти дней'
    if text == '2-3 дня':
        text = 'до 5-ти дней'
    elif text.lower() == 'в наличии' or text == 'В наличии':
        text = 'до 3-х дней'
    # #
    elif text.lower() == 'звоните' or text == 'Звоните':
        text = 'Уточняйте'
    return text


def extendsion(url):
    # Получение расширения файла
    try:
        ext = '.jpg'
        if url.find('.png') != -1:
            ext = '.png'
        if url.find('.jpg') != -1:
            ext = '.jpg'
        if url.find('.jpeg') != -1:
            ext = '.jpeg'
        if url.find('.gif') != -1:
            ext = '.gif'
        return ext
    except:
        print('Ссылка не работает.')
        ext = '.jpg'
        return ext


def download_img(alias, tinko_foto):
    ext = extendsion(tinko_foto)
    print('получили ext')
    media_file = (alias + ext)
    print('получили ' + media_file)
    try:
        print('kachaem')
        print(tinko_foto)
        urllib.urlretrieve(tinko_foto, media_file)
    except:
        print('Файл есть, не качаем')
        print(sys.exc_info())

    return 'item_foto/' + alias + ext
