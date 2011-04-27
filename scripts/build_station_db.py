#!/usr/bin/env python
#coding=utf8
'''
Train Query Tool
'''

def main():
    import time
    import datetime
    from train.provider._12306 import get_suggestion
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    today = datetime.datetime.today().strftime('%Y%m%d')
    for c1 in letters:
        for c2 in letters:
            print 'get suggest for ',c1+c2
            f = open(c1 + c2 + '.txt', 'w')
            f.write(u','.join(get_suggestion(c1+c2, today)).encode('utf-8'))
            f.close()
            time.sleep(1)

        
if __name__ == "__main__":
    main()
