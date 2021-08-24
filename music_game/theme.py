import tkinter as tk

import time
import json

class MenuPage(tk.Frame):
    def __init__(self, master, themes=None):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='beige', width=600, height=400)
        self.pack_propagate(0)
        tk.Label(self, text="挑戰主題", font=('微軟正黑體', 18, "bold"), bg='beige',height=2).pack(side="top", fill="x")
        self.click = [False] * len(themes)
        self.score = 0
        # 未來要連動

        tk.Label(self, text=("積分："+ str(score)), font=('微軟正黑體', 12, "bold"),
                 bg='beige').pack(anchor=tk.NE, padx=15)
        for i, theme in themes:
        	tk.Label(self, text="%d.%s"(%i + 1, theme['title']), font=('微軟正黑體', 15, "bold"),
	                  bg='beige', fg=theme['color']).pack(padx=5, pady=5)

        tk.Button(self, text="結束挑戰", font=('微軟正黑體', 12, "bold"), relief ="groove",
                  command=exitgame).place(x=510, y=100)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=220, y=320)

        def themechoice():
        	chioce = UserEntry.get()
        	try:
        		choice = int(choice) -1
        	except:
        		tk.messagebox.showinfo("大歌星您好", f"{choice}不是合法輸入！", "請輸入數子1-5~")
        		return 

        	if choice < 0 or choice > 4:
        		tk.messagebox.showinfo("大歌星您好", f"{choice}不是合法輸入！", "請輸入數子1-5~")

        	if self.click[chioce]:
        		tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
        	else:

        		theme = Theme(themes[chioce]['title'], themes[chioce]['song'])
        		master.switch_frame(theme)

        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",
                  command=themechoice).place(y=320, x=355)
        #.pack(anchor=tk.NE, padx=5, pady=5)

class Theme(tk.Frame):       
    def __init__(self, master, title, song_configs): # 要有五首歌
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text=title, font=('微軟正黑體', 18, "bold"),
                 height=2, bg="beige", fg="#198962").pack(side="top", fill="x", pady=5)
        for song_id in song_ids:

            tk.Label(self, text=song[song_id].title, font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        # tk.Label(self, text="2.光良-童話", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        # tk.Label(self, text="3.張雨生-天天想你", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        # tk.Label(self, text="4.陳昇-把悲傷留給自己", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        # tk.Label(self, text="5.香香-老鼠愛大米", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#198962").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        def songchoice():
            entry = int(UserEntry.get())
            master.switch_frame(song_configs[entry - 1])

        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",command=songchoice).place(y=320, x=355)
