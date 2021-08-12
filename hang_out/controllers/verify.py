from models import CallDatabase
from templates import flexmsg_g, flexmsg_r

# 驗證是否回答完畢，判斷要問下一題或summary
def next_msg(status, data, progress = 0):
    print("進入verify.next_msg")
    if None in data: # 還有欄位未填，問下一題
        i = data.index(None)
        if "activity" in status:
            col = flexmsg_g.columns[i]
            activity_date = data[2]
            msg = flexmsg_g.question(col, activity_date, progress)
        else:
            col = flexmsg_r.columns[i] 
            msg = flexmsg_r.question(col, progress)
        print("問下一題")
            
    else: # 所有欄位都填了，回傳summary
        if "activity" in status:
            msg = flexmsg_g.summary(data)  
        else:
            activity_id = data[2]
            activity_name = CallDatabase.get_data("activity", ["activity_name"], condition = [f"id = {activity_id}"], all_data = False)[0]
            msg = flexmsg_r.summary(data, activity_name)

    return msg

# 驗證使用者報名是否重複
def duplicate_registration(activity_id, user_id):
    condition = [f"activity_id = {activity_id}", "condition = 'closed'"]
    attendee_user_id = CallDatabase.get_data("registration", ["user_id"], condition = condition)
    attendee_user_id = [data[0] for data in attendee_user_id]

    return user_id in attendee_user_id #如果使用者輸入的電話重複則報名失敗

# 驗證使用者有無歷史資料
def user_info(table, user_id):
    condition = ["condition != 'initial'", f"line_id = '{line_id}'"]

    if table == "group_data":
        data = CallDatabase.get_data(table, condition = condition, order = "activity_no", ASC = False, all_data = False)
        name_phone = (data[13], data[14]) if data else False

    elif table == "registration_data":
        data = CallDatabase.get_data(table, condition = condition, order = "registration_no", ASC = False, all_data = False)
        name_phone = (data[3], data[4]) if data else False

    return name_phone    
