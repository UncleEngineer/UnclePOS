import sqlite3

conn = sqlite3.connect('posdb.sqlite3')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS product (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            title TEXT,
            price REAL,
            quantity REAL,
            other TEXT
            ) """)


def insert_product(barcode,title,price,quantity,other=None):
    with conn:
        command = 'INSERT INTO product VALUES (?,?,?,?,?,?)'
        c.execute(command,(None,barcode,title,price,quantity,other))
    conn.commit() #save

def view_product():
    with conn:
        command = 'SELECT * FROM product'
        c.execute(command)
        result = c.fetchall()
        print(result)
    return result

def table_add_product():
    with conn:
        command = 'SELECT ID,barcode,title,price,quantity FROM product'
        c.execute(command)
        result = c.fetchall()
        #print(result)
    return result

def search_single(barcode):
    with conn:
        command = 'SELECT ID,barcode,title,price FROM product WHERE barcode=(?)'
        c.execute(command,([barcode]))
        result = c.fetchone()
        if result != None:
            result = list(result)
            result.append(1) #เพิ่มจำนวน 1 รายการเข้าไป
    return result

def delete_product(ID):
    with conn:
        command = 'DELETE FROM product WHERE ID=(?)'
        c.execute(command,([ID]))
    conn.commit()

def update_product(ID,field,data):
    with conn:
        command = 'UPDATE product SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,([data,ID]))
    conn.commit()


# s = search_single('1002')
# print(s)

#insert_product('1001','พ่อรวยสอนลูก',150,3)
#delete_product(8)
# update_product(1,'barcode','1002')
# update_product(1,'price',200)
#view_product()

# table_add_product()