# -*- coding: utf-8 -*-

from linebot.models import *
import datetime as dt
import json

def quick_reply_button(label, record_type):
    quick_reply_button = QuickReplyButton(
        action = PostbackAction(
            label = label, 
            data = f"報名紀錄_{record_type}",  
            display_text = f"查詢[{label}]"
        )
    )
    return quick_reply_button

def record_type():
    all_label = ["歷史報名紀錄", "我報名的團"]
    all_type = ["已結束", "進行中"]
    
    record_type = TextSendMessage(
        text = "請選擇查詢 [歷史報名紀錄] 或 [我報名的團]",
        quick_reply = QuickReply(
            items = [quick_reply_button(label, record_type) for label, record_type in zip(all_label, all_type)]
        )
    )
    return record_type  
#------------------------------------------------------------------------------------------     
def activity_in_index(row):
    activity_id, registration_id, activity_name, activity_date = row
    activity_in_index = BoxComponent(
        layout = "baseline",
        contents = [
            IconComponent(
                url =  "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                size =  "sm"
            ),
            TextComponent(
                text = f"{activity_name}",  
                align = "start",
                size = "md",
                color = "#227C9D",
                margin = "md",
                action = PostbackAction(
                    display_text = f"查看 {activity_name} 的詳細資訊",
                    data = f"查報名_{activity_id}_{registration_id}"
                )
            )
        ]
    )
    return activity_in_index

def page_button(new_page, record_type, i):
    i = i-8 if new_page == "上一頁" else i+8
    page_button = ButtonComponent(
        action = PostbackAction(
            label = new_page,
            data = f"newPage_{record_type}_{i}_報名紀錄",
            display_text = new_page
        ),
        height = "sm",
        style = "primary",
        color = "#A7D5E1",
        gravity = "bottom"
    )
    return page_button

def my_registration_list(data, record_type, i = 0):
    if i < 0:
        i = 0
    elif i >= len(data):
        i -= 8
    
    if data:
        index_content = [activity_in_index(row) for row in data[i: i+8]]  
        rlist_index = BubbleContainer(
            size = "kilo",
            direction = "ltr",
            header = BoxComponent(
                layout = "horizontal",
                contents = [
                    TextComponent(
                        text = f"我的報名列表 ({record_type})",
                        size = "lg",
                        weight = "bold",
                        color = "#AAAAAA"
                    )
                ]
            ),
            body = BoxComponent(
                layout = "vertical",
                spacing = "md",
                contents = index_content
            ),
            footer = BoxComponent(
                layout = "horizontal",
                spacing = "sm",
                contents = [
                    page_button("上一頁", record_type, i),
                    page_button("下一頁", record_type, i)
                ]
            )
        )
    else:
        rlist_index = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                size = "xs",
                layout = "vertical",
                contents = [
                    TextComponent(
                        text = f"目前沒有報名資料！",
                        size = "lg",
                        weight = "bold",
                        color = "#AAAAAA"
                    )
                ]
            )
        )

    my_registration_list = FlexSendMessage(
        alt_text = "我的報名",
        contents = rlist_index
    )

    return my_registration_list
#------------------------------------------------------------------------------------------    
def climate(activity_no, activity_name):
    climate = BoxComponent(
        layout = "vertical",
        spacing = "sm",
        background_color = "#A7D5E1",
        width = "80px",
        height = "25.5px",                                           
        contents = [
            TextComponent(
                text = "天氣預報",
                size = "sm",
                color = "#FFFFFF",
                align = "center",
                offset_top = "2.5px"
            )
        ],
        action = PostbackAction(
            label = "天氣預報",
            data = f"climate_{activity_no}",
            display_text = f"{activity_name}的天氣預報"
        )
    )
    return climate

def info_text(text, color = "#8c8c8c", size = "xs", weight = "regular"):
    info_text = TextComponent(
        text = text,
        wrap = True,
        color = color,
        size = size,
        weight = weight
    ) 
    return info_text   

def button(label, data, display_text):
    button = ButtonComponent(
        style = "primary",
        height = "sm",
        color = "#A7D5E1",
        gravity = "bottom",
        action = PostbackAction(
            label = label,
            data = data,
            display_text = display_text
        )
    )
    return button   

def activity_info(data, owner_info):
    activity_id, activity_name = data[0], data[2]
    activity_dt, location, cost, photo = f"{data[3]} {str(data[4])[:5]}", data[5], data[9], data[12]
    owner_name, owner_phone = owner_info[0], owner_info[1]

    if "https://i.imgur.com/" not in photo:
        link="https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip11.jpg"
    else:
        link = f"{photo}"
    
    activity_info = BubbleContainer(
        size = "kilo",
        direction = "ltr",
        header = BoxComponent(
            layout = "vertical",
            background_color = "#A7D5E1",
            contents = [
                TextComponent(
                    text = "活動詳細資訊",
                    size = "lg",
                    align = "start",
                    color = "#ffffff"
                )
            ]
        ),
        hero = ImageComponent(
            size = "full",
            aspectMode = "cover",
            aspectRatio = "320:213",
            url = f"{link}"
        ),
        body = BoxComponent(
            layout = "vertical",
            paddingAll = "13px",
            spacing = "md",
            contents = [
                info_text(f"{activity_name}", color = "#000000", size = "md", weight = "bold"),
                climate(activity_id, activity_name),
                BoxComponent(
                    layout = "vertical",
                    margin = "md",
                    spacing = "sm",
                    contents = [
                        info_text(f"地點: {location}"), 
                        info_text(f"時間: {activity_dt}"),
                        info_text(f"費用: {cost}"),
                        info_text(f"主揪: {owner_name}"),
                        info_text(f"主揪電話: {owner_phone}")
                    ]
                )
            ]
        )
    )
    return activity_info

def registration_info(user_info, registration_id, activity_id):
    name, phone = user_info
    
    registration_info = BubbleContainer(
        size = "kilo",
        direction = "ltr",
        header = BoxComponent(
            layout = "vertical",
            background_color = "#A7D5E1",
            contents = [
                TextComponent(
                    text = "報名資訊",
                    size = "lg",
                    align = "start",
                    color = "#ffffff"
                )
            ]
        ),
        body = BoxComponent(
            layout = "vertical",
            paddingAll = "13px",
            spacing = "md",
            contents = [
                BoxComponent(
                    layout = "vertical",
                    margin = "md",
                    spacing = "sm",
                    contents = [
                        info_text(f"姓名: {name}", size = "md"),
                        info_text(f"電話: {phone}", size = "md")
                    ]
                )
            ]
        ),
        footer = BoxComponent(
            layout = "horizontal",
            spacing = "sm",
            contents = [
                button("取消報名", f"取消報名_{registration_id}_{activity_id}", "取消報名")
            ]
        )
    )
    return registration_info

def activity_registration_info(activity_data, owner_info, user_info, registration_id):
    activity_id = activity_data[0]
    info_content = [activity_info(activity_data, owner_info), registration_info(user_info, registration_id, activity_id)]

    activity_registration_info = FlexSendMessage(
        alt_text = "活動資訊與報名資訊",
        contents = CarouselContainer(
            contents = info_content
        )
    )
    return activity_registration_info
    
