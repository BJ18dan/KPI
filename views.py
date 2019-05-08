"""存放场用的方法"""
import calendar
import datetime
import time
from mongobdhelper import get_mongodb_conn
from mysqlhelper import DealTable
from business_calendar import Calendar, MO, TU, WE, TH, FR
from sql_centence import get_sign_data

def caculate_add_time(checkType,workday_temp,userCheckTime_temp,scheduleName):
    hours = 0
    seconds = 0
    if checkType == 'offDuty':
        if scheduleName != "管理班次":
            seconds = userCheckTime_temp - workday_temp - 64800
        else:
            seconds = userCheckTime_temp - workday_temp - 63000
    if seconds >= 7200:
        hours = seconds / 3600
    return hours

def timestamp_from_objectid(objectid):
    """提取objectid中的时间戳"""
    result = 0
    try:
        result = time.mktime(objectid.generation_time.timetuple()) + 28800
    except:
        pass
    return result

def judge_time():
    """获得时间戳，用于筛选每日要处理的数据"""
    t = time.strftime('%Y-%m-%d', time.localtime())
    timeArray = time.strptime(t, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))  # today day
    timeStamp_yesterday = timeStamp - 86400  # last day

    timeStamp = timeStamp*1000
    timeStamp_yesterday = timeStamp_yesterday*1000
    return timeStamp, timeStamp_yesterday

# def timestamp_to_date(time_stamp):
#     timeArray = time.localtime(time_stamp)
#     date_time1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     date_time = datetime.datetime.strptime(date_time1, "%Y-%m-%d %H:%M:%S")  # <class 'datetime.datetime'>
#
#     return date_time

def timestamp_to_date(time_stamp, time_style):
    """时间戳转化为时间"""
    timeArray = time.localtime(time_stamp)
    if time_style == 1:
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    else:
        otherStyleTime = time.strftime("%Y-%m-%d  %H:%M:%S", timeArray)
    return  otherStyleTime

def add_loss_data():
    """判断时间，records表中增量添加数据.如果前天——1个月前数据量不一致则，重新存入一个月前至昨天的数据，否则存入昨天数据"""
    deal = DealTable()

    today, yesterday = judge_time()
    before_yesterday =  today-86400000
    month_ago = 1554051600000
    before_yesterday_date = str(timestamp_to_date(before_yesterday/1000-86400, time_style=0))
    month_ago_date = str(timestamp_to_date(month_ago/1000, time_style=0))
    filter = {'workday': {'$gte': month_ago, '$lt': before_yesterday}}
    sql = "select count(1) from records where workday between '{month_ago_date}' and '{before_yesterday_date}'".format(month_ago_date=month_ago_date,before_yesterday_date=before_yesterday_date)
    length1 = get_mongodb_conn(choose='records', filter=filter, flag=0)
    length2 = deal.get_data(sql=sql, return_results=1)[0][0]

    if length1 != length2:
        filter = {'workday': {'$gte': month_ago, '$lt': today}}
    else:
        filter = {'workday': {'$gte': yesterday, '$lt': today}}

    datas = get_mongodb_conn(choose='records', filter=filter, flag=1)
    return datas

def get_workdays(year, month, tail):
    date1 = datetime.datetime(year, month, 1)
    # normal calendar, no holidays
    cal = Calendar(workdays=[MO, TU, WE, TH, FR])
    date2 = datetime.datetime(year, month, tail)
    days = cal.busdaycount(date1, date2)
    return days

def get_month_workdays():
    """year:年  d：月  """
    FORMAT = "%d-%d-%d"
    year = 2019
    month_work_days = {}
    for m in range(1, 13):
        d = calendar.monthrange(year, m)
        x = FORMAT % (year, m, 1)
        y = FORMAT % (year, m, d[1])
        tail = d[1]
        # b=time.strftime('%Y%m%d',time.strptime(x,'%Y-%m-%d'))
        # c=time.strftime('%Y%m%d',time.strptime(y,'%Y-%m-%d'))
        # d=time.strftime('%Y-%m-%d',time.strptime(str(b),'%Y%m%d'))
        # e=time.strftime('%Y-%m-%d',time.strptime(str(c),'%Y%m%d'))
        days = get_workdays(year, m, tail)
        m = str(m) if m > 9 else str(0) + str(m)
        key = str(year) + '-' + m
        month_work_days[key] = days
    return month_work_days

def get_sign_date():
    deal = DealTable()
    results_sign = deal.get_data(sql=get_sign_data, return_results=1)
    dic1 = {}
    for r in results_sign:
        dic_month = {}
        employee_id = r[0]
        month = r[1]
        num = r[2]
        if employee_id not in dic1.keys():  # 人在字典中
            dic_month[month] = num
            dic1[employee_id] = dic_month
        elif month not in dic1[employee_id].keys():
            dic1[employee_id][month] = num
    return dic1

def get_department():
    deal = DealTable()
    sql1 = "select employee_id,name, corp_id, corp_name, depart_id, depart_name, org_id, org_name, job_title from users"
    results = deal.get_data(sql=sql1, return_results=1)  # 获得个人部门信息
    dic1 = {}
    for result in results:
        employee_id = result[0]
        dic1[employee_id] = result
    return dic1

def get_month_range(start_day):
    end_day = datetime.date.today()  # 将指定格式的当前时间以字符串输出
    months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
    month_range = ['%s-%s' % (start_day.year + mon // 12, mon % 12 + 1)
                   for mon in range(start_day.month - 1, start_day.month + months)]
    for i in range(len(month_range)):
        if len(month_range[i]) == 6:
            month_range[i] = month_range[i].replace("-", "-0")
    return month_range
