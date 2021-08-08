from __future__ import unicode_literals
from flask import Flask, request, abort
import configparser  # 使用config.ini時需要
import psycopg2      # 使用heroku的postgreSQL資料庫
import datetime as dt
import requests

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, PostbackEvent, LocationMessage, ImageMessage

from templates import flexmsg_g, flexmsg_r, flexmsg_glist, flexmsg_rlist, flexmsg_climate
from controllers import reset, verify, climate, updatePhoto
from models import CallDatabase

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
handler = WebhookHandler(config.get("line-bot", "channel_secret"))
mapbox_key = config.get("mapbox", "access_token")
climate_key = config.get("climate", "authorization")

activity_columns = flexmsg_g.columns
registration_columns = flexmsg_r.columns
user_columns = ["name", "phone"]#to-do

# 接收 LINE 的資訊
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(f"event_body:{body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def message_event(event):
    line_id = event.source.user_id

    user_id = CallDatabase.get_data("users", ["id"], condition = [f"line_id = '{line_id}'"], all_data = False)
    user_id = user_id[0] if user_id else None
    init_condition = ["condition = 'initial'", f"user_id = {user_id}"]
    init_user = [f"line_id = '{line_id}'"]

    activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False) if user_id else []
    user_info = CallDatabase.get_data("users", user_columns, condition = init_user, all_data = False)
    registration_info = CallDatabase.get_data("registration", ["activity_id"], condition = init_condition, all_data = False)
    
    data_activity = activity_info + user_info if activity_info and user_info else None
    data_registration = user_info + registration_info if user_info and registration_info else None
    print(f"data:{data_activity}")

    msg = TextSendMessage(text = "點開下方選單，開始揪團！")
    user_text = event.message.text
    # to-do 隱藏功能，未來可刪
    if event.message.text == "~cancel":
        reset.reset(user_id)
        msg = TextSendMessage(text = "取消成功")

    elif data_activity and (None in data_activity):
        i_activity = data_activity.index(None) # 寫入資料的那一格
        try:
            # 輸入資料型態正確則更新
            if i_activity <= 11:
                CallDatabase.update("activity", columns = [activity_columns[i_activity]], values = [user_text], condition = init_condition)
                activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False)
            else:
                CallDatabase.update("users", columns = [activity_columns[i_activity]], values = [user_text], condition = init_user)
                user_info = CallDatabase.get_data("users", ["name", "phone"], condition = init_user, all_data = False)
            
            data_activity = activity_info + user_info
            
            progress_activity = 5 if data_activity[13] else 7 #to-do 進度條待改
            msg = verify.next_msg("activity", data_activity, progress_activity)  #to-do 進度條待改
        except psycopg2.DataError:
            msg = TextSendMessage(text = "請重新輸入")      

    elif data_registration and (None in data_registration):       
        i_user = user_info.index(None)
        try:
            # 輸入資料型態正確則更新
            CallDatabase.update("users", columns = [user_columns[i_user]], values = [user_text], condition = init_user)

            user_info = CallDatabase.get_data("users", user_columns, condition = init_user, all_data = False)

            data_registration = user_info + registration_info  # name phone activity_id

            progress_user = 2   #to-do 進度條待改
            msg = verify.next_msg("registration", data_registration, progress_user) #to-do 進度條待改
            ## 報名階段user資料填完後，機器人不會知道現在是在填哪個活動的報名

        except psycopg2.DataError:
            # 輸入資料型態錯誤則回應 "請重新輸入"
            msg = TextSendMessage(text = "請重新輸入")  

    line_bot_api.reply_message(
        event.reply_token,
        msg
    )    

@handler.add(PostbackEvent)
def postback_event(event):
    #to-do 進度條待改
    progress_group = 7
    progress_registration = 2

    line_id = event.source.user_id

    user_id = CallDatabase.get_data("users", ["id"], condition = [f"line_id = '{line_id}'"], all_data = False)
    user_id = user_id[0] if user_id else None
    init_condition = ["condition = 'initial'", f"user_id = {user_id}"]
    init_user = [f"line_id = '{line_id}'"]

    activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False) if user_id else []
    user_info = CallDatabase.get_data("users", user_columns, condition = init_user, all_data = False)
    registration_info = CallDatabase.get_data("registration", ["activity_id"], condition = init_condition, all_data = False)

    today_tw = (dt.datetime.now() + dt.timedelta(hours = 8)).date()

    postback_data = event.postback.data

    if postback_data == "我要開團":
        #把只創建卻沒有寫入資料的列刪除
        reset.reset(user_id)

        msg = flexmsg_g.activity_type()
        print("準備開團") # 顯示在heroku後台，只有登入後端才看得到

    elif "開團活動類型" in postback_data:
        
        activity_type = postback_data.split("_")[1]
        if not user_id:
            CallDatabase.insert("users", columns = ["line_id"], values = [line_id])  
            user_id = CallDatabase.get_data("users", ["id"], condition = init_user, all_data = False)[0]
            user_info = CallDatabase.get_data("users", ["name", "phone"], condition = init_user, all_data = False)
            init_condition = ["condition = 'initial'", f"user_id = {user_id}"]

        #創建一列(condition = initial)
        columns = ["condition", "user_id", "activity_type", "attendee", "photo", "description"]
        values = ["initial", user_id, activity_type, 0, "無", "無"]
        CallDatabase.insert("activity", columns = columns, values = values)

        activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False)
        data_activity = activity_info + user_info
        #回傳問題
        progress_activity = 5 if data_activity[13] else 7 #to-do 進度條待改
        msg = flexmsg_g.question("activity_name", data_activity, progress_activity)  #to-do 進度條待改

    elif "回覆活動時間" in postback_data:
        # 由回傳的datetime，取出 activity_date, activity_time
        activity_date, activity_time = event.postback.params["datetime"].split("T")
        # 預設 due_date 為 activity_date 的前一天
        due_date_default = dt.datetime.strptime(activity_date, "%Y-%m-%d") - dt.timedelta(days=1)

        columns = ["activity_date", "activity_time", "due_date"]
        values = [activity_date, activity_time, due_date_default]
        CallDatabase.update("activity", columns = columns, values = values, condition = init_condition)
        
        activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False)
        data_activity = activity_info + user_info

        progress_activity = 5 if data_activity[13] else 7 #to-do 進度條待改
        msg = verify.next_msg("activity", data_activity, progress_activity)  #to-do 進度條待改

    elif "回覆報名截止時間" in postback_data:
        due_date = event.postback.params["date"]
        print(due_date)

        CallDatabase.update("activity", columns = ["due_date"], values = [due_date], condition = init_condition)

        activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False)
        data_activity = activity_info + user_info

        msg = verify.next_msg("activity", data_activity)  #to-do 進度條待改

    elif "修改開團" in postback_data:
        # 在回傳summary後，點選修改後
        column = postback_data.split("_", 1)[1]

        # 將資料庫中該題的內容清除
        CallDatabase.update("activity", columns = [column], values = ["Null"], condition = init_condition)
        
        # 回傳提問
        activity_date = activity_info[2]
        msg = flexmsg_g.question(column, activity_date, 0)

    elif "確認開團" in postback_data:
        
        # 將活動狀態由initial改為pending
        CallDatabase.update("activity", columns = ["condition"], values = ["pending"], condition = init_condition)
        
        msg = TextSendMessage(text = "開團成功！")

    elif "取消開團" in postback_data:
        # 將活動資訊資料庫中，將該列資料刪除
        CallDatabase.update("activity", columns = ["condition"], values = ["delete"], condition = init_condition)

        msg = TextSendMessage(text = "取消成功！")
#-------------------------------------------------------------------------------------
    elif postback_data == "我要報名":
        #把只創建卻沒有寫入資料的列刪除
        reset.reset(user_id)

        msg = flexmsg_r.activity_type()
        print("準備可報名團資訊")
        
    # 按下rich menu中"我要報名" 選擇其中一種活動類型後
    elif "報名活動類型" in postback_data: #這裡的event.message.text會是上面quick reply回傳的訊息(四種type其中一種)
        activity_type = postback_data.split("_")[1]
      
        # 篩選可以報名的團
        condition = [f"due_date >= '{today_tw}'", f"activity_type = '{activity_type}'", "people > attendee", "condition = 'pending'"]
        data_carousel = CallDatabase.get_data("activity", condition = condition, order = "activity_date")
        
        #傳可報名的團的選單
        msg = flexmsg_r.carousel(data_carousel, activity_type)

    elif "詳細資訊" in postback_data :
        activity_id = postback_data.split("_")[1]
        
        #根據該活動的編號找出活動資訊
        condition = [f"id = {activity_id}"]
        activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = condition, all_data = False)

        owner_user_id = CallDatabase.get_data("activity", ["user_id"], condition = condition, all_data = False)[0]
        condition = [f"id = {user_id}"]
        owner_user_info = CallDatabase.get_data("users", ["name", "phone"], condition = condition, all_data = False)

        activity_info = activity_info + owner_user_info
        
        # 回傳該團活動資訊
        msg = flexmsg_r.more_info(activity_info, activity_id)

    elif "立即報名" in postback_data: 
        reset.reset(user_id)
        #立即報名_{activity_id}
        activity_id = postback_data.split("_")[1]

        if user_id and verify.duplicate_registration(activity_id, user_id):
            print("報名重複")
            msg = flexmsg_r.duplication()
        
        else:
            if not user_id:
                CallDatabase.insert("users", columns = ["line_id"], values = [line_id])
                user_id = CallDatabase.get_data("users", ["id"], condition = init_user, all_data = False)[0]

            #在報名資訊資料庫創建一列，準備寫入使用者回答的資訊該列報名狀態為initial
            columns = ["activity_id", "condition", "user_id"]
            values = [activity_id, "initial", user_id]
            CallDatabase.insert("registration", columns = columns, values = values)
            registration_id = CallDatabase.get_data("registration", ["id"], condition = init_condition, all_data = False)[0]

            user_info = CallDatabase.get_data("users", user_columns, condition = init_user, all_data = False)
            data_registration = user_info + (activity_id, registration_id)
            msg = verify.next_msg("registration", data_registration, progress = 2)   #to-do 進度條待改
            
    elif "修改user" in postback_data:
        # 在回傳summary後，點選修改後
        column = postback_data.split("_", 1)[1]  
        
        # 將資料庫中該題的內容清除
        CallDatabase.update("users", columns = [column], values = ["Null"], condition = init_user)
        
        # 回傳提問
        msg = flexmsg_r.question(column, 0)

    elif "確認報名" in postback_data:
        #找到他報的團的編號activity_no
        activity_id = postback_data.split("_")[1]
        #找到該團現在的活動資訊
        condition = [f"id = {activity_id}"]
        people, activity_condition = CallDatabase.get_data("activity", ["people", "condition"], condition = condition, all_data = False)

        if activity_condition != "pending":
            msg = TextSendMessage(text = "報名失敗！")
            
        else:
            # 報名成功 該活動已報名人數+1
            condition = [f"activity_id = {activity_id}"]
            attendee = len(CallDatabase.get_data("registration", condition = condition))

            #檢查報名人數attendee是否達上限people（上面有先從資料庫取出people了）
            #人數達上限則將活動狀態改為closed
            condition = [f"id = {activity_id}"]
            if attendee >= people:
                CallDatabase.update("activity", columns = ["condition"], values = ["closed"], condition = condition)

            #將更新的報名人數attendee記錄到報名表單group_data裡
            CallDatabase.update("activity", columns = ["attendee"], values = [attendee], condition = condition)
            
            #將報名表單的condition改成closed
            CallDatabase.update("registration", columns = ["condition"], values = ["closed"], condition = init_condition)
            
            # 回應 報名成功
            msg = TextSendMessage(text = "報名成功！")

    elif "取消報名" in postback_data: #按下取消報名按鈕將回傳(record_activity_取消報名)
        registration_id, activity_id = postback_data.split('_')[1:]

        # 從報名資訊資料庫中，刪除該報名紀錄
        condition = [f"id = {registration_id}"]
        CallDatabase.update("registration", columns = ["condition"], values = ["delete"], condition = condition)

        # 更新活動資訊資料庫，該活動已報名人數
        condition = [f"activity_id = {activity_id}", f"condition = 'closed'"]
        count_attendee = len(CallDatabase.get_data("registration", condition = condition))
        condition = [f"id = {activity_id}"]
        CallDatabase.update("activity", columns = ["attendee"], values = [count_attendee], condition = condition)

        # 若該團的活動狀態為closed，則更新為pending
        activity_condition = CallDatabase.get_data("activity", ["condition"], condition = condition, all_data = False)[0]
        if activity_condition == "closed":
            CallDatabase.update("activity", columns = ["condition"], values = ["pending"], condition = condition)

        # 回應 取消成功
        msg = TextSendMessage(text = "取消成功！")
#-------------------------------------------------------------------------------------
    elif postback_data == "我的開團":
        reset.reset(user_id)

        msg = flexmsg_glist.record_type()
        print("查詢開團紀錄")
        
    elif "開團紀錄" in postback_data:  
        record_type = postback_data.split("_")[1] 

        # 依照活動時間篩選為已結束或進行中
        condition = ["condition IN ('closed', 'closed by owner')", f"user_id = '{user_id}'"]
        condition.append(f"activity_date < '{today_tw}'") if record_type == "已結束" else condition.append(f"activity_date >= '{today_tw}'")

        # 取得開團紀錄
        activity_info = CallDatabase.get_data("activity", ["id", "activity_name"], condition = condition, order = "activity_date", all_data = True)
        print(f"activity_info:{activity_info}")

        # 回傳回傳開團列表
        msg = flexmsg_glist.my_group_list(activity_info, record_type)
        
    elif "開團資訊" in postback_data:
        activity_id = postback_data.split("_")[1]
        # 根據該活動的編號，從活動資訊資料庫中找出活動資訊
        condition = [f"id = {activity_id}"]
        activity_info = CallDatabase.get_data("activity", condition = condition, all_data = False)
        
        # 回傳活動資訊
        msg = flexmsg_glist.activity_info(activity_info)
        print("回傳活動資訊")
            
    #主揪查看報名者資訊(報名者暱稱、電話)
    elif "報名者資訊" in postback_data:
        activity_id = postback_data.split("_")[1]

        condition = [f"id = {activity_id}"]
        activity_name = CallDatabase.get_data("activity", ["activity_name"], condition = condition, all_data = False)[0]

        # 取得該團的報名資訊
        condition = [f"activity_id = {activity_id}", f"condition = 'closed'"]
        all_attendee_id = [data[0] for data in CallDatabase.get_data("registration", ["user_id"], condition = condition)]
        attendee_data = [CallDatabase.get_data("users", ["name", "phone"], condition = [f"id = {attendee_id}"], all_data = False) for attendee_id in all_attendee_id]
        
        msg = flexmsg_glist.attendee_info(activity_name, attendee_data)

    #主揪提早關團
    elif "結束報名" in postback_data:
        activity_id = postback_data.split("_")[1]
        
        #更新活動資訊資料庫，將該活動的狀態改為 closed by owner
        condition = [f"id = {activity_id}"]
        CallDatabase.update("activity", columns = ["condition"], values = ["closed by owner"], condition = condition)

        # 回應 成功結束報名
        msg = TextSendMessage(text = "成功結束報名！")
#-------------------------------------------------------------------------------------
    elif postback_data == "我的報名":
        reset.reset(user_id)

        msg = flexmsg_rlist.record_type()
        print("查詢報名紀錄")
        
    elif "報名紀錄" in postback_data:
        record_type = postback_data.split("_")[1]

        # 依照活動時間篩選為已結束或進行中
        condition = ["condition = 'closed'", f"user_id = '{user_id}'"]
      
        # 取得報名紀錄   
        registration_data = CallDatabase.get_data("registration", ["activity_id", "id"], condition = condition,  all_data = True)
        all_activity_id = [data[0] for data in registration_data]
        activity_name_date = [CallDatabase.get_data("activity", ["activity_name", "activity_date"], condition = [f"id = {activity_id}"], all_data = False) for activity_id in all_activity_id]
        registration_data = [data[0] + list(data[1]) for data in zip(registration_data, activity_name_date)]  # activity_id, registration_id, activity_name
        if record_type == "已結束":
            registration_data = [data for data in registration_data if data[3] < today_tw]
        else:
            registration_data = [data for data in registration_data if data[3] >= today_tw]
        registration_data = sorted(registration_data, key = lambda x:x[3])    
        # 回傳回傳報名列表
        print(registration_data)  # activity_id, registration_id, activity_name
        msg = flexmsg_rlist.my_registration_list(registration_data, record_type)

    # 在報名列表 點選活動
    elif "查報名" in postback_data:
        activity_id, registration_id = postback_data.split('_')[1:]

        # 根據回傳的 activity_id，從 activity 裡找到活動資訊
        condition = [f"id = {activity_id}"]
        activity_data = CallDatabase.get_data("activity", condition = condition, all_data = False)
        
        # 取得 owner 資料
        condition = [f"id = {activity_data[15]}"]
        owner_info = CallDatabase.get_data("users", ["name", "phone"], condition = condition, all_data = False)

        # 取得 user 資料
        user_info = CallDatabase.get_data("users", ["name", "phone"], condition = init_user, all_data = False)
        
        # 回傳活動資訊及報名資訊
        msg = flexmsg_rlist.activity_registration_info(activity_data, owner_info, user_info, registration_id)
        
#-------------------------------------------------------------------------------------
    elif "newPage" in postback_data:
        all_activity_type = ["登山踏青", "桌遊麻將", "吃吃喝喝", "唱歌跳舞"]

        record = postback_data.split("_") 
        button_type = record[1]
        i = int(record[2])  # i代表要從資料庫中第幾個資料開始呈現，下一頁的 i=i+8，上一頁的 i=i-8

        # [我要報名] 可報名列表的上下頁
        if button_type in all_activity_type:
            # 篩選可以報名的團

            condition = [f"due_date >= '{today_tw}'", f"activity_type = '{button_type}'", "people > attendee", "condition = 'pending'"]
            data_carousel = CallDatabase.get_data("activity", condition = condition, order = "activity_date")
            
            # 回傳 下一頁或上一頁的列表
            msg = flexmsg_r.carousel(data_carousel, button_type, i)

        # [我的開團]、[我的報名] 列表的下一頁
        else:
            condition = ["condition IN ('closed', 'closed by owner')", f"user_id = '{user_id}'"]
            
            # 我的開團紀錄
            if "開團紀錄" in postback_data:
                condition.append(f"activity_date < '{today_tw}'") if button_type == "已結束" else condition.append(f"activity_date >= '{today_tw}'")
                activity_info = CallDatabase.get_data("activity", ["id", "activity_name"], condition = condition, order = "activity_date", all_data = True)
                msg = flexmsg_glist.my_group_list(activity_info, button_type, i)
            
            # 我的報名紀錄
            elif "報名紀錄" in postback_data:
                # 取得報名紀錄   
                registration_data = CallDatabase.get_data("registration", ["activity_id", "id"], condition = condition,  all_data = True)
                all_activity_id = [data[0] for data in registration_data]
                activity_name_date = [CallDatabase.get_data("activity", ["activity_name", "activity_date"], condition = [f"id = {activity_id}"], all_data = False) for activity_id in all_activity_id]
                registration_data = [data[0] + list(data[1]) for data in zip(registration_data, activity_name_date)]  # activity_id, registration_id, activity_name
                if button_type == "已結束":
                    registration_data = [data for data in registration_data if data[3] < today_tw]
                else:
                    registration_data = [data for data in registration_data if data[3] >= today_tw]
                registration_data = sorted(registration_data, key = lambda x:x[3])    
                # 回傳回傳報名列表
                msg = flexmsg_rlist.my_registration_list(registration_data, button_type, i)

#-------------------------------------------------------------------------------------
    elif "climate" in postback_data:
        activity_id = postback_data.split("_")[1]
        condition = [f"id = {activity_id}"]
        activity_info = CallDatabase.get_data("activity", ["location_longitude", "location_latitude", "activity_date", "activity_time"], condition = condition, all_data = False)

        location_longitude, location_latitude, activity_date, activity_time = activity_info

        county, district = climate.geo_data(mapbox_key, location_longitude, location_latitude)
        climate_info = climate.climate(climate_key, county, district, activity_date, activity_time)

        if climate_info == "no_climate":
            msg = flexmsg_climate.no_climate()
        elif climate_info == "no_data": 
            msg = flexmsg_climate.no_data()
        else:
            msg = flexmsg_climate.climate(activity_date, county, district, climate_info)
            
    line_bot_api.reply_message(
        event.reply_token,
        msg
    )



@handler.add(MessageEvent, message = LocationMessage)
def location(event):
    # to-do 進度條待改
    line_id = event.source.user_id

    user_id = CallDatabase.get_data("users", ["id"], condition = [f"line_id = '{line_id}'"], all_data = False)
    user_id = user_id[0] if user_id else None
    init_condition = ["condition = 'initial'", f"user_id = {user_id}"]
    init_user = [f"line_id = '{line_id}'"]
    
    # 取得地點名稱、經度、緯度, 如果該地點沒有名稱，則用地址取代
    location_info = event.message
    position, latitude, longitude = location_info.title, location_info.latitude, location_info.longitude 
    if position == None:
        position = location_info.address[:50]

    CallDatabase.update("activity", columns = ["location_title", "location_latitude", "location_longitude"], values = [position, latitude, longitude], condition = init_condition)
    
    activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False) if user_id else []
    user_info = CallDatabase.get_data("users", ["name", "phone"], condition = init_user, all_data = False)
    data_activity = activity_info + user_info

    progress_activity = 5 if data_activity[13] else 7 #to-do 進度條待改

    msg = verify.next_msg("activity", data_activity, progress_activity)  #to-do 進度條待改
    line_bot_api.reply_message(
        event.reply_token,
        msg
    )


@handler.add(MessageEvent, message = ImageMessage)
def pic(event):
    line_id = event.source.user_id

    user_id = CallDatabase.get_data("users", ["id"], condition = [f"line_id = '{line_id}'"], all_data = False)
    user_id = user_id[0] if user_id else None
    init_condition = ["condition = 'initial'", f"user_id = {user_id}"]
    init_user = [f"line_id = '{line_id}'"]

    activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False) if user_id else []
    user_info = CallDatabase.get_data("users", user_columns, condition = init_user, all_data = False)
    data_activity = activity_info + user_info if activity_info and user_info else None

    photo_content = line_bot_api.get_message_content(event.message.id)
    activity_name = data_activity[1]
    imgur_config = [config.get('imgur', 'client_id'), config.get('imgur', 'client_secret'), config.get('imgur', 'access_token'), config.get('imgur', 'refresh_token'), config.get('imgur', 'album_id')]

    msg_text = updatePhoto.photo(data_activity, photo_content, user_id, activity_name, imgur_config)
    msg = [TextSendMessage(text = msg_text)]

    if data_activity:
        activity_info = CallDatabase.get_data("activity", activity_columns[:-2], condition = init_condition, all_data = False) 
        data_activity = activity_info + user_info    
        msg.append(verify.next_msg("activity", data_activity))

    line_bot_api.reply_message(
        event.reply_token,
        msg
    )


if __name__ == "__main__":
    app.run()