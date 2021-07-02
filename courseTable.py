import requests
import json
from tkinter import *
from api.courseTable.courseTable import *

url = 'https://raw.githubusercontent.com/snsd0805/NCNU_Course/master/%E6%AD%B7%E5%B9%B4%E8%AA%B2%E7%A8%8B%E8%B3%87%E6%96%99/1092_output.json'
response = requests.get(url)

data = json.loads(response.text)

class Choose():
    def __init__(self,root,name,typeS):
        self.frame=Frame(root)
        self.classname = Label(self.frame, font="10", width="10", text=name)
        self.listbox = Listbox(self.frame)
        self.scrollbar=Scrollbar(self.frame)
        self.checkBtn = Button(self.frame, text="選取")
        self.checkBtn.config(
            command=lambda: self.setDepartment() if self.type=="department" else self.setCourse()
        )
        self.type = typeS
    
    def setDepartment(self):
        # print("set department")
        # print(self.listbox.get(ACTIVE))
        self.update()
    
    def setCourse(self):
        # print("set course")
        # print(self.listbox.get(ACTIVE).split(' ')[0])
        courseTable.add(
            self.listbox.get(ACTIVE).split(' ')[0]
        )
        self.update()
    
    def update(self):
        courses = courseTable.courseFilter(box[0].listbox.get(ACTIVE))
        courses = ["{} {}({})".format(course['number'], course['name'], course['time']) for course in courses]
        box[1].listbox.delete(0, END)
        box[1].insert(courses)

        # update table draw
        for j in range(5):
            for i in range(13):
                if courseTable.table[str(j+1) + tmp[i]] != None:
                    table[18 + (13*j+i)].classname.config(text=
                        courseTable.table[str(j+1) + tmp[i]]['name']
                    )
                    table[18 + (13*j+i)].removeBtn.grid()

    def insert(self,LIST):
        self.listbox.insert(END,*LIST)

    def grid(self,Row,Column,span):
        self.listbox.selection_set(15)
        self.frame.grid(row=Row,column=Column,rowspan=span,padx=10,sticky="n"+"s")
        self.classname.pack()
        self.scrollbar.pack(fill=Y,side=RIGHT)        
        self.listbox.pack()
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.checkBtn.pack()          

class Space():
    def __init__(self, root, name=None):
        self.frame = Frame(root)
        self.classname = Label(self.frame, font="10", width="10", text=name)
        self.removeBtn = Button(self.frame, font="10", text="刪")
        self.classname.config(relief=RIDGE)

    def grid(self,Row,Column):
        if Row==5:
            self.classname.config(bg="green")
        self.frame.grid(row=Row,column=Column,padx=20)
        self.classname.grid(row=0,column=0)
        self.removeBtn.grid(row=0,column=1)
        self.removeBtn.grid_forget()
        
root = Tk()
root.geometry('800x600')

courseTable = CourseTable()

box=[]
box.append(Choose(root,name="科系",typeS='department'))
departments = courseTable.getDepartmentList()
box[0].insert(departments)
box[0].listbox.select_set(0)
box[0].grid(0,0,5)

box.append(Choose(root,name="課程",typeS='courses'))
courses = courseTable.courseFilter("21, 資工系")

box[1].insert(["{} {}({})".format(course['number'], course['name'], course['time']) for course in courses])
box[1].grid(5,0,5)


table = []
k=0

tmp=list("abcdzefghijklm")

for j in range(5):
    table.append(Label(root,text=j+1,font=("Curier New",20)))
    table[k].grid(row=0,column=j+3)
    k+=1

for i in range(13):
    table.append(Label(root,text=tmp[i]))
    table[k].grid(row=i+1,column=1)
    
    k+=1

table[9].config(bg="green")

# 18~
for j in range(5):
    for i in range(13):
        table.append(Space(root))
        table[k].grid(i+1,j+3)
        k+=1
print(len(table))
    
    

root.mainloop()