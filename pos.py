from tkinter import *
from tkinter import ttk
from windowclass import Addproduct, ButtonHomepage
from posdb import *

GUI = Tk()
GUI.title('โปรแกรม POS')
GUI.geometry('1200x800')
GUI.state('zoomed')
########CLASS########
addproduct = Addproduct()
# addproduct.gui = GUI

B_addproduct = ttk.Button(GUI,text='+',command=addproduct.popup,width=3)
B_addproduct.place(x=650,y=20)


##############CONFIGURATION###############

# treeview
style = ttk.Style()
style.configure('Treeview.Heading',font=(None,25))
style.configure('Treeview',font=(None,25),rowheight=40)

# button
Bfont = ttk.Style()
Bfont.configure('TButton',font=(None,15))

# home_products = {1:'ปากกา',
#                  2:'ยางลบ',
#                  3:'ดินสอ',
#                  4:'กบเหลา',
#                  5:'หมึกซึม',
#                  6:'สีน้ำ'} 



########TABLE##########

FTABLE = Frame(GUI)
FTABLE.place(x=20,y=100)

header = ['ID','Barcode','ชื่อสินค้า','ราคา','จำนวน']
hwidth = [100,200,300,100,100]

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
v_total = StringVar()
v_total.set('0.0')

# ฟังชั่นค้นหาที่ใช้คู่กับปุ่ม fav เท่านั้น
def search_button(barcode):
    global total # เพื่อให้ total ในฟังชั่นนี้ไปแทนที่ total นอกฟังชั่น 
    
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


home_products = home_products_button()
# home_products = {'1002': 'พ่อรวยสอนลูก', '1003': 'ไพทอนพื้นฐาน', '1005': 'หนังสือพิมพ์', '5555': 'ประวัตินักวิทย์', '7777': 'ไพทอน gui'}
buttonhomepage = ButtonHomepage(GUI,home_products,3,{'search':search_button})
buttonhomepage.place(x=1000,y=100)

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
L = ttk.Label(GUI,text='Total: ',font=(None,25),justify=RIGHT).place(x=980,y=800)


LTotal = ttk.Label(GUI,textvariable=v_total,font=(None,35,'bold'),foreground='green')
LTotal.place(x=1200,y=790)

# F1 = Frame(GUI)
# F1.place(x=300,y=300)
# L = ttk.Label(F1,text='ㅤㅤㅤ',font=(None,25),anchor='e',justify=RIGHT).grid(row=0,column=0)
# L = ttk.Label(F1,text='ㅤㅤㅤ',font=(None,25),anchor='e',justify=RIGHT).grid(row=0,column=1)
# L = ttk.Label(F1,text='Total: ',font=(None,25),anchor='e',justify=RIGHT).grid(row=1,column=0)
# LTotal = ttk.Label(F1,textvariable=v_total,font=(None,35,'bold'),foreground='green')
# LTotal.grid(row=1,column=1,sticky='E')

FReset = Frame(GUI)
FReset.place(x=1000,y=880)
def reset(event=None):
    global table_product
    table_product = {}
    update_table()
    v_total.set('0.0')

BReset = ttk.Button(FReset,text='Reset',command=reset)
BReset.pack(ipadx=20,ipady=10)



GUI.bind('<F12>',reset)
GUI.mainloop()