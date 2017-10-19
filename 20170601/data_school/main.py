# encoding:gbk
import json
import os
import urllib.request
from bs4 import BeautifulSoup
import time

wllist = ['1', '2', '3']
# subjects = {'1': '�Ŀ�', '2': '���', '3': '�ۺ�'}
subjects = {'1': '�Ŀ�', '2': '���'}

provinces = {'1': '����', '2': '���', '3': '�Ϻ�', '4': '����', '5': '�ӱ�', '6': '����', '7': 'ɽ��', '8': 'ɽ��', '9': '����',
             '10': '����', '11': '����', '12': '�㽭', '13': '����', '14': '����', '15': '�㶫', '16': '����', '17': '����', '18': '����',
             '19': '�Ĵ�', '20': '����', '21': '�ຣ', '22': '����', '23': '������', '24': '����', '25': '����', '26': '����',
             '27': '�½�', '28': '���ɹ�', '29': '����', '30': '����', '31': '����', '32': '�۰�̨'}
plist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
# array_batch = {'00': '����', '01': '������ǰ��', '11': '����һ��', '12': '���ƶ���', '123': '���ƶ�����', '13': '��������', '21': 'ר��'}
array_batch = {'01': '������ǰ��', '11': '����һ��', '12': '���ƶ���', '13': '��������'}


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
    file.write('��������,ѧУ,���,���,ƽ��,Ͷ��,¼ȡ����,¼ȡ����,¼ȡ�߲�,��Ŀ,ʡ��' + '\r\n')


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

# ��������������Զϵ�����
for node_area in node_areas[0:32]:
    area = node_area.get_text()
    print(area)
    output_w = open(os.path.join('data', area + '_�Ŀ�.txt'), 'a')
    output_l = open(os.path.join('data', area + '_���.txt'), 'a')

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

    # ����ѧУ
    for school in schools:
        href2 = school[1]
        college_name = school[0]
        collegeid = href2[- 11:-6]

        # ������Ŀ
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

                    # ��ʡ�ݲ�����
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
                            # δ����Ĳ�ͳ��
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
