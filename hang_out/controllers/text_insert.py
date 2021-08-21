from models import CallDatabase
from templates import flexmsg_activity
from controllers import verify
from linebot.models import TextSendMessage

activity_columns = flexmsg_activity.columns
user_columns = ["name", "phone"]

def text_insert(user_text, user_id, activity_info, user_info, registration_info, init_condition, user_condition):
    msg = TextSendMessage(text = "點開下方選單，開始揪團！")

   # to-do 隱藏功能，未來可刪
    if user_text == "~cancel":
        reset.reset(user_id)
        msg = TextSendMessage(text = "取消成功")

    elif activity_info or registration_info:
        if activity_info and (None in activity_info):
            table, columns, condition = "activity", activity_columns[activity_info.index(None)], init_condition
            progress = 5 if user_info[1] else 7
        elif user_info and (None in user_info):
            table, columns, condition = "users", user_columns[user_info.index(None)], user_condition
            progress = 2 if not activity_info else 7

        try:
            CallDatabase.update(table, columns = [columns], values = [user_text], condition = condition)
            activity_info = basic_info.basic_info(init_condition)[0]
            user_info = basic_info.user_info(user_condition)
            data_activity = activity_info + user_info if activity_info and user_info else None
            data_registration = user_info + registration_info if user_info and registration_info else None
            
            status, data = ["activity", data_activity] if activity_info else ["registration", data_registration]
            msg = verify.next_msg(status, data, progress)

        except psycopg2.DataError:
            msg = TextSendMessage(text = "請重新輸入")  

    return msg
