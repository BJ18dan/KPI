from  mysqlhelper import DealTable
from sql_centence import create_users,create_records,create_leave_sign_records,create_people_records,create_worker_attendance,create_score,create_score_plan
# -----------创建表----------------
def create_table():
    # 创建表格（判断是否存在，若不存在，则创建）
    deal = DealTable()
    if not deal.table_exists(table_name='users'):
        deal.deal_table(sql=create_users)  # 创建用户表
        print('create users success')
    if not deal.table_exists(table_name='records'):
        deal.deal_table(sql=create_records)  # 创建出勤表
        print('create records success')
    if not deal.table_exists(table_name='leave_sign_records'):
        deal.deal_table(sql=create_leave_sign_records)  # 创建出勤表
        print('create leave_sign_records success')
    if not deal.table_exists(table_name='people_records'):
        deal.deal_table(sql=create_people_records)  # 创建员工每日打卡表
        print('create people_records success')
    if not deal.table_exists(table_name='worker_attendance'):
        deal.deal_table(sql=create_worker_attendance)  # 创建员工考勤表
        print('create worker_attendance success')
    if not deal.table_exists(table_name='score'):
        deal.deal_table(sql=create_score)  # 创建员工考勤表
        print('create score success')
    if not deal.table_exists(table_name='score_plan'):
        deal.deal_table(sql=create_score_plan)  # 创建计划得分表
        print('create score_plan success')




if __name__ == "__main__":
    create_table()