from tkinter import *
from tkinter import ttk
from windowclass import Addproduct
from posdb import *

GUI = Tk()
GUI.title('โปรแกรม POS')
GUI.geometry('800x600')
########CLASS########
addproduct = Addproduct()
# addproduct.gui = GUI

B_addproduct = ttk.Button(GUI,text='+',command=addproduct.popup,width=3)
B_addproduct.place(x=650,y=20)

########TABLE##########
FTABLE = Frame(GUI)
FTABLE.place(x=20,y=100)

header = ['ID','Barcode','ชื่อสินค้า','ราคา','จำนวน']
hwidth = [50,100,150,50,50]

table = ttk.Treeview(FTABLE, columns=header, show='headings', height=20)
table.pack()

# style = ttk.Style()
# style.configure('Treeview.Heading',font=(None,15))
# style.configure('Treeview',font=(None,13),rowheight=30)

# table.column('ค่าใช้จ่าย',anchor=E)
# table.column('รายการ',anchor=CENTER)

for h,w in zip(header,hwidth):
    table.column(h,width=w)
    table.heading(h,text=h)

#########SEARCH##########
Fsearch = Frame(GUI)
Fsearch.place(x=50,y=40)

v_search = StringVar()
Esearch = ttk.Entry(Fsearch,textvariable=v_search,font=(None,20))
Esearch.grid(row=0,column=0)

table_product = {} #เก็บข้อมูลชั่วคราวในการซื้อขาย ณ ปัจจุบัน
total = 0

def update_table():
    data = table_product.values()
    table.delete(*table.get_children()) #clear table
    for d in  data:
        table.insert('','end',values=d)

def search(event=None):
    global total # เพื่อให้ total ในฟังชั่นนี้ไปแทนที่ total นอกฟังชั่น 
    barcode = v_search.get()
    d = search_single(barcode) # [2, '1002', 'ฟิสิกส์ 1', 100.0, 1]
    if d != None:
        bc = d[1] #barcode
        if bc not in table_product:
            table_product[bc] = d
            #table.insert('','end',values=d)
            update_table()
        else:
            table_product[bc][-1] = table_product[bc][-1] + 1
            update_table()
    # clear barcode
    v_search.set('')
    print('---------')
    print(table_product)
    total = sum([ t[3] * t[4] for t in table_product.values()])
    v_total.set('{:,.2f}'.format(total))


Bsearch = ttk.Button(Fsearch,text='Search',command=search)
Bsearch.grid(row=0,column=1,padx=20,ipadx=20,ipady=10)

Esearch.bind('<Return>',search)
Esearch.focus() #set cursur at search box 

# TOTAL TEXT
L = ttk.Label(GUI,text='Total: ',font=(None,25),justify=RIGHT).place(x=450,y=400)
v_total = StringVar()
v_total.set('0.0')

LTotal = ttk.Label(GUI,textvariable=v_total,font=(None,35,'bold'),foreground='green')
LTotal.place(x=600,y=390)

# F1 = Frame(GUI)
# F1.place(x=300,y=300)
# L = ttk.Label(F1,text='ㅤㅤㅤ',font=(None,25),anchor='e',justify=RIGHT).grid(row=0,column=0)
# L = ttk.Label(F1,text='ㅤㅤㅤ',font=(None,25),anchor='e',justify=RIGHT).grid(row=0,column=1)
# L = ttk.Label(F1,text='Total: ',font=(None,25),anchor='e',justify=RIGHT).grid(row=1,column=0)
# LTotal = ttk.Label(F1,textvariable=v_total,font=(None,35,'bold'),foreground='green')
# LTotal.grid(row=1,column=1,sticky='E')

FReset = Frame(GUI)
FReset.place(x=450,y=480)
def reset(event=None):
    global table_product
    table_product = {}
    update_table()
    v_total.set('0.0')

BReset = ttk.Button(FReset,text='Reset',command=reset)
BReset.pack(ipadx=20,ipady=10)


GUI.bind('<F12>',reset)
GUI.mainloop()