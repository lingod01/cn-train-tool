#!/usr/bin/env python
#coding=utf8
'''
Train Query Tool
'''

if __name__ == "__main__":
    from optparse import OptionParser
    import sys
    parser = OptionParser()
    parser.add_option("-d", "--date", dest="date",
                      help="date train leaves")
    parser.add_option("-s", "--start", dest="start_station",
                      help="start station")
    parser.add_option("-a", "--arrive", dest="arrive_station",
                      help="arrive station")
    parser.add_option("-t", "--train", dest="train_code",
                      help="train_code")
    (options, args) = parser.parse_args()

    from train.provider._12306 import yupiao,format_trains
    if options.date and options.start_station and options.arrive_station:
        if options.train_code:
            ret = yupiao(options.date, options.start_station.decode(sys.stdin.encoding), options.arrive_station.decode(sys.stdin.encoding), options.train_code)
        else:
            ret = yupiao(options.date, options.start_station.decode(sys.stdin.encoding), options.arrive_station.decode(sys.stdin.encoding))
        if not sys.stdout.encoding:
            print format_trains(ret).encode('utf-8')
        else:
            print format_trains(ret)
    else:
        parser.error('argument not enough')
        parser.print_usage()
