from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm, inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime
import subprocess

def Bill(products):

    #set font
    pdfmetrics.registerFont(TTFont('F1','tahoma.ttf'))
    pdfmetrics.registerFont(TTFont('F2','tahoma.ttf'))

    #create canvas = whiteboard
    c = canvas.Canvas('product_bill.pdf')

    #papersize (WxH : 80x150 )
    PW = 80 # paper width

    count = len(products)
    diff = count * 5 # product * 5 mm per line
    PH = 80 + diff # paper height
    c.setPageSize( (PW * mm, PH * mm) )

    c.setFont('F1',15)
    c.drawCentredString(40 * mm, (PH - 10) * mm, 'ใบเสร็จรับเงิน')

    c.setFont('F2',18)
    c.drawCentredString(40 * mm, (PH - 20) * mm, 'ร้านของชำลุง')

    # products = [[3,'พ่อรวยสอนลูก',150],
    #            [1,'เขียนโปรแกรมไพทอน',100],
    #            [1,'คิดเลขเร็ว',1150],
    #            [3,'พ่อรวยสอนลูก',150],
    #            [1,'เขียนโปรแกรมไพทอน',100],
    #            [1,'คิดเลขเร็ว',1150]]
    
    c.setFont('F1',8)
    for i,p in enumerate(products):
        c.drawString(10 * mm, (PH - (40+(i*5))) * mm, '{:,.0f}'.format(p[0]))
        pname = '{}@{}'.format(p[1],p[2])
        c.drawString(20 * mm, (PH - (40+(i*5))) * mm, pname)
        c.drawRightString(70 * mm, (PH - (40+(i*5)))  * mm, '{:,.2f}'.format(p[0] * p[2]))

    total = sum([ p[0]* p[2] for p in products])
    c.drawCentredString(40 * mm, (PH - (50+(i*5))) * mm, 'Total')
    c.drawRightString(70 * mm, (PH - (50+(i*5)))  * mm, '{:,.2f}'.format(total))
    c.showPage()
    c.save()
    subprocess.Popen('product_bill.pdf',shell=True)




# products = [[3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150],
#                [3,'พ่อรวยสอนลูก',150],
#                [1,'เขียนโปรแกรมไพทอน',100],
#                [1,'คิดเลขเร็ว',1150]]

# Bill(products)