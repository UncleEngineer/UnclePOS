from tkinter import *
from tkinter import ttk,messagebox
from posdb import *

class Addproduct:

    def __init__(self):
        self.info = 'เพิ่มสินค้า'

    def popup(self):
        PGUI = Toplevel()
        PGUI.title('เพิ่มรายการสินค้า')
        PGUI.geometry('1000x600')
        FONT = (None,15)
        L = ttk.Label(PGUI,text='เพิ่มรายการสินค้า',font=FONT)
        L.pack(pady=20)

        v_barcode = StringVar()
        v_title = StringVar()
        v_price = StringVar()
        v_price.set('10')
        v_quantity = StringVar()
        v_quantity.set('1')

        F1 = Frame(PGUI)
        F1.place(x=600,y=50)

        L = ttk.Label(F1,text='Barcode',font=FONT).pack()
        E1 = ttk.Entry(F1,textvariable=v_barcode,font=FONT)
        E1.pack(pady=10)
        E1.focus()

        L = ttk.Label(F1,text='ชื่อสินค้า',font=FONT).pack()
        E2 = ttk.Entry(F1,textvariable=v_title,font=FONT)
        E2.pack(pady=10)

        L = ttk.Label(F1,text='ราคา',font=FONT).pack()
        E3 = ttk.Entry(F1,textvariable=v_price,font=FONT)
        E3.pack(pady=10)

        L = ttk.Label(F1,text='จำนวน',font=FONT).pack()
        E4 = ttk.Entry(F1,textvariable=v_quantity,font=FONT)
        E4.pack(pady=10)

        def save():
            barcode = v_barcode.get()
            title = v_title.get()
            price = v_price.get()
            quantity = v_quantity.get()

            insert_product(barcode,title,float(price),float(quantity))
            messagebox.showinfo('Done!','บันทึกสำเร็จแล้ว')
            PGUI.focus_force() #กลับไปเลือกหน้าเดิม
            v_barcode.set('')
            v_title.set('')
            v_price.set('10')
            v_quantity.set('1')
            update_table()


        B_save = ttk.Button(F1,text='save',command=save)
        B_save.pack()

        F2 = Frame(PGUI)
        F2.place(x=20,y=100)

        header = ['ID','Barcode','ชื่อสินค้า','ราคา','จำนวน']
        hwidth = [50,100,150,50,50]

        table = ttk.Treeview(F2, columns=header, show='headings', height=20)
        table.pack()

        # style = ttk.Style()
        # style.configure('Treeview.Heading',font=(None,15))
        # style.configure('Treeview',font=(None,13),rowheight=30)

        # table.column('ค่าใช้จ่าย',anchor=E)
        # table.column('รายการ',anchor=CENTER)

        for h,w in zip(header,hwidth):
            table.column(h,width=w)
            table.heading(h,text=h)


        def update_table():
            data = table_add_product()
            table.delete(*table.get_children()) #clear table
            for d in  data:
                table.insert('','end',values=d)

        update_table()

        PGUI.mainloop()