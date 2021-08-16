import threading, pygame, time

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
