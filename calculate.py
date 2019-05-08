
import datetime
import math
from sql_centence import select_users,create_score,create_score_plan,insert_score_plan,insert_score,check_score_data
from views import get_month_range
from mysqlhelper import DealTable
from sql_centence import select_worker_attendance,select_worker_plan,check_score_data_plan,delete_score_data_plan,delete_score_data


def caculate_worker_attendance():
    """计算个人-出勤得分"""
    deal = DealTable()
    dic1 = {}  # 存放所有员工考勤
    results = deal.get_data(sql=select_worker_attendance, return_results=1)  # 获得个人出勤结果 worker_attendance
    temp_name = ''

    for r in results:
        list_temp_people = {}  # 存放人
        list_temp_data = []  # 存放人信息

        year_month = r[4].strftime("%Y-%m")  # 年月
        list_temp_data.extend([r[5], r[6], r[7], r[8], r[9], r[10]])

        if r[2] != temp_name:
            if r[2] not in dic1.keys():
                list_temp_people[year_month] = list_temp_data
                dic1[r[2]] = list_temp_people
            elif year_month not in dic1[r[2]].keys():  # 名字在，月份不在
                dic1[r[2]][year_month] = list_temp_data
        elif year_month not in dic1[temp_name].keys():
            dic1[temp_name][year_month] = list_temp_data

        temp_name = r[2]

    for name in dic1.keys():

        for month, values in dic1[name].items():
            month_attendance_score = 0

            over_time_cnt = math.floor(values[0])  # 加班次数
            late_cnt = values[1]  # 迟到次数
            leave_early_cnt = values[2]  # 早退次数
            add_record = values[5]  # 补录次数

            leave_cnt = values[3]  # 请假天数
            abssent_score = values[4]  # 旷工次数

            overtime_score = -0.3 * over_time_cnt  # 计算加班得分
            if over_time_cnt > 10:
                overtime_score += -(over_time_cnt - 10) * 0.2

            late_score = -0.1 * (late_cnt + leave_early_cnt - add_record)  # 计算（迟到和早退）-补卡 得分
            if (late_cnt + leave_early_cnt - add_record) > 5:
                late_score += -(late_cnt + leave_early_cnt - add_record - 5) * 0.05

            leave_score = -0.3 * leave_cnt  # 计算请假
            if leave_cnt > 3:
                leave_score += -(leave_cnt - 3) * 0.2


            month_attendance_score = 20 + overtime_score + late_score + leave_score - abssent_score
            dic1[name][month] = month_attendance_score
    # print('个人-考勤得分：', dic1)
    return dic1

def plan_score(days, over, plan_type):
    """计算每项任务得分"""
    if plan_type == "部门重点计划":
        plan_type_score = 1.2
    elif plan_type == '总体部考核计划':
        plan_type_score = 1.1
    else:
        plan_type_score = 1

    cycle = int(days) / 31  # 任务耗时周期
    real_score = 0  # 实际得分

    if over == 1:
        if cycle <= 1:  # 按时完成，得分
            real_score = plan_type_score
        elif cycle > 1 and cycle <= 2:  # 顺延到第二个月完成，得分0
            real_score = 0
        else:
            real_score = -2 * plan_type_score * (math.ceil(cycle) - 2)  # 二个月仍未完成扣除分数
    elif over == 0:  # 计划为完成，扣分
        if cycle > 2:
            real_score = -2 * plan_type_score * (math.ceil(cycle) - 2) # 未完成，且超过二个月
    else:
        print("计算得分出错")
    return real_score, 1

def plan_dic(results_2):
    dic2 = {}  # 存放所有员工计划
    temp_name = ''
    for r in results_2:

        list_temp_people = {}  # 存放人
        list_temp_month = {}  # 存放月份信息
        list_temp_data = []  # 存在计划信息
        year_month = r[1]  # 年-月
        plan_name = r[2]
        list_temp_data.extend([r[3], r[4], r[5], r[6], r[7],r[8],r[2]])

        list_temp_month[plan_name] = list_temp_data

        if r[0] != temp_name:  # 人名不同

            if r[0] not in dic2.keys():  # 名字不同，且不存在字典中

                list_temp_people[year_month] = list_temp_month
                dic2[r[0]] = list_temp_people

            elif year_month not in dic2[r[0]].keys():  # 名字在，月份不在
                dic2[r[0]][year_month] = list_temp_month

            elif plan_name not in dic2[r[0]][year_month].keys():  # 名字不同，已在，月份在，计划不在
                dic2[r[0]][year_month][plan_name] = list_temp_data

        elif year_month not in dic2[temp_name].keys():  # 名字同，月份不在
            dic2[r[0]][year_month] = list_temp_data
        elif r[2] not in dic2[temp_name][year_month].keys():  # 名字同，月份在，计划不在
            dic2[r[0]][year_month][plan_name] = list_temp_data

        temp_name = r[0]  # 重置

    return dic2

def caculate_worker_plan():
    """计算个人-计划每月得分"""
    deal = DealTable()
    results_2 = []  # 存放所有员工
    results = deal.get_data(sql=select_worker_plan, return_results=1)

    for r in results:
        start_time = r[3]
        end_time = r[4]
        complete_status = r[6]

        if complete_status == 1:
            days = int((end_time - start_time).days)  # 完成-相差天数
            over = 1
        elif complete_status == 2:
            timeArray = datetime.date.today()  # 将字符串转换为时间格式
            days = int((timeArray - start_time).days)  # 未完成相差天数
            over = 0
        else:
            days=30
            over = 0
        # if end_time is None and start_time is not None:
        #     timeArray = datetime.date.today()  # 将字符串转换为时间格式
        #     days = int((timeArray - start_time).days)  # 未完成相差天数
        #     over = 0
        # elif end_time >= start_time:
        #     days = int((end_time - start_time).days) # 完成-相差天数
        #     over = 1
        # else:
        #     print('time is error')

        name = r[2]

        plan = r[10]  # 计划内容
        plan_type = r[5]  # 计划类型
        org_name = r[11]  # 组织名称

        real_score, stand_score = plan_score(days=days, over=over, plan_type=plan_type)

        r_new = []
        r_new.append(name)  # 姓名
        r_new.append(end_time.strftime("%Y-%m"))  # 年月)  # 计划时间
        r_new.append(plan)  # 计划内容
        r_new.append(days)  # 耗时天数
        r_new.append(over)  # 是否完成 1-完成 0-未完成

        r_new.append(plan_type)  # 计划类型
        r_new.append(real_score)  # 实际得分
        r_new.append(stand_score)  # 理论得分
        r_new.append(org_name)  # 组织名称

        results_2.append(r_new)
    results_plan = plan_dic(results_2)  # 将各月数据整合到个人名下


    name_list = results_plan.keys()
    for name in name_list:
        month_list = results_plan[name].keys()
        for month in month_list:
            real_month_score = 0  # 实际月得分
            stand_month_score = 0  # 理论月得分
            for key, value in results_plan[name][month].items():
                    # print(value)
                    real_month_score += value[3]
                    stand_month_score += value[4]
            results_plan[name][month] = [real_month_score, stand_month_score, real_month_score * 80/stand_month_score, value[5], value[6]]
    # print('个人-计划得分：', results_plan)

    return results_plan

def caculate_month_score(dic_attendance, dic_plan):
    """计算个人每月总得分"""
    deal = DealTable()
    name_list = deal.get_data(sql=select_users, return_results=1)  # 用户表，匹配个人信息

    for i in range(len(name_list)):
        worker_id = name_list[i][0]  # 员工id
        name = name_list[i][1]  # 当前查询姓名
        corp_id = name_list[i][5]  # 公司id
        corp_name = name_list[i][6]  # 公司名字
        depart_id = name_list[i][7]  # 部门id
        depart_name = name_list[i][8]  # 部门名字
        org_id = str(name_list[i][9])  # 组织id
        job_title = name_list[i][11]  # 职位
        org_name = name_list[i][10]  # 组织名字

        if org_name != '':
            try:
                org_name = list(dic_plan[name].values())[0][3]
            except Exception as e:
                pass
        else:
            org_name = ''

        start_work_month = datetime.date(2019,4,1)
        month_list = get_month_range(start_work_month)

        for month in month_list:
            try:
                month_attendance_score = dic_attendance[name][month]
            except:
                month_attendance_score = 0

            try:
                month_plan_score = dic_plan[name][month][2]
            except:
                month_plan_score = 0

            score = month_plan_score + month_attendance_score

            single_info = (worker_id, month, score)

            try:
                # print(name, org_name, list(dic_plan[name].values())[0][4])
                if org_name != '' and list(dic_plan[name].values())[0][4] != '' and depart_id == 2:
                    insert_sql_plan = insert_score_plan.format(worker_id=worker_id, name=name, month=month, corp_id=corp_id,
                                                          corp_name=corp_name, depart_id=depart_id, depart_name=depart_name,
                                                          org_id=org_id, org_name=org_name, job_title=job_title,
                                                          month_attendance_score=month_attendance_score,
                                                          month_plan_score=month_plan_score, score=score)
                    check_sql_plan = check_score_data_plan.format(worker_id=worker_id, month=month)  # 查询记录
                    delete_sql_plan = delete_score_data_plan.format(worker_id=worker_id, month=month)
                    deal.check_if_exist(single_info, insert_sql_plan, check_sql_plan, delete_sql_plan)
            except KeyError:
                pass

            insert_sql = insert_score.format(worker_id=worker_id, name=name, month=month, corp_id=corp_id,
                                         corp_name=corp_name, depart_id=depart_id, depart_name=depart_name,
                                         org_id=org_id, org_name=org_name, job_title=job_title,
                                         month_attendance_score=month_attendance_score,
                                         month_plan_score=month_plan_score, score=score)
            check_sql = check_score_data.format(worker_id=worker_id, month=month)  # 查询记录
            delete_sql = delete_score_data.format(worker_id=worker_id, month=month)
            deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)
    #

def get_score():
    dic_attendance = caculate_worker_attendance()  # 计算个人-出勤得分
    dic_plan = caculate_worker_plan()  # 计算个人-计划得分
    caculate_month_score(dic_attendance, dic_plan)


if __name__ == "__main__":
    get_score()
