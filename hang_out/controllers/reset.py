# -*- coding: utf-8 -*-
from models import CallDatabase

def reset(user_id):
    if user_id:
        init_condition = ["condition = 'initial'", f"user_id = '{user_id}'"]

        CallDatabase.delete("activity", condition = init_condition)       # 刪除開團表單中未完成的資料
        CallDatabase.delete("registration", condition = init_condition)   # 刪除報名表單中未完成的資料
    
        print("刪除未成功資料")


# 這邊開始先不用看，這是之前寫的功能，後來發現應該不會用到
# def cancel(line_bot_api, cursor, conn, event):

#     postgres_select_query=f'''SELECT * FROM group_data WHERE user_id = '{event.source.user_id}' AND condition= 'initial';'''
#     cursor.execute(postgres_select_query)
#     data = cursor.fetchone()

#     postgres_select_query=f'''SELECT * FROM registration_data WHERE user_id = '{event.source.user_id}' AND condition= 'initial';'''
#     cursor.execute(postgres_select_query)
#     data_2 = cursor.fetchone()

#     postgres_delete_query = f"""DELETE FROM group_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
#     cursor.execute(postgres_delete_query)
#     conn.commit()
#     postgres_delete_query = f"""DELETE FROM registration_data WHERE (condition, user_id) = ('initial', '{event.source.user_id}');"""
#     cursor.execute(postgres_delete_query)
#     conn.commit()
    
#     if data or data_2:
#         print("取消成功")
#         return TextSendMessage(text = "取消成功")
        
#     else:
#         print("無可取消的開團/報名資料")
#         return TextSendMessage(text = "無可取消的開團/報名資料")

        



