def hms_to_second(hms):
    hour, minute, second = map(int, hms.split(sep=':'))
    return hour * 3600 + minute * 60 + second


def second_to_hms(second):
    hour = second // 3600
    minute = (second % 3600) // 60
    second = second % 60
    
    return '%02d:%02d:%02d' % (hour, minute, second)
