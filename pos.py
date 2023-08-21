from tkinter import *
from tkinter import ttk
from windowclass import Addproduct, ButtonHomepage
from posdb import *
from bill import Bill

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

#################CHECK OUT###################

FCheckout = Frame(GUI)
FCheckout.place(x=1200,y=880)

def checkout(event=None):
    GUI2 = Toplevel() #
    GUI2.title('หน้าสรุปยอดเงิน')

    W = 1000
    H = 700
    MW = GUI.winfo_screenwidth()
    MH = GUI.winfo_screenheight()
    # print(MW,MH) # current screen width,height
    SX = (MW/2) - (W/2)
    SY = (MH/2) - (H/2)
    GUI2.geometry('{}x{}+{:.0f}+{:.0f}'.format(W,H,SX,SY))


    t = total

    v1 = StringVar()
    v1.set('รวมยอดทั้งหมด: {:,.2f} บาท'.format(t))
    v2 = StringVar()
    v3 = StringVar()
    v3.set('ทอน: - บาท')

    T1 = ttk.Label(GUI2,textvariable=v1,font=(None,30))
    T1.place(x=50,y=50)

    T2 = ttk.Label(GUI2,text='รับเงิน:',font=(None,30))
    T2.place(x=50,y=150)
    ET2 = ttk.Entry(GUI2,textvariable=v2,font=(None,30),width=5)
    ET2.place(x=200,y=150)

    def calculate(sv):
        cal = float(v2.get()) - total
        # print('CHECK',v2.get())
        v3.set('ทอน: {:,.2f} บาท'.format(cal))

    v2.trace("w", lambda name, index, mode, sv=v2: calculate(sv))
    T3 = ttk.Label(GUI2,textvariable=v3,font=(None,30))
    T3.place(x=50,y=250)

    FB = Frame(GUI2)
    FB.place(x=300,y=550)

    def Save():
        reportlist = []
        for p in table_product.values():
            d = [p[-1],p[-3],p[-2]]
            reportlist.append(d)
        Bill(reportlist)

    BS = ttk.Button(FB,text='บันทึก',command=Save)
    BS.pack(ipadx=20,ipady=10)

    FBanknote = Frame(GUI2)
    FBanknote.place(x=30,y=340)

    global money_get
    money_get = 0
    def add(v):
        global money_get
        money_get += v
        v2.set(money_get)

    img1 = PhotoImage(file='b20.png')
    img2 = PhotoImage(file='b50.png')
    img3 = PhotoImage(file='b100.png')
    img4 = PhotoImage(file='b500.png')
    img5 = PhotoImage(file='b1000.png')
    B20 = ttk.Button(FBanknote,image=img1,command=lambda x=20: add(x)).grid(row=0,column=0,ipady=15,)
    B50 = ttk.Button(FBanknote,image=img2,command=lambda x=50: add(x)).grid(row=0,column=1,ipady=15)
    B100 = ttk.Button(FBanknote,image=img3,command=lambda x=100: add(x)).grid(row=0,column=2,ipady=15)
    B500 = ttk.Button(FBanknote,image=img4,command=lambda x=500: add(x)).grid(row=0,column=3,ipady=15)
    B1000 = ttk.Button(FBanknote,image=img5,command=lambda x=1000: add(x)).grid(row=0,column=4,ipady=15)



    GUI2.mainloop()

BCheckout = ttk.Button(FCheckout,text='Checkout',command=checkout)
BCheckout.pack(ipadx=20,ipady=10)




















GUI.bind('<F12>',reset)
GUI.mainloop()