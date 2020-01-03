import http.client
global get_figure
global level
level=0
get_figure=False
HOST_DNS='docs.oracle.com'
CHARSET='utf-8'
#URL='/en/database/oracle/oracle-database/19/sqlrf/COMMIT.html'
URL='/en/database/oracle/oracle-database/19/sqlrf/index.html'
URL='/en/database/oracle/oracle-database/19/sqlrf/ADMINISTER-KEY-MANAGEMENT.html'
URL='/en/database/oracle/oracle-database/19/sqlrf/CREATE-CLUSTER.html'
#URL='/en/database/oracle/oracle-database/19/sqlrf/CREATE-TABLE.html'
conn = http.client.HTTPSConnection(HOST_DNS)
#conn = http.client.HTTPSConnection("www.python.org")
conn.request("GET", URL)
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()  # This will return entire content.
# The following example demonstrates reading data in chunks.
conn.request("GET", URL)
r1 = conn.getresponse()
#while not r1.closed:
#for _ in range(20):
#    print(r1.read(200))  # 200 bytes
data=r1.read()
#conn.close()
from html.parser import HTMLParser

class SubHTMLParser(HTMLParser):
    def handle_data(self, data):
        print(data)
    
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global get_figure
        global level
        level+=1
        #print("Encountered a start tag:", tag)
        if get_figure:
            #print('Found_get_figure')
            if tag == 'div':
                #print('Found_div')
                if ('class','figure') in attrs:
                    #print('Found_class_figure')
                    pass
            for pair in attrs:
                if pair[0]=='href':
                    if pair[1].startswith('img_text/'):
                    #print('Found_longdesc')
                        urltail=pair[1]
                        print(urltail)
                        urlhead=URL[:URL.rindex('/')]
                        conn.request("GET", urlhead+'/'+urltail)
                        r1 = conn.getresponse()
                        data=r1.read()
                        print(data)
                        subparser.feed(data.decode(CHARSET))
                        get_figure=False

    def handle_endtag(self, tag):
        global level
        level-=1

    def handle_data(self, data):
        global get_figure
        global prev_data
        if '::=' in data:
            if data.startswith('::='):
                print(prev_data+'::=')
                get_figure=True
            else:
                print(data)
        prev_data=data

subparser=SubHTMLParser()
parser = MyHTMLParser()
parser.feed(data.decode(CHARSET) )
