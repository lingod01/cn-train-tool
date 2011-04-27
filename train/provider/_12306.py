#coding=utf8
#铁路客户服务中心(http://www.12306.cn/) 的协议实现
import math
import urllib2
import urllib
import re
    
DEFAULT_ENCODE_PWD = 'liusheng'

#TODO cache it 
def get_ict_value():
    page = urllib2.urlopen('http://dynamic.12306.cn/TrainQuery/leftTicketByStation.jsp')
    content = page.read()
    pattern = re.compile(r"<input type=\"hidden\" id=\"(ict\w+)\" name=\"(ict\w+)\" value=\"(\d+)\"\/>")
    match = pattern.search(content)
    return match.group(2),match.group(3)
    
def yupiao(date, start_station, arrive_station, train_code = None):
    u'''查询余票数目
    返回结果为一个列表，列表元素为字典, 比如
    [
      {'train_code' : 'G70310',
       'start_station' : u'南京',
       'arrive_station' : u'上海',
       'start_time' : '2011-04-26 21:00',
       'end_time' : '2011-04-26 22:23',
       'duration' : '01:23',
       'ticket' : {
         u'软卧' : '--', #None 表示无此席别 
         u'特等座' : 15,
         u'一等座' : 38,
         u'二等座' : 431,
         u'高级软卧' : '--', 
         u'无座' :  '有',  #True 表示有
       }
      }
    ]
    '''
    date = date.split('-')
    month = '%02d' %(int(date[0]))
    day = '%02d' %(int(date[1]))
    if not train_code:
        train_code = ''

    post_data = {
        'nmonth3' : month,
        'nmonth3_new_value' : 'true', #not sure what is this
        'nday3' : day,
        'nday3_new_value' : 'false',  #not sure what is this
        'startStation_ticketLeft' : _encode_station(start_station, DEFAULT_ENCODE_PWD),
        'startStation_ticketLeft_n...' : 'false',
        'arriveStation_ticketLeft' :  _encode_station(arrive_station, DEFAULT_ENCODE_PWD),
        'arriveStation_ticketLeft_...' : 'false',
        'trainCode' : train_code,
        'trainCode_new_value' : 'true',

        #no idea what is this
        'rFlag' : 1,
        'fdl' : 'fdl',
        'lx' : 00,
        'name_ckball' : 'value_ckball',
    }
    ictKey,ictValue = get_ict_value()
    post_data[ictKey] = ictValue
    for flag in ('DC', 'K', 'LK', 'PK', 'PKE', 'T', 'Z'):
        post_data['tFlag%s' %flag] = flag

    f = urllib2.urlopen('http://dynamic.12306.cn/TrainQuery/iframeLeftTicketByStation.jsp',
        data = urllib.urlencode(post_data))
    train_data = f.read()
    return parse_trains(train_data)

    
def get_suggestion(code, date):
    u'''
    >>> len(get_suggestion('NJ', '20110424'))
    10
    '''
    page = urllib2.urlopen(
        'http://dynamic.12306.cn/TrainQuery/autocomplete.do?method=getStationName&inputValue=%s&date=%s' %(code,date)
    )
    content = page.read()
    matches = re.findall(r'<option value=\'.*?\'>(.*?)</option>', content)
    return [m.decode('utf-8') for m in matches]

def parse_trains(data):
    pattern = re.compile(r'parent\.mygrid\.addRow\(\d+,\"([^"]+)\" , \d+\);')
    matches = pattern.findall(data)
    trains = []
    for match in matches:
        match = match.decode('utf-8')
        seq,train_code,start_station,arrive_station,start_time,arrive_time,duration,yz,rz,yw,rw,tdz,ydz,edz,gzrw,wz,train_class = match.split(',')
        train = {
            u'train_code' : train_code.split('^')[0],
            u'start_station' : start_station.split('^')[0],
            u'arrive_station' : arrive_station.split('^')[0],
            u'start_time' : start_time,
            u'arrive_time' : arrive_time,
            u'duration' : duration,
            u'yz' : yz,
            u'rz' : rz,
            u'yw' : yw,
            u'rw' : rw,
            u'tdz' : tdz,
            u'ydz' : ydz,
            u'edz' : edz,
            u'gjrw' : gzrw, 
            u'wz' :  wz,  
        }
        trains.append(train)
    return trains
    
FIELDS = (
    (u'train_code' , u'车次'),
    (u'start_station' , u'发站'),
    (u'arrive_station' , u'到站'),
    (u'start_time' , u'发时'),
    (u'arrive_time' , u'到时'),
    (u'duration' , u'历时'),
    (u'yz', u'硬座'),
    (u'rz', u'软座'),
    (u'yw', u'硬卧'),
    (u'rw', u'软卧'),
    (u'tdz', u'特等座'),
    (u'ydz', u'一等座'),
    (u'edz', u'二等座'),
    (u'gjrw', u'高级软卧'),
    (u'wz', u'无座'), 
)

def format_trains(trains, format = 'text'):
    if format == 'text':
        ret = [u'|'.join([item[1] for item in FIELDS])]
        for train in trains:
            ret.append(u'|'.join([train[key].strip() for key,value in FIELDS]))
        return u'\n'.join(ret)
    elif format == 'html':
        ret = ['<table>']
        ret.append(u"<tr>%s</tr>" % u''.join([u"<th>%s</th>" % item[1] for item in FIELDS]))
        for train in trains:
            ret.append(u"<tr>%s</tr>" % u''.join([u"<td>%s</td>" %train[key].strip() for key,value in FIELDS]))
        ret.append('</table>')
        return u'\n'.join(ret)
 
        

def _encode_station(string, pwd, salt = None):
    u'''
    >>> _encode_station(u'南京西', 'liusheng', 41736839)
    '53574e13891e027cda87'
    '''
    prand = ''.join([str(ord(x)) for x in pwd])
    pos = len(prand) / 5
    mult = int(prand[pos] + prand[pos*2] + prand[pos*3] + prand[pos*4] + prand[pos*5], 10)
    incr = int(math.ceil(len(pwd) * 1.0 / 2))
    modu = int(math.pow(2, 31) - 1)
    if salt is None:
        #salt = 57614332
        import random
        salt = int(round(random.random() * 1000000000) % 1000000000)
    prand += str(salt)
    prand = (mult * len(prand) + incr) % modu
    enc_chr = ""
    enc_str = ""
    for ch in string:
        enc_chr = ord(ch) ^ int(math.floor((1.0 * prand / modu) * 255))
        enc_str += '%02x' %enc_chr
        prand = (mult * prand + incr) % modu
    salt = "%08x" %salt
    enc_str += salt
    return enc_str


if __name__ == "__main__":
    #print parse_trains(s)
    #print yupiao('04-27', u'南京', u'上海')
    #print get_ict_value()
    import doctest
    doctest.testmod()
    #print u','.join(get_suggestion('NJ', '20110425'))
