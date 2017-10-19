# encoding:gbk
import json
import os
import urllib.request
from bs4 import BeautifulSoup
import time

wllist = ['1', '2', '3']
# subjects = {'1': '文科', '2': '理科', '3': '综合'}
subjects = {'1': '文科', '2': '理科'}

provinces = {'1': '北京', '2': '天津', '3': '上海', '4': '重庆', '5': '河北', '6': '河南', '7': '山东', '8': '山西', '9': '安徽',
             '10': '江西', '11': '江苏', '12': '浙江', '13': '湖北', '14': '湖南', '15': '广东', '16': '广西', '17': '云南', '18': '贵州',
             '19': '四川', '20': '陕西', '21': '青海', '22': '宁夏', '23': '黑龙江', '24': '吉林', '25': '辽宁', '26': '西藏',
             '27': '新疆', '28': '内蒙古', '29': '海南', '30': '福建', '31': '甘肃', '32': '港澳台'}
plist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
# array_batch = {'00': '不详', '01': '本科提前批', '11': '本科一批', '12': '本科二批', '123': '本科二三批', '13': '本科三批', '21': '专科'}
array_batch = {'01': '本科提前批', '11': '本科一批', '12': '本科二批', '13': '本科三批'}


def get_html(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        return html
    except:
        time.sleep(3)
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        return html


def get_data(collegeid, provid, wl):
    href_data = "http://kaoshi.edu.sina.com.cn/?p=college&s=api2015&a=getCollegeScore&collegeid=%s&syear=5&wl=%s&provid=%s" % (collegeid, wl, provid)
    print(href_data)
    return get_html(href_data)


def write_file(file, row):
    file.write((",".join(row) + '\r\n'))


def write_header(file):
    file.write('招生地区,学校,年份,最高,平均,投档,录取人数,录取批次,录取线差,科目,省份' + '\r\n')


def get_areacollege(href):
    html = get_html(href)
    soup = BeautifulSoup(html, 'html.parser')

    college_nodes = soup.select('.tabsContainer_ul li')
    schools = []
    for school in college_nodes:
        href_college = school.a.get('href')
        text = school.select('.college_info > .clearfix')[0].a.h4.get_text()
        schools.append((text, href_college))
    return schools


html1 = get_html("http://edu.sina.com.cn/college/index.shtml?")
# print(html1)
soup1 = BeautifulSoup(html1, 'html.parser')
row = []

node_areas = soup1.select('.w700r > a')

# 分区，在这里可以断点续传
for node_area in node_areas[0:32]:
    area = node_area.get_text()
    print(area)
    output_w = open(os.path.join('data', area + '_文科.txt'), 'a')
    output_l = open(os.path.join('data', area + '_理科.txt'), 'a')

    write_header(output_w)
    write_header(output_l)

    # more
    href_more1 = node_area.get('href')
    schools = []
    schools.extend(get_areacollege(href_more1))

    try:
        totalPage = BeautifulSoup(get_html(href_more1), 'html.parser').select('.pageNumWrap')[0]['totalpage']

        for pageNum in range(2, int(totalPage) + 1):
            schools.extend(get_areacollege(href_more1 + '&page=' + str(pageNum)))
    except:
        print('area:%s has not more pages' % area)

    # 区内学校
    for school in schools:
        href2 = school[1]
        college_name = school[0]
        collegeid = href2[- 11:-6]

        # 遍历科目
        for wl in subjects:
            for provid in plist:
                data = get_data(collegeid, provid, wl)
                if data != '[]':
                    try:
                        decodejson = json.loads(data)
                    except:
                        print('collegeid:%s provid:%s wl:%s college_name:%s area:%s' % (
                        collegeid, provid, wl, college_name, area))
                        continue

                    # 该省份不招生
                    if not 'data' in decodejson.keys():
                        continue

                    for rowdata in decodejson['data']['list']:
                        row = []
                        batch_diff = str(rowdata['batch_diff'])
                        score_max = rowdata['score_max']
                        score_avg = rowdata['score_avg']
                        score_td = rowdata['score_td']
                        plan = rowdata['plan']

                        batch_data = rowdata['batch']
                        batch = ""

                        if batch_diff == '0.00':
                            batch_diff = ''
                        elif len(batch_diff) > 1 and batch_diff[0] == '-':
                            batch_diff = ''

                        if score_max == '0.00':
                            score_max = ''

                        if score_avg == '0.00':
                            score_avg = ''

                        if score_td == '0.00':
                            score_td = ''

                        if plan == '0.00' or plan == '0':
                            plan = ''

                        if batch_data in array_batch.keys():
                            batch = array_batch[rowdata['batch']]
                        else:
                            batch = 'undefined'
                            # 未定义的不统计
                            continue

                        try:
                            row.extend(
                                [area, college_name, rowdata['syear'], score_max, score_avg, score_td, plan, batch,
                                 batch_diff, subjects[wl], provinces[provid]])
                        except:
                            print('collegeid:%s provid:%s wl:%s college_name:%s area:%s' % (
                            collegeid, provid, wl, college_name, area))
                            raise Exception('Data Error...')
                        if wl == '1':
                            write_file(output_w, row)
                        elif wl == '2':
                            write_file(output_l, row)

    output_w.close()
    output_l.close()

print('Congratulations Success')
