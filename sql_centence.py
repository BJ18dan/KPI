
# ---------------创建表格------------------------
# 员工表
create_users = '''
        create table users( \
        employee_id int not null primary key comment '员工id', \
        name varchar (100)  comment '姓名', \
        pinyin VARCHAR (255)  comment '拼音', \
        date_time DATE comment '时间', \
        userId  VARCHAR (255), \
        corp_id int  comment '公司id', \
        corp_name VARCHAR (255) comment '公司名称', \
        depart_id int  comment '部门id', \
        depart_name VARCHAR (255) comment '部门名称', \
        org_id VARCHAR (255) comment '组织id(可空)', \
        org_name VARCHAR (255) comment '组织名称（可空）', \
        job_title VARCHAR (255) comment '职位名称', \
        primarys int, \
        orgId VARCHAR (255), \
        isAdmin int ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''
# 考勤表
create_records = '''
        create table records(  \
        id int NOT NULL auto_increment primary key, \
        records_id VARCHAR (255) UNIQUE ,  \
        employee_id int not null  comment '员工id', \
        name varchar (100)  comment '姓名', \
        workday DATE comment '日期', \
        userCheckTime DATETIME comment '打卡时间', \
        checkType VARCHAR (255)  comment '打卡类型',  \
        locationResult VARCHAR (255)  comment '打卡范围(Normal:范围内；Outside:范围外)', \
        timeResult  VARCHAR (255)  comment '打卡状态（Normal:正常;Early:早退; Late:迟到;SeriousLate:严重迟到；NotSigned:未打卡）', \
        locationName VARCHAR (255)  comment '坐标名称', \
        location VARCHAR (255)  comment '坐标',  \
        userId VARCHAR (255)  comment '用户组',  \
        scheduleId VARCHAR (255) comment '技术班次id', \
        scheduleName VARCHAR (255) comment '技术班次', \
        add_times FLOAT comment '加班时间'
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

'''
# 创建外勤打卡表
create_signinrecords = '''
        create table signinrecords(  \
        id int NOT NULL auto_increment primary key, \
        employee_id int not null  comment '员工id', \
        name varchar (100)  comment '姓名', \
        sign_type varchar (100)  comment '打卡类型normal 普通签到、outwork 外勤签到、普通签到没有records数组', \
        date DATE comment '签到时间', \
        startTime DATE comment '外勤开启时间', \
        endTime DATE comment '外勤结束时间', \
        address VARCHAR (255)  comment '坐标名称', \
        timeStatus VARCHAR (255) default '全天' comment '当日外勤状态：全天、上午、下午'
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8; '''
# 创建请假表
create_leave_records = '''
        create table leave_records(  \
        id int NOT NULL auto_increment primary key, \
        employee_id int not null  comment '员工id', \
        name varchar (100)  comment '姓名', \
        date DATE comment '请假时间', \
        startTime DATETIME comment '请假开启时间', \
        endTime DATETIME comment '请假结束时间', \
        leaveType VARCHAR (255)  comment '请假类型:年休假（记入正常考勤），其他（记入正常请假）', \
        timeStatus VARCHAR (255) default '全天' comment '当日请假状态：全天、上午、下午'
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
        '''
# 创建员工每日打卡表
create_people_records = '''
        create table people_records( \
        id int not null auto_increment primary key, \
        employee_id int not null comment '员工id',  \
        workday date not null comment '打卡日',  \
        onDuty_time VARCHAR (255) comment '上班打卡时间', \
        onDuty_checktype VARCHAR (255) comment '上班打卡状态', \
        offDuty_time VARCHAR (255) comment '下班打卡时间', \
        offDuty_checktype VARCHAR (255) comment '下班打卡状态', \
        scheduleName VARCHAR (255)  comment '考勤班次', \
        add_times FLOAT comment '加班时间'
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''
# 创建员工每月打卡记录表
create_worker_attendance = '''
        create table worker_attendance(  \
        id int auto_increment primary key not null, \
        employee_id int not null comment '员工id',  \
        name varchar(100) not null comment '员工姓名',  \
        department VARCHAR(255) not null comment '所在部门',  \
        date_time  date comment '日期', \
        over_time_cnt FLOAT comment '加班次数',  \
        late_cnt int comment '迟到次数',  \
        leave_early_cnt int comment '早退次数',  \
        leave_cnt int comment '请假天数（天，非年假）',  \
        abbsent_cnt int comment '旷工次数',  \
        add_record int comment '补录次数(小于等于3次)', \
        corp_id int comment '公司id', \
        corp_name VARCHAR (255) comment '公司名称', \
        depart_id int comment '部门id', \
        org_id VARCHAR (30) comment '组织id', \
        org_name VARCHAR (255) comment '组织名称', \
        job_title VARCHAR (255) comment '职位'
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''
# 创建绩效表
create_score = '''
    create table score(  \
    id int not null auto_increment primary key,  \
    worker_id int not null comment '员工Id',  \
    name VARCHAR (255) comment '姓名', \
    month VARCHAR (100) comment '月份', \
    corp_id int comment '公司id', \
    corp_name VARCHAR (255) comment '公司名称', \
    depart_id int comment '部门id',  \
    depart_name VARCHAR (255) comment '部门名称', \
    org_id VARCHAR (50) comment '组织id', \
    org_name VARCHAR (255) comment '组织名称',  \
    job_title VARCHAR (255) comment '工作岗位',  
    month_attendance_score  FLOAT  comment '考勤分', \
    month_plan_score FLOAT comment '计划分',  \
    score FLOAT  comment '总分' 
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''
# 创建外勤请假统计表
create_leave_sign_records = '''
    create table leave_sign_records( \
    id int not null auto_increment primary key, \
    employee_id int not null comment '员工id', \
    name varchar (100)  comment '姓名', \
    time varchar (100)  comment '月份', \
    leave_other_cnt float comment '请假天数(其他)', \
    leave_year_cnt float comment '请假天数（年休假）', \
    signrecord_cnt float comment '外勤天数' 
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

'''
# 创建计划得分表
create_score_plan = '''
    create table score_plan(  \
    id int not null auto_increment primary key,  \
    worker_id int not null comment '员工Id',  \
    name VARCHAR (255) comment '姓名', \
    month VARCHAR (100) comment '月份', \
    corp_id int comment '公司id', \
    corp_name VARCHAR (255) comment '公司名称', \
    depart_id int comment '部门id',  \
    depart_name VARCHAR (255) comment '部门名称', \
    org_id VARCHAR (50) comment '组织id', \
    org_name VARCHAR (255) comment '组织名称',  \
    job_title VARCHAR (255) comment '工作岗位',  
    month_attendance_score  FLOAT  comment '考勤分', \
    month_plan_score FLOAT comment '计划分',  \
    score FLOAT  comment '总分' 
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''



# ---------------插入数据------------------------
# 插入-员工数据
insert_users_data = "INSERT INTO users(employee_id,name,pinyin,date_time,userId,corp_id,corp_name,depart_id,depart_name,org_id,org_name,job_title,primarys,orgId,isAdmin) VALUES ('{employee_id}','{name}','{pinyin}','{date_time}','{userId}','{corp_id}','{corp_name}','{depart_id}','{depart_name}','{org_id}','{org_name}','{job_title}','{primarys}','{orgId}','{isAdmin}')"
# 插入-考勤数据
insert_records_data = "INSERT INTO records(records_id, workday, employee_id, name, checkType,userCheckTime,add_times,locationResult, timeResult, locationName,location, userId, scheduleId, scheduleName)  VALUES ('{records_id}','{workday}','{employee_id}','{name}','{checkType}','{userCheckTime}','{add_times}','{locationResult}','{timeResult}','{locationName}','{location}','{userId}','{scheduleId}','{scheduleName}')"
# 插入-外勤数据
insert_signinrecords_data = "insert into signinrecords(records_id,employee_id,name,sign_type,type,date,startTime,endTime,startOfDay,endOfDay,address,location,userId,destination,description) values('{records_id}','{employee_id}','{name}','{sign_type}','{type}','{date}','{startTime}','{endTime}','{startOfDay}','{endOfDay}','{address}','{location}','{userId}','{destination}','{description}')"
# 插入-请假外勤数据
insert_leave_sign_records = "insert into leave_sign_records(employee_id, name, time, leave_other_cnt, leave_year_cnt, signrecord_cnt) values('{employee_id}', '{name}', '{time}', '{leave_other_cnt}','{leave_year_cnt}', '{signrecord_cnt}')"
# 插入-员工每日打卡数据
insert_people_records = "insert into people_records(employee_id,workday,onDuty_time,onDuty_checktype,offDuty_time,offDuty_checktype,scheduleName,add_times) values('{employee_id}','{workday}','{onDuty_time}','{onDuty_checktype}','{offDuty_time}','{offDuty_checktype}','{scheduleName}','{add_times}')"
# 插入-考勤数据
insert_worker_attendance_data = '''
        insert into worker_attendance(employee_id,name,department,date_time,over_time_cnt,late_cnt,leave_early_cnt,leave_cnt,abbsent_cnt,add_record,corp_name,corp_id,depart_id,org_id,org_name,job_title) \
        values('{employee_id}','{name}','{department}','{date_time}','{over_time_cnt}','{late_cnt}','{leave_early_cnt}','{leave_cnt}','{abbsent_cnt}','{add_record}','{corp_name}','{corp_id}','{depart_id}','{org_id}','{org_name}','{job_title}')
'''
# 插入-计划得分数据
insert_score_plan = '''insert into score_plan(worker_id, name, month, corp_id,corp_name,depart_id, depart_name,org_id,org_name,job_title, month_attendance_score, month_plan_score, score)  values('{worker_id}', '{name}', '{month}', '{corp_id}','{corp_name}','{depart_id}', '{depart_name}','{org_id}','{org_name}','{job_title}', '{month_attendance_score}', '{month_plan_score}', '{score}')'''
# 插入-得分数据
insert_score = '''insert into score(worker_id, name, month, corp_id,corp_name,depart_id, depart_name,org_id,org_name,job_title, month_attendance_score, month_plan_score, score)  values('{worker_id}', '{name}', '{month}', '{corp_id}','{corp_name}','{depart_id}', '{depart_name}','{org_id}','{org_name}','{job_title}', '{month_attendance_score}', '{month_plan_score}', '{score}')'''



# --------------检查数据--------------------------
# 检查-员工数据
check_users_data = "select employee_id, name, depart_id, org_id, job_title from users where employee_id='{employee_id}'"
# 检查-出勤数据
check_records_data = "select employee_id, checkType, userCheckTime, timeResult, add_times from records where records_id='{records_id}' and workday='{workday}'"
# 检查-外勤数据
check_signrecords_data = "select employee_id, sign_type, type from signrecords where employee_id='{employee_id}' and startTime='{startTime}'"
# 检查-请假外勤数据
check_leave_sign_records = "select employee_id, time, leave_other_cnt,leave_year_cnt, signrecord_cnt from leave_sign_records where employee_id = '{employee_id}' and time = '{time}'"  # 更新数据
check_leave_sign_records_1 = "select employee_id, time, signrecord_cnt from leave_sign_records where employee_id = '{employee_id}' and time = '{time}'"  # 更新数据
# 检查-员工每日打卡数据
check_people_records = "select employee_id, workday, onDuty_time,onDuty_checktype, offDuty_time,offDuty_checktype, scheduleName, add_times from people_records where employee_id='{employee_id}' and workday='{workday}'"
# 检查-考勤数据
check_worker_attendance = "select employee_id, name, department, date_time, over_time_cnt, late_cnt, leave_early_cnt, leave_cnt, \
              abbsent_cnt, add_record, corp_id, depart_id, org_id, job_title from worker_attendance where employee_id = '{employee_id}' and date_time = '{date_time}'"  # 更新数据


select_worker_attendance = "select * from worker_attendance "
select_worker_plan = "select * from worker_plan"
select_users = "select * from users"
check_score_data_plan = "select worker_id, month, score from score_plan where worker_id = '{worker_id}' and month = '{month}'"  # 更新数据
check_score_data = "select worker_id, month, score from score where worker_id = '{worker_id}' and month = '{month}'"  # 更新数据






# --------------删除数据--------------------------
# 删除-员工变动
delete_users_data = "delete from users where employee_id = '{employee_id}'"
# 删除-考勤变动
delete_records_data = "delete from records where records_id = '{records_id}'"
# 删除-外勤变动
delete_signrecords_data = "delete from signrecords where records_id = '{records_id}'"
# 删除-请假外勤数据
delete_leave_sign_records = "delete from leave_sign_records where employee_id = '{employee_id}' and time = '{time}'"  # 更新数据
# 删除-原每日打卡数据
delete_people_records = "delete from people_records where employee_id='{employee_id}' and workday='{workday}'"
# 删除-考勤数据
delete_worker_attendance = "delete from worker_attendance where employee_id = '{employee_id}' and date_time = '{date_time}'"  # 更新数据
# 删除-得分计划数据
delete_score_data_plan = "delete from score_plan where worker_id = '{worker_id}' and month = '{month}'"  # 更新数据
# 删除-得分数据
delete_score_data = "delete from score where worker_id = '{worker_id}' and month = '{month}'"  # 更新数据




# ---------------------更新数据----------------------
# 更新-请假外勤数据
update_signrecord_cnt = "update leave_sign_records set signrecord_cnt = '{signrecord_cnt}' where employee_id = '{employee_id}' and time = '{time}'"

# ------------------统计出现次数------------------------------
count_times = """SELECT employee_id, date_format(workday,'%Y-%m') month,
		SUM(if(onDuty_checktype='Normal',1,0)) sign_in_normal, 
		SUM(if(onDuty_checktype='NotSigned',1,0)) sign_in_miss_cnt ,  \
		SUM(if(onDuty_checktype='Late' or onDuty_checktype='SeriousLate',1,0)) as late_cnt,  \
		SUM(if(onDuty_checktype='Early',1,0)) as leave_early_cnt,  \
 		SUM(if(offDuty_checktype='Normal',1,0)) sign_out_normal,   \
 		SUM(if(offDuty_checktype='NotSigned',1,0)) sign_out_miss_cnt,  \
 		SUM(add_times)/4 as over_time_cnt,  \
 		COUNT(DISTINCT workday) as dyas_cnt \
        FROM people_records  \
        GROUP BY employee_id, date_format(workday,'%Y-%m') """

# 通过关联考勤表、请假表和外勤表获得员工存在记录的天数
get_sign_data = '''
        select employee_id, months, count(distinct date) \
        from(  \
            SELECT employee_id  \
	               ,date_format(date, "%Y-%m") months  \
	               ,date  \
            from  \
	            (SELECT employee_id, date FROM leave_records   \
	             UNION  \
		         SELECT employee_id, date FROM signinrecords  \
		         UNION  \
		         SELECT employee_id, workday AS date FROM people_records  \
		    ) t  \
		) tt \
	    group by employee_id, months 
'''