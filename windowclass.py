from tkinter import *
from tkinter import ttk,messagebox
from posdb import *

class Addproduct:

    def __init__(self):
        self.info = 'เพิ่มสินค้า'
        self.currentid = 0
        self.state = 'save'  # save, update

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

            if self.state == 'save':
                insert_product(barcode,title,float(price),float(quantity))
                #messagebox.showinfo('Done!','บันทึกสำเร็จแล้ว')
            else:
                update_product(self.currentid,'barcode',v_barcode.get())
                update_product(self.currentid,'title',v_title.get())
                update_product(self.currentid,'price',float(v_price.get()))
                update_product(self.currentid,'quantity',float(v_quantity.get()))
                # after update
                self.state = 'save'
                B_save.configure(text='save')
                B_reset.pack_forget()
            
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


        def delete(event):
            #PGUI.attributes('-topmost',True)
            # self.gui.lower(PGUI)
            
            check = messagebox.askyesno('ลบสินค้า','คุณต้องการลบสินค้าชิ้นนี้ใช่หรือไม่?')
            if check == True:
                print('CHECK:',check)
                select = table.selection()
                data = table.item(select)['values']
                print(data)
                delete_product(data[0])
                update_table()
            
            PGUI.focus_force()
            
        table.bind('<Delete>',delete)

        def clickupdate(event):
            select = table.selection() 
            data = table.item(select)['values'] # [1, 1002, 'พ่อรวยสอนลูก', '200.0', '3.0']
            print(data)
            self.currentid = data[0]
            v_barcode.set(data[1])
            v_title.set(data[2])
            v_price.set(data[3])
            v_quantity.set(data[4])
            self.state = 'update'
            B_save.configure(text='update')
            B_reset.pack()

        
        def reset():
            v_barcode.set('')
            v_title.set('')
            v_price.set('10')
            v_quantity.set('1')
            self.state = 'save'
            B_save.configure(text='save')
            B_reset.pack_forget()
            
        B_reset = ttk.Button(F1,text='reset',command=reset)
        B_reset.pack()
        B_reset.pack_forget()


        table.bind('<Double-1>',clickupdate)

        update_table()
        #PGUI.attributes('-topmost',True)
        #PGUI.overrideredirect(True) # clear  title bar
        PGUI.mainloop()