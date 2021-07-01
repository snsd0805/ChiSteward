from tkinter import *
from tkinter import ttk

def firstWin():
    first=Tk()
    first.geometry("600x400")
    first.minsize(400,400)
    first.maxsize(600,600)
    first.configure(background="skyblue")
    
    frame=Frame(first,bg="skyblue")
    go_to_loginwin_btn=Button(first,text="進入登入畫面",font="Helvetica 20",bg="yellow",command=lambda: [first.destroy(),loginwin()] )
    text_lb=Label(frame,text="歡迎來到暨管家",font=("Courier New Greek",40),bg="skyblue")
    photo = PhotoImage(file="100_100.gif")
    imgLabel =Label(frame,image=photo,bg="skyblue")
    
    frame.pack(expand=1)
    imgLabel.pack()
    text_lb.pack(padx=100)
    go_to_loginwin_btn.pack(pady=50)
    
    first.mainloop()

def loginwin():
    login=Tk()
    login.geometry("300x200")
    login.configure(bg="lightgreen")
    login.resizable(width=0,height=0)
    
    frame=Frame(login,width=100,height=100,bg="lightgreen")
    frame1=Frame(login,width=300,height=100,bg="lightgreen")
    frame2=Frame(login,width=300,height=100,bg="lightgreen")
    frame3=Frame(login,width=300,height=100,bg="lightgreen")

    prompt_lb=Label(frame,text="請輸入你的學號與密碼",font="Helvetica 20",bg="lightgreen")
    login_btn=Button(frame3,text="登入",command=lambda:print("1")) 
    enter_name=Entry(frame1,bd=3)
    enter_password=Entry(frame2,show="*",bd=3)
    name_lb=Label(frame1,text="學號",font="Helvetica 12",bg="lightgreen")
    pw_lb=Label(frame2,text="密碼",font="Helvetica 12",bg="lightgreen")
    show_password=Button( frame3,text="透視密碼")
    show_password.bind( '<Button-1>',lambda event:enter_password.config(show=""))
    show_password.bind( '<ButtonRelease-1>',lambda event : enter_password.config(show="*") )
    
    frame.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack() 
    prompt_lb.pack(pady=10,side="top")
    name_lb.pack(side="left")
    enter_name.pack(side="left")
    pw_lb.pack(side="left")
    enter_password.pack(side="left")
    show_password.pack(side="left",pady=10,padx=10)
    login_btn.pack(side="left",pady=10)

    login.mainloop()

firstWin()    

