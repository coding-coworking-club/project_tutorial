import tkinter as tk
from tkinter import messagebox, ttk
import time
import pygame
import threading
import random
         
class Song(tk.Frame):
    """
    song_frame = Song(self, songs[0])
    self.switch_frame(song_frame)
    """
    def __init__(self, master, config):
        super().__init__(master)
        super().configure(width=600, height=400, bg='#264653')
        self.pack_propagate(0)
        self.title = config[0][:-4]
        
        def parse_lyric(ans_str):
            ans_str = ans_str.replace('[', '').split(']')
            time = ans_str[0].split(':')
            time = int(time[0]) * 60 + float(time[1])
            return [time, ans_str[1]]
            

        self.content = [parse_lyric(a) for a in config[1]]
        print(config[1] , self.content)
        tk.Label(self, text=self.title, font=('微軟正黑體', 14, "bold")
                , height=2, bg = '#264653', fg='white').pack(padx=5, pady=5)

        t, Ans = random.choice(self.content[3:])
        print(self.config)
        play = Songplay(t,
                        Ans,
                        tk.StringVar(),
                        'songfile/%s.mp3'%self.title,
                        self.content,
                        self)
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

            self.after(int((play.ques_time + 1) * 1000), pop_btn)
            
        self.start_btn = tk.Button(self, text="▶️", font=('微軟正黑體', 10), relief='groove', command = play_off)
        self.start_btn.pack()
        
        player_input = tk.Entry(self, width = 20)
class Songplay():
    def __init__(self, ques_time, Ans, showing, filepath, musicLrc, song_page):
        self.ques_time = ques_time
        self.Ans = Ans
        self.showing = showing
        self.filepath = filepath
        self.musicLrc = musicLrc
        self.tmp_idx = -1
        self.tmp_time = 0
        self.song_page = song_page
        pygame.mixer.init() # 改main
        
        
    def play(self):
        track = pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(10)

        tmp_time = 0
        for t,lyc in self.musicLrc: #停止時間進行輸出。
            
            
            sleep_time = t - tmp_time
            print(t ,sleep_time, self.ques_time)
            tmp_time = t
            time.sleep(sleep_time)
            
            if t == self.ques_time:
                
                self.showing.set('請輸入接續歌詞：'+'*'*len(self.Ans))
                pygame.mixer.music.fadeout(0.5)
                self.song_page.pop_btn()

                break
            else:
                self.showing.set(lyc)
                global app
                app.update()
    
    def switch(self):
        ##
        pass
    def output_lyrics_music(self):
        ## 新建執行緒(threading)
        playing_work = threading.Thread(target = self.play, name = 'play')
        playing_work.start()
