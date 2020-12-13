# coding: utf8

import sys

import urllib3
from bs4 import BeautifulSoup

from . import utils


def page_pars(url):  # парсинг страницы нового товара
    print('Начало page_pars')
    http = urllib3.PoolManager()
    try:
        html = http.request('GET', url)
        soup = BeautifulSoup(html.data, "html.parser")
        items_tinko = {'type_name': '', 'category_name': '', 'name_item': '', 'title': '', 'alias': '', 'articul': '',
                       'foto': '', 'maker': 'No name', 'pre_description': '', 'tinko_foto': '',
                       'description': '', 'teh_description': '', 'filter_category': 'Null', 'articul_maker': ''}
        print('BEGIN - Хлебные крошки \n')
        breadcrumb = soup.find("ul", {"class": "breadcrumbs-list"})
        li_bread = breadcrumb.findAll('li')  # тип товара
        try:
            items_tinko['type_name'] = li_bread[2].text
            items_tinko['category_name'] = li_bread[3].text
        except:
            pass
        try:
            items_tinko['filter_category'] = li_bread[4].text
        except:
            pass
        print('END - Хлебные крошки \n')

        print('BEGIN - Название товара \n')

        for title in soup.findAll("div", {"class": "product-detail__title"}):
            for y in title.findAll('h1'):
                items_tinko['name_item'] = y.text
                items_tinko['alias'] = utils.trr(y.text)
                print('Название товара: ' + y.text)
        print('END - Название товара \n')

        print('BEGIN - Фото товара \n')
        for title in soup.findAll("div", {"class": "product-detail__image"}):
            for y in title.findAll("a"):
                items_tinko['tinko_foto'] = str(y.get('href')).replace('//', '')
                if items_tinko['tinko_foto'].find('http://') == -1:
                    items_tinko['tinko_foto'] = 'https://www.tinko.ru' + items_tinko['tinko_foto']
                items_tinko['foto'] = utils.download_img(items_tinko['alias'], items_tinko['tinko_foto'])
        print('END - Фото товара \n')

        print('BEGIN - Артикул, Производитель и Заголовок \n')
        for title in soup.findAll("div", {"class": "product-detail__row-1"}):
            for y in title.findAll("div", {"class": "product-detail__property"}):
                if str(y).find('Код') != -1:
                    for g in y.findAll("span"):
                        if str(g.text).find('Код') == -1:
                            try:
                                items_tinko['articul'] = (int(g.text) * 3) - 41
                                items_tinko['alias'] = items_tinko['alias'] + '_' + str(items_tinko['articul'])
                                print('Alias товара: ' + items_tinko['alias'])
                            except:
                                print(sys.exc_info())
                if str(y).find('Производитель') != -1:
                    print('Производитель')
                    for g in y.findAll("a"):
                        items_tinko['maker'] = (g.text).replace('	', '').replace('\n', '').replace(
                            '\t', '').replace('                                                ', '')
                        print(items_tinko['maker'])
                if str(y).find('Артикул производителя:') != -1:
                    print('Артикул производителя')
                    spans = y.findAll('span')
                    items_tinko['articul_maker'] = (
                        spans[1].text.replace('	', '').replace('\n', '').replace('\t', ''))

            for y in title.findAll('h2'):
                print('Заголовок товара: ' + y.text)
                items_tinko['title'] = y.text
        print('END - Фото товара \n')

        print('BEGIN - Краткое описание \n')
        for title in soup.findAll("div", {"class": "product-detail__row-3"}):
            for y in title.findAll("div", {"class": "product-detail__short-description"}):
                if str(y.text).find('описание') != -1:
                    items_tinko['pre_description'] = y.text.replace("'", '"').replace(
                        'Краткое описание: ', '')
                    print('Краткое описание: ' + items_tinko['pre_description'])
        print('END - Краткое описание \n')

        print('BEGIN - Полное описание \n')
        full_description = soup.find('div', {'id': 'description_inner'})
        for desc in full_description.find_all("p"):
            items_tinko['description'] = items_tinko['description'] + '<p>' + desc.text + '</p>'
        print('END - Полное описание \n')

        print('BEGIN - Тех. характеристики \n')
        for title in soup.findAll("div", {"class": "product-detail__characteristic_mobile"}):
            for tech_desc in title.findAll('div'):
                items_tinko['teh_description'] = items_tinko['teh_description'] + str(tech_desc)
        print('END - Тех. характеристики \n')

        return items_tinko
    except:
        return 'error'

print(page_pars('https://www.tinko.ru/catalog/product/001041/'))