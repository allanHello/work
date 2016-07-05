# -*- coding: utf-8 -*-

import urllib2
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

host = "http://amma.artron.net/"
data_file = open("data.txt", "a")


def write_file(lists):
    result = "|".join(lists) + "\n";
    data_file.write(result)


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0',
               'cookie': '''eSID4=0C35203B9FB7DAA3; Hm_lvt_851619594aa1d1fb8c108cde832cc127=1467083451,1467084565,1467105634; _at_pt_0_=678125; _at_pt_1_=billybilly10; _at_pt_2_=80d4afd836a19d9169e7d0d89ba9c857; artron_67ae_saltkey=ZSyqwz5M; artron_67ae_lastvisit=1467087334; artron_67ae_sid=q4747g; artron_67ae_lastact=1467097734%09uc.php%09; artron_67ae_auth=5c87gK2fqpJMJvmpQIlPeD6ItmzxgJdEhOASHq23s1S3EPR2MrH3sh8O2S63dRWoAvbnFygRzvkLcuB%2FrumdfHexvi4; artron_auth=c0baJpnLmZ0IK14O0TaQcELrfL9B3crD2ZOHnSL%2FRGW0vznUorleh7d3hwXmj0UlnvpC93t6GNAwobAtkCNe5RTO3DQ; artron_loginuser=billybilly10; Hm_lpvt_851619594aa1d1fb8c108cde832cc127=1467169278; tulu_pop=1; PHPSESSID=b392ee638e79ef1261604bec7976a2ba'''}
    req = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(req)
    html_content = page.read()
    return html_content


def step2(node, name):
    first_url = host + node.a['href']
    html_content = get_html(first_url)
    html_soup = BeautifulSoup(html_content, 'html.parser')
    table = html_soup.find('table', class_='detail-table')
    for tr in table.tbody.find_all('tr'):
        second_node = tr.find('a')
        if not second_node is None:
            step3(second_node['href'], name)


def step3(url, name):
    third_url = host + url
    html_content = get_html(third_url)
    html_soup = BeautifulSoup(html_content, 'html.parser')
    table = html_soup.find("table", class_='detail-table')

    num = ""
    artname = ""
    price = ""
    deal = ""
    date = ""
    com = ""

    for tr in table.tbody.find_all(class_='tr'):
        td_list = tr.find_all("td")
        try:
            num = td_list[0].string
            artname = td_list[1].a.string.strip()
            price = td_list[2].string.strip()
            deal = td_list[3].string.strip()
            date = td_list[4].string.strip()
            com = td_list[5].string.strip()
            step4(td_list[1].a['href'], name, num, artname, price,
                  deal, date, com)
        except:
            print td_list[1].a['href']  # 有些第四层打不开
            write_file([name, num, artname, price, deal, date, com])


# 需要转换url
def step4(url, name, num, artname, price, deal, date, com):
    name2 = ""  # 名称2
    scale = ""  # 尺寸
    type = ""  # 作品分类
    create_date = ""  # 创作年代
    price1 = ""  # 估价
    deal_price = ""  # 成交价
    place = ""  # 专场
    date1 = ""  # 拍卖时间
    com1 = ""  # 拍卖公司
    com2 = ""  # 拍卖会
    note1 = ""  # 说明1
    note2 = ""  # 说明2
    note3 = ""  # 说明3

    split_value = url.split('?')[1].split('=')[1]
    url = "http://auction.artron.net/" + "paimai-" + split_value
    html_content = get_html(url)
    html_soup = BeautifulSoup(html_content, 'html.parser')

    name2 = html_soup.find("div", class_='titLeft').h1.string
    mainBody = html_soup.find_all("div", 'worksInfo')[1].find_all("tr")

    scale = mainBody[0].find_all("td")[1].find("em").string
    row1 = mainBody[1].find_all("td")
    type = row1[0].string
    create_date = row1[1].string
    price1 = mainBody[2].td.em.string.strip()

    li_list = mainBody[3].td.find_all("li")
    if not li_list:
        raise NameError("未登录")
    li_deal_price = map(lambda x: x.string.strip(), li_list)
    if len(li_deal_price) > 1:
        deal_price = "&".join(li_deal_price)
    else:
        deal_price = li_deal_price[0]

    row4 = mainBody[4].find_all("td")
    place = row4[0].a.string
    date1 = row4[1].em.string

    row5 = mainBody[5].find_all("td")
    com1 = row5[0].a.font.string
    com2 = row5[1].a.string

    k = 0
    for tr_note in mainBody[6:]:
        if k == 0:
            for sub in tr_note.td.stripped_strings:
                note1 = note1 + "&" + sub
            note1 = note1[1:]
        elif k == 1:
            for sub in tr_note.td.stripped_strings:
                note2 = note2 + "&" + sub
            note2 = note2[1:]
        elif k == 2:
            for sub in tr_note.td.stripped_strings:
                note3 = note3 + "&" + sub
            note3 = note3[1:]
        else:  # 多余的补到note3里
            for sub in tr_note.td.stripped_strings:
                note3 = note3 + "&" + sub
        k += 1

    write_file([name, num, artname, price, deal, date, com, name2, scale, type, create_date, price1, deal_price, place, date1,
         com1, com2, note1, note2, note3])


html = get_html("http://amma.artron.net/artronindex_artistall.php")
soup = BeautifulSoup(html, 'html.parser')
write_file(['艺术家姓名', '序号', '名称', '估价', '成交价', '拍卖日期', '拍卖机构', '名称2', '尺寸', '作品分类', '创作年代', '估价', '成交价', '专场', '拍卖时间', '拍卖公司', '拍卖会', '说明1', '说明2', '说明3'])
i = 0
for name_node in soup.body.find_all("div", class_='sub-Aritst-Area')[1].find_all("li")[i:]:
    try:
        content_name = name_node.a.string
        print "[{0}]{1}".format(i, content_name)
        i += 1
        step2(name_node, content_name)
        # break
    except Exception as e:
        print e

data_file.close()