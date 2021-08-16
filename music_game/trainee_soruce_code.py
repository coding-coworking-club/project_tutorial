#視窗程式
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import pygame
import threading
import random
#from PIL import Image,ImageTk

click1, click2, click3, click4, click5 = 0, 0, 0, 0, 0 ##global變數－各主題點擊次數，避免重複挑戰
score = 0


class mainwin(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
            
class StartPage(tk.Frame):##E0FFFF
    def __init__(self, master):#anchor=tk.CENTER, 
        tk.Frame.__init__(self, master, width=600, height=400)
        tk.Frame.configure(self,bg='beige')
        self.pack_propagate(0)
        #photo = tk.PhotoImage(file="BR.gif")
        #label = tk.Label(image="BR.gif")
        #label.image = photo # keep a reference! label.pack()
        #tk.Label(self, image = "BR.gif").pack()
        tk.Label(self, text='百萬大歌星', background='beige', height=2, font=('微軟正黑體', 24, "bold")).place(x=220, y=90)
        tk.Label(self, text='你認識的歌曲夠多夠廣夠深入嗎?', background='beige',
                 font=('微軟正黑體', 18, "bold")).place(x=126, y=160)
        tk.Button(self, text="開始挑戰", font=('微軟正黑體', 14, "bold"), relief ="groove", 
                  command=lambda: master.switch_frame(MenuPage)).place(x=175, y=220)
        #pack(anchor=tk.CENTER ,padx=10, pady=10)
        tk.Button(self, text="遊戲規則", font=('微軟正黑體', 14, "bold"), relief ="groove",
                  command=lambda: master.switch_frame(RulePage)).place(x=338, y=220)
        #style = ttk.Style()
        #style.configure('W.TButton', font =('calibri', 10, 'bold', 'underline'), foreground = 'red') anchor=tk.CENTER
        #ttk.Button(self, text="遊戲規則", style ="W.TButton",
                  #command=lambda: master.switch_frame(RulePage)).pack(anchor=tk.CENTER, fill='both', pady=5)
        
        
class RulePage(tk.Frame):
    def __init__(self, master): #, bg='#F08080'
        tk.Frame.__init__(self, master, width=600, height=400)
        tk.Frame.configure(self,bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="遊戲規則介紹", font=('微軟正黑體', 18, "bold"),
                 height=2, bg='beige').pack(side="top", fill="both")
        tk.Label(self, text="""
        1.共有五個挑戰主題，請依照個人喜好依序選取
        2.每個主題中有五首歌，請依照個人喜好選擇歌曲作答
        3.當歌曲進行到中間時，歌曲內其中一句歌詞會消失，
           挑戰者就要把這句歌詞完整回答出來
        4.挑戰成功可得積分2000分，挑戰成功的主題不可再挑戰
        5.每當挑戰失敗則積分歸零，需重新開始挑戰
        6.完成所有主題，積分累積至10000分，則視為挑戰成功
        """,
                 bg='beige',
                 font=('微軟正黑體', 14), justify = tk.LEFT).pack(padx=5, pady=5)
        tk.Button(self, text="回到主畫面", font=('微軟正黑體', 12, "bold"), relief ="groove",
                  command=lambda: master.switch_frame(StartPage)).pack(anchor=tk.S, padx=5, pady=5)
        
#未完成挑戰，中途離開遊戲
def exitgame():
    exitbox = tk.messagebox.askquestion('訊息','尚未完成挑戰，確定要離開嗎?')
    if exitbox == 'yes':
        app.destroy()
class MenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='beige', width=600, height=400)
        self.pack_propagate(0)
        tk.Label(self, text="挑戰主題", font=('微軟正黑體', 18, "bold"), bg='beige',height=2).pack(side="top", fill="x")
        global score
        tk.Label(self, text=("積分："+ str(score)), font=('微軟正黑體', 12, "bold"),
                 bg='beige').pack(anchor=tk.NE, padx=15)
        tk.Label(self, text="1.歌名比高速公路還長", font=('微軟正黑體', 15, "bold"),
                 bg='beige', fg='#264653').pack(padx=5, pady=5)
        tk.Label(self, text="2.九零年代金曲", font=('微軟正黑體', 15, "bold"),
                 bg='beige', fg="#198962").pack(padx=5, pady=5)
        tk.Label(self, text="3.獨立音樂", font=('微軟正黑體', 15, "bold"),
                 bg='beige', fg='#DFAC2A').pack(padx=5, pady=5)
        tk.Label(self, text="4.電影/電視主題曲", font=('微軟正黑體', 15, "bold"),
                 bg='beige', fg='#F4A261').pack(padx=5, pady=5)
        tk.Label(self, text="5.我要飆高音", font=('微軟正黑體', 15, "bold"),
                 bg='beige', fg='#E76F51').pack(padx=5, pady=5)
        tk.Button(self, text="結束挑戰", font=('微軟正黑體', 12, "bold"), relief ="groove",
                  command=exitgame).place(x=510, y=100)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=220, y=320)
        def themechoice():
            if UserEntry.get() == "1":
                global click1
                click1 += 1
                if click1 <= 1:
                    master.switch_frame(First_theme)
                else:
                    tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
            elif UserEntry.get() == "2":
                global click2
                click2 += 1
                if click2 <= 1:
                    master.switch_frame(Second_theme)
                else:
                    tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
            elif UserEntry.get() == "3":
                global click3
                click3 += 1
                if click3 <= 1:
                    master.switch_frame(Third_theme)
                else:
                    tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
            elif UserEntry.get() == "4":
                global click4
                click4 += 1
                if click4 <= 1:
                    master.switch_frame(Fourth_theme)
                else:
                    tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
            elif UserEntry.get() == "5":
                global click5
                click5 += 1
                if click5 <= 1:
                    master.switch_frame(Fifth_theme)
                else:
                    tk.messagebox.showinfo("大歌星您好", "這個主題已經挑戰成功囉")
            else:
                pass
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",
                  command=themechoice).place(y=320, x=355)
        #.pack(anchor=tk.NE, padx=5, pady=5)

#主題頁面       
class First_theme(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="歌名比高速公路還長", font=('微軟正黑體', 18, "bold"),
                 height=2, bg="beige", fg="#264653").pack(side="top", fill="x", pady=5)
        tk.Label(self, text="1.理想混蛋-不是因為天氣晴朗才愛你", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="2.五月天-有些事現在不做一輩子都不會做了", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="3.吳宗憲-是不是這樣的夜晚你才會這樣的想起我", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="4.陳綺貞-我喜歡上你時的內心活動", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="5.林宥嘉-我總是一個人在練習一個人", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#264653").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        #UserEntry.pack(side=tk.LEFT)
        def songchoice():
            if UserEntry.get() == "1":
                master.switch_frame(Song11)
            elif UserEntry.get() == "2":
                master.switch_frame(Song12)
            elif UserEntry.get() == "3":
                master.switch_frame(Song13)
            elif UserEntry.get() == "4":
                master.switch_frame(Song14)
            elif UserEntry.get() == "5":
                master.switch_frame(Song15)
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",command=songchoice).place(y=320, x=355)
        #(備存)tk.Button(self, text="重新選擇", command=lambda: master.switch_frame(MenuPage)).pack(padx=5,pady=5)

class Second_theme(tk.Frame):       
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="九零年代金曲", font=('微軟正黑體', 18, "bold"),
                 height=2, bg="beige", fg="#198962").pack(side="top", fill="x", pady=5)
        tk.Label(self, text="1.張惠妹-聽海", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="2.光良-童話", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="3.張雨生-天天想你", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="4.陳昇-把悲傷留給自己", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="5.香香-老鼠愛大米", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#198962").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        def songchoice():
            if UserEntry.get() == "1":
                master.switch_frame(Song21)
            elif UserEntry.get() == "2":
                master.switch_frame(Song22)
            elif UserEntry.get() == "3":
                master.switch_frame(Song23)
            elif UserEntry.get() == "4":
                master.switch_frame(Song24)
            elif UserEntry.get() == "5":
                master.switch_frame(Song25)
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), relief ="groove",command=songchoice).place(y=320, x=355)
    
class Third_theme(tk.Frame):       
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="獨立音樂", font=('微軟正黑體', 18, "bold"),
                height=2, bg="beige", fg='#DFAC2A').pack(side="top", fill="x", pady=5)
        tk.Label(self, text="1.好樂團-他們說我是沒有用的年輕人", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="2.甜約翰-留給你的我從未", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="3.告五人-披星戴月的想你", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="4.南西肯恩-煙花", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="5.棉花糖-100個太陽月亮", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#DFAC2A").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        def songchoice():
            if UserEntry.get() == "1":
                master.switch_frame(Song31)
            elif UserEntry.get() == "2":
                master.switch_frame(Song32)
            elif UserEntry.get() == "3":
                master.switch_frame(Song33)
            elif UserEntry.get() == "4":
                master.switch_frame(Song34)
            elif UserEntry.get() == "5":
                master.switch_frame(Song35)
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), command=songchoice, relief ="groove").place(y=320, x=355)
        
class Fourth_theme(tk.Frame):       
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="電影/電視主題曲", font=('微軟正黑體', 18, "bold"),
                 height=2, bg="beige", fg='#F4A261').pack(side="top", fill="x", pady=5)
        tk.Label(self, text="1.八三夭-想見你想見你想見你", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="2.王藍茵-惡作劇", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="3.楊丞琳-曖昧", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="4.韋禮安-還是會", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="5.周興哲-以後別做朋友", font=('微軟正黑體', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#F4A261").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        def songchoice():
            if UserEntry.get() == "1":
                master.switch_frame(Song41)
            elif UserEntry.get() == "2":
                master.switch_frame(Song42)
            elif UserEntry.get() == "3":
                master.switch_frame(Song43)
            elif UserEntry.get() == "4":
                master.switch_frame(Song44)
            elif UserEntry.get() == "5":
                master.switch_frame(Song45)
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), command=songchoice, relief ="groove").place(y=320, x=355)
        
class Fifth_theme(tk.Frame):       
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text="我要飆高音", font=('Helvetica', 18, "bold"),
                height=2, bg="beige", fg='#E76F51').pack(side="top", fill="x", pady=5)
        tk.Label(self, text="1.鄧紫棋-泡沫", font=('Helvetica', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="2.丁噹-我是一隻小小鳥", font=('Helvetica', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="3.飛兒樂團-我們的愛", font=('Helvetica', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="4.蕭敬騰-王妃", font=('Helvetica', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="5.陳芳語-愛你", font=('Helvetica', 15), bg="beige").pack(padx=5, pady=5)
        tk.Label(self, text="請輸入歌曲代碼：", font=('微軟正黑體', 12, 'bold'), bg="beige", fg="#E76F51").pack(padx=5, pady=5)
        UserEntry = tk.Entry(self, bd =2)
        UserEntry.place(height = 37, x=210, y=320)
        def songchoice():
            if UserEntry.get() == "1":
                master.switch_frame(Song51)
            elif UserEntry.get() == "2":
                master.switch_frame(Song52)
            elif UserEntry.get() == "3":
                master.switch_frame(Song53)
            elif UserEntry.get() == "4":
                master.switch_frame(Song54)
            elif UserEntry.get() == "5":
                master.switch_frame(Song55)
        tk.Button(self, text="確定", font=('微軟正黑體', 12, "bold"), command=songchoice, relief ="groove").place(y=320, x=355)

#答對、錯頁面
gbingo_time = 0

class Bingo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text=("~挑戰成功~"), font=('微軟正黑體', 20, "bold"),
                 bg='beige', fg='red', height=4).place(x=225, y=80)
        
        #score += 1500
        global gbingo_time
        self.scoreVar = tk.StringVar()
        self.scoreArr = ['積分:2000','積分:4000','積分:6000','積分:8000','積分:10000']
        global score
        score += 2000
        while gbingo_time < 5:
            self.scoreVar.set(self.scoreArr[gbingo_time])
            break
        #當分數到最大值時，跳到結束頁面
        def score_max():
            global gbingo_time
            if gbingo_time == 5:
                master.switch_frame(EndPage) 
                ###break
            else:
                master.switch_frame(MenuPage)
        gbingo_time += 1
        tk.Label(self, textvariable=self.scoreVar, font=('微軟正黑體', 14), bg='beige').place(x=255, y=180)
        #回主題選單
        tk.Button(self, text="確定", font=('微軟正黑體', 14), relief='groove',
                  command=score_max).place(x=270, y=240)  

class Wrong(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text=("...挑戰失敗..."), font=('微軟正黑體', 20, "bold"),
                 bg='beige', fg='red', height=4).place(x=225, y=80)
        ###score 重設為0
        global score
        score = 0
        def score_reset():
            master.switch_frame(MenuPage)
            global gbingo_time
            gbingo_time = 0
            global click1, click2, click3, click4, click5     ##歸零點擊次數
            click1, click2, click3, click4, click5 = 0, 0, 0, 0, 0 
        tk.Label(self, text=("積分歸零"), font=('微軟正黑體', 14), bg='beige').place(x=263, y=180)
        tk.Button(self, text="重新挑戰", font=('微軟正黑體', 14), relief='groove', command=score_reset).place(x=260, y=240)   #回主題

#結束畫面
class EndPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='beige')
        self.pack_propagate(0)
        tk.Label(self, text=("恭喜挑戰成功\n~百萬大歌星是你~"), font=('微軟正黑體', 20, 'bold'),
                 bg='beige', fg='red').place(x=185, y=90)
        tk.Label(self, text=("積分："+"10000"), font=('微軟正黑體', 14, "bold"), bg='beige').place(x=240, y=180)
        tk.Button(self, text="結束遊戲", font=('微軟正黑體', 14, "bold"),
                  command=lambda:app.destroy()).place(x=310 ,y=240)   #關閉視窗
        tk.Button(self, text="再次挑戰", font=('微軟正黑體', 14, "bold"),
                  command=lambda: master.switch_frame(MenuPage)).place(x=200 ,y=240)  #回主題選單
        global click1, click2, click3, click4, click5     ##歸零點擊次數
        click1, click2, click3, click4, click5 = 0, 0, 0, 0, 0
        global score
        score = 0

class Songplay():
    def __init__(self, n, Ans, showing, filepath, musicLrc):
        self.n = n
        self.Ans = Ans
        self.showing = showing
        self.filepath = filepath
        self.musicLrc = musicLrc
        
    def playmusic(self):
        pygame.mixer.init()
        track = pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1) #音量
        time.sleep(self.n) #音樂播放的時間
        pygame.mixer.music.stop()
        
    def output_lyrics(self):
        time_list = []  
        sleep_time = [] 
        music = {} 
        time_miao = []  
        fist_splines = []
        fist_splines = self.musicLrc.splitlines()
        
        for x in fist_splines:                  
            time_num = x.count("[")              #統計一行中有多少個時間資料
            x = x.replace("[", "")               #去掉資料裡的" [ "
            fist_splines = x.split("]")          #分隔資料
    
            for y in range(time_num):            
                music[fist_splines[y]] = fist_splines[-1] #將一行中的所有時間當成key存到字典中
                fen = float(fist_splines[y][:2])         #分鐘 
                miao = float(fist_splines[y][3:])         #秒
                time_miao.append(fen * 60 + miao)         #把分鐘換算成秒存入列表

        time_miao = sorted(time_miao)

        for x in range(len(time_miao)):  #x是停頓的時間
            if x == 0:                                               #當他是第一個的時候 我們第一次停的時間是他本身
                sleep_time.append(time_miao[x])
            else:
                sleep_time.append(time_miao[x] - time_miao[x-1])    #其他都是後一個減去前一個  
    
        #對字典按照key值進行排序，得到的是list，裡面是元組 #字典輸出時是有序的，但是它的儲存是無序的
        music = sorted(music.items(), key=lambda e:e[0])
    
        for x,y in enumerate(music): #停止時間進行輸出。
            time.sleep(sleep_time[x])
            if y[1][:len(self.Ans)] == self.Ans:
                self.showing.set('請輸入接續歌詞：'+'*'*len(self.Ans))
                break
            else:
                self.showing.set(y[1])
                global app
                app.update()
    
    def output_lyrics_music(self):
        ## 新建執行緒(threading)
        work1 = threading.Thread(target = self.playmusic, name = 'playmusic')
        work2 = threading.Thread(target = self.output_lyrics, name = 'output_lyrics')
        work1.start()
        work2.start()
            
###主題A歌名比高速公路還長
#1-1理想混蛋-不是因為天氣晴朗才愛你
class Song11(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#264653')
        self.pack_propagate(0)
        tk.Label(self, text="理想混蛋-不是因為天氣晴朗才愛你", font=('微軟正黑體', 14, "bold"), height=2,
                bg = '#264653', fg='white').pack(padx=5, pady=5)
        def Question(n, Ans):
            Ans_lst = [[46.04,'不是因為剛好沒有別的事'],[51.64,'才一直一直一直在腦海裡複習'],[62.15,'擁抱你什麼角度最合適'],
                       [68.52,'其實我常會想像我們老了的樣子'],[76.06,'左邊牽著手右手拉小狗'],[80.42,'可能還有很多小孩子'],
                       [84.02,'其實我不是因為好天氣才這麼說'],[91.02,'牽著你走過大雨盛開水花的路口'],[98.04,'也是我一樣喜歡的夢'],
                       [116.56,'不是因為天氣晴朗才愛你']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\A-1. 理想混蛋-不是因為天氣晴朗才愛你.mp3",
                        """[00:00.00]歌名：不是因為天氣晴朗才愛你
[00:31.68]不是因為天氣晴朗才愛你
[00:37.11]不是因為看見星星才想你
[00:45.74]不是因為剛好沒有別的事
[00:51.34]才一直一直一直在腦海裡複習
[01:01.85]擁抱你什麼角度最合適
[01:08.22]其實我常會想像我們老了的樣子
[01:15.76]左邊牽著手右手拉小狗
[01:19.82]可能還有很多小孩子
[01:22.92]其實我不是因為好天氣才這麼說
[01:30.72]牽著你走過大雨盛開水花的路口
[01:37.04]也是我一樣喜歡的夢
[01:56.26]不是因為天氣晴朗才愛你
""")
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#264653',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)

#1-2 五月天-有些事現在不做一輩子都不會做了
class Song12(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#264653')
        self.pack_propagate(0)
        tk.Label(self, text="五月天-有些事現在不做一輩子都不會做了", font=('微軟正黑體', 14, "bold")
                , height=2, bg = '#264653', fg='white').pack(padx=5, pady=5)
        def Question(n, Ans):
            Ans_lst = [[19.77,'也停不了一秒鐘'],[23.84,'跌倒以後有痛後悔以後有痛'],
                       [31.29,'問你最痛會是哪一種'],[35.12,'答案說明所有'],[40.59,'想像你的孫子孫女充滿光的瞳孔'],
                       [48.02,'正等著你開口等著你說'],[52.34,'你最光輝的一次傳說'],[57.68,'每個平凡的自我都曾幻想過'],
                       [65.30,'以你為名的小說會是枯燥或是雋永'],[79.78,'從前只想裝懂裝作什麼都懂'],[86.91,'懂得生存的規則之後'],
                       [91.13,'卻只想要都不懂'],[94.72,'如果人類的臉長得全都相同'],[102.36,'那麼你和人們的不同'],
                       [106.45,'就看你怎麼活'],[111.48,'想像你的白髮皺紋緊貼你的輪廓'],[118.98,'你最終的朋友就是此刻']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\A-2. 五月天-有些事現在不做一輩子都不會做了.mp3",
                        """[00:00.00]歌名：有些事現在不做一輩子都不會做了
[00:08.72]年輪裡面有鐘皺紋裡面有鐘
[00:15.94]就算暫停全世界的鐘
[00:19.77]也停不了一秒鐘
[00:23.84]跌倒以後有痛後悔以後有痛
[00:31.29]問你最痛會是哪一種
[00:35.12]答案說明所有
[00:40.59]想像你的孫子孫女充滿光的瞳孔
[00:48.02]正等著你開口等著你說
[00:52.34]你最光輝的一次傳說
[00:57.68]每個平凡的自我都曾幻想過
[01:05.30]以你為名的小說會是枯燥或是雋永
[01:19.78]從前只想裝懂裝作什麼都懂
[01:26.91]懂得生存的規則之後
[01:31.13]卻只想要都不懂
[01:34.72]如果人類的臉長得全都相同
[01:42.36]那麼你和人們的不同
[01:46.45]就看你怎麼活
[01:51.48]想像你的白髮皺紋緊貼你的輪廓
[01:58.98]你最終的朋友就是此刻
[02:03.41]那些最瘋最愛和最痛
""")
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 14)
                 , fg = '#264653',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self,font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self, width = 20)
        
        
#1-3 吳宗憲-是不是這樣的夜晚你才會這樣的想起我
class Song13(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#264653')
        self.pack_propagate(0)
        tk.Label(self, text="吳宗憲-是不是這樣的夜晚你才會這樣的想起我", font=('微軟正黑體', 14, "bold")
                , height=2, bg = '#264653', fg='white').pack(padx=5, pady=5)
        def Question(n, Ans):
            Ans_lst = [[36.62,'轉到昨天的頻道讓聲音驅走寂靜'],[43.93,'總是同樣的劇情'],
                       [46.93,'同樣的對白同樣的空白'],[54.81,'是不是這樣的夜晚你才會這樣的想起我'],
                       [61.81,'這樣的夜晚適合在電話裡'],[68.37,'只有幾句小心的彼此問候'],
                       [71.72,'繫著兩端的猜測'],[75.97,'是這樣的夜晚想起我']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\A-3. 吳宗憲-是不是這樣的夜晚你才會這樣的想起我.mp3",
                        """[00:00.00]歌名：是不是這樣的夜晚你才會這樣的想起我
[00:20.24]結束忙碌的一天換回熟悉的寂寞
[00:27.55]懶懶的躺在沙發上像母親溫暖臂彎
[00:36.62]轉到昨天的頻道讓聲音驅走寂靜
[00:43.93]總是同樣的劇情
[00:46.93]同樣的對白同樣的空白
[00:54.81]是不是這樣的夜晚你才會這樣的想起我
[01:01.81]這樣的夜晚適合在電話裡
[01:08.37]只有幾句小心的彼此問候 
[01:11.72]繫著兩端的猜測
[01:15.97]是這樣的夜晚想起我
[01:23.54]是不是這樣的夜晚你才會這樣的想起我
[01:31.10]這樣的夜晚適合在電話裡
[01:37.47]雖然幾句小心的彼此問候
[01:40.91]現在牽未來的手
[01:45.16]是這樣的日子需要改變
[02:33.24]轉到昨天的頻道讓聲音驅走寂靜
""")
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 14)
                , fg = '#264653',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#1-4 陳綺貞-我喜歡上你時的內心活動
class Song14(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#264653')
        self.pack_propagate(0)
        tk.Label(self, text="陳綺貞-我喜歡上你時的內心活動", font=('微軟正黑體', 14, "bold")
                , height=2, bg = '#264653', fg='white' ).pack(padx=5, pady=5)
        def Question(n, Ans):
            Ans_lst = [[25.83,'窗外它水管在開花'],[31.92,'椅子在異鄉樹葉有翅膀'],
                       [38.04,'上海的街道雪山在邊上'],[44.72,'你靠著車窗我心臟一旁'],
                       [53.79,'我們去哪'],[70.30,'你看那九點鐘方向'],[79.60,'日內瓦湖的房子貴嗎'],
                       [85.34,'世界上七千個地方'],[94.24,'我們定居哪'],[98.91,'告訴我答案是什麼'],
                       [104.39,'你喜歡去哪'],[107.32,'青海或三亞冰島或希臘'],[114.20,'南美不去嗎沙漠你愛嗎']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\A-4. 陳綺貞-我喜歡上你時的內心活動.mp3",
                        """[00:00.00]歌名：我喜歡上你時的內心活動
[00:11.39]在九月
[00:15.55]潮溼的車廂你看著車窗
[00:25.83]窗外它水管在開花
[00:31.92]椅子在異鄉樹葉有翅膀
[00:38.04]上海的街道雪山在邊上
[00:44.72]你靠著車窗我心臟一旁
[00:53.79]我們去哪
[01:11.30]你看那九點鐘方向
[01:19.60]日內瓦湖的房子貴嗎
[01:25.34]世界上七千個地方
[01:34.24]我們定居哪 
[01:38.91]告訴我答案是什麼
[01:43.39]你喜歡去哪
[01:47.32]青海或三亞冰島或希臘 
[01:54.20]南美不去嗎沙漠你愛嗎
[02:05.03]我問太多了
""")
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing,  font=('微軟正黑體', 12, "bold"),
                 fg = '#264653',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#1-5 林宥嘉-我總是一個人在練習一個人
class Song15(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        tk.Label(self, text="林宥嘉-我總是一個人在練習一個人", font=('微軟正黑體', 14, "bold")).pack(padx=5, pady=5)
        def Question(n, Ans):
            Ans_lst = []
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\A-5. 林宥嘉-我總是一個人在練習一個人.mp3",
                        """[00:00.00]歌名：我總是一個人在練習一個人
[00:17.55]一個人去上班
[00:21.69]又一個人去吃飯
[00:24.50]再和更多的一個人糾纏
[00:33.08]話才說到一半沒有人聽完
[00:40.65]我不孤單孤單只是情緒氾濫
[00:47.42]一個人出去逛又一個人躺在床
[00:55.46]這晚有多少的一個人沒伴
[01:03.08]不夠分另一半
[01:07.58]愛已經用完
[01:09.55]我不孤單孤單只是不夠果斷
[01:17.00]我總是一個人在練習一個人
[01:25.64]寂寞是腳跟回憶是凹痕
[01:30.14]也沒有人見證
[01:32.81]我總是一個人在練習一個人
[01:40.86]寂寞是腳跟回憶是凹痕
[01:45.06]我一個人共存
[02:06.84]我總是一個人在練習一個人
""")
        ###動態歌詞
        play.showing.set("~前奏~請耐心等候~")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 14),width=55, height=9).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.pack(padx=20,pady=20)
            tk.Button(self, text="提交", command = Answer).pack()
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="Start", command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self, width = 20)
        tk.Button(self, text="提交", command = Answer)

###主題B九零年代金曲
#2-1張惠妹-聽海
class Song21(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#198962')
        self.pack_propagate(0)
        tk.Label(self, text="張惠妹-聽海", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[58.18,'灰色是不想說'],[65.49,'而漂泊的你'],[73.92,'寫信告訴我今夜'],
                       [81.59,'夢裡外的我是否'],[88.79,'我揪著一顆心'],[97.48,'為何你明明動了情'],
                       [105.57,'聽海哭的聲音'],[112.34,'嘆惜著誰又被傷了心'],[116.51,'卻還不清醒'],
                       [121.49,'一定不是我'],[127.79,'可是淚水'],[143.14,'這片海未免也太多情'],
                       [147.72,'悲泣到天明'],[152.32,'寫封信給我'],[158.5,'說你在離開我的時候']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\B-1. 張惠妹-聽海.mp3",
                        """[00:22.33]歌名：聽海
[00:42.98]寫信告訴我今天 海是什麼顏色
[00:50.77]夜夜陪著你的海 心情又如何
[00:58.18]灰色是不想說 藍色是憂鬱
[01:05.49]而漂泊的你 狂浪的心 停在哪裡
[01:13.92]寫信告訴我今夜 你想要夢什麼
[01:21.59]夢裡外的我是否 都讓你無從選擇
[01:28.79]我揪著一顆心 整夜都閉不了眼睛
[01:37.48]為何你明明動了情 卻又不靠近
[01:45.57]聽海哭的聲音
[01:52.34]嘆惜著誰又被傷了心 卻還不清醒
[02:01.49]一定不是我 至少我很冷靜
[02:07.79]可是淚水 就連淚水也都不相信
[02:16.42]聽海哭的聲音
[02:23.14]這片海未免也太多情 悲泣到天明
[02:32.32]寫封信給我 就當最後約定
[02:38.50]說你在離開我的時候 是怎樣的心情""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️",font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#2-2 光良-童話
class Song22(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#198962')
        self.pack_propagate(0)
        tk.Label(self, text="光良-童話", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[27.16,'我想了很久我開始慌了'],[34.25,'是不是我又做錯了什麼'],
                       [41.19,'你哭著對我說童話裡都是騙人的'],[48.69,'我不可能是你的王子'],
                       [55.19,'也許你不會懂從你說愛我以後'],[62.53,'我的天空星星都亮了'],
                       [69.56,'我願變成童話裡你愛的那個天使'],[76.72,'張開雙手變成翅膀守護你'],
                       [83.59,'你要相信相信我們會像童話故事裡'],[91.06,'幸福和快樂是結局']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\B-2. 光良-童話.mp3",
                        """[00:00.00]歌名：童話
[00:13.14]忘了有多久再沒聽到你
[00:20.15]對我說你最愛的故事
[00:27.16]我想了很久我開始慌了
[00:34.08]是不是我又做錯了什麼
[00:41.19]你哭著對我說童話裡都是騙人的
[00:48.19]我不可能是你的王子
[00:55.19]也許你不會懂從你說愛我以後
[01:02.23]我的天空星星都亮了
[01:09.26]我願變成童話裡你愛的那個天使
[01:16.22]張開雙手變成翅膀守護你
[01:23.29]你要相信相信我們會像童話故事裡
[01:30.76]幸福和快樂是結局
[01:47.90]你哭著對我說童話裡都是騙人的
[01:54.88]我不可能是你的王子
[02:01.84]也許你不會懂從你說愛我以後""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#2-3 張雨生-天天想你
class Song23(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#198962')
        self.pack_propagate(0)
        tk.Label(self, text="張雨生-天天想你", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[38.08,'當我徘徊在深夜你在我心田'],[44.54,'你的每一句誓言迴盪在耳邊'],
                       [51.95,'隱隱約約閃動的雙眼藏著你的羞怯'],[60.91,'加深我的思念兩顆心的交界'],
                       [68.08,'你一定會看見只要你願意走向前'],[77.71,'天天想你天天問自己'],
                       [84.64,'到什麼時候才能告訴你'],[90.64,'天天想你天天守住一顆心'],
                       [97.06,'把我最好的愛留給你']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\B-3. 張雨生-天天想你.mp3",
                        """[00:00.00]歌名：天天想你
[00:25.61]當我佇立在窗前你愈走愈遠
[00:32.04]我的每一次心跳你是否聽見
[00:38.48]當我徘徊在深夜你在我心田
[00:44.64]你的每一句誓言迴盪在耳邊
[00:51.95]隱隱約約閃動的雙眼藏著你的羞怯
[01:00.61]加深我的思念兩顆心的交界
[01:08.08]你一定會看見只要你願意走向前
[01:17.71]天天想你天天問自己
[01:24.44]到什麼時候才能告訴你
[01:30.64]天天想你天天守住一顆心
[01:37.06]把我最好的愛留給你
[02:00.10]當我佇立在窗前""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#2-4 陳昇-把悲傷留給自己
class Song24(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#198962')
        self.pack_propagate(0)
        tk.Label(self, text="陳昇-把悲傷留給自己", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[31.43,'回去的路有些黑暗擔心讓妳一個人走'],[42.14,'我想是因為我不夠溫柔不能分擔妳的憂愁'],
                       [54.50,'如果這樣說不出口就把遺憾放在心中'],[67.21,'把我的悲傷留給自己妳的美麗讓妳帶走'],
                       [77.72,'從此以後我再沒有快樂起來的理由'],[97.76,'我想我可以忍住悲傷'],
                       [103.34,'可不可以妳也會想起我'],[110.98,'是不是可以牽妳的手呢']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\B-4. 陳昇-把悲傷留給自己.mp3",
                        """[00:00.00]歌名：把悲傷留給自己
[00:19.53]能不能讓我陪著妳走
[00:25.64]既然妳說留不住妳
[00:30.43]回去的路有些黑暗擔心讓妳一個人走
[00:42.14]我想是因為我不夠溫柔不能分擔妳的憂愁
[00:53.90]如果這樣說不出口就把遺憾放在心中
[01:06.81]把我的悲傷留給自己妳的美麗讓妳帶走
[01:17.72]從此以後我再沒有快樂起來的理由
[01:27.14]把我的悲傷留給自己妳的美麗讓妳帶走
[01:37.76]我想我可以忍住悲傷
[01:43.34]可不可以妳也會想起我
[01:51.28]是不是可以牽妳的手呢
[02:14.73]從來沒有這樣要求""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#2-5 香香-老鼠愛大米
class Song25(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#198962')
        self.pack_propagate(0)
        tk.Label(self, text="張雨生-天天想你", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[44.90,'我記得有一個人永遠留在我心中'],[52.35,'哪怕只能夠這樣的想你'],
                       [58.80,'如果真的有一天愛情理想會實現'],[66.45,'我會加倍努力好好對你永遠不改變'],
                       [73.58,'不管路有多麼遠一定會讓它實現'],[80.50,'我會輕輕在你耳邊對你說對你說'],
                       [90.69,'我愛你愛著你就像老鼠愛大米'],[98.26,'不管有多少風雨我都會依然陪著你'],
                       [104.75,'我想你想著你不管有多麼的苦'],[112.35,'只要能讓你開心我什麼都願意']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\B-5. 香香-老鼠愛大米.mp3",
                        """[00:00.00]歌名：香香-老鼠愛大米
[00:29.86]我聽見你的聲音有種特別的感覺
[00:37.71]讓我不斷想不敢再忘記你
[00:44.38]我記得有一個人永遠留在我心中
[00:51.74]哪怕只能夠這樣的想你
[00:59.10]如果真的有一天愛情理想會實現
[01:05.95]我會加倍努力好好對你永遠不改變
[01:12.08]不管路有多麼遠一定會讓它實現
[01:20.09]我會輕輕在你耳邊對你說對你說
[01:30.69]我愛你愛著你就像老鼠愛大米
[01:37.76]不管有多少風雨我都會依然陪著你
[01:44.25]我想你想著你不管有多麼的苦
[01:51.71]只要能讓你開心我什麼都願意
[01:58.30]這樣愛你""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
###主題C.獨立樂團
#3-1好樂團-他們說我是沒有用的年輕人
class Song31(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#DFAC2A')
        self.pack_propagate(0)
        tk.Label(self, text="好樂團-他們說我是沒有用的年輕人", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#DFAC2A', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[32.97,'你會不會和我一樣知道勉強卻還在掙扎'],[40.07,'你會不會和我一樣被生活覆蓋夢想和希望'],
                       [48.70,'我們只喜歡小確幸放棄去改變不公平'],[56.40,'我們都空有想像力你們說的也有道理'],
                       [79.52,'他們說我是沒有用的年輕人'],[83.72,'只顧著自己眼中沒有其他人'],
                       [91.70,'不懂得犧牲只想過得安穩']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\C-1. 好樂團-他們說我是沒有用的年輕人.mp3",
                        """[00:00.00]歌名：他們說我是沒有用的年輕人
[00:16.03]你會不會和我一樣覺得自己最多就是這樣
[00:23.92]你會不會和我一樣把希望寄託在別人的身上
[00:31.97]你會不會和我一樣知道勉強卻還在掙扎
[00:39.97]你會不會和我一樣被生活覆蓋夢想和希望
[00:47.63]我們只喜歡小確幸放棄去改變不公平
[00:55.65]我們都空有想像力你們說的也有道理
[01:03.68]我們只喜歡小確幸放棄去改變不公平
[01:11.77]我們都空有想像力你們說的也有道理
[01:18.60]他們說我是沒有用的年輕人
[01:22.72]只顧著自己眼中沒有其他人
[01:26.68]他們說我是沒有用的年輕人
[01:30.63]不懂得犧牲只想過得安穩
[01:34.60]他們說我是沒有用的年輕人
[01:38.66]只顧著自己眼中沒有其他人
[01:42.64]他們說我是沒有用的年輕人
[01:46.62]不懂得犧牲只想過得安穩
[02:07.85]你會不會和我一樣""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#DFAC2A',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)

        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
    
        
#3-2甜約翰-留給你的我從未
class Song32(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#DFAC2A')
        self.pack_propagate(0)
        tk.Label(self, text="甜約翰-留給你的我從未", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#DFAC2A', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[43.66,'努力走過漫漫長夜'],[48.00,'才能讓你看見'],
                       [55.00,'其實我也不是真的不了解'],[80.84,'茫茫人海中的妥協'],
                       [86.50,'雨後也未必有晴天'],[90.22,'但我腦海的畫面'],
                       [96.46,'你的眼神比想像中還要和煦深邃'],[103.25,'提醒我會不會看起來開心得太狼狽']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\C-2. 甜約翰-留給你的我從未.mp3",
                        """[00:00.00]歌名：留給你的我從未
[00:29.93]每過一天叮嚀自己再勇敢一點
[00:38.60]面對生活再堅決一些
[00:44.66]努力走過漫漫長夜
[00:48.81]才能讓你看見
[01:12.11]其實我也不是真的不了解
[01:20.84]茫茫人海中的妥協
[01:25.99]雨後也未必有晴天
[01:30.22]但我腦海的畫面
[01:36.46]你的眼神比想像中還要和煦深邃
[01:40.52](在你的面前)
[01:41.44]提醒我會不會看起來開心得太狼狽
[01:46.31](hoo hoo) 沈澱了整片藍天
[01:51.56]hoo hoo woo daladada
[02:20.33]Can’t mention your name""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#DFAC2A',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#3-3 告五人-披星戴月的想你
class Song33(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#DFAC2A')
        self.pack_propagate(0)
        tk.Label(self, text="告五人-披星戴月的想你", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#DFAC2A', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[34.85,'公車從旁擦身而過'],[38.85,'突如其來的念頭'],
                       [43.92,'幻想化成流星的你我'],[48.45,'明亮的夜漆黑的宇宙通通來自夜空'],
                       [58.14,'我會披星戴月的想你'],[64.20,'我會奮不顧身的前進'],
                       [69.02,'遠方煙火越來越唏噓'],[73.85,'凝視前方身後的距離']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\C-3. 告五人-披星戴月的想你.mp3",
                        """[00:00.00]歌名：披星戴月的想你
[00:21.66]突如其來的美夢是你離去時捲起的泡沫
[00:30.73]踢著石頭默默的走
[00:35.00]公車從旁擦身而過
[00:40.05]突如其來的念頭
[00:44.12]幻想化成流星的你我
[00:50.45]明亮的夜漆黑的宇宙通通來自夜空
[00:58.94]我會披星戴月的想你
[01:02.26]我會奮不顧身的前進
[01:07.02]遠方煙火越來越唏噓
[01:11.85]凝視前方身後的距離
[01:16.60]我會披星戴月的想你
[01:21.43]我會奮不顧身的前進
[01:26.28]遠方煙火越來越唏噓
[01:31.05]凝視前方身後的距離
[02:34.04]順其自然的藉口像森林般圍繞著你我""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing,  font=('微軟正黑體', 12, "bold"),
                 fg = '#DFAC2A',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#3-4南西肯恩-煙花  
class Song34(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,width=600, height=400, bg='#DFAC2A')
        self.pack_propagate(0)
        tk.Label(self, text="南西肯恩-煙花", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#DFAC2A', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[39.43,'這不是我想要的說什麼無所謂'],[47.70,'還不是讓自己好過一點'],
                       [59.00,'絢爛煙花總會落下'],[73.32,'天真善良終究要長大'],
                       [81.15,'成一道光就得要熾熱的綻放'],[88.50,'哪怕路再長哪怕受再多的傷'],
                       [96.26,'哪怕前方有阻擋也要照亮'],[103.75,'這不是你想像的對吧'],
                       [110.00,'在眾人眼光之下孤獨而徬徨'],[118.56,'這不是我想要的說真的無所謂']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\C-4. 南西肯恩-煙花.mp3",
                        """[00:00.00]歌名：煙花
[00:24.66]這不是你想像的對吧
[00:29.17]雖然早有準備卻還是流淚
[00:39.23]這不是我想要的說什麼無所謂
[00:47.05]還不是讓自己好過一點
[01:06.25]絢爛煙花總會落下
[01:12.92]天真善良終究要長大
[01:20.45]成一道光就得要熾熱的綻放
[01:27.94]哪怕路再長哪怕受再多的傷
[01:35.76]哪怕前方有阻擋也要照亮
[01:44.02]這不是你想像的
[01:49.85]在眾人眼光之下孤獨而徬徨
[01:58.60]這不是我想要的說真的無所謂
[02:07.43]到最後我還是必須面對""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#DFAC2A',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
        
#3-5 棉花糖-100個太陽月亮 
class Song35(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#DFAC2A')
        self.pack_propagate(0)
        tk.Label(self, text="棉花糖-100個太陽月亮", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#DFAC2A', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[24.96,'若世界不再有希望愛要如何理直氣壯'],[32.61,'是否擁有了更多故事我們能進化變得更強'],
                       [40.70,'分享了所有狀似大方來吧許下願望'],[52.75,'你不要害怕你不要失望'],
                       [56.75,'我們都活在當下哪管受傷都是美好的荒唐'],[68.60,'要我輕輕唱要我去前往'],
                       [72.70,'這沿途風光明媚多麼漂亮'],[77.42,'漸漸長大也別忘了那個家'],
                       [84.16,'唱一首勇敢的歌吧做一場轟烈的夢吧'],[93.80,'讓眼淚有它的瀟灑愛就更加理直氣壯'],
                       [109.67,'接管了所有胡思亂想來吧許下願望']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n,
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\C-5. 棉花糖-100個太陽月亮.mp3",
                        """[00:00.00]歌名：100個太陽月亮
[00:17.20]若我不曾為誰感傷
[00:21.14]若我不曾為誰瘋狂
[00:24.96]若世界不再有希望愛要如何理直氣壯
[00:32.61]是否擁有了更多故事我們能進化變得更強
[00:40.66]分享了所有狀似大方來吧許下願望
[00:48.64]100個太陽你不要緊張
[00:52.64]你不要害怕你不要失望
[00:56.52]我們都活在當下哪管受傷都是美好的荒唐
[01:04.52]100個月亮要我慢慢想
[01:08.22]要我輕輕唱要我去前往
[01:12.24]這沿途風光明媚多麼漂亮
[01:17.19]漸漸長大也別忘了那個家
[01:26.16]唱一首勇敢的歌吧做一場轟烈的夢吧
[01:33.65]讓眼淚有它的瀟灑愛就更加理直氣壯
[01:41.66]是否擁有了更多故事我們能進化變得更強
[01:49.47]接管了所有胡思亂想來吧許下願望
[01:57.57]100個太陽你不要緊張
[02:01.41]你不要害怕你不要失望""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing,font=('微軟正黑體', 12, "bold"),
                 fg = '#DFAC2A',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)


###主題D.我要飆高音
#4-1.八三夭-想見你想見你想見你
class Song41(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#F4A261')
        self.pack_propagate(0)
        tk.Label(self, text="八三夭-想見你想見你想見你", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#F4A261', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[32.87,'若能回到冰河時期多想把你抱緊處理'],[40.82,'你的笑多療癒讓人生也甦醒'],
                       [46.96,'失去你的風景像座廢墟像失落文明'],[54.13,'能否一場奇蹟一線生機'],[58.87,'能不能有再一次相遇'],
                       [65.14,'想見你只想見你'],[68.02,'未來過去我只想見你'],[72.59,'穿越了千個萬個'],[75.17,'時間線裡人海裡相依'],
                       [80.05,'用盡了邏輯心機'],[82.88,'推理愛情最難解的謎'],[87.38,'會不會妳也和我一樣'],[91.54,'在等待一句我願意'],
                       [111.27,'永遠不退流行是青澀的真心'],[117.07,'未來先進科技無法模擬']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 240
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, ##C:\\Users\\瑄\\Downloads\\songsfile\\C-1. 好樂團-他們說我是沒有用的年輕人.mp3
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\D-1. 八三夭-想見你想見你想見你.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]想見你想見你想見你
[00:18.55]當愛情遺落成遺跡用象形刻劃成回憶
[00:26.12]想念幾個世紀才是刻骨銘心
[00:32.87]若能回到冰河時期多想把你抱緊處理
[00:40.82]你的笑多療癒讓人生也甦醒
[00:46.66]失去你的風景像座廢墟像失落文明
[00:53.13]能否一場奇蹟一線生機
[00:58.87]能不能有再一次相遇
[01:05.14]想見你只想見你
[01:08.02]未來過去我只想見你
[01:12.59]穿越了千個萬個
[01:15.17]時間線裡人海裡相依
[01:20.05]用盡了邏輯心機
[01:22.58]推理愛情最難解的謎
[01:27.38]會不會妳也和我一樣
[01:31.54]在等待一句我願意
[01:43.50]任時光更迭了四季任宇宙物換或星移
[01:50.97]永遠不退流行是青澀的真心
[01:56.77]未來先進科技無法模擬
[02:01.36]你擁抱暖意
[02:04.10]如果另個時空另個身體
[02:08.85]能不能換另一種結局""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#F4A261',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#4-2 王藍茵-惡作劇
class Song42(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#F4A261')
        self.pack_propagate(0)
        tk.Label(self, text="王藍茵-惡作劇", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#F4A261', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[37.63,'這感覺太奇異我抱歉不能說明'],[43.98,'我相信這愛情的定義'],
                       [48.26,'奇蹟會發生也不一定'],[51.82,'風溫柔的清晰也許飄來好消息'],[58.39,'一切新鮮有點冒險'],
                       [61.93,'請告訴我怎麼走到終點'],[65.51,'沒有人瞭解沒有人像我和陌生人的愛戀'],[72.88,'我想我會開始想念你'],
                       [76.64,'可是我剛剛才遇見了你'],[80.04,'我懷疑這奇遇只是個惡作劇'],[86.37,'我想我已慢慢喜歡你'],
                       [90.79,'因為我擁有愛情的勇氣'],[94.35,'我任性投入你給的惡作劇'],[100.10,'你給的惡作劇']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 110
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\D-2. 王藍茵-惡作劇.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]惡作劇
[00:29.58]我找不到很好的原因
[00:33.75]去阻擋這一切的情意
[00:37.63]這感覺太奇異我抱歉不能說明
[00:43.98]我相信這愛情的定義
[00:47.26]奇蹟會發生也不一定
[00:51.82]風溫柔的清晰也許飄來好消息
[00:58.09]一切新鮮有點冒險
[01:01.93]請告訴我怎麼走到終點
[01:05.21]沒有人瞭解沒有人像我和陌生人的愛戀
[01:12.28]我想我會開始想念你
[01:16.04]可是我剛剛才遇見了你
[01:20.04]我懷疑這奇遇只是個惡作劇
[01:26.07]我想我已慢慢喜歡你
[01:30.14]因為我擁有愛情的勇氣
[01:34.35]我任性投入你給的惡作劇
[01:39.60]你給的惡作劇""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing,  font=('微軟正黑體', 12, "bold"),
                 fg = '#F4A261',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#4-3 楊丞琳-曖昧
class Song43(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#F4A261')
        self.pack_propagate(0)
        tk.Label(self, text="楊丞琳-曖昧", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#F4A261', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[26.10,'何時該前進何時該放棄'],[32.30,'連擁抱都沒有勇氣'],[64.39,'畢竟有些事不可以'],
                       [68.95,'超過了友情還不到愛情'],[74.70,'遠方就要下雨的風景'],[81.02,'到底該不該哭泣'],
                       [86.52,'想太多的是我還是你'],[91.91,'我很不服氣也開始懷疑'],[98.08,'眼前的人是不是同一個真實的你']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 160
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\D-3. 楊丞琳-曖昧.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]曖昧
[00:15.54]曖昧讓人受盡委屈
[00:21.07]找不到相愛的證據
[00:25.80]何時該前進何時該放棄
[00:32.00]連擁抱都沒有勇氣
[00:58.03]只能陪你到這裡
[01:04.39]畢竟有些事不可以
[01:08.95]超過了友情還不到愛情
[01:14.20]遠方就要下雨的風景
[01:20.72]到底該不該哭泣
[01:26.22]想太多的是我還是你
[01:31.41]我很不服氣也開始懷疑
[01:37.38]眼前的人是不是同一個真實的你
[01:48.44]曖昧讓人受盡委屈
[01:54.07]找不到相愛的證據
[01:58.15]何時該前進何時該放棄
[02:05.32]連擁抱都沒有勇氣
[02:11.54]曖昧讓人變得貪心
[02:16.03]直到等待失去意義
[02:21.11]無奈我和你寫不出結局
[02:27.37]放遺憾的美麗停在這裡""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#F4A261',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#4-4 韋禮安-還是會
class Song44(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#F4A261')
        self.pack_propagate(0)
        tk.Label(self, text="韋禮安-還是會", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#F4A261', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[24.42,'在離開以前能不能再說一些真心的諾言'],[35.13,'能不能給我更多的時間就躺在你的身邊'],
                       [45.55,'把這畫面你靜靜的臉溫柔的肩記在心裡面'],[61.67,'害怕醒來不在你身邊的時候'],
                       [67.54,'害怕從此不在你左右'],[73.11,'還是會還是會還是會不知所措'],[78.93,'從今以後沒有我你會不會'],
                       [85.79,'太寂寞']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 90
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\D-4. 韋禮安-還是會.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]還是會
[00:12.51]在日出之前能不能再看一眼你的臉
[00:24.22]在離開以前能不能再說一些真心的諾言
[00:35.13]能不能給我更多的時間就躺在你的身邊
[00:45.25]把這畫面你靜靜的臉溫柔的肩記在心裡面
[01:00.11]還是會
[01:01.37]害怕醒來不在你身邊的時候
[01:07.14]害怕從此不在你左右
[01:11.95]或許我
[01:13.11]還是會還是會還是會不知所措
[01:18.63]從今以後沒有我你會不會
[01:25.79]太寂寞""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#F4A261',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#4-5 周興哲-以後別做朋友
class Song45(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#F4A261')
        self.pack_propagate(0)
        tk.Label(self, text="周興哲-以後別做朋友", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#F4A261', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[31.78,'保持著距離一顆心的遙遠'],[37.96,'我的寂寞你就聽不見'],[46.01,'我走回從前你往未來飛'],
                       [53.58,'遇見對的人錯過交叉點'],[61.06,'明明你就已經站在我面前'],[66.88,'我卻不斷揮手說再見'],
                       [73.01,'以後別做朋友朋友不能牽手'],[81.82,'想愛你的衝動我只能笑著帶過'],[88.71,'最好的朋友有些夢不能說出口'],
                       [98.33,'就不用承擔會失去你的心痛']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 110
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\D-5. 周興哲-以後別做朋友.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]以後別做朋友
[00:16.50]習慣聽你分享生活細節
[00:23.81]害怕破壞完美的平衡點
[00:31.78]保持著距離一顆心的遙遠
[00:37.36]我的寂寞你就聽不見
[00:46.01]我走回從前你往未來飛
[00:53.58]遇見對的人錯過交叉點
[01:01.06]明明你就已經站在我面前
[01:06.88]我卻不斷揮手說再見
[01:13.01]以後別做朋友朋友不能牽手
[01:21.22]想愛你的衝動我只能笑著帶過
[01:28.71]最好的朋友有些夢不能說出口
[01:38.33]就不用承擔會失去你的心痛""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing,  font=('微軟正黑體', 12, "bold"),
                 fg = '##F4A261',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",  font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,  text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)

###主題E.我要飆高音
#5-1.
class Song51(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,width=600, height=400, bg='#E76F51')
        self.pack_propagate(0)
        tk.Label(self, text="鄧紫棋-泡沫",font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#E76F51', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[07.97,'就像被騙的我是幸福的'],[14.80,'追究什麼對錯你的謊言'],[22.24,'基於你還愛我'],
                       [27.80,'美麗的泡沫雖然一剎花火'],[35.18,'你所有承諾雖然都太脆弱'],[42.57,'但愛像泡沫如果能夠看破'],
                       [49.76,'有什麼難過'],[57.17,'早該知道泡沫一觸就破'],[64.21,'就像已傷的心不勝折磨'],
                       [71.44,'也不是誰的錯謊言再多'],[98.72,'愛本是泡沫如果能夠看破']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 110
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\E-1. 鄧紫棋-泡沫.mp3",   
                        """[00:00.00]!歌曲即將開始!
[00:00.30]陽光下的泡沫是彩色的
[00:07.77]就像被騙的我是幸福的
[00:14.80]追究什麼對錯你的謊言
[00:21.94]基於你還愛我
[00:27.80]美麗的泡沫雖然一剎花火
[00:35.38]你所有承諾雖然都太脆弱
[00:42.37]但愛像泡沫如果能夠看破
[00:49.46]有什麼難過
[00:57.17]早該知道泡沫一觸就破
[01:04.21]就像已傷的心不勝折磨
[01:11.14]也不是誰的錯謊言再多
[01:18.21]基於你還愛我
[01:24.65]美麗的泡沫雖然一剎花火
[01:31.35]你所有承諾雖然都太脆弱
[01:38.42]愛本是泡沫如果能夠看破
[01:45.57]有什麼難過
""")
        
        ###動態歌詞
        play.showing.set("!歌曲即將開始!")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#E76F51',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self,text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#5-2
class Song52(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#E76F51')
        self.pack_propagate(0)
        tk.Label(self, text="丁噹-我是一隻小小鳥", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#E76F51', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[31.27,'也許有一天我棲上枝頭卻成為獵人的目標'],[38.06,'我飛上了青天才發現自己從此無依無靠'],
                       [45.75,'每次到了夜深人靜的時候我總是睡不著'],[52.40,'我懷疑是不是只有我的明天沒有變得更好'],
                       [59.96,'未來會怎樣究竟有誰會知道'],[66.81,'幸福是否只是一種傳說我永遠都找不到'],
                       [74.75,'我是一隻小小小小鳥'],[81.41,'想要飛呀飛卻飛也飛不高'],[88.42,'我尋尋覓覓尋尋覓覓一個溫暖的懷抱'],
                       [95.07,'這樣的要求算不算太高']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 130
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\E-2. 丁噹-我是一隻小小鳥.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]我是一隻小小鳥
[00:16.30]有時候我覺得自己像一隻小小鳥
[00:23.86]想要飛卻怎麼樣也飛不高
[00:31.27]也許有一天我棲上枝頭卻成為獵人的目標
[00:37.86]我飛上了青天才發現自己從此無依無靠
[00:45.75]每次到了夜深人靜的時候我總是睡不著
[00:52.40]我懷疑是不是只有我的明天沒有變得更好
[00:59.96]未來會怎樣究竟有誰會知道
[01:06.61]幸福是否只是一種傳說我永遠都找不到
[01:14.75]我是一隻小小小小鳥
[01:21.41]想要飛呀飛卻飛也飛不高
[01:28.42]我尋尋覓覓尋尋覓覓一個溫暖的懷抱
[01:35.07]這樣的要求算不算太高
[01:43.29]我是一隻小小小小鳥
[01:49.84]想要飛呀飛卻飛也飛不高
[01:57.18]我尋尋覓覓尋尋覓覓一個溫暖的懷抱
[02:03.97]這樣的要求算不算太高""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#E76F51',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",  font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#5-3
class Song53(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,width=600, height=400, bg='#E76F51')
        self.pack_propagate(0)
        tk.Label(self, text="飛兒樂團-我們的爱", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#E76F51', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[35.26,'那時的你說要和我手牽手'],[43.30,'一起走到時間的盡頭'],[50.51,'從此以後我都不敢抬頭看'],
                       [57.69,'彷彿我的天空失去了顏色'],[63.44,'從那一天起我忘記了呼吸'],[71.55,'眼淚啊永遠不再不再哭泣'],
                       [80.79,'我們的愛過了就不再回來'],[89.01,'直到現在我還默默的等待'],[95.11,'我們的愛我明白已變成你的負擔'],
                       [103.05,'只是永遠我都放不開'],[108.13,'最後的溫暖你給的溫暖']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\E-3. 飛兒樂團-我們的爱.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]我們的爱
[00:22.54]回憶裡想起模糊的小時候
[00:29.54]雲朵漂浮在藍藍的天空
[00:35.26]那時的你說要和我手牽手
[00:43.30]一起走到時間的盡頭
[00:50.51]從此以後我都不敢抬頭看
[00:57.69]彷彿我的天空失去了顏色
[01:03.44]從那一天起我忘記了呼吸
[01:11.25]眼淚啊永遠不再不再哭泣
[01:20.79]我們的愛過了就不再回來
[01:28.71]直到現在我還默默的等待
[01:34.81]我們的愛我明白已變成你的負擔
[01:42.75]只是永遠我都放不開
[01:47.83]最後的溫暖你給的溫暖""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#E76F51',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#5-4
class Song54(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#E76F51')
        self.pack_propagate(0)
        tk.Label(self, text="蕭敬騰-王妃", font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#E76F51', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[30.08,'誰忠心的跟隨充其量當個侍衛'],[33.94,'腳下踩著玫瑰回敬一個吻當安慰'],
                       [45.14,'像蠢動的音樂教人們怎麼成眠'],[48.98,'不知名的香水窒息的鬼魅'],[52.60,'鋒利的高跟鞋讓多少心腸破碎'],
                       [56.68,'彎刀一般的眉捍衛你的秘密花園'],[61.09,'夜太美儘管再危險總有人黑著眼眶熬著夜'],
                       [69.33,'愛太美儘管再危險願賠上了一切超支千年的淚'],[76.99,'痛太美儘管再卑微也想嘗粉身碎骨的滋味'],
                       [84.29,'你太美儘管再無言我都想用石堆隔絕世界'],[91.07,'我的王妃我要霸佔你的美'],
                       [101.51,'那催情的音樂聽起來多麼愚昧'],[105.86,'妳武裝的防備傷你的是誰'],
                       [109.38,'靠近我一點點是不一樣的世界'],[113.16,'安睡在我的肩我用生命為你加冕']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\E-4. 蕭敬騰-王妃.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]王妃
[00:22.36]搖晃的紅酒杯嘴唇像染著鮮血
[00:26.07]那不尋常的美難赦免的罪
[00:29.78]誰忠心的跟隨充其量當個侍衛
[00:33.64]腳下踩著玫瑰回敬一個吻當安慰
[00:41.92]可憐
[00:45.14]像蠢動的音樂教人們怎麼成眠
[00:48.68]不知名的香水窒息的鬼魅
[00:52.60]鋒利的高跟鞋讓多少心腸破碎
[00:55.98]彎刀一般的眉捍衛你的秘密花園
[01:01.09]夜太美儘管再危險總有人黑著眼眶熬著夜
[01:09.33]愛太美儘管再危險願賠上了一切超支千年的淚
[01:16.99]痛太美儘管再卑微也想嘗粉身碎骨的滋味
[01:24.29]你太美儘管再無言我都想用石堆隔絕世界
[01:30.87]我的王妃我要霸佔你的美
[01:41.01]那催情的音樂聽起來多麼愚昧
[01:45.56]妳武裝的防備傷你的是誰
[01:48.88]靠近我一點點是不一樣的世界
[01:53.16]安睡在我的肩我用生命為你加冕""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#E76F51',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交", font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)
        
#5-5
class Song55(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width=600, height=400, bg='#E76F51')
        self.pack_propagate(0)
        tk.Label(self, text="陳芳語-愛你",  font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#E76F51', fg='white').pack(padx=5, pady=5)
        
        def Question(n, Ans):
            Ans_lst = [[20.78,'你微笑的唇型總勾著我的心'],[28.05,'每一秒初吻我每一秒都想要吻你'],
                       [36.95,'就這樣愛你愛你愛你隨時都要一起'],[43.93,'我喜歡愛你外套味道還有你的懷裡'],
                       [50.21,'把我們衣服鈕扣互扣那就不用分離'],[57.81,'美好愛情我就愛這樣貼近因為你'],
                       [84.45,'你的緊張在意讓我覺得安心'],[91.07,'從你某個角度我總看見自己'],
                       [97.91,'到底你懂我或其實我本來就像你']]
            # 前兩句不問
            # 注意不同秒數，但歌詞一樣
            x = random.randint(0, len(Ans_lst)-1)
            #     x = random.randint(0, 2) #測試用
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans
        
        n = 130
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(n, 
                        Ans,
                        tk.StringVar(),
                        r"C:\\Users\\User\\Downloads\\songsfile\\E-5. 陳芳語-愛你.mp3",   ###C:\data\檔名2.txt
                        """[00:00.00]愛你
[00:07.77]我閉上眼睛貼著你心跳呼吸
[00:14.41]而此刻地球只剩我們而已
[00:20.78]你微笑的唇型總勾著我的心
[00:27.75]每一秒初吻我每一秒都想要吻你
[00:36.95]就這樣愛你愛你愛你隨時都要一起
[00:43.63]我喜歡愛你外套味道還有你的懷裡
[00:50.21]把我們衣服鈕扣互扣那就不用分離
[00:57.81]美好愛情我就愛這樣貼近因為你
[01:17.85]有時沒生氣故意鬧脾氣
[01:24.45]你的緊張在意讓我覺得安心
[01:31.07]從你某個角度我總看見自己
[01:37.71]到底你懂我或其實我本來就像你
[01:46.85]就這樣愛你愛你愛你隨時都要一起
[01:53.57]我喜歡愛你外套味道還有你的懷裡
[02:00.10]把我們衣服鈕扣互扣那就不用分離
[02:07.73]美好愛情我就愛這樣貼近因為你""")
        
        ###動態歌詞
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#E76F51',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   ######跳接答對頁面
                master.switch_frame(Bingo)
            else:                   ######跳接答錯頁面
                master.switch_frame(Wrong)
        def pop_btn():
            player_input.place(width=200, height=32, x=170, y=330)
            tk.Button(self, text="提交",font=('微軟正黑體', 11, "bold"), relief='groove', command = Answer).place(x=375, y=330)
        ###播放按鈕
        def play_off():
            play.output_lyrics_music()
            self.start_btn['state'] = tk.DISABLED
            global app
            app.after(int((play.n+1)*1000),pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self)

if __name__ == "__main__": #程式是直接執行時，__name__的值就是__main__
    ###score = 0
    app = mainwin()
    app.title("百萬大歌星")
    app.geometry('600x400')
    app.configure(background='beige')
    app.iconbitmap('RBmic.ico')
    app.resizable(width=0, height=0)
    app.mainloop()