from api.eventRigestry import EventRegistry
from config import CONFIG
from tkinter import *
from tkhtmlview import HTMLLabel

class textBox():
    def __init__(self, root, key, value, Stype):
        self.key = key
        self.value = value
        self.type = Stype
        self.frame = Frame(root)
        self.label = Label(self.frame, text=key)
        self.entry = Entry(self.frame)
        self.entry.insert(0, value)

        if Stype==False:
            self.entry.config(state='disabled')
    
    def pack(self):
        self.label.pack(side=LEFT)
        self.entry.pack(side=RIGHT)
        self.frame.pack()
        

def createRigestryWin():
    
    root=Tk()
    frame1=Frame(root)
    frame2=Frame(root)
    frame1.pack(side=LEFT)
    frame2.pack()
    winScrollBar=Scrollbar(frame1)
    htmlLb=HTMLLabel(frame1,html="")
    
    
    winScrollBar.pack(side=RIGHT,fill="y")
    htmlLb.pack(fill=BOTH)
    htmlLb.configure(yscrollcommand=winScrollBar.set)

    ht='''<span style="background-color:#ffcccc"><h5>讀取中</h5></span>'''  
    htmlLb.set_html(ht)
    root.update()
    html=''''''
        
    root.update()
    
    
    rigestry=EventRegistry(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
    tmpid=[]
    tmpname=[]
    events = rigestry.getEventsList()
    if rigestry.status:
        for i in events:
            html+='''<tr> <td>活動ID:{}</td> <td>學期{}</td> <br> <td>活動報名狀態:{}</td> <br> <td>活動名稱:{}</td> <br> <td>活動開始時間: {}</td> <br> <td>報名方式:{}</td> <br> <td>時數: {}</td> <br><td>講師: {}</td> <br> <td>申請為教師之能活動: {}</td> </tr><p> '''.format(
            i.get("id"),i.get("semester"),i.get("status"),i.get("name"),i.get("time"),i.get("method"),i.get("hour"),i.get("speaker"),i.get("teacherEvevt") )
            tmpid.append(i.get("id"))
            tmpname.append(i.get("name"))    
        htmlLb.set_html(html)
    else:
        print("NO")

    def signUpWin(event):
        win=Tk()
        data = rigestry.signUpPrepare(event.get('id'))
        
        idBox = textBox(win, "學號：", data['x_applicantID'], False)
        idBox.pack()

        nameBox = textBox(win, "姓名：", data['x_applicantName'], False)
        nameBox.pack()

        departmentBox = textBox(win, "科系：", data['x_applicantUabbrname'], False)
        departmentBox.pack()

        authBox = textBox(win, "身份：", data['x_applicantTitle'], False)
        authBox.pack()

        iphoneBox = textBox(win, "分機：", data['x_iphone'], True)
        iphoneBox.pack()

        phoneBox = textBox(win, "電話：", data['x_phone'], True)
        phoneBox.pack()

        mailBox = textBox(win, "mail：", data['x_zemail'], True)
        mailBox.pack()

        markBox = textBox(win, "備註：", data['x_remark'], True)
        markBox.pack()

        submit = Button(win, text="報名")
        submit.pack()
            
        win.mainloop()
        

    for i in events:
        if i.get('status') == "B, 開放公告":
            Button(frame2,text="我要報名  {}".format(i.get('name')),command=lambda:signUpWin(i) ).pack(anchor="w")
        
    root.update()        

    root.mainloop()

