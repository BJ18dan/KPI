from sql_centence import *
from views import *



# ---------------用户表---------------
def mongo_to_mysql_users():
    deal = DealTable()
    datas = get_mongodb_conn(choose='users',filter='', flag='')

    for data in datas:
        time_stamp = timestamp_from_objectid(data.get("_id"))  # 调用上面的方法生成一个objid,返回数据创建的时间戳
        date_time1 = timestamp_to_date(time_stamp, time_style=1)
        date_time = datetime.datetime.strptime(date_time1, "%Y-%m-%d")
        org_name = ''
        org_id = ''
        name = data.get("name")
        pinyin = data.get("pinyin")
        orgId = data.get("orgId")
        userId = data.get("userId")
        isAdmin = 1 if data.get("isAdmin") else 0

        position = data.get('position')[0]  # 转为字典
        for key, values in position.items():
            if key == "display_nodes":
                for i in range(len(values)):
                    val = values[i]
                    length = val['path'].count("/")
                    if length == 2:
                        corp_name = val['name']
                        corp_id = val['id']
                    elif length == 3:
                        depart_name = val['name']
                        depart_id = val['id']
                    elif length == 4:
                        org_name = val['name']
                        org_id = val['id']
            elif key == 'primary':
                primarys = 1 if position['primary'] else 0
            elif key == 'job_title':
                job_title = position['job_title']
            elif key == 'employee_id':
                employee_id = position['employee_id']

        single_info = (employee_id, name, corp_id, depart_id, org_id, job_title)
        insert_sql = insert_users_data.format(employee_id=employee_id, name=name, pinyin=pinyin, date_time=date_time, userId=userId,corp_id=corp_id,
                               corp_name=corp_name,depart_id=depart_id,depart_name=depart_name,org_id=org_id,org_name=org_name,
                               job_title=job_title,primarys=primarys,orgId=orgId,isAdmin=isAdmin)
        check_sql = check_users_data.format(employee_id=employee_id)
        delete_sql = delete_users_data.format(employee_id=employee_id)  # 删除sql,更新数据若发生变化，则删除重新插入
    #
        deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)

# ---------------考勤表----------------
def mongo_to_mysql_records():
    deal = DealTable()
    datas = add_loss_data()  # 获得出勤表

    for data in datas:
        name = data.get("userName")  # 姓名
        records_id = str(data.get("_id"))
        workday_temp = int(str(data.get("workday"))[0:10])  # 打卡所属日期标识
        workday = timestamp_to_date(workday_temp, time_style=0)
        userCheckTime_temp = int(str(data.get("userCheckTime"))[0:10])  # 实际打卡时间
        userCheckTime = timestamp_to_date(userCheckTime_temp, time_style=0)
        checkType = data.get("checkType")  # 打卡结果状态 onDuty、offDuty
        locationResult = data.get("locationResult")  # 打卡范围
        timeResult = data.get("timeResult")  # 打卡状态
        locationName = data.get("locationName")  # 坐标名称
        location = str(data.get("location")['longitude']) + '|' + str(data.get("location")['latitude'])  # 坐标经纬度
        userId = data.get("userId")  # 用户组id
        scheduleId = data.get("scheduleId")  # 技术班次id
        scheduleName = data.get("scheduleName")  # 技术班次名称
        employee_id = data.get('positions')[0]['employee_id']  # 转为字典
        add_times = caculate_add_time(checkType, workday_temp, userCheckTime_temp, scheduleName)  # 加班时间

        # ------------------数据的插入------------------------------
        single_info = (employee_id, checkType, userCheckTime, timeResult, add_times)
        insert_sql = insert_records_data.format(records_id=records_id,workday=workday,employee_id=employee_id, name=name,checkType=checkType, userCheckTime=userCheckTime,add_times=add_times, locationResult=locationResult, timeResult=timeResult, locationName=locationName,location=location, userId=userId, scheduleId=scheduleId, scheduleName=scheduleName)
        check_sql = check_records_data.format(records_id=records_id, workday=workday)
        delete_sql = delete_records_data.format(records_id=records_id)   # 删除sql,更新数据若发生变化，则删除重新插入

        deal.check_if_exist(single_info, insert_sql, check_sql, delete_sql)


# --------------外勤表---------------------
# def mongo_to_mysql_singrecords():
    # select_sql = {'age': {'$gte': 23, '$lte': 26}}
    # datas = get_mongodb_conn(choose='signrecords')
    # for data in datas:
    #     name = data.get("name")  # 姓名
    #     records_id = str(data.get("_id"))
    #     startTime_temp = int(str(data.get("startTime"))[0:10]) # 外勤开始时间
    #     startTime = timestamp_to_date(startTime_temp, time_style=1)
    #
    #     endTime_temp = int(str(data.get("endTime"))[0:10]) # 外勤结束时间
    #     endTime = timestamp_to_date(endTime_temp, time_style=1)
    #
    #     sign_type = data.get("type")  # normal 普通签到， outwork 外勤签到，普通签到没有records数组
    #     startOfDay_temp = int(str(data.get("startOfDay"))[0:10])  # 签到开启日期
    #     startOfDay = timestamp_to_date(startOfDay_temp, time_style=1)
    #
    #     endOfDay_temp = int(str(data.get("endOfDay"))[0:10])   # 签到结束日期
    #     endOfDay = timestamp_to_date(endOfDay_temp, time_style=1)
    #
    #     employee_id = data.get('positions')[0]['employee_id'] # 转为字典
    #     userId = data.get("userId")  # 用户id
    #
    #     records = data.get("records")
    #     date_temp = int(str(records[0]["date"])[0:10])
    #     date = timestamp_to_date(date_temp, time_style=1)  # 签到时间
    #
    #     description = records[0]["description"]  # 外出描述
    #     type = records[0]["type"]  # (start , normal, end) 第一次外勤 正常外勤  最后一次外勤
    #     location = str(records[0]["location"]["longitude"]) + '|' + str(records[0]["location"]["longitude"])
    #     address = records[0]["location"]["address"]  # 打卡地址
    #     destination = records[0]["location"]["name"]  # 目的地
    #
    #     # print(sign_type, type, '签到时间:', date, '外勤开启时间',startTime,'外勤结束时间',endTime, '签到开启',startOfDay,'签到结束', endOfDay )
    #     # print(date,records_id, employee_id, name, sign_type,type, startTime, endTime, startOfDay, endOfDay, userId, location, address, destination, description)
    #     single_info = (employee_id, sign_type, type)
    #     insert_sql = insert_signinrecords_data.format(records_id=records_id,employee_id=employee_id,name=name,sign_type=sign_type,type=type,date=date,startTime=startTime,endTime=endTime,startOfDay=startOfDay,endOfDay=endOfDay,address=address,location=location,userId=userId,destination=destination,description=description)
    #     check_sql = check_signrecords_data.format(records_id, startTime)
    #     delete_sql = delete_signrecords_data
    #     check_if_exist(single_info, insert_sql, check_sql, delete_sql)


if __name__ == "__main__":
    mongo_to_mysql_users()
    mongo_to_mysql_records()