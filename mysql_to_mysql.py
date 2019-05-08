"""
处理人员  请假表 和 外勤表

将records表中的打卡记录，整理成个人每天的打卡记录，生成people_records表
将个人打卡记录整理成个人月打卡记录，生成 worker_attendance 表
"""
import datetime
from sql_centence import count_times,insert_leave_sign_records,check_leave_sign_records,delete_leave_sign_records,check_leave_sign_records_1,update_signrecord_cnt,insert_people_records,check_worker_attendance,check_people_records,delete_people_records,insert_worker_attendance_data,delete_worker_attendance
from mysqlhelper import DealTable
from views import get_month_workdays,get_sign_date,get_department

def deal_leave_records():

    sql1 = "select * from leave_records"
    deal = DealTable()
    results1 = deal.get_data(sql=sql1, return_results=1)
    dic1 = {}  # 存放所有员工请假信息
    temp_name = ''
    for r in results1:
        # print(r)
        list_temp_people = {}  # 存放人
        list_temp_month = {}  # 存放月份信息
        list_temp_data = []  # 存放请假信息
        year_month = r[3].strftime("%Y-%m")  # 年-月
        time = r[3]
        list_temp_data.extend([r[1], r[3], r[6], r[7]])

        list_temp_month[time] = list_temp_data

        if r[2] != temp_name:  # 人名不同
            if r[2] not in dic1.keys():  # 名字不同，且不存在字典中
                list_temp_people[year_month] = list_temp_month
                dic1[r[2]] = list_temp_people
            elif year_month not in dic1[r[2]].keys():  # 名字在，月份不在
                dic1[r[2]][year_month] = list_temp_month

            elif time not in dic1[r[2]][year_month].keys():  # 名字不同，已在，月份在，计划不在
                dic1[r[2]][year_month][time] = list_temp_data
        elif year_month not in dic1[temp_name].keys():  # 名字同，月份不在
            dic1[r[2]][year_month] = list_temp_month
        elif r[2] not in dic1[temp_name][year_month].keys():  # 名字同，月份在，计划不在
            dic1[r[2]][year_month][time] = list_temp_data
        temp_name = r[2]  # 重置

    for k1, v1 in dic1.items():
        for k2, v2 in v1.items():
            leave_year_cnt = 0  # 年假
            leave_other_cnt = 0  # 事假
            signrecord_cnt = 0  # 外勤
            for k3, v3 in v2.items():
                employee_id = v3[0]
                if v3[2] == '年休假':
                    if v3[3] == '全天':
                        leave_year_cnt += 1.0
                    else:
                        leave_year_cnt += 0.5
                else:
                    if v3[3] == '全天':
                        leave_other_cnt += 1.0  # 外勤天数加1（使）
                    else:
                        leave_other_cnt += 0.5

            single_info = (employee_id, k1, k2,leave_other_cnt, leave_year_cnt, signrecord_cnt)
            insert_sql = insert_leave_sign_records.format(employee_id=employee_id, name=k1, time=k2, leave_other_cnt=leave_other_cnt, leave_year_cnt=leave_year_cnt,signrecord_cnt=signrecord_cnt)
            check_sql = check_leave_sign_records.format(employee_id=employee_id, time=k2)  # 查询记录
            delete_sql = delete_leave_sign_records.format(employee_id=employee_id, time=k2)
            deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)

def deal_signinrecords():
    deal = DealTable()
    sql1 = "select employee_id, name, date, timeStatus from signinrecords"
    results = deal.get_data(sql=sql1, return_results=1)
    dic1 = {}  # 存放所有员工请假信息
    temp_name = ''
    for r in results:
        # print(r)
        list_temp_people = {}  # 存放人
        list_temp_month = {}  # 存放月份信息
        list_temp_data = []  # 存放请假信息
        year_month = r[2].strftime("%Y-%m")  # 年-月
        time = r[2]
        list_temp_data.extend([r[0], r[2], r[3]])
        list_temp_month[time] = list_temp_data

        if r[1] != temp_name:  # 人名不同
            if r[1] not in dic1.keys():  # 名字不同，且不存在字典中
                list_temp_people[year_month] = list_temp_month
                dic1[r[1]] = list_temp_people
            elif year_month not in dic1[r[1]].keys():  # 名字在，月份不在
                dic1[r[1]][year_month] = list_temp_month
            elif time not in dic1[r[1]][year_month].keys():  # 名字不同，已在，月份在，计划不在
                dic1[r[1]][year_month][time] = list_temp_data

        elif year_month not in dic1[temp_name].keys():  # 名字同，月份不在
            dic1[r[1]][year_month] = list_temp_month
        elif r[1] not in dic1[temp_name][year_month].keys():  # 名字同，月份在，计划不在
            dic1[r[1]][year_month][time] = list_temp_data
        temp_name = r[1]  # 重置

    for k1, v1 in dic1.items():
        # print(k1)
        for k2, v2 in v1.items():
            # print(k2)  # 月
            leave_other_cnt = 0
            leave_year_cnt = 0
            signrecord_cnt = 0.0  # 外勤签到
            for k3, v3 in v2.items():
                employee_id = v3[0]
                if v3[2] == '全天':
                    signrecord_cnt += 1.0
                else:
                    signrecord_cnt += 0.5
        #
            single_info = (employee_id, k2, signrecord_cnt)
            insert_sql = insert_leave_sign_records.format(employee_id=employee_id, name=k1, time=k2,leave_other_cnt=leave_other_cnt, leave_year_cnt=leave_year_cnt, signrecord_cnt=signrecord_cnt)
            check_sql = check_leave_sign_records_1.format(employee_id=employee_id, time=k2)  # 查询记录

            check_results = deal.get_data(sql=check_sql, return_results=1)  # 查询出勤记录是否在表中
            if check_results == ():  # 如果某条记录不存在，则插入数据
                deal.deal_table(sql=insert_sql)
            else:
                md5_1 = deal.get_md5_value(str(check_results[0]))
                md5_2 = deal.get_md5_value(str(single_info))
                if md5_1 != md5_2:
                    update_sql = update_signrecord_cnt.format(signrecord_cnt=signrecord_cnt, employee_id=employee_id, time=k2)
                    deal.deal_table(sql=update_sql)  # 插入新数据

def get_people_records():
    deal = DealTable()
    sql1 = "select employee_id, name, workday, userCheckTime, checkType, timeResult, scheduleName, add_times from records"
    results1 = deal.get_data(sql=sql1, return_results=1)  # 获得结果

    dic1 = {}
    for result1 in results1:
        dic2 = {}
        # result [employee_id, name, workday, userCheckTime, checkType, timeResult, scheduleName, add_times]
        key_list = dic1.keys()
        employee_id = result1[0]  # 用户id
        on_off_day = result1[4]  # checkType : onDuty or offDuty
        time = result1[3].strftime("%Y-%m-%d %H:%M:%S")  # userCheckTime 打卡时间
        # time = result1[3]  # userCheckTime 打卡时间
        type = result1[5]  # timeResult 打卡结果
        # workday = result1[2].strftime("%Y-%m-%d")  # 年月  # 工作日
        workday = result1[2]  # 年月  # 工作日
        if employee_id not in key_list:  # 员工没有存入字典
            list_temp = [-1, -1, -1, -1, -1, -1]  # [上班时间，上班结果，下班时间，下班结果，班次，加班时间]
            if on_off_day == 'onDuty':
                list_temp[0] = time
                list_temp[1] = type
            elif on_off_day == 'offDuty':
                list_temp[2] = time
                list_temp[3] = type
                list_temp[5] = result1[7]  # 存入加班时长
            list_temp[4] = result1[6]  # 存入打卡分组
            dic2[workday] = list_temp
            dic1[employee_id] = dic2
        else:
            if workday not in dic1[employee_id].keys():  # 员工id在，工作日不在
                list_temp = [-1, -1, -1, -1, -1, -1]
                if on_off_day == 'onDuty':
                    list_temp[0] = time
                    list_temp[1] = type
                elif on_off_day == 'offDuty':
                    list_temp[2] = time
                    list_temp[3] = type
                    list_temp[5] = result1[7]  # 存入加班时长
                list_temp[4] = result1[6]  # 存入打卡分组
                dic1[employee_id][workday] = list_temp
            else:  # 员工id在，工作日在，判断是上午or下午
                list_temp2 = dic1[employee_id][workday]
                if on_off_day == 'onDuty':
                    list_temp2[0] = time
                    list_temp2[1] = type
                elif on_off_day == 'offDuty':
                    list_temp2[2] = time
                    list_temp2[3] = type
                    list_temp2[5] = result1[7]  # 存入加班时长
    for key, values in dic1.items():
        for k, val in values.items():
            if val[0] == -1:
                val[0] = ''
                val[1] = 'NotSigned'
            if val[2] == -1:
                val[2] = ''
                val[3] = 'NotSigned'
            if val[5] == -1:
                val[5] = 0

            employee_id = key
            workday = k
            onDuty_time = val[0]
            onDuty_checktype = val[1]
            offDuty_time = val[2]
            offDuty_checktype = val[3]
            scheduleName = val[4]
            add_times = float(val[5])

            single_info = (employee_id, workday, onDuty_time,onDuty_checktype, offDuty_time,offDuty_checktype, scheduleName, add_times)
            insert_sql = insert_people_records.format(employee_id=employee_id, workday=workday, onDuty_time=onDuty_time,
                                              onDuty_checktype=onDuty_checktype, offDuty_time=offDuty_time,
                                              offDuty_checktype=offDuty_checktype, scheduleName=scheduleName,
                                              add_times=add_times)

            check_sql = check_people_records.format(employee_id=employee_id, workday=workday)  # 查询记录
            delete_sql = delete_people_records.format(employee_id=employee_id, workday=workday)
            deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)

def get_attendence():

    deal = DealTable()
    days_list = get_month_workdays()  # 获得每月法定工作天数
    results = deal.get_data(sql=count_times, return_results=1)
    results_sign = get_sign_date()  # 获得每人每月出现记录次数

    dic_worker = get_department()  # 获得每人工作信息
    for result in results:
        employee_id = result[0]  # 用户id
        date_time = result[1]  # 考勤月份

        date_time1 = datetime.date(int(date_time[0:4]),int(date_time[5:]),1)
        sign_in_normal = result[2]  # 早上正常签到
        sign_in_miss_cnt = result[3]  # 早上未打卡
        late_cnt = int(result[4])  # 迟到

        sign_out_normal = result[6]  # 下班打卡正常
        sign_out_miss_cnt = result[7]  # 下班未打卡
        over_time_cnt = round(result[8],6)  # 加班次数,控制小数精度

        leave_early_cnt = int(result[5] + sign_in_miss_cnt + sign_out_miss_cnt)  # 早退(未正常打卡算作早退)
        leave_cnt = 0.0  # 请假天数（无数据暂定为0.0）
        add_record = 0  # 补录次数（暂定为0）

        sql_leave_sign = "select employee_id, name, time, leave_other_cnt,leave_year_cnt, signrecord_cnt from leave_sign_records where employee_id='{employee_id}' and time='{time}'".format(employee_id=employee_id, time=date_time)
        result_temp = deal.get_data(sql=sql_leave_sign, return_results=1)

        days_cnt = results_sign[employee_id][date_time]
        abbsent_cnt = days_list[date_time] - days_cnt  # 旷工天数

        if result_temp != ():
            leave_cnt = result_temp[0][3]  # 添加请假数据(不包含年休假)

        info_list = dic_worker[employee_id]
        name = info_list[1]  # 姓名
        corp_id = info_list[2]  # 公司id
        corp_name = info_list[3]  # 公司名称
        depart_id = info_list[4]  # 部门id
        department = info_list[5]  # 部门名称
        org_id = info_list[6]  # 组织id
        org_name = info_list[7]  # 组织名称
        job_title = info_list[8]  # 职位

        single_info = (employee_id, name, department, date_time1, over_time_cnt, late_cnt, leave_early_cnt, leave_cnt,
              abbsent_cnt, add_record, corp_id, depart_id, org_id, job_title)

        insert_sql = insert_worker_attendance_data.format(employee_id=employee_id, name=name, department=department, date_time=date_time1,
                               over_time_cnt=over_time_cnt, late_cnt=late_cnt, leave_early_cnt=leave_early_cnt,
                               leave_cnt=leave_cnt, abbsent_cnt=abbsent_cnt, add_record=add_record, corp_name=corp_name,
                               corp_id=corp_id, depart_id=depart_id, org_id=org_id, org_name=org_name,
                               job_title=job_title)


        check_sql = check_worker_attendance.format(employee_id=employee_id, date_time=date_time1)  # 查询记录
        delete_sql = delete_worker_attendance.format(employee_id=employee_id, date_time=date_time1)
        deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)

if __name__ == "__main__":

    deal_leave_records()
    deal_signinrecords()
    get_people_records()
    get_attendence()