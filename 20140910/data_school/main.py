#encoding:gbk
import urllib
from bs4 import BeautifulSoup
import json
import os
import time

wllist = ['1','2','3']
subjects = {'1':'�Ŀ�','2':'���','3':'�ۺ�'}

provinces = {'1':'����','2':'���','3':'�Ϻ�','4':'����','5':'�ӱ�','6':'����','7':'ɽ��','8':'ɽ��','9':'����','10':'����','11':'����','12':'�㽭','13':'����','14':'����','15':'�㶫','16':'����','17':'����','18':'����','19':'�Ĵ�','20':'����','21':'�ຣ','22':'����','23':'������','24':'����','25':'����','26':'����','27':'�½�','28':'���ɹ�','29':'����','30':'����','31':'����','32':'�۰�̨'}
plist = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
array_batch = {'00':'����','01':'������ǰ��','11':'����һ��','12':'���ƶ���','123':'���ƶ�����','13':'��������','21':'ר��'}

def get_html(url):
    try:
        page = urllib.urlopen(url)
        html = page.read()
        return html
    except:
        time.sleep(3)
        page = urllib.urlopen(url)
        html = page.read()
        return html

def get_data(collegeid,provid,wl):
    return get_html("http://kaoshi.edu.sina.com.cn/iframe/i_collegescore.php?_action=collegescore&provid=%s&collegeid=%s&wl=%s&num=%s" % (provid,collegeid,wl,'0'))

def write_file(file, row):
    file.write((",".join(row)+'\r\n').encode('gbk'))

def write_header(file):
    file.write('��������,ѧУ,���,���,ƽ��,Ͷ��,¼ȡ����,¼ȡ����,¼ȡ�߲�,��Ŀ,ʡ��'+'\r\n')

def get_areacollege(href):
    html = get_html(href)
    soup = BeautifulSoup(html)

    college_nodes = soup.select('tr .td1 a')
    schools = []
    for school in college_nodes:
        href_college = school.get('href')
        schools.append((school.get_text(), href_college))
    return schools

html1 = get_html("http://edu.sina.com.cn/college/index.shtml?")
soup1 = BeautifulSoup(html1)
row = []


node_areas = soup1.select('.box-01 .b_cont')

#��������������Զϵ�����
for node_area in node_areas[27:]:
    area = node_area.select('h3 .t_name a')[0].get_text()
    output_w = open(os.path.join('data',area+'_�Ŀ�.txt'.decode('gbk')),'a')
    output_l = open(os.path.join('data',area+'_���.txt'.decode('gbk')),'a')
    output_z = open(os.path.join('data',area+'_�ۺ�.txt'.decode('gbk')),'a')
    write_header(output_w)
    write_header(output_l)
    write_header(output_z)
    node_colleges = node_area.select('.list_002 li a[href^="http://kaoshi.edu.sina.com.cn/college"]')

    #more
    more = node_area.select('h3 .t_more a')
    href_more1 = more[0].get('href')
    schools = []
    schools.extend(get_areacollege(href_more1))

    try:
        college_page_nodes = BeautifulSoup(get_html(href_more1)).select('.pagebox_cur_page')[0].parent.parent.select('a[title^="page"]')
        for college_page_node in college_page_nodes:
            schools.extend(get_areacollege('http://kaoshi.edu.sina.com.cn'+college_page_node.get('href')))
    except:
        print 'area:%s has not more pages' % (area)
        
    #more
    #Find Error
##    print get_data(13282,16,1)=='[]'
##    break
    #Find Error
    
    #����ѧУ
    for school in schools:    
        href2 = school[1]
        college_name = school[0]
        collegeid = href2[len(href2)-11:-6]

        #������Ŀ
        for wl in subjects:
            for provid in plist:
                data = get_data(collegeid,provid,wl)
                if data != '[]':
                    try:
                        decodejson = json.loads(data)
                    except:
                        print data
                        print 'collegeid:%s provid:%s wl:%s college_name:%s area:%s' % (collegeid,provid,wl,college_name,area)
                        continue
                        
                    for rowdata in decodejson:
                        row = []
                        batch_diff = rowdata['batch_diff']
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
                            batch = array_batch[rowdata['batch']].decode('gbk')
                        else:
                            batch = 'undefined'

                        try:
                            row.extend([area,college_name,rowdata['syear'],score_max,score_avg,score_td,plan,batch,batch_diff,subjects[wl].decode('gbk'),provinces[provid].decode('gbk')])
                        except:
                            print data
                            print 'collegeid:%s provid:%s wl:%s college_name:%s area:%s' % (collegeid,provid,wl,college_name,area)
                            raise Exception('Data Error...')
                        if wl=='1':
                            write_file(output_w,row)
                        elif wl=='2':
                            write_file(output_l,row)
                        else:
                            write_file(output_z,row)

    output_w.close()
    output_l.close()
    output_z.close()

print 'Congratulations Success'


