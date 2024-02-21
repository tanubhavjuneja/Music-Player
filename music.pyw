import os
import vlc
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
import time
import cv2
import customtkinter as ctk
from PIL import Image
import tkfilebrowser
import logging
from functools import wraps
import threading
logging.basicConfig(filename='music_player.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception("%s: %s", func.__name__, e)
            raise
    return wrapper
def play_video(event=None):
    global n,vp,clip,emit,pf,video_playback
    video_playback=True
    if ff[-4:]==".mp4":
        func() 
        clip_time = time.time()
        clip = cv2.VideoCapture(ff) 
        clip.set(cv2.CAP_PROP_POS_MSEC, emit*1000)
        cv2.namedWindow('Video Player', cv2.WINDOW_NORMAL) 
        cv2.setWindowProperty('Video Player', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while clip.isOpened(): 
            ret, frame = clip.read()
            if ret: 
                cv2.imshow('Video Player', frame)
                key = cv2.waitKey(25) & 0xFF
                if key!=255:
                    if key == ord('f'):
                        video_playback=False
                        break
                    elif key == ord('a'):
                        rewind()
                    elif key == ord('d'):
                        fastf()
                    elif key == 32:
                        vp.pause()
                        break
                    elif key == ord('b'):
                        clip.release()
                        cv2.destroyAllWindows()
                        previous(None)
                        play_video(None)
                    elif key == ord('n'):
                        clip.release()
                        cv2.destroyAllWindows()
                        nextxx(None)
                        play_video(None)
                    elif key ==ord('e'):
                        open_equalizer_window(None)
                        break   
                    elif key ==ord('p'):
                        open_playlist_window(None)
                        break  
                    elif key == ord('r'):
                        repeat(None)
                    elif key == ord('s'):
                        shuffle()
            else:
                break
        clip.release()
        cv2.destroyAllWindows()
        return video_playback
def update_song_color():
    global n,song_buttons,ff,pforg,pf,qi,np,queue_buttons,queue_playing,small_window,queue_order
    if small_window==False:
        for sn,song_button in enumerate(song_buttons):
            if sn == n:
                song_button.configure(fg_color="DarkOrchid3")
            else:
                song_button.configure(fg_color=bgcc)
def org_list():
    global search_bar,back_button,searched,queue_buttons,song_buttons
    back_button.destroy()
    search_bar.delete("0.0", "end")
    search_bar.configure(width=320)
    search_bar.place_configure(relx=0.03)
    searched=False
    for queue_button in queue_buttons:
        queue_button.destroy()
    for song_button in song_buttons:
        song_button.destroy()
    song_buttons=[]
    queue_buttons=[]
    queue_icon = ctk.CTkImage(Image.open(mfl+"icons/queue.png"), size=(25, 25))
    for sn in range(len(pforg)):
        song_namex = pforg[sn][:-5]
        song_button = ctk.CTkButton(scrollable_frame, width=270, text=song_namex, font=("Arial", 16, "bold"), height=30,bg_color=bgcc, fg_color=bgcc, border_width=0, anchor="w",hover_color="DarkOrchid3")
        song_button.bind("<Button-1>", lambda e, index=sn: jump(index))
        song_buttons.append(song_button)
        song_button.grid(row=sn, column=0)
        queue_button = ctk.CTkButton(scrollable_frame, image=queue_icon,text="",width=1)
        queue_button.configure(command=lambda index=sn: queue(index))
        queue_buttons.append(queue_button)
        queue_button.grid(row=sn, column=1)
    update_song_color()
def search_song(event):
    global search_bar,playlist_window,song_buttons,queue_buttons,back_button,searched,scrollable_frame,pforg,search_results
    if searched==False:
        searched=True
        search_bar.configure(width=290)
        search_bar.place_configure(relx=0.1)
        back_icon = ctk.CTkImage(Image.open(mfl+"icons/back.png"), size=(20, 20))
        back_button = ctk.CTkButton(playlist_window, image=back_icon, command=org_list,text="",width=1)
        back_button.place(rely=0.07)
    else:
        pass
    queue_icon = ctk.CTkImage(Image.open(mfl+"icons/queue.png"), size=(25, 25))
    for queue_button in queue_buttons:
        queue_button.destroy()
    for song_button in song_buttons:
        song_button.destroy()
    search_results=[]
    song_buttons=[]
    queue_buttons=[]
    search = search_bar.get("0.0", "end").rstrip()
    for sn in range(len(pforg)):
        if search in pforg[sn].lower():
            search_results.append(pforg[sn])
            song_namex = pforg[sn][:-5]
            song_button = ctk.CTkButton(scrollable_frame, width=270, text=song_namex, font=("Arial", 16, "bold"), height=30,bg_color=bgcc, fg_color=bgcc, border_width=0, anchor="w",hover_color="DarkOrchid3")
            song_button.bind("<Button-1>", lambda e, index=sn: jump(pf.index(index)))
            song_buttons.append(song_button)
            song_button.grid(row=sn, column=0)
            queue_button = ctk.CTkButton(scrollable_frame, image=queue_icon,text="",width=1)
            queue_button.configure(command=lambda index=sn: queue(pf.index(index)))
            queue_buttons.append(queue_button)
            queue_button.grid(row=sn, column=1)
    update_song_color()
def open_playlist_window(event):
    global playlist_window, pf, bgcc, n,song_buttons,open_window,pforg,mfl,queue_buttons,edit,playlist_window_x,playlist_window_y,search_bar,scrollable_frame
    if open_window==False:
        open_window=True
        playlist_window = ctk.CTkToplevel()
        playlist_window.title("Playlist")
        playlist_window.geometry(f"340x590+{playlist_window_x}+{playlist_window_y}")
        playlist_window.overrideredirect(True)
        playlist_label=ctk.CTkLabel(playlist_window,text="Playlist", font=("Arial", 16, "bold"))
        playlist_label.place(rely=0.01,relx=0.05)
        close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(13, 13))
        close_button = ctk.CTkButton(playlist_window, image=close_icon, command=on_playlist_window_close,text="",width=1)
        close_button.place(relx=0.9,rely=0.01)
        search_bar=ctk.CTkTextbox(playlist_window,height=25,width=320,wrap=ctk.WORD)
        search_bar.bind("<KeyRelease>", lambda event: search_song(event))
        search_bar.bind("<Return>", lambda e: "break")
        search_bar.place(rely=0.065,relx=0.03)
        search_icon = ctk.CTkImage(Image.open(mfl+"icons/search.png"), size=(20, 20))
        search_button = ctk.CTkButton(search_bar, image=search_icon,fg_color="gray20",command=lambda:search_song(None),text="",width=1)
        search_button.place(relx=0.88,rely=0.05)
        scrollable_frame = ctk.CTkScrollableFrame(playlist_window, width=310, height=450)
        scrollable_frame.place(rely=0.12)
        queue_icon = ctk.CTkImage(Image.open(mfl+"icons/queue.png"), size=(25, 25))
        song_buttons=[]
        queue_buttons=[]
        for sn in range(len(pf)):
            song_namex = pforg[pf[sn]][:-5]
            song_button = ctk.CTkButton(scrollable_frame, width=270, text=song_namex, font=("Arial", 16, "bold"), height=30,bg_color=bgcc, fg_color=bgcc, border_width=0, anchor="w",hover_color="DarkOrchid3")
            song_button.bind("<Button-1>", lambda e, index=sn: jump(index))
            song_buttons.append(song_button)
            song_button.grid(row=sn, column=0)
            queue_button = ctk.CTkButton(scrollable_frame, image=queue_icon,text="",width=1)
            queue_button.configure(command=lambda index=sn: queue(index))
            queue_buttons.append(queue_button)
            queue_button.grid(row=sn, column=1)
        reset_button = ctk.CTkButton(playlist_window,text="Reset",width=300,height=30,command=reset_queue,fg_color="DarkOrchid3",font=("Arial", 16, "bold"))
        reset_button.place(rely=0.92,relx=0.05)
        update_song_color()
        if edit==True:
            playlist_window.bind("<B1-Motion>", lambda event, window=playlist_window: on_drag_motion(event, window))
            playlist_window.bind("<ButtonPress-1>", lambda event, window=playlist_window: on_drag_start(event, window))
    else:
        on_playlist_window_close()
def reset_queue():
    global pf,pforg,n,np,queue_playing,pforg,shuffled,queue_order
    queue_order=[]
    queue_playing=False
    shuffled=False
    n=pforg.index(np)
    pf=list(range(0, len(pforg)))
    for i in range(0,len(pf)):
        change_element(i)
    update_song_color()
def on_playlist_window_close():
    global playlist_window,open_window
    playlist_window.destroy()
    open_window=False
def jump(index):
    global n,pf,pforg,vp
    if n!=index:
        vp.stop()
        n=index
        play()
def change_element(index):
    global song_buttons, queue_buttons,pf,pforg
    song_namex = pforg[pf[index]][:-5]
    song_button=song_buttons[index]
    song_button.unbind()
    song_button.bind("<Button-1>", lambda e, index=index: jump(index))
    song_button.configure(text=song_namex)
    queue_button=queue_buttons[index]
    queue_button.unbind()
    queue_button.configure(command=lambda index=index: queue(index))
def queue(index):
    global n,playlist_window,pf,vp,qi,pforg,ff,song_buttons,queue_buttons,queue_playing,pbs,fscreen,search_results,queue_order,shuffled
    queue_playing=True
    queue_item=pf[index]
    if queue_item not in queue_order:
        if n>index:
            pf.remove(queue_item)
            pf.insert(n+len(queue_order),queue_item)
            queue_order.append(queue_item)
            n-=1
            for i in range(index,n+len(queue_order)+1):
                change_element(i)
        else:
            queue_order.append(queue_item)
            pf.remove(queue_item)
            pf.insert(n+len(queue_order),queue_item)
            for i in range(n+len(queue_order),index+1):
                change_element(i)
    else:
        queue_order.remove(queue_item)
        pf.remove(queue_item)
        pf.insert(index,queue_item)
    update_song_color()
    return queue_playing
def fastf():
    global vp, clip
    currtime = vp.get_time()
    newtime = currtime + 10000
    vp.pause()
    vp.set_time(newtime) 
    clip.set(cv2.CAP_PROP_POS_MSEC, newtime)
    vp.play()
def rewind():
    global vp, clip
    currtime = vp.get_time()
    newtime = currtime - 10000
    vp.pause()
    vp.set_time(newtime) 
    clip.set(cv2.CAP_PROP_POS_MSEC, newtime)
    vp.play()
def func():
        global emit
        emit=vp.get_time()//1000
        if emit==-1:
            func()
        return emit
def read_file_location():
    global mfl
    try:
        file=open('file_location.txt', 'r')
        mfl = file.read().strip()
        file.close()
        if not os.path.isfile(os.path.join(mfl, 'myjson.json')):
            get_file_location()
    except FileNotFoundError:
        get_file_location()
def get_file_location():
    global main
    main=ctk.CTk()
    main.geometry("200x50+860+420")
    main.attributes('-topmost', True)
    main.attributes("-alpha",100.0)
    main.lift()
    file_button = ctk.CTkButton(main, text="Select File Location",command=select_file_location,width=1)
    file_button.pack(pady=10)
    main.mainloop()
def select_file_location():
    global main
    mfl = str(tkfilebrowser.askopendirname())+"/"
    mfl = mfl.replace('\\', '/')
    file=open('file_location.txt', 'w')
    file.write(mfl)
    file.close()
    main.destroy()
    read_file_location()
def sort_songs():
    global mfl,pf,pforg,ptop,romantic,happy,sad,confident,relaxed
    ptop = mfl+"music"
    pforg = os.listdir(ptop)
    romantic=[]
    happy=[]
    sad=[]
    confident=[]
    relaxed=[]
    for song in pforg:
        cat=song[-5]
        if cat=="1":
            romantic.append(song)
        elif cat=="2":
            happy.append(song)
        elif cat=="3":
            sad.append(song)
        elif cat=="4":
            confident.append(song)
        elif cat=="5":
            relaxed.append(song)
    pforg.sort()
    pf=list(range(0, len(pforg)))
def start():
    global shuffled,queue_order,searched,scheduler,dws,open_window3,debug_window_x,debug_window_y,mws,open_window2,mood_window_x,mood_window_y,equalizer_window_y,equalizer_window_x,playlist_window_x,playlist_window_y,window_x,window_y,edit,small_window,pforg,qi,repeat_song,song_name_label,cunt,fscreen,equalizer,song_progress_label,song_length,song_progress_slider,ptop,pf,n,vs,main,pp,video_playback,open_window,queue_playing,bgc,bgcc,count,song_name,playing,pbs,ews,mfl,open_window1
    video_playback=False
    count=0
    theme="dark"
    repeat_song=False
    read_file_location()
    if theme == "dark":
        bgc="gray14"
        bgcc="gray12"
    elif theme == "light":
        bgc="gray92"
        bgcc="gray95"
    ctk.set_appearance_mode(theme)
    ctk.set_default_color_theme(mfl+"myjson.json")
    equalizer = vlc.libvlc_audio_equalizer_new()
    scheduler=None
    cunt=0
    vs=100
    n = 0
    qi=0
    queue_playing=False
    song_length=0
    open_window=False
    open_window1=False
    open_window2=False
    open_window3=False
    searched=False
    fscreen=False
    shuffled=False
    small_window=False
    sort_songs()
    song_name = pforg[n][:-5]
    queue_order=[]
    playing=False
    pbs=False
    mws=False
    ews=False
    dws=False
    edit=False
    window_x = 740
    window_y = 340
    playlist_window_y=230
    playlist_window_x=390
    equalizer_window_x=1190
    equalizer_window_y=230
    mood_window_x=740
    mood_window_y=230
    debug_window_x=740
    debug_window_y=600
    mainstart()
def open_mood_window(event):
    global mood_window,mood_window_x,mood_window_y,open_window2,romantic,happy,sad,confident,edit,relaxed
    if open_window2==False:
        open_window2=True
        mood_window = ctk.CTkToplevel()
        mood_window.title("Mood")
        mood_window.geometry(f"440x100+{mood_window_x}+{mood_window_y}")
        mood_window.overrideredirect(True)
        close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(13, 13))
        close_button = ctk.CTkButton(mood_window, image=close_icon, command=on_mood_window_close,text="",width=1)
        close_button.place(relx=0.928,rely=0.01)
        romantic_icon = ctk.CTkImage(Image.open(mfl+"icons/romantic.png"), size=(55, 55))
        happy_icon = ctk.CTkImage(Image.open(mfl+"icons/happy.png"), size=(50, 50))
        sad_icon = ctk.CTkImage(Image.open(mfl+"icons/sad.png"), size=(50, 50))
        confident_icon = ctk.CTkImage(Image.open(mfl+"icons/confident.png"), size=(50, 50))
        relaxed_icon = ctk.CTkImage(Image.open(mfl+"icons/relaxed.png"), size=(50, 50))
        romantic_button=ctk.CTkButton(mood_window,image=romantic_icon,command=lambda:set_mood(romantic),text="",width=1)
        happy_button=ctk.CTkButton(mood_window,image=happy_icon,command=lambda:set_mood(happy),text="",width=1)
        sad_button=ctk.CTkButton(mood_window,image=sad_icon,command=lambda:set_mood(sad),text="",width=1)
        confident_button=ctk.CTkButton(mood_window,image=confident_icon,command=lambda:set_mood(confident),text="",width=1)
        relaxed_button=ctk.CTkButton(mood_window,image=relaxed_icon,command=lambda:set_mood(confident),text="",width=1)
        romantic_button.pack(side="left",padx=10)
        happy_button.pack(side="left",padx=10)
        sad_button.pack(side="left",padx=10)
        confident_button.pack(side="left",padx=10)
        relaxed_button.pack(side="left",padx=10)
        mood_window.bind('<Down>', lambda event: vmove(vs))
        mood_window.bind('<Up>', lambda event: vmove(vs))
        mood_window.bind('<Left>', previous)
        mood_window.bind('<Alt_L>', previous)
        mood_window.bind('<b>', previous)
        mood_window.bind('<space>', ppl)
        mood_window.bind('<Return>', ppl)
        mood_window.bind('<n>', nextxx)
        mood_window.bind('<Right>', nextxx)
        mood_window.bind('<Alt_R>', nextxx)
        mood_window.bind("<s>",lambda event:shuffle(None))
        mood_window.bind("<r>",lambda event:repeat(None))
        mood_window.bind("<e>",lambda event:open_equalizer_window(None))
        mood_window.bind("<f>",lambda event:play_video(None))
        mood_window.bind("<a>",lambda event:rewindr(None))
        mood_window.bind("<d>",lambda event:fastff(None))
        mood_window.bind("<p>",lambda event:open_playlist_window(None)) 
        mood_window.bind("<m>",lambda event:open_mood_window(None)) 
        mood_window.bind("<z>",lambda event:open_debug_window(None)) 
        if edit==True:
            mood_window.bind("<B1-Motion>", lambda event, window=mood_window: on_drag_motion(event, window))
            mood_window.bind("<ButtonPress-1>", lambda event, window=mood_window: on_drag_start(event, window))
    else:
        on_mood_window_close()
def set_mood(mood):
    global n,pforg,vp,pf
    reset_queue()
    for song in mood:
        queue(pf.index(pforg.index(song)))
    n=0
    if pf[n]not in mood:
        n=1
    vp.stop()
    play()
def on_mood_window_close():
    global mood_window,open_window2
    mood_window.destroy()
    open_window2=False
class CTkLogHandler(logging.Handler):
    def __init__(self, debug_frame):
        super().__init__()
        self.debug_frame = debug_frame
    def emit(self, record):
        msg = self.format(record)
        self.debug_frame.configure(state=ctk.NORMAL)
        self.debug_frame.insert('end', msg + '\n')
        self.debug_frame.see('end')
        self.debug_frame.configure(state=ctk.DISABLED)
def create_debug_window():
    global debug_window,debug_handler,debug_frame
    debug_window = ctk.CTkToplevel()
    debug_window.title("Debug")
    debug_window.geometry(f"440x220+{debug_window_x}+{debug_window_y}")
    debug_window.overrideredirect(True)
    debug_label=ctk.CTkLabel(debug_window,text="Debug", font=("Arial", 16, "bold"))
    debug_label.place(relx=0.05,rely=0.008)
    debug_frame = ctk.CTkTextbox(debug_window, width=430, height=190,font=("Arial",16,"bold"),text_color="limegreen",fg_color=bgcc, state=ctk.DISABLED)
    debug_frame.place(relx=0.01,rely=0.12)
    close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(13, 13))
    close_button = ctk.CTkButton(debug_window, image=close_icon, command=on_debug_window_close,text="",width=1)
    close_button.place(relx=0.928,rely=0.01)
    debug_handler = CTkLogHandler(debug_frame)
    logging.getLogger().setLevel(logging.INFO)
    debug_handler.setLevel(logging.INFO)
    debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(debug_handler)
    debug_window.bind('<Down>', lambda event: vmove(vs-5))
    debug_window.bind('<Up>', lambda event: vmove(vs+5))
    debug_window.bind('<Left>', previous)
    debug_window.bind('<Alt_L>', previous)
    debug_window.bind('<b>', previous)
    debug_window.bind('<space>', ppl)
    debug_window.bind('<Return>', ppl)
    debug_window.bind('<n>', nextxx)
    debug_window.bind('<Right>', nextxx)
    debug_window.bind('<Alt_R>', nextxx)
    debug_window.bind("<s>",lambda event:shuffle(None))
    debug_window.bind("<r>",lambda event:repeat(None))
    debug_window.bind("<e>",lambda event:open_equalizer_window(None))
    debug_window.bind("<f>",lambda event:play_video(None))
    debug_window.bind("<a>",lambda event:rewindr(None))
    debug_window.bind("<d>",lambda event:fastff(None))
    debug_window.bind("<p>",lambda event:open_playlist_window(None))
    debug_window.bind("<m>",lambda event:open_mood_window(None))
    if edit==True:
        debug_window.bind("<B1-Motion>", lambda event, window=debug_window: on_drag_motion(event, window))
        debug_window.bind("<ButtonPress-1>", lambda event, window=debug_window: on_drag_start(event, window))
def open_debug_window(event):
    global open_window3,edit
    if open_window3==False:
        open_window3=True
        new_thread = threading.Thread(target=create_debug_window)
        new_thread.start()
    else:
        on_debug_window_close()
def on_debug_window_close():
    global debug_window,open_window3,debug_handler
    logging.getLogger().removeHandler(debug_handler)
    logging.getLogger().setLevel(logging.ERROR)
    debug_window.destroy()
    open_window3=False
def mainstart():
    global dws,vp,mws,window_y,window_x,edit,vslider,song_name_label,cunt,equalizer,repeat_button,song_progress_label,song_progress_slider,song_length,ptop,pf,n,vs,main,pp,open_window,bgc,bgcc,count,song_name,playing,mfl,open_window1,pbs,ews
    main = ctk.CTk()
    main.title("Music Player")
    main.geometry(f"440x250+{window_x}+{window_y}")
    main.overrideredirect(True)
    main.attributes("-alpha",100.0)
    main.lift()
    if len(song_name)>=17:
        song_name_label = ctk.CTkLabel(main, text=song_name, font=("Arial", 25, "bold"))
    else:
        song_name_label = ctk.CTkLabel(main, text=song_name, font=("Arial", 40, "bold"))
    song_name_label.place(relx=0.5, rely=0.16, anchor="n")
    vslider = ctk.CTkSlider(main, from_=0, to=100, orientation='vertical', width=20, height=90, command=vmove)
    vslider.set(vs)
    vslider.place(relx=0.97, rely=0.32, anchor="e")
    song_progress_label = ctk.CTkLabel(main, text="0:00", font=("Arial", 25, "bold"))
    song_progress_label.place(relx=0.5, rely=0.41, anchor="center")
    song_progress_slider = ctk.CTkSlider(main, from_=0, to=0, orientation='horizontal', width=410, height=20, command=lambda x: update_song_progress(song_progress_slider.get() * 1000))
    song_progress_slider.bind("<ButtonRelease-1>", lambda event: set_song_length())
    song_progress_slider.bind("<ButtonPress-1>", on_slider_press)
    song_progress_slider.bind("<ButtonRelease-1>", on_slider_release)
    song_progress_slider.place(relx=0.5, rely=0.545, anchor="center")
    npp=ctk.CTkFrame(main)
    otf=ctk.CTkFrame(main)
    playlist_icon = ctk.CTkImage(Image.open(mfl+"icons/playlist.png"), size=(30, 30))
    equalizer_icon = ctk.CTkImage(Image.open(mfl+"icons/equalizer.png"), size=(20, 20))
    shuffle_icon = ctk.CTkImage(Image.open(mfl+"icons/shuffle.png"), size=(30, 30))
    repeat_icon = ctk.CTkImage(Image.open(mfl+"icons/repeat.png"), size=(30, 30))
    repeat_icon1 = ctk.CTkImage(Image.open(mfl+"icons/repeat1.png"), size=(30, 30))
    pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(40, 40))
    video_icon = ctk.CTkImage(Image.open(mfl+"icons/video.png"), size=(30, 30))
    previous_icon = ctk.CTkImage(Image.open(mfl+"icons/previous.png"), size=(40, 40))
    next_icon = ctk.CTkImage(Image.open(mfl+"icons/next.png"), size=(40, 40))
    minimize_icon = ctk.CTkImage(Image.open(mfl+"icons/minimize.png"), size=(20, 20))
    fullscreen_icon = ctk.CTkImage(Image.open(mfl+"icons/fullscreen.png"), size=(18, 18))
    close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(15, 15))
    music_icon = ctk.CTkImage(Image.open(mfl+"icons/logo.png"), size=(25, 25))
    edit_icon = ctk.CTkImage(Image.open(mfl+"icons/edit.png"), size=(17, 17))
    debug_icon= ctk.CTkImage(Image.open(mfl+"icons/debug.png"), size=(22, 22))
    mood_icon=ctk.CTkImage(Image.open(mfl+"icons/mood.png"), size=(30, 30))
    logo = ctk.CTkLabel(main, image=music_icon,width=1,text="")
    logo.place(relx=0.03,rely=0.04)
    toolbar = ctk.CTkFrame(main, bg_color=bgcc,fg_color=bgcc)
    debug_button = ctk.CTkButton(toolbar, image=debug_icon, command=lambda:open_debug_window(None),text="",width=1)
    debug_button.pack(side="left",padx=2)
    equalizer_button = ctk.CTkButton(toolbar, image=equalizer_icon, command=lambda:open_equalizer_window(None),text="",width=1)
    equalizer_button.pack(side="left",padx=2)
    edit_button = ctk.CTkButton(toolbar, image=edit_icon, command=edit_state,text="",width=1)
    edit_button.pack(side="left", padx=2, pady=2)
    minimize_button = ctk.CTkButton(toolbar, image=minimize_icon, command=sw,text="",width=1)
    minimize_button.pack(side="left", padx=2, pady=2)
    maximize_button = ctk.CTkButton(toolbar, image=fullscreen_icon, command=call_fullscreen,text="",width=1)
    maximize_button.pack(side="left", padx=2, pady=2)
    close_button = ctk.CTkButton(toolbar, image=close_icon, command=ee,text="",width=1)
    close_button.pack(side="left", padx=2, pady=2)
    toolbar.place(rely=0.01,relx=0.47)
    pre = ctk.CTkButton(npp, image=previous_icon, command=lambda: previous(None),text="",width=1)
    pp = ctk.CTkButton(npp, image=pause_icon, command=lambda: ppl(None),text="",width=1)
    next = ctk.CTkButton(npp, image=next_icon, command=lambda: nextxx(None),text="",width=1)
    pre.pack(side="left",padx=40)
    pp.pack(side="left",padx=45)
    next.pack(side="left",padx=45)
    npp.place(rely=0.6,relx=0.02)
    shuffle_button = ctk.CTkButton(otf, image=shuffle_icon, command=lambda:shuffle(None),text="",width=1)
    repeat_button = ctk.CTkButton(otf, image=repeat_icon, command=lambda:repeat(None),text="",width=1)
    if repeat_song==True:
        repeat_button.configure(image=repeat_icon1)
    fullscreen_button = ctk.CTkButton(otf, image=video_icon,command=lambda:play_video(None),text="",width=1)
    playlist_button = ctk.CTkButton(otf, image=playlist_icon,command=lambda:open_playlist_window(None),text="",width=1)
    mood_button = ctk.CTkButton(otf, image=mood_icon,command=lambda:open_mood_window(None),text="",width=1)
    playlist_button.pack(side="left",padx=20)
    fullscreen_button.pack(side="left",padx=21)
    repeat_button.pack(side="left",padx=21)
    shuffle_button.pack(side="left",padx=21)
    mood_button.pack(side="left",padx=21)
    otf.place(rely=0.82)
    main.bind('<Down>', lambda event: vmove(vs-5))
    main.bind('<Up>', lambda event: vmove(vs+5))
    main.bind('<Left>', previous)
    main.bind('<Alt_L>', previous)
    main.bind('<b>', previous)
    main.bind('<space>', ppl)
    main.bind('<Return>', ppl)
    main.bind('<n>', nextxx)
    main.bind('<Right>', nextxx)
    main.bind('<Alt_R>', nextxx)
    main.bind("<s>",lambda event:shuffle(None))
    main.bind("<r>",lambda event:repeat(None))
    main.bind("<e>",lambda event:open_equalizer_window(None))
    main.bind("<f>",lambda event:play_video(None))
    main.bind("<a>",lambda event:rewindr(None))
    main.bind("<d>",lambda event:fastff(None))
    main.bind("<p>",lambda event:open_playlist_window(None))
    main.bind("<m>",lambda event:open_mood_window(None))
    if edit==True:
        main.bind("<B1-Motion>", lambda event, window=main: on_drag_motion(event, window))
        main.bind("<ButtonPress-1>", lambda event, window=main: on_drag_start(event, window))
    main.focus_force()
    if pbs==True:
        open_playlist_window(None)
        pbs=False
    if ews==True:
        open_equalizer_window(None)
        ews=False
    if mws==True:
        open_mood_window(None)
        mws=False
    if dws==True:
        open_debug_window(None)
        dws=False
    if playing != True:
        play()
        playing=True
    else:
        set_song_length()
    main.mainloop()
def edit_state():
    global edit,main,open_window,pbs,ews,mws,dws
    edit=not edit
    if open_window==True:
        on_playlist_window_close()
        pbs=True
    if open_window1==True:
        destroy_equalizer()
        ews=True
    if open_window2==True:
        on_mood_window_close()
        mws=True
    if open_window3==True:
        on_debug_window_close()
        dws=True
    main.destroy()
    mainstart()
def on_drag_start(event, window):
    window.x = event.x
    window.y = event.y
def on_drag_motion(event, window):
    global window_x, window_y,mood_window_x,mood_window_y, equalizer_window_x, equalizer_window_y, playlist_window_x, playlist_window_y,debug_window_x,debug_window_y
    delta_x = event.x - window.x
    delta_y = event.y - window.y
    window_title = window.title()
    if window_title=="Music Player":
        window_x = window.winfo_x() + delta_x
        window_y = window.winfo_y() + delta_y
        window.geometry(f"+{window_x}+{window_y}")
    elif window_title == "Equalizer":
        equalizer_window_x = window.winfo_x() + delta_x
        equalizer_window_y = window.winfo_y() + delta_y
        window.geometry(f"+{equalizer_window_x}+{equalizer_window_y}")
    elif window_title == "Playlist":
        playlist_window_x = window.winfo_x() + delta_x
        playlist_window_y = window.winfo_y() + delta_y
        window.geometry(f"+{playlist_window_x}+{playlist_window_y}")
    elif window_title == "Mood":
        mood_window_x = window.winfo_x() + delta_x
        mood_window_y = window.winfo_y() + delta_y
        window.geometry(f"+{mood_window_x}+{mood_window_y}")
    elif window_title == "Debug":
        debug_window_x = window.winfo_x() + delta_x
        debug_window_y = window.winfo_y() + delta_y
        window.geometry(f"+{debug_window_x}+{debug_window_y}")
def pb(event):
    global main, pf, bgcc, n,song_buttons,pbs,scrollable_frame,queue_buttons,reset_button
    if pbs==False:
        pbs=True
        scrollable_frame = ctk.CTkScrollableFrame(main, width=410, height=580)
        scrollable_frame.place(rely=0.05)
        queue_icon = ctk.CTkImage(Image.open(mfl+"icons/queue.png"), size=(40, 40))
        song_buttons=[]
        queue_buttons=[]
        if len(pf)<len(pforg):
            for sn in range(len(pforg)):
                song_namex = pforg[sn][:-5]
                song_button = ctk.CTkButton(scrollable_frame, width=350, text=song_namex, font=("Arial", 25, "bold"), height=30,bg_color=bgcc, fg_color=bgcc, border_width=0, anchor="w",hover_color="DarkOrchid3")
                song_button.bind("<Button-1>", lambda e, index=sn: jump(index))
                song_buttons.append(song_button)
                song_button.grid(row=sn, column=0)
                queue_button = ctk.CTkButton(scrollable_frame, image=queue_icon,text="",width=1)
                queue_button.configure(command=lambda index=sn: queue(index))
                queue_buttons.append(queue_button)
                queue_button.grid(row=sn, column=1)
        else:
            for sn in range(len(pf)):
                song_namex = pf[sn][:-5]
                song_button = ctk.CTkButton(scrollable_frame, width=350, text=song_namex, font=("Arial", 28, "bold"), height=30,bg_color=bgcc, fg_color=bgcc, border_width=0, anchor="w",hover_color="DarkOrchid3")
                song_button.bind("<Button-1>", lambda e, index=sn: jump(index))
                song_buttons.append(song_button)
                song_button.grid(row=sn, column=0)
                queue_button = ctk.CTkButton(scrollable_frame, image=queue_icon,text="",width=1)
                queue_button.configure(command=lambda index=sn: queue(index))
                queue_buttons.append(queue_button)
                queue_button.grid(row=sn, column=1)
        reset_button = ctk.CTkButton(main,text="Reset",width=410,height=40,command=reset_queue,fg_color="DarkOrchid3",font=("Arial", 25, "bold"))
        reset_button.place(rely=0.6,relx=0.01)
        update_song_color()
    else:
        scrollable_frame._scrollbar.destroy()
        scrollable_frame.destroy()
        reset_button.destroy()
        pbs=False
def ew(event):
    global main,vslider,ews,equalizer_window
    if ews==False:
        ews=True
        vslider.place(relx=0.805)
        equalizer_window=ctk.CTkFrame(main)
        preamp_label = ctk.CTkLabel(equalizer_window, text="Preamp", font=("Arial", 25, "bold"))
        preamp_label.pack()
        preamp_scale = ctk.CTkSlider(equalizer_window, from_=-20, to=20, orientation='horizontal',command=update_preamp,height=25,width=350)
        preamp_scale.set(vlc.libvlc_audio_equalizer_get_preamp(equalizer))
        preamp_scale.pack()
        band_scales = []
        band_frequencies = [60, 170, 310, 600, 1000, 3000, 6000, 12000, 14000, 16000]
        for i in range(10):
            freq = band_frequencies[i]
            freq_label = ctk.CTkLabel(equalizer_window, text=f'{freq} Hz', font=("Arial", 25, "bold"))
            freq_label.pack()
            scale = ctk.CTkSlider(equalizer_window, from_=-20, to=20, orientation='horizontal',command=lambda val, i=i: update_band(i, val),height=25,width=350)
            scale.set(vlc.libvlc_audio_equalizer_get_amp_at_index(equalizer, i))
            scale.pack()
            band_scales.append(scale)
        equalizer_window.place(rely=0.05,relx=0.81)
    else:
        equalizer_window.destroy()
        ews=False
        vslider.place(relx=0.97)
def sw():
    global main,scheduler,small_window,pbs,ews
    small_window=True
    if open_window==True:
        on_playlist_window_close()
        pbs=True
    if open_window1==True:
        destroy_equalizer()
        ews=True
    scheduler.shutdown(wait=False)
    scheduler=None
    main.destroy()
    main = ctk.CTk()
    main.geometry("40x40+1860+980")
    main.attributes('-topmost', True)
    main.overrideredirect(True)
    main.attributes("-alpha",100.0)
    fr_icon = ctk.CTkImage(Image.open(mfl+"icons/scale.png"), size=(28, 28))
    backfull = ctk.CTkButton(main, image=fr_icon,width=1,text="",command=restart)
    backfull.pack()
    main.bind('<Left>', previous)
    main.bind('<Alt_L>', previous)
    main.bind('<b>', previous)
    main.bind('<space>', ppl)
    main.bind('<Return>', ppl)
    main.bind('<n>', nextxx)
    main.bind('<Right>', nextxx)
    main.bind('<Alt_R>', nextxx)
    main.bind("<s>",lambda event:shuffle(None))
    main.bind("<r>",lambda event:repeat(None))
    main.bind("<e>",lambda event:open_equalizer_window(None))
    main.bind("<f>",lambda event:play_video(None))
    main.bind("<a>",lambda event:rewindr(None))
    main.bind("<d>",lambda event:fastff(None))
    main.bind("<p>",lambda event:open_playlist_window(None))
    main.mainloop()
def call_fullscreen(): 
    global main,fscreen,scheduler,open_window,open_window1,open_window2,dws
    if open_window==True:
        on_playlist_window_close()
        open_window=True
    if open_window1==True:
        destroy_equalizer()
        open_window1=True
    if open_window2==True:
        on_mood_window_close()
        open_window2=True
    if open_window3==True:
        on_debug_window_close()
        dws=True
    scheduler.shutdown(wait=False)
    scheduler=None
    main.destroy()
    fscreen=True
    fullscreen()
def mw(event):
    global mws,main,mood_frame,romantic,happy,sad,confident
    if mws==False:
        mws=True
        mood_frame=ctk.CTkFrame(main)
        romantic_icon = ctk.CTkImage(Image.open(mfl+"icons/romantic.png"), size=(78, 78))
        happy_icon = ctk.CTkImage(Image.open(mfl+"icons/happy.png"), size=(70, 70))
        sad_icon = ctk.CTkImage(Image.open(mfl+"icons/sad.png"), size=(70, 70))
        confident_icon = ctk.CTkImage(Image.open(mfl+"icons/confident.png"), size=(70, 70))
        relaxed_icon = ctk.CTkImage(Image.open(mfl+"icons/relaxed.png"), size=(70, 70))
        romantic_button=ctk.CTkButton(mood_frame,image=romantic_icon,command=lambda:set_mood(romantic),text="",width=1)
        happy_button=ctk.CTkButton(mood_frame,image=happy_icon,command=lambda:set_mood(happy),text="",width=1)
        sad_button=ctk.CTkButton(mood_frame,image=sad_icon,command=lambda:set_mood(sad),text="",width=1)
        confident_button=ctk.CTkButton(mood_frame,image=confident_icon,command=lambda:set_mood(confident),text="",width=1)
        relaxed_button=ctk.CTkButton(mood_frame,image=relaxed_icon,command=lambda:set_mood(relaxed),text="",width=1)
        romantic_button.pack(side="left",padx=30)
        happy_button.pack(side="left",padx=30)
        sad_button.pack(side="left",padx=30)
        confident_button.pack(side="left",padx=30)
        relaxed_button.pack(side="left",padx=30)
        mood_frame.place(relx=0.3,rely=0.4)
    else:
        mood_frame.destroy()
        mws=False
def fullscreen():
    global open_window2,repeat_icon1,vslider,ews,pbs,mws,song_name_label,repeat_button,vslider,cunt,scheduler,equalizer,fscreen,song_progress_label,song_length,song_progress_slider,ptop,pf,n,vs,main,pp,open_window,bgc,bgcc,count,song_name,playing, pf, bgcc, n,song_buttons,open_window1
    ews=False
    mws=False
    pbs=False
    main = ctk.CTk()
    main.attributes('-fullscreen', True)
    main.title("Music Player")
    main.overrideredirect(True)
    main.attributes("-alpha",100.0)
    main.lift()
    main.focus_force()
    if len(song_name)>=17:
        song_name_label = ctk.CTkLabel(main, text=song_name, font=("Arial", 60, "bold"))
    else:
        song_name_label = ctk.CTkLabel(main, text=song_name, font=("Arial", 120, "bold"))
    song_name_label.pack(pady=10)
    song_name_label.place(relx=0.5, rely=0.15, anchor="n")
    vslider = ctk.CTkSlider(main, from_=0, to=100, orientation='vertical', width=25, height=610, command=vmove)
    vslider.set(vs)
    vslider.place(relx=0.98, rely=0.335, anchor="e")
    song_progress_label = ctk.CTkLabel(main, text="0:00", font=("Arial", 50, "bold"))
    song_progress_label.place(relx=0.5, rely=0.6, anchor="center")
    song_progress_slider = ctk.CTkSlider(main, from_=0, to=0, orientation='horizontal', width=1800, height=30, command=lambda x: update_song_progress(song_progress_slider.get() * 1000))
    song_progress_slider.bind("<ButtonRelease-1>", lambda event: set_song_length())
    song_progress_slider.bind("<ButtonPress-1>", on_slider_press)
    song_progress_slider.bind("<ButtonRelease-1>", on_slider_release)
    song_progress_slider.place(relx=0.5, rely=0.67, anchor="center")
    npp=ctk.CTkFrame(main)
    otf=ctk.CTkFrame(main)
    playlist_icon = ctk.CTkImage(Image.open(mfl+"icons/playlist.png"), size=(90,90))
    equalizer_icon = ctk.CTkImage(Image.open(mfl+"icons/equalizer.png"), size=(20,20))
    shuffle_icon = ctk.CTkImage(Image.open(mfl+"icons/shuffle.png"), size=(90,90))
    repeat_icon = ctk.CTkImage(Image.open(mfl+"icons/repeat.png"), size=(90,90))
    repeat_icon1 = ctk.CTkImage(Image.open(mfl+"icons/repeat1.png"), size=(90,90))
    video_icon = ctk.CTkImage(Image.open(mfl+"icons/video.png"), size=(90,90))
    pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(90,90))
    previous_icon = ctk.CTkImage(Image.open(mfl+"icons/previous.png"), size=(90,90))
    next_icon = ctk.CTkImage(Image.open(mfl+"icons/next.png"), size=(90,90))
    minimize_icon = ctk.CTkImage(Image.open(mfl+"icons/minimize.png"), size=(20, 20))
    close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(15, 15))
    restore_icon = ctk.CTkImage(Image.open(mfl+"icons/restore.png"), size=(20, 20))
    music_icon = ctk.CTkImage(Image.open(mfl+"icons/logo.png"), size=(25, 25))
    mood_icon=ctk.CTkImage(Image.open(mfl+"icons/mood.png"), size=(90, 90))
    logo = ctk.CTkLabel(main, image=music_icon,width=1,text="")
    logo.place(relx=0.01,rely=0.01)
    toolbar = ctk.CTkFrame(main, bg_color=bgcc,fg_color=bgcc)
    equalizer_button = ctk.CTkButton(toolbar, image=equalizer_icon, command=lambda:ew(None),text="",width=1)
    equalizer_button.pack(side="left",padx=2,pady=2)
    minimize_button = ctk.CTkButton(toolbar, image=minimize_icon, command=sw,text="",width=1)
    minimize_button.pack(side="left", padx=2, pady=2)
    restore_button = ctk.CTkButton(toolbar, image=restore_icon, command=restart1,text="",width=1)
    restore_button.pack(side="left", padx=2, pady=2)
    close_button = ctk.CTkButton(toolbar, image=close_icon, command=ee,text="",width=1)
    close_button.pack(side="left", padx=2, pady=2)
    toolbar.place(relx=0.92)
    pre = ctk.CTkButton(npp, image=previous_icon, command=lambda: previous(None),text="",width=1)
    pp = ctk.CTkButton(npp, image=pause_icon, command=lambda: ppl(None),text="",width=1)
    next = ctk.CTkButton(npp, image=next_icon, command=lambda: nextxx(None),text="",width=1)
    pre.pack(side="left",padx=270)
    pp.pack(side="left",padx=270)
    next.pack(side="left",padx=270)
    npp.place(rely=0.74)
    shuffle_button = ctk.CTkButton(otf, image=shuffle_icon, command=lambda:shuffle(None),text="",width=1)
    repeat_button = ctk.CTkButton(otf, image=repeat_icon, command=lambda:repeat(None),text="",width=1)
    if repeat_song==True:
        repeat_button.configure(image=repeat_icon1)
    fullscreen_button = ctk.CTkButton(otf, image=video_icon,command=lambda:play_video(None),text="",width=1)
    playlist_button = ctk.CTkButton(otf, image=playlist_icon,command=lambda:pb(None),text="",width=1)
    mood_button = ctk.CTkButton(otf, image=mood_icon,command=lambda:mw(None),text="",width=1)
    playlist_button.pack(side="left",padx=128)
    fullscreen_button.pack(side="left",padx=150)
    repeat_button.pack(side="left",padx=150)
    shuffle_button.pack(side="left",padx=150)
    mood_button.pack(side="left",padx=150)
    otf.place(rely=0.87)
    main.bind('<Down>', lambda event: vmove(vs))
    main.bind('<Up>', lambda event: vmove(vs))
    main.bind('<Left>', previous)
    main.bind('<Alt_L>', previous)
    main.bind('<b>', previous)
    main.bind('<space>', ppl)
    main.bind('<Return>', ppl)
    main.bind('<n>', nextxx)
    main.bind('<Right>', nextxx)
    main.bind('<Alt_R>', nextxx)
    main.bind("<s>",lambda event:shuffle(None))
    main.bind("<r>",lambda event:repeat(None))
    main.bind("<e>",lambda event:ew(None))
    main.bind("<f>",lambda event:play_video(None))
    main.bind("<a>",lambda event:rewindr(None))
    main.bind("<d>",lambda event:fastff(None))
    main.bind("<p>",lambda event:pb(None)) 
    main.bind("<m>",lambda event:mw(None)) 
    main.focus_force()
    if open_window==True:
        pb(None)
        open_window=False
    if open_window1==True:
        ew(None)
        open_window1=False
    if open_window2==True:
        mw(None)
        open_window2=False
    set_song_length()
    main.mainloop()
def restart(): 
    global main,fscreen,small_window
    main.destroy()
    small_window=False
    if fscreen==True:
        fullscreen()
    if fscreen==False:
        mainstart()
def restart1():
    global main,fscreen,scheduler,pbs
    scheduler.shutdown(wait=False)
    scheduler=None
    fscreen=False
    main.destroy()
    mainstart()
def fastff(event):
    global vp
    vp.pause()
    currtime = vp.get_time()
    newtime = currtime + 10000
    vp.set_time(newtime) 
    vp.play()
def rewindr(event):
    global vp
    vp.pause()
    currtime = vp.get_time()
    newtime = currtime - 10000
    vp.set_time(newtime)
    vp.play()
def update_song_name():
    global song_name_label,fscreen,small_window,np,song_name
    song_name = np[:-5]
    if small_window==False:
        if  fscreen==False:
            if len(song_name)>=17:
                song_name_label.configure(text=song_name,font=("Arial", 25, "bold"))
            else:
                song_name_label.configure(text=song_name,font=("Arial", 40, "bold"))
        else:
            if len(song_name)>=17:
                song_name_label.configure(text=song_name,font=("Arial", 60, "bold"))
            else:
                song_name_label.configure(text=song_name,font=("Arial", 120, "bold"))
def ppl(event):
    global pp,pause_icon,play_icon, video_playback,small_window,vp
    if  fscreen==False:
        play_icon = ctk.CTkImage(Image.open(mfl+"icons/play.png"), size=(40, 40))
        pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(40, 40))
    else:
        play_icon = ctk.CTkImage(Image.open(mfl+"icons/play.png"), size=(90, 90))
        pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(90, 90))
    status=vp.get_state()
    if status == vlc.State.Playing:
        vp.pause()
        if small_window==False:    
            pp.configure(image=play_icon)
    elif status ==vlc.State.Paused:
        vp.play()
        if small_window==False:
            pp.configure(image=pause_icon)
        if video_playback==True:
            play_video(None)
def handle_next():
    global n,pf,pforg,queue_playing,open_window,shuffled,queue_buttons,queue_order,repeat_song
    if repeat_song==False:
        n += 1
    if n >= len(pf):
        n=0
        pf=list(range(0, len(pforg)))
        queue_order=[]
        shuffled=False
        refresh_window()
        queue_playing=False
    if queue_playing==True:
        if pf[n] in queue_order:
            queue_order.remove(pf[n])
def nextx(event):
    handle_next()
    play()
def nextxx(event):
    global vp
    vp.stop()
    handle_next()
    play()   
def previous(event):
    global n,pf,vp
    vp.stop()
    n -= 1
    if n < 0:
        n = len(pforg) - 1
    play()
def play():
    global n,pf,vp,ptop,ff,video_playback,pp,vlc_instance,np,repeat_song,csg,pforg
    vlc_args = "--no-xlib --no-video"
    vlc_instance = vlc.Instance(vlc_args.split())
    vp = vlc_instance.media_player_new()
    if repeat_song==True:
        np=pforg[csg]
    else:
        np=pforg[pf[n]]
    if open_window==True or pbs==True:
        update_song_color()
    ff = os.path.join(ptop, np)
    media = vlc_instance.media_new(ff)
    media.add_option("no-video") 
    vp.set_media(media)
    update_song_name()
    vp.audio_set_volume(vs)
    vp.play()
    if small_window==False:
        if  fscreen==False:
            pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(40, 40))
        else:
            pause_icon = ctk.CTkImage(Image.open(mfl+"icons/pause.png"), size=(90, 90))
        pp.configure(image=pause_icon)
        set_song_length()
    if video_playback==True:
        play_video()
    vp.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, nextx)
def vmove(val):
    global vs,vp,vslider
    vs = int(val)
    vp.audio_set_volume(vs)
    vslider.set(vs)
is_dragging = False
def on_slider_press(event):
    global is_dragging
    is_dragging = True
def on_slider_release(event):
    global is_dragging
    is_dragging = False
    on_slider_move(event)
def on_slider_move(event):
    current_time = int(song_progress_slider.get())
    minutes = current_time // 60
    seconds = current_time % 60
    timeobj = datetime.time(minute=minutes, second=seconds)
    timestr = timeobj.strftime('%M:%S')
    song_progress_label.configure(text=str(timestr)+"/"+str(time_str))
    vp.set_time(current_time * 1000)
def update_song_progress(val):
    global vp,song_length,is_dragging,current_time,song_progress_slider,small_window
    if small_window==False and not is_dragging:
        status = vp.get_state()
        if status == vlc.State.Playing:
            current_time = vp.get_time() // 1000
            if current_time<=0:
                current_time=0
            minutes=current_time//60
            seconds=current_time%60
            timeobj = datetime.time(minute=minutes, second=seconds)
            timestr = timeobj.strftime('%M:%S')
            song_progress_label.configure(text=str(timestr)+"/"+str(time_str))
            song_progress_slider.set(current_time)
def set_song_length():
    global vp,time_str,songlength,scheduler
    time.sleep(0.2)
    songlength = int(vp.get_length()) // 1000
    if songlength==-1:
        songlength=0
    minutes=songlength//60
    seconds=songlength%60
    time_obj = datetime.time(minute=minutes, second=seconds)
    time_str = time_obj.strftime('%M:%S')
    song_progress_slider.configure(to=songlength)
    timestr="00:00"
    song_progress_label.configure(text=str(timestr)+"/"+str(time_str))
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_song_progress,'interval', seconds=1, args=['value'],max_instances=150)
        scheduler.start()
def destroy_equalizer():
    global equalizer_window,open_window1
    equalizer_window.destroy()
    open_window1=False
def open_equalizer_window(event):
    global main,open_window1,equalizer_window,edit,equalizer_window_x,equalizer_window_y
    if open_window1==False:
        open_window1=True
        equalizer_window = ctk.CTkToplevel( )
        equalizer_window.title("Equalizer")
        equalizer_window.geometry(f"340x590+{equalizer_window_x}+{equalizer_window_y}")
        equalizer_window.overrideredirect(True)
        equalizer_label=ctk.CTkLabel(equalizer_window,text="Equalizer", font=("Arial", 16, "bold"))
        equalizer_label.place(relx=0.05,rely=0.008)
        close_icon = ctk.CTkImage(Image.open(mfl+"icons/close.png"), size=(13, 13))
        close_button = ctk.CTkButton(equalizer_window, image=close_icon, command=destroy_equalizer,text="",width=1)
        close_button.place(relx=0.9,rely=0.008)
        equalizer_frame=ctk.CTkFrame(equalizer_window)
        preamp_label = ctk.CTkLabel(equalizer_frame, text="Preamp", font=("Arial", 16, "bold"))
        preamp_label.pack()
        preamp_scale = ctk.CTkSlider(equalizer_frame, from_=-20, to=20, orientation='horizontal',command=update_preamp,height=20,width=300)
        preamp_scale.set(vlc.libvlc_audio_equalizer_get_preamp(equalizer))
        preamp_scale.pack()
        band_scales = []
        band_frequencies = [60, 170, 310, 600, 1000, 3000, 6000, 12000, 14000, 16000]
        for i in range(10):
            freq = band_frequencies[i]
            freq_label = ctk.CTkLabel(equalizer_frame, text=f'{freq} Hz', font=("Arial", 16, "bold"))
            freq_label.pack()
            scale = ctk.CTkSlider(equalizer_frame, from_=-20, to=20, orientation='horizontal',command=lambda val, i=i: update_band(i, val),height=20,width=300)
            scale.set(vlc.libvlc_audio_equalizer_get_amp_at_index(equalizer, i))
            scale.pack()
            band_scales.append(scale)
        equalizer_frame.pack(pady=30)
        equalizer_window.bind('<Down>', lambda event: vmove(vs))
        equalizer_window.bind('<Up>', lambda event: vmove(vs))
        equalizer_window.bind('<Left>', previous)
        equalizer_window.bind('<Alt_L>', previous)
        equalizer_window.bind('<b>', previous)
        equalizer_window.bind('<space>', ppl)
        equalizer_window.bind('<Return>', ppl)
        equalizer_window.bind('<n>', nextxx)
        equalizer_window.bind('<Right>', nextxx)
        equalizer_window.bind('<Alt_R>', nextxx)
        equalizer_window.bind("<s>",lambda event:shuffle(None))
        equalizer_window.bind("<r>",lambda event:repeat(None))
        equalizer_window.bind("<e>",lambda event:open_equalizer_window(None))
        equalizer_window.bind("<f>",lambda event:play_video(None))
        equalizer_window.bind("<a>",lambda event:rewindr(None))
        equalizer_window.bind("<d>",lambda event:fastff(None))
        equalizer_window.bind("<p>",lambda event:open_playlist_window(None)) 
        equalizer_window.bind("<m>",lambda event:open_mood_window(None)) 
        equalizer_window.bind("<z>",lambda event:open_debug_window(None)) 
        if edit==True:
            equalizer_window.bind("<B1-Motion>", lambda event, window=equalizer_window: on_drag_motion(event, window))
            equalizer_window.bind("<ButtonPress-1>", lambda event, window=equalizer_window: on_drag_start(event, window))
    else:
        destroy_equalizer()
        open_window1=False
def update_preamp(val):
    vlc.libvlc_audio_equalizer_set_preamp(equalizer, float(val))
    vp.set_equalizer(equalizer)
def update_band(index, val):
    vlc.libvlc_audio_equalizer_set_amp_at_index(equalizer, float(val), index)
    vp.set_equalizer(equalizer)
def shuffle(event):
    global pf,cunt,np,pforg,n,queue_order,shuffled,queue_playing,queue_order
    shuffled=True
    if queue_playing==False:
        pf.remove(n)
        random.shuffle(pf)
        pf.insert(n,n)
    else:
        queue_order=[]
        queue_playing=False
        random.shuffle(pf)
        for no in pforg:
            if pforg.index(no) not in pf:
                pf.append(pforg.index(no))
    for i in range(0,len(pf)):
        change_element(i)
    return pf
def refresh_window():
    global open_window
    if open_window==True:
        on_playlist_window_close()
        open_window=False
        open_playlist_window(None)
    if pbs==True:
        pb(None)
        time.sleep(0.1)
        pb(None)
def ee():
    global vp,main,scheduler,open_window3
    vp.stop()
    if open_window1==True:
        destroy_equalizer()
    if open_window==True:
        on_playlist_window_close()
    if open_window3==True:
        on_debug_window_close()
    scheduler.shutdown(wait=False)
    main.destroy()
    os._exit(0)
def repeat(event):
    global cunt,pf,n,repeat_song,repeat_button
    cunt+=1
    if fscreen==False:
        repeat_icon = ctk.CTkImage(Image.open(mfl+"icons/repeat.png"), size=(30, 30))
        repeat_icon1 = ctk.CTkImage(Image.open(mfl+"icons/repeat1.png"), size=(30, 30))
    else:
        repeat_icon = ctk.CTkImage(Image.open(mfl+"icons/repeat.png"), size=(90,90))
        repeat_icon1 = ctk.CTkImage(Image.open(mfl+"icons/repeat1.png"), size=(90,90))
    if cunt%2!=0:
        repeat_song=True
        repeat_button.configure(image=repeat_icon1)
    elif cunt%2==0:
        repeat_song=False
        repeat_button.configure(image=repeat_icon)
start()