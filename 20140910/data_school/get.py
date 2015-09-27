import urllib

def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

html = get_html("http://kaoshi.edu.sina.com.cn/iframe/i_collegescore.php?_action=collegescore&provid=%s&collegeid=%s&wl=%s&num=%s" % ('20','10001','1','0'))
print html
