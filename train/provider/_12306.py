#coding=utf8
#铁路客户服务中心(http://www.12306.cn/) 的协议实现
import math
import urllib2
import urllib
import re
    
DEFAULT_ENCODE_PWD = 'liusheng'

def yupiao(date, start_station, arrive_station, train_code = ''):
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
         u'软卧' : None, #None 表示无此席别 
         u'特等座' : 15,
         u'一等座' : 38,
         u'二等座' : 431,
         u'高级软卧' : -1, 
         u'无座' :  True,  #True 表示有
       }
      }
    ]
    '''
    date = date.split('-')
    month = '%02d' %(int(date[0]))
    day = '%02d' %(int(date[1]))

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
        'ictN' : 629,
        'lx' : 00,
        'name_ckball' : 'value_ckball',
    }
    for flag in ('DC', 'K', 'LK', 'PK', 'PKE', 'T', 'Z'):
        post_data['tFlag%s' %flag] = flag

    f = urllib2.urlopen('http://dynamic.12306.cn/TrainQuery/iframeLeftTicketByStation.jsp',
        data = urllib.urlencode(post_data))
    train_data = f.read()
    return parse_trains(train_data)

    

def parse_trains(data):
    pattern = re.compile(r'parent\.mygrid\.addRow\(\d+,\"([^"]+)\" , \d+\);')
    matches = pattern.findall(data)
    trains = []
    for match in matches:
        seq,train_code,start_station,arrive_station,start_time,arrive_time,duration,yz,rz,yw,rw,tdz,ydz,edz,gzrw,wz,train_class = match.split(',')
        train = {
            'train_code' : train_code.split('^')[0],
            'start_station' : start_station.split('^')[0],
            'arrive_station' : arrive_station.split('^')[0],
            'start_time' : start_time,
            'arrive_time' : arrive_time,
            'duration' : duration,
            'ticket': {
                u'硬座' : yz,
                u'软座' : rz,
                u'硬卧' : yw,
                u'软卧' : rw,
                u'特等座' : tdz,
                u'一等座' : ydz,
                u'二等座' : edz,
                u'高级软卧' : gzrw, 
                u'无座' :  wz,  
            }
        }
        trains.append(train)
    return trains
    
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
    '''parent.mygrid.addRow(0,"1,G7389(南京->杭州)^skbcx.jsp?cxlx=cc&date=20110427&trainCode=G7389 ,南京^skbcx.jsp?cxlx=czjgcc&zm=&date=20110427&stationName_passTrain=%E5%8D%97%E4%BA%AC , 上海虹桥^skbcx.jsp?cxlx=czjgcc&zm=&date=20110427&stationName_passTrain=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5, 19:25 ,21:10 ,01:45, -- , -- ,--,--,--,88,333,--,有,高速" , 0);
    '''
    #print parse_trains(s)
    print yupiao('04-27', u'南京', u'上海')
    #import doctest
    #doctest.testmod()
