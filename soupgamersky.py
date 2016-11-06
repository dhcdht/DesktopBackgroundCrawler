#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dhcdht'


from bs4 import BeautifulSoup
from urllib import parse, request
import os


def downloadResource(dic):

    src = dic['src']
    des = dic['des']

    src_path = parse.urlparse(src).path
    full_file_name = os.path.basename(src_path)
    ext_name = os.path.splitext(full_file_name)[1]
    file_name = full_file_name
    if des and len(des) < 20:
        file_name = des + ext_name
    elif len(file_name) < 15:
        addition_name = os.path.split(os.path.split(src_path)[0])[1]
        file_name = addition_name + "_" + file_name
    rel_res_name = os.path.join('./res/gamersky/wp', file_name)
    if not os.path.exists(rel_res_name):
        try:
            request.urlretrieve(src, rel_res_name)
        except:
            print('error download url (%s) description (%s) to file (%s)' % (src, des, rel_res_name))
            return
        print('scrapy url (%s) description (%s) to file (%s)' % (src, des, rel_res_name))
    else:
        print('duplicate file : (%s) (%s)' % (rel_res_name, src))

def scrapyPicsPage(page_href):
    try:
        resp = request.urlopen(page_href)
        html = resp.read()
    except:
        print('except : %s' % page_href)
        return
    soup = BeautifulSoup(html, 'html.parser')

    list_img = soup.findAll('img', attrs={'class': 'picact'})

    for img_node in list_img:
        a_node = img_node.parent
        link = a_node.attrs['href']
        href = parse.urlparse(link).query
        href = parse.urljoin(page_href, href)

        if not href.endswith('jpg') and not href.endswith('png') and not href.endswith('JPG') and not href.endswith('PNG'):
            print('ignore href : %s', href)
            continue

        text_list = a_node.parent.findAll(text=True)
        des = ''.join(text_list)
        des = des.strip()

        dic = {
            'src': href,
            'des': des,
        }
        downloadResource(dic)

    page_div = soup.find('div', attrs={'class': 'Mid2L_con'})

    next_page_node = page_div.find('a', text='下一页')
    if next_page_node:
        next_href = next_page_node.attrs['href']
        next_href = parse.urljoin(page_href, next_href)

        scrapyPicsPage(next_href)

def scrapyMainList(list_href):
    try:
        resp = request.urlopen(list_href)
        html = resp.read()
    except:
        print('except : %s' % list_href)
        return
    soup = BeautifulSoup(html, 'html.parser')

    main_ul = soup.find('ul', attrs={'class': 'pictxt contentpaging'})

    list_a = main_ul.findAll('a', attrs={'target': '_blank'}, text=True)

    for a_node in list_a:
        href = a_node.attrs['href']
        href = parse.urljoin(list_href, href)

        scrapyPicsPage(href)

def main():
    scrapyMainList('http://www.gamersky.com/ent/wp/')

if __name__ == '__main__':
    main()
