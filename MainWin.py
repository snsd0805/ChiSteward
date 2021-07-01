from tkinter import * 

def createMainWin():
    '''
    用綠色校園作為基底色
    以暨大的三大特色
    1.穿山甲-moodle
    2.櫻花-暨大官網 #ffcccc
    3.國際性-教務系統
    去做三個網頁的底色
    '''
    win=Tk()
    win.configure(bg="#b2ffa6")


    createMoodleWin=Button(win,text="Moodle",font="Helvetica 30",bg="#888084",fg="white",relief=GROOVE)
    createNcnuMainWin=Button(win,text="暨大官網",font="Helvetica 30",bg="#ffcccc",fg="white",relief=GROOVE)
    createNcnuWin=Button(win,text="暨大教務系統",font="Helvetica 30",bg="#df99ff",fg="white",relief=GROOVE)
    
    
    createMoodleWin.pack(fill="x")
    createNcnuMainWin.pack(fill="x")
    createNcnuWin.pack(fill="x")

    win.mainloop()

createMainWin()
