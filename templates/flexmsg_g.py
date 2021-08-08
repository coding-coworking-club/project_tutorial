# -*- coding: utf-8 -*-
from linebot.models import *
import datetime as dt
import json

columns = ["activity_type", "activity_name", "activity_date", "activity_time", 
            "location_title", "location_latitude", "location_longitude", "people", "cost", "due_date", 
            "description", "photo", "name", "phone"]
columns_text = ["活動類型", "活動名稱", "活動時間", "活動時間",
            "活動地點", "活動地點", "活動地點", "活動人數", "活動費用", "報名截止日期", 
            "活動敘述", "活動相片", "主揪姓名", "主揪電話"]



#-------------------------------------------------------------------------------------
def quick_reply_button(activity_type):
    quick_reply_button = QuickReplyButton(
        action = PostbackAction(
            label = activity_type, 
            data = f"開團活動類型_{activity_type}",  
            display_text = activity_type
        )
    )
    return quick_reply_button

def activity_type():
    all_type = ["登山踏青", "桌遊麻將", "吃吃喝喝", "唱歌跳舞"]
    activity_type = TextSendMessage(
        text = "請選擇開團活動類型",
        quick_reply = QuickReply(
            items = [quick_reply_button(activity_type) for activity_type in all_type]
        )
    )
    return activity_type
#-------------------------------------------------------------------------------------
def flex_header(text):
    flex_header = BoxComponent(
        layout = "vertical",
        height = "63px",
        contents = [
            TextComponent(
                text = text, 
                weight = "bold", 
                size = "lg", 
                align = "center"
            )
        ]
    )
    return flex_header

def flex_body(text):
    flex_body = BoxComponent(
        layout = "vertical",
        contents = [
            TextComponent(
                text = f"請告訴我{text}" if text != "活動相片" else "請上傳一張相片",
                size = "md", 
                color = "#666666"
            )
        ]
    )
    return flex_body

def prog_rate(col, q_count):   
    progress_i = {"activity_name": 1, "activity_date": 2, "location_title":3, "people": 4, "cost": 5, "name": 6, "phone": 7}
    i = progress_i.get(col, 0)
    
    prog_rate = BoxComponent(
        layout = "vertical",
        margin = "md",
        height = "45px",
        contents = [
            TextComponent(
                text = f"{i} / {q_count} ", 
                weight = "bold", 
                size = "md"
            ),
            BoxComponent(
                layout = "vertical", 
                margin = "md", 
                width = f"{int(i / q_count * 100 + 0.5 )}%",
                background_color = "#3DE1D0",
                height = "6px"
            )
        ]
    )
    return prog_rate 

def button(col, activity_date = None):
    if col == "activity_date":
        action = DatetimePickerAction(
            label = "點我選時間",
            data = "回覆活動時間",
            mode = "datetime"
        )
        
    elif col == "location_title":
        action = URIAction(
            label = "點我選地點",
            uri = "https://line.me/R/nv/location"
        )
        
    elif col == "due_date":
        action = DatetimePickerAction(
            label = "點我選時間",
            data = "回覆報名截止時間",
            mode = "date",
            max = str(activity_date)
        )

    button = ButtonComponent(
        action = action,
        height = "sm",
        margin = "md",
        style = "primary",
        color = "#A7D5E1",
        gravity = "bottom"
    )
    return button

def question(col, activity_date, progress = 0):
    text = columns_text[columns.index(col)]

    footer_contents = []
    if progress:
        footer_contents.append(prog_rate(col, progress))
    if col in ["activity_date", "location_title", "due_date"]:
        footer_contents.append(button(col, activity_date))

    question = FlexSendMessage(
        alt_text = f"請告訴我{text}",
        contents = BubbleContainer(
            direction = "ltr",
            header = flex_header(text),
            body = flex_body(text),
            footer = BoxComponent(
                layout = "vertical",
                margin = "md",
                contents = footer_contents
            )
        )
    )
    return question
#----------------------------------------------------------------------
def content_edit(info, text, col, action = None, color = "#141414"):
    content_edit = BoxComponent(
        layout = "horizontal",
        margin = "lg",
        contents = [
            TextComponent(
                text = f"{text}：{info}",
                size = "md",
                flex = 6,
                action = action,
                color = color,
                wrap = True,
            ),
            SeparatorComponent(),
            TextComponent(
                text = "修改",
                size = "md",
                flex = 1,
                align = "end",
                gravity = "top",
                color = "#229C8F",
                action = PostbackAction(
                    label = f"修改{text}",
                    data = f"修改開團_{col}" if col not in ["name", "phone"] else f"修改user_{col}",
                    display_text = f"修改{text}"
                )
            )
        ]
    )
    return content_edit

def summary_content(data):
    activity_dt = f"{data[2]}  {str(data[3])[:5]}"

    summary_content = []
    for i in [0, 1, 2, 4, 7, 8, 9, 10, 11, 12, 13]:
        info, text, col, action, color = data[i], columns_text[i], columns[i], None, "#141414"
        if i == 3:
            info = activity_dt
        if i == 11 and data[11] != "無":
            info, action, color = "點我查看圖片", URIAction(uri = f"{data[11]}"), "#229C8F"
        summary_content.append(content_edit(info, text, col, action, color))

    return summary_content    

def summary_button(text):
    button = ButtonComponent(
        style = "link",
        height = "sm",
        margin = "none",
        color = "#229C8F",
        gravity = "bottom",
        action = PostbackAction(
            label = text,
            data = text,
            display_text = text
        )
    )
    return button

def summary(data):
    summary = FlexSendMessage(
        alt_text = "請確認開團資訊",
        contents = BubbleContainer(
            direction = "ltr",
            header = BoxComponent(
                layout = "vertical",
                contents = [
                    TextComponent(
                        text = "請確認開團資訊：",
                        weight = "bold",
                        size = "md",
                        align = "start",
                        color = "#000000"
                    )
                ]
            ),
            body = BoxComponent(
                layout = "vertical",
                contents = summary_content(data)
            ),
            footer = BoxComponent(
                layout = "horizontal",
                contents = [
                    summary_button("確認開團"),
                    SeparatorComponent(),
                    summary_button("取消開團")
                ]
            )
        )
    )
    return summary