# -*- coding: utf-8 -*-

from linebot.models import *
import datetime as dt
import json

def quick_reply_button(label, record_type):
    quick_reply_button = QuickReplyButton(
        action = PostbackAction(
            label = label, 
            data = f"開團紀錄_{record_type}",  
            display_text = f"查詢[{label}]"
        )
    )
    return quick_reply_button

def record_type():
    all_label = ["歷史開團紀錄", "即將來臨的活動"]
    all_type = ["已結束", "進行中"]
    
    record_type = TextSendMessage(
        text = "請選擇查詢 [已結束的活動] 或 [即將來臨的活動]",
        quick_reply = QuickReply(
            items = [quick_reply_button(label, record_type) for label, record_type in zip(all_label, all_type)]
        )
    )
    return record_type  
#------------------------------------------------------------------------------------------     
def activity_in_index(activity_id, activity_name):
    activity_in_index = BoxComponent(
        layout = "baseline",
        contents = [
            IconComponent(
                url =  "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                size =  "sm"
            ),
            TextComponent(
                text = f"{activity_name}",  # activity_name
                align = "start",
                size = "md",
                color = "#227C9D",
                margin = "md",
                action = PostbackAction(
                    display_text = f"查看 {activity_name} 的詳細資訊",
                    data = f"開團資訊_{activity_id}"
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
            data = f"newPage_{record_type}_{i}_開團紀錄",
            display_text = new_page
        ),
        height = "sm",
        style = "primary",
        color = "#A7D5E1",
        gravity = "bottom"
    )
    return page_button

def my_group_list(data, record_type, i = 0):
    if i < 0:
        i = 0
    elif i >= len(data):
        i -= 8
    
    if data:
        index_content = [activity_in_index(row[0], row[1]) for row in data[i: i+8]]  
        glist_index = BubbleContainer(
            size = "kilo",
            direction = "ltr",
            header = BoxComponent(
                layout = "horizontal",
                contents = [
                    TextComponent(
                        text = f"我的開團列表 ({record_type})",
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
        glist_index = BubbleContainer(
            direction = "ltr",
            body = BoxComponent(
                size = "xs",
                layout = "vertical",
                contents = [
                    TextComponent(
                        text = f"目前沒有開團資料！",
                        size = "lg",
                        weight = "bold",
                        color = "#AAAAAA"
                    )
                ]
            )
        )

    my_group_list = FlexSendMessage(
        alt_text = "我的開團",
        contents = glist_index
    )

    return my_group_list
#--------------------------------------------------------------------------------------
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

def activity_info(data):
    activity_id, activity_name = data[0], data[2]
    activity_dt, location, cost, photo = f"{data[3]} {str(data[4])[:5]}", data[5], data[9], data[12]
    attendee, people, condition = data[13], data[8], data[14]
    print(activity_id, activity_name)

    if "https://i.imgur.com/" not in photo:
        link = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip11.jpg"
    else:
        link = f"{photo}"
    
    activity_info = FlexSendMessage(
        alt_text = "我的開團資訊",
        contents = BubbleContainer(
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
                    info_text(activity_name, color = "#000000", size = "md", weight = "bold"),
                    climate(activity_id, activity_name),
                    BoxComponent(
                        layout = "vertical",
                        margin = "md",
                        spacing = "sm",
                        contents = [
                            info_text(f"地點: {location}"), 
                            info_text(f"時間: {activity_dt}"),
                            info_text(f"費用: {cost}"),
                            info_text(f"已報名人數: {attendee}/{people}"),
                            info_text(f"狀態: {condition}"),
                        ]
                    )
                ]
            ),
            footer = BoxComponent(
                layout = "horizontal",
                spacing = "sm",
                contents = [
                    button("報名者資訊", f"報名者資訊_{activity_id}", "查看報名者資訊"),
                    button("結束報名", f"結束報名_{activity_id}", "結束報名")
                ]
            )
        )
    )
    
    return activity_info
#--------------------------------------------------------------------------
def attendee_info(activity_name, attendee_data):
    print(attendee_data)
    if attendee_data:
        attendee_info = [f"{activity_name}", "報名者資訊："] + [f"{data[0]} {data[1]}" for data in attendee_data]
        
        attendee_info = TextSendMessage(
            text = "\n".join(attendee_info)
        )

    else:
        attendee_info = TextSendMessage(
            text = "目前無人報名"
        )

    return attendee_info
