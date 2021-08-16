import tkinter as tk
from song_play import Songplay
import random

# SongName: str
# SongIngo: [[歌詞timestamp, '歌詞'] x N]
# file_loc: 歌曲相對路徑
# whole_lyrics: 整首歌[時間戳記, '歌詞']

class gen_song(tk.Frame):
    def __init__(self, master, SongName,SongInfo):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, width = 600, height = 400, bg = '#198962')
        tk.Frame.pack_propagate(0)
        tk.Label(self, text = SongName, font=('微軟正黑體', 14, "bold"), height=2,
                 bg = '#198962', fg='white').pack(padx=5, pady=5)


        # 這個method的功能是預先安排好問題點，隨機挑一個出來
        def Question(n, Ans):
            Ans_lst = [[i[0], i[1]] for i in  SongInfo]
            x = random.randint(0, len(Ans_lst)-1)
            n = Ans_lst[x][0]
            Ans = Ans_lst[x][1]
            return n, Ans            
        n = 120
        Ans = ''
        n, Ans = Question(n, Ans)
        
        play = Songplay(
            n,
            Ans,
            tk.StringVar(),
            f'{file_loc}',
            whole_lyrics
            )
        
        play.showing.set("準備好後請按撥放鍵▶️")
        tk.Label(self, textvariable = play.showing, font=('微軟正黑體', 12, "bold"),
                 fg = '#198962',width=45, height=10).pack(padx=5, pady=5)
        
        def Answer():
            if player_input.get() == Ans:   # 跳接答對頁面
                master.switch_frame(Bingo)  
            else:                   
                master.switch_frame(Wrong)  # 跳接答錯頁面
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


# try to instantiate class "gen_song"


file_loc = 'ccClub專案\songsfile\_A-5. 林宥嘉-我總是一個人在練習一個人.mp3'

whole_lyrics = """
[00:00.00]歌名：有些事現在不做一輩子都不會做了
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
"""


######### TypeError: __init__() takes 4 positional arguments but 5 were given
# 求救！！
song1= gen_song('lullaby',[[15, 'baby'], [17, 'go sleep']], f, whole_lyrics)
#########