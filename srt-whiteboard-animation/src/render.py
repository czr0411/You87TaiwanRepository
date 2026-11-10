from PIL import Image,ImageDraw,ImageFont
import math, subprocess
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "work"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
W,H=1280,720
INK='#202a32'; BLUE='#237da0'; GREEN='#39876b'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(n):return ImageFont.truetype(font,n,index=3)
scenes=[(0,3.8,'智慧型手機，怎麼選？','兩大陣營，各有優勢'),(3.8,7.2,'Apple iOS','流暢體驗  /  保值'),(7.2,10.6,'Android','品牌選擇多  /  自由度高'),(10.6,14,'找到適合自己的手機','拍照派？電競派？')]
subs=[(1,3.5,'挑選智慧型手機，主要分為兩大陣營。'),(3.8,6.8,'第一種是 Apple 的 iOS 系統，主打流暢與保值。'),(7.2,10.2,'第二種是 Android 系統，品牌選擇多、自由度高。'),(10.6,14,'不論你重視拍照還是電競，都能找到適合自己的機款。')]
def frame(t):
 im=Image.new('RGB',(W,H),'#fffef9');d=ImageDraw.Draw(im)
 d.text((58,30),'SMARTPHONE  /  選購小筆記',font=f(19),fill=BLUE)
 idx=next(i for i,s in enumerate(scenes) if s[0]<=t<s[1]);start,end,title,tag=scenes[idx];q=t-start
 d.text((1220,30),f'0{idx+1}',font=f(20),fill=BLUE,anchor='ra')
 d.text((640,100),title,font=f(48),fill=INK,anchor='mm')
 paths=[]
 def line(points,c=INK,w=5):paths.append((points,c,w))
 def rect(x,y,w,h,c=INK):line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],c)
 def circle(x,y,r,c=INK):line([(x+math.cos(a*math.pi/30)*r,y+math.sin(a*math.pi/30)*r) for a in range(61)],c)
 def phone(x,y,label,c):
  rect(x,y,140,230);line([(x+45,y+17),(x+95,y+17)]);line([(x+18,y+195),(x+122,y+195)],c);circle(x+70,y+213,4)
  return (x+70,y+112,label,c)
 labels=[]
 if idx==0:
  labels=[phone(340,228,'iOS',BLUE),phone(800,228,'Android',GREEN)]
  line([(490,333),(580,333),(565,320)],BLUE);line([(790,333),(700,333),(715,320)],GREEN)
 elif idx==1:
  labels=[phone(340,220,'iOS',BLUE)]
  line([(570,290),(600,322),(660,252)],BLUE,8)
  circle(806,300,57,BLUE);line([(780,300),(800,320),(837,278)],BLUE,6)
  labels.extend([(615,381,'流暢',BLUE),(806,381,'保值',BLUE)])
 elif idx==2:
  labels=[phone(260,220,'A',GREEN),phone(570,220,'B',GREEN),phone(880,220,'C',GREEN)]
  for x in [300,610,920]:
   for j in range(3):line([(x,395+j*12),(x+52,395+j*12)],GREEN,3)
 else:
  rect(245,285,220,140);line([(285,285),(305,258),(360,258),(380,285)]);circle(355,353,44,BLUE);circle(355,353,26,BLUE);circle(430,309,6)
  line([(777,289),(865,289),(900,305),(935,390),(925,425),(899,435),(858,391),(784,391),(743,435),(717,425),(707,390),(742,305),(777,289)])
  line([(750,337),(790,337)],GREEN,7);line([(770,317),(770,357)],GREEN,7);circle(867,326,8,GREEN);circle(891,351,8,GREEN)
  labels=[(355,473,'拍照',BLUE),(820,473,'電競',GREEN)]
 total=sum(max(1,len(p)-1) for p,c,w in paths);budget=min(1,q/1.5)*total;tip=None
 for p,c,w in paths:
  for a,b in zip(p,p[1:]):
   if budget<=0:break
   z=min(1,budget);pt=(a[0]+(b[0]-a[0])*z,a[1]+(b[1]-a[1])*z);d.line([a,pt],fill=c,width=w);tip=pt;budget-=1
  if budget<=0:break
 if q>0.8:
  for x,y,s,c in labels:d.text((x,y),s,font=f(31),fill=c,anchor='mm')
 if tip and q<1.5:
  x,y=tip
  d.polygon([(x,y),(x+14,y-6),(x+74,y+64),(x+59,y+78)],fill='#f2bd87',outline=INK)
  d.line([(x+6,y+4),(x+57,y+63)],fill=INK,width=9)
 d.text((640,541),tag,font=f(28),fill=INK,anchor='mm')
 d.line([(90,584),(1190,584)],fill='#dadbd3',width=2)
 for a,b,s in subs:
  if a<=t<b:d.text((640,631),s,font=f(29),fill=INK,anchor='mm')
 d.line([(90,685),(90+1100*t/14,685)],fill=BLUE,width=4)
 return im
out=str(OUTPUT_DIR / 'smartphone-whiteboard.mp4')
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
for i in range(420):p.stdin.write(frame(i/30).tobytes())
p.stdin.close();assert p.wait()==0
imgs=[frame(t).resize((640,360)) for t in [2.8,5.9,9.5,13.4]]
contact=Image.new('RGB',(1280,720),'white')
for i,im in enumerate(imgs):contact.paste(im,((i%2)*640,(i//2)*360))
contact.save(OUTPUT_DIR / 'preview.jpg')
with open(OUTPUT_DIR / 'smartphone.srt','w',encoding='utf-8') as h:
 for i,(a,b,s) in enumerate(subs,1):
  def tc(x):return f'00:00:{int(x):02},{round((x%1)*1000):03}'
  h.write(f'{i}\n{tc(a)} --> {tc(b)}\n{s}\n\n')
print(out)
