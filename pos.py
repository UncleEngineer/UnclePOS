from tkinter import *
from tkinter import ttk
from windowclass import Addproduct
from posdb import *

GUI = Tk()
GUI.title('โปรแกรม POS')
GUI.geometry('700x600')
########CLASS########
addproduct = Addproduct()

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

table_product = {}

def update_table():
    data = table_product.values()
    table.delete(*table.get_children()) #clear table
    for d in  data:
        table.insert('','end',values=d)

def search():
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

Bsearch = ttk.Button(Fsearch,text='Search',command=search)
Bsearch.grid(row=0,column=1,padx=20,ipadx=20,ipady=10)


GUI.mainloop()