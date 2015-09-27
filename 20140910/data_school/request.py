import urllib
import urllib2

def request_ajax_data(url,data,referer=None,**headers):
    req = urllib2.Request(url)
    req.add_header('Content-Type','text/html; charset=gb2312')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0')
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    params = urllib.urlencode(data)
    response = urllib2.urlopen(req, params)
    jsonText = response.read()
    return json.loads(jsonText)

ajaxRequestBody = {"_action":"collegescore","provid":"20","collegeid":"10001","wl":"1","num":"0"}
ajaxResponse = request_ajax_data('http://outofmemory.cn/fakeAjax',ajaxRequestBody,"http://kaoshi.edu.sina.com.cn/college/c/10001.shtml")
print ajaxResponse
