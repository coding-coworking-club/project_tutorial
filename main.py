import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import pygame
import threading
import random


# ---------------------------------------------------------------------
# 修改過的mainwin，如果是class照常運作，如果是instance則跳過class(self)
class mainwin(tk.Tk):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        if self._frame is not None:
            self._frame.destroy()
        if type(frame_class) == type: 
            new_frame = frame_class(self)
            self._frame = new_frame
            self._frame.pack()

        else:
            self._frame = frame_class
            self._frame.pack()



# 測試實體化的Theme class能否讓修改過的mainwin正常運作
# 已確認可以運作
class Theme(tk.Frame):
    def __init__(self, theme_name):
        super().__init__(self)
        super().configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)

        tk.Label(self, text=theme_name[0], font=('微軟正黑體', 18, "bold"),height=2, bg="beige", fg="#264653").pack(side="top", fill="x", pady=5)
        for song_name in theme_name[1]:
            tk.Label(self, text= song_name, font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#264653").pack(padx=5, pady=5)
        
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",
        command=print('1')).place(y=320, x=355)                 
        # 隨便寫一個function代替master.switch_frame   

class StartPage(tk.Frame):
    def __init__(self, master):#anchor=tk.CENTER, 
        super().__init__(master, width=600, height=400)
        super().configure(bg='beige')
        theme2 = Theme2(master, ['讚讚主題',['a','b','c']])
        self.pack_propagate(0)
        tk.Label(self, text='百萬大歌星', background='beige', height=2, font=('微軟正黑體', 24, "bold")).place(x=220, y=90)
        tk.Button(self, text="遊戲規則", font=('微軟正黑體', 14, "bold"), relief ="groove", 
        command=lambda: master.switch_frame(theme2)).place(x=338, y=220)
class Theme2(tk.Frame):
    def __init__(self, master, theme_name):
        super().__init__(master)
        super().configure(width=600, height=400, bg='beige')
        self.pack_propagate(0)

        tk.Label(self, text=theme_name[0], font=('微軟正黑體', 18, "bold"),height=2, bg="beige", fg="#264653").pack(side="top", fill="x", pady=5)
        for song_name in theme_name[1]:
            tk.Label(self, text= song_name, font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#264653").pack(padx=5, pady=5)
        
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",command= lambda: master.switch_frame(StartPage)).place(y=320, x=355)
                                                                                                            
# 實體化
# t1 = Theme(['讚讚主題',['a','b','c']])

# class StartPage(tk.Frame):##E0FFFF
#     def __init__(self, master):#anchor=tk.CENTER, 
#         super().__init__(master, width=600, height=400)
#         super().configure(bg='beige')
#         self.pack_propagate(0)
#         tk.Label(self, text='百萬大歌星', background='beige', height=2, font=('微軟正黑體', 24, "bold")).place(x=220, y=90)
#         tk.Button(self, text="遊戲規則", font=('微軟正黑體', 14, "bold"), relief ="groove", 
#         # t1 = theme的實體
#         command=lambda: master.switch_frame(t1)).place(x=338, y=220)
# StartPage點選遊戲規則會跳轉到上面的t1頁面

app = mainwin()
app.title("百萬大歌星")
app.geometry('600x400')
app.configure(background='beige')
# app.iconbitmap('RBmic.ico')
app.resizable(width=0, height=0)
app.mainloop()





# ---------------------------------------------------------------
# 如果theme 有用到master?
# 動不了



# StartPage點選遊戲規則會跳轉到上面的t2頁面

app = mainwin()
app.title("百萬大歌星")
app.geometry('600x400')
app.configure(background='beige')
app.iconbitmap('RBmic.ico')
app.resizable(width=0, height=0)
app.mainloop()




