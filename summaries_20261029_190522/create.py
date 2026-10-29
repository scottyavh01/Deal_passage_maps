from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
W,_=landscape(A3)
H=980  # taller sheet: more map area, with a fixed-size information banner
STYLE=sys.argv[1] if len(sys.argv)>1 else 'ocean'
if STYLE not in ('ocean','light'):
    raise ValueError('style must be ocean or light')
NAVY=HexColor('#102b3c'); TEAL=HexColor('#387989')
RIP_MODE=False

def text(c,x,y,s,size=9,bold=False,color=NAVY):
    s=re.sub(r'(?<=\d)\s+(?=(?:nm|h|m|kn|kts)\b)', '', s)
    scale=1.29 if y>H-82 else 1.18
    c.setFillColor(color); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size*scale)
    if RIP_MODE:
        c.drawString(x,y,s)
    else:
        c.drawString(x,y,s)

def panel(c,x,y,w,h,title):
    c.setFillColor(white); c.setStrokeColor(HexColor('#435f6a'))
    c.roundRect(x,y,w,h,3,fill=1,stroke=1)
    if STYLE=='ocean' and title:
        c.setFillColor(TEAL); c.rect(x+0.5,y+h-25,w-1,24.5,fill=1,stroke=0)
        color=white
    else:
        c.setStrokeColor(HexColor('#a8b9bc')); c.line(x,y+h-25,x+w,y+h-25)
        color=NAVY
    text(c,x+10,y+h-17,title,10,True,color)

def rows(c,x,top,data,step=18):
    for i,(d,s) in enumerate(data):
        text(c,x,top-i*step,d,11,True); text(c,x+62,top-i*step,s.replace('  ', '    '),11)

def rip_rows(c,x,top,data,step=17):
    for i,(day,line) in enumerate(data):
        y=top-i*step
        text(c,x,y,day,11,True)
        pairs=re.findall(r'(\d\d:\d\d) > (\d\d:\d\d(?:\+1d)?) ([+-][\d.]+)',line)
        for j,(slack,maximum,rate) in enumerate(pairs):
            left=x+62+j*137
            text(c,left,y,slack,11,True,HexColor('#08743c'))
            text(c,left+35,y,'>',11)
            text(c,left+47,y,maximum,11,True,HexColor('#b3261e'))
            text(c,left+47+(58 if '+1d' in maximum else 36),y,rate,10)

def create(name,img,title,subtitle,points):
    global H
    iw,ih=ImageReader(str(ROOT/img)).getSize()
    bottom=110 if name.startswith('part_1') else 0
    H=82+W*ih/iw+bottom
    c=canvas.Canvas(str(HERE/name),pagesize=(W,H))
    # Fit the entire image into the available map area without distortion.
    c.setFillColor(HexColor('#d8e9ea')); c.rect(0,0,W,H,fill=1,stroke=0)
    x,y,w,h=0,bottom,W,H-82-bottom
    c.setFillColor(HexColor('#d8e9ea')); c.rect(x,y,w,h,fill=1,stroke=0)
    c.drawImage(ImageReader(str(ROOT/img)),x,y,width=w,height=h,preserveAspectRatio=True,anchor='n')
    c.setFillColor(NAVY); c.rect(0,H-82,W,82,fill=1,stroke=0)
    c.setFillColor(HexColor('#c51e2f')); c.rect(900,H-82,W-900,82,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#6a8994')); c.setLineWidth(0.8)
    c.line(545,H-71,545,H-12); c.line(900,H-71,900,H-12)
    text(c,20,H-29,title,20,True,white); text(c,21,H-57,subtitle,11,True,white)
    text(c,565,H-21,'PASSAGE ESTIMATE',11,True,white)
    if name.startswith('part_1'):
        text(c,565,H-42,'190nm  |  5.5kn: 34h 33m  |  6kn: 31h 40m',11,True,white)
        text(c,565,H-63,'Arrival: 5.5kts: 17h33m / 6kts: 14h40m (1 Nov)',10,True,white)
    else:
        text(c,565,H-42,'65nm  |  5.5kn: 11h 49m  |  6kn: 10h 50m',11,True,white)
        text(c,565,H-63,'Arrival: 5.5kts: 17h36m / 6kts: 16h37m (6 Nov)',10,True,white)
    text(c,912,H-21,'COMMUNICATIONS',11,True,white)
    text(c,912,H-44,'VHF 16 distress / calling | 67 weather',12.2,True,white)
    if name.startswith('part_2'):
        text(c,912,H-65,'Port Welshpool Coast Guard: 0428 366 467',10,True,white)
    return c

c=create('part_1_st_kilda_deal.pdf','St_Kilda_to_Deal_with_passage.png','01  ST KILDA  >  DEAL ISLAND','Planned departure 31 OCT 2026, 07:00  |  Flight S1747',[])
c.saveState(); c.translate(0,110)
c.saveState(); c.translate(1164,368); c.scale(1.32,1.32); c.translate(-1164,-368)
panel(c,835,225,329,143,'DEAL ISLAND  |  GARDEN COVE HIGH / LOW')
text(c,848,326,'H = high   L = low',11,True)
rows(c,848,305,[('1 Nov','H 04:40  L 10:37  H 16:24  L 23:00'),('2 Nov','H 05:27  L 11:28  H 17:18  L 23:51'),('3 Nov','H 06:13  L 12:19  H 18:11'),('4 Nov','L 00:40  H 06:56  L 13:11  H 19:05')],20)
c.restoreState()
c.saveState(); c.translate(8,5+280*1.14-280*1.34); c.scale(1.20,1.34); c.translate(-25,-22)
c.saveState(); c.translate(0,-20)
RIP_MODE=True
panel(c,25,42,345,280,'')
text(c,38,305,'THE RIP  |',10,True,NAVY)
text(c,98,305,'SLACK',10,True,HexColor('#08743c'))
text(c,142,305,'>',10,True,NAVY)
text(c,156,305,'SUBSEQUENT MAXIMUM',10,True,HexColor('#b3261e'))
text(c,38,279,'Times paired; maximum rate (kn). +1d = next day.',11,True)
rip_rows(c,38,257,[('30 Oct','00:07 > 02:51 +4.84   06:52 > 09:23 -4.54'),('','12:47 > 15:18 +3.33   17:43 > 20:32 -6.41'),('31 Oct','00:53 > 03:35 +4.76   07:36 > 10:06 -4.53'),('','13:27 > 15:56 +3.36   18:28 > 21:18 -6.32'),('1 Nov','01:39 > 04:20 +4.56   08:20 > 10:48 -4.47'),('','14:09 > 16:39 +3.32   19:16 > 22:08 -5.98'),('2 Nov','02:25 > 05:05 +4.30   09:04 > 11:31 -4.38'),('','14:53 > 17:28 +3.18   20:10 > 23:04 -5.46'),('3 Nov','03:13 > 05:53 +3.97   09:48 > 12:16 -4.29'),('','15:44 > 18:29 +3.00   21:12 > 00:05+1d -4.84'),('4 Nov','04:02 > 06:47 +3.62   10:35 > 13:04 -4.20'),('','16:45 > 19:37 +2.85   22:28 > 01:13+1d -4.20')],17)
RIP_MODE=False
c.restoreState()
c.restoreState()
heads_y=(H-82-110)*0.75-80
c.saveState(); c.translate(330,heads_y+80); c.scale(1.32,1.32)
panel(c,0,0,300,67,'ST KILDA TO PORT PHILLIP HEADS')
text(c,13,18,'34 nm: 6 h 11 m at 5.5 kn / 5 h 40 m at 6 kn.',11,True)
c.restoreState()
c.restoreState()
c.showPage(); c.save()

c=create('part_2_deal_welshpool.pdf','Deal_to_Welshpool_with_passage.png','02  DEAL ISLAND  >  PORT WELSHPOOL','Planned departure 6 NOV 2026, 05:47  |  Flight S1747',[])
c.saveState(); c.translate(1152,H-87); c.scale(1.27,1.27); c.translate(-1152,-(H-87))
c.saveState(); c.translate(-25,0)
panel(c,827,H-283,350,196,'PORT WELSHPOOL PIER  |  HIGH / LOW')
text(c,840,H-130,'H = high water   L = low water',11,True)
rows(c,840,H-150,[('4 Nov','L 02:20  H 08:57  L 15:01  H 20:50'),('5 Nov','L 03:07  H 09:33  L 15:52  H 21:48'),('6 Nov','L 03:58  H 10:13  L 16:47  H 22:56'),('7 Nov','L 04:56  H 10:57  L 17:45'),('8 Nov','H 00:15  L 06:03  H 11:49  L 18:46'),('9 Nov','H 01:35  L 07:14  H 12:49  L 19:45')],19)
text(c,840,H-266,'Pier tides are not current slack; entrance offsets vary.',11,True)
panel(c,827,H-506,350,213,'RABBIT ISLAND  |  HIGH / LOW')
text(c,840,H-333,'H = high   L = low',11,True)
rows(c,840,H-354,[('4 Nov','L 01:16  H 07:48  L 13:51  H 19:46'),('5 Nov','L 02:04  H 08:30  L 14:44  H 20:48'),('6 Nov','L 02:57  H 09:15  L 15:42  H 22:03'),('7 Nov','L 03:57  H 10:08  L 16:44  H 23:28'),('8 Nov','L 05:05  H 11:06  L 17:46'),('9 Nov','H 00:48  L 06:17  H 12:07  L 18:45')],19)
text(c,840,H-469,'Rabbit Island high and low waters are about 1 hour',10,True)
text(c,840,H-485,'20 minutes earlier than Port Welshpool Pier on average.',10,True)
c.restoreState()
c.restoreState()
c.saveState(); c.translate(50,25); c.scale(1.32,1.32); c.translate(-50,-25)
c.saveState(); c.translate(25,0)
panel(c,25,25,330,201,'DEAL ISLAND  |  GARDEN COVE HIGH / LOW')
text(c,38,185,'H = high water   L = low water',11,True)
rows(c,38,164,[('4 Nov','L 00:40  H 06:56  L 13:11  H 19:05'),('5 Nov','L 01:29  H 07:40  L 14:04  H 20:02'),('6 Nov','L 02:20  H 08:27  L 15:01  H 21:03'),('7 Nov','L 03:14  H 09:16  L 16:00  H 22:07'),('8 Nov','L 04:13  H 10:09  L 16:59  H 23:16'),('9 Nov','L 05:15 (0.87m)  H 11:05 (2.06m)'),('','L 17:56 (0.36m)')],19)
c.restoreState()
c.restoreState()
c.showPage(); c.save()

# Render lossless phone-friendly images from the exact PDF artwork.
import pymupdf
for stem in ('part_1_st_kilda_deal', 'part_2_deal_welshpool'):
    source=HERE/f'{stem}.pdf'
    with pymupdf.open(source) as document:
        document[0].get_pixmap(matrix=pymupdf.Matrix(2,2), alpha=False).save(str(source.with_suffix('.png')))
