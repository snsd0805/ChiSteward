from tkinter import *

c=[{'id': '47552', 'name': '1092-210021 組合數學 '}, {'id': '47553', 'name': '1092-210022 資料結構與演算法(二) '}, {'id': '47555', 'name': '1092-210026 線性代數 '}, {'id': '47562', 'name': '1092-210111 機率 '}, {'id': '47620', 'name': '1092-219152 Python網頁擷取程式設計 '}, {'id': '48261', 'name': '1092-902044h 體育:高爾夫球 '}, {'id': '48275', 'name': '1092-902047c 體育:網球 '}, {'id': '48477', 'name': '1092-985216 資工系服務學習(下) '}, {'id': '48604', 'name': '1092-994003 綠色能源 '}, {'id': '48606', 'name': '1092-994010 東南亞教育制度 '}]

def itemSelected(event):
    obj = event.widget
    index = obj.curselection()
    
def getIdAndName(course):
    coursesId=[]
    courseName=[]
    for i in course:
        coursesId.append(i.get("id"))
        tmp=i.get("name").split(" ")
        courseName.append(tmp[1])
    return coursesId ,courseName   

def createMoodleWin(courses,upComingEvent):
    win=Tk()

    leftFrame=Frame(win)
    rightFrame=Frame(win,bg="red")
    leftFrame.pack(fill=BOTH)
    rightFrame.pack(fill=BOTH)
    

    coursesId,coursesName=getIdAndName(c)

    #=====leftframe 1.button ->show UpComingEvent 2.choose courses=======
    upComingEventBtn=Button(leftFrame,text="未來事件",font="Helvetica 20")
    coursesListBox=Listbox(leftFrame)
    mylb=Label(leftFrame,text="我的課程",font="Helvetica 15")

    coursesListBox.insert(END,*coursesName)
    upComingEventBtn.pack(fill=BOTH,pady=10)
    mylb.pack(fill=X)
    coursesListBox.pack(fill=BOTH)

    #=======rightframe show everything======


    win.mainloop()

createMoodleWin(1,1)
