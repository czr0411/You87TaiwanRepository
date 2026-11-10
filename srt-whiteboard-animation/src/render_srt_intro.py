"""Render the nine-cue SRT introduction as a silent whiteboard animation."""
from pathlib import Path
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
W, H, FPS, DURATION = 1280, 720, 30, 58
INK, BLUE, GREEN = '#25333a', '#237da0', '#39876b'
CUES = [
 (0,6,'歡迎使用 SRT 字幕範例檔案！','歡迎認識 SRT','字幕，讓內容更容易理解'),
 (6.5,12.5,'這是一個 SRT 字幕的示範。','SRT 字幕示範','編號 ＋ 時間碼 ＋ 字幕文字'),
 (13,19,'你可以使用 SRT 檔案為影片加入字幕。','替影片加入字幕','影片與字幕，一起播放'),
 (19.5,25.5,'每段字幕都包含編號、時間碼和字幕文字。','每段字幕的三個元素','01 編號　02 時間碼　03 文字'),
 (26,32,'時間碼格式為時：分：秒，毫秒。','讀懂時間碼','時：分：秒，毫秒'),
 (32.5,38.5,'你可以調整時間，讓字幕與影片同步。','讓字幕與影片同步','調整開始與結束時間'),
 (39,45,'請確保字幕文字清楚易讀。','清楚易讀的字幕','適當字級・清楚對比・簡潔分行'),
 (45.5,51.5,'這就是製作 SRT 字幕檔案的方法！','完成你的 SRT','編寫 → 對時 → 儲存 .srt'),
 (52,58,'祝你製作字幕愉快！','開始製作你的字幕吧！','讓每一句話，都被看見'),
]

def font(n): return ImageFont.truetype(FONT,n,index=3)

def frame(t):
 i=max(j for j,c in enumerate(CUES) if c[0]<=t)
 a,b,subtitle,title,tag=CUES[i]; q=t-a
 im=Image.new('RGB',(W,H),'#fffef9'); d=ImageDraw.Draw(im)
 d.text((58,30),'SRT  /  字幕入門小筆記',font=font(20),fill=BLUE)
 d.text((1220,30),f'{i+1:02} / 09',font=font(20),fill=BLUE,anchor='ra')
 d.text((640,114),title,font=font(46),fill=INK,anchor='mm')
 strokes=[]; labels=[]
 def line(p,c=INK,w=5): strokes.append((p,c,w))
 def rect(x,y,w,h,c=INK):line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],c)
 def circle(x,y,r,c=INK):line([(x+math.cos(k*math.pi/40)*r,y+math.sin(k*math.pi/40)*r) for k in range(81)],c)
 def text(x,y,s,n=28,c=INK):labels.append((x,y,s,n,c))
 def doc(x,y):
  rect(x,y,178,220);line([(x+28,y+48),(x+148,y+48)],BLUE)
  for k in range(3):line([(x+28,y+102+k*30),(x+148,y+102+k*30)],INK,3)
  text(x+89,y+75,'.srt',30,BLUE)
 def play(x,y):
  rect(x,y,300,192);line([(x+129,y+48),(x+129,y+118),(x+187,y+83),(x+129,y+48)],BLUE)
  line([(x+24,y+153),(x+276,y+153)],GREEN,5)
 if i in [0,1]:
  doc(310,225);line([(535,335),(670,335),(650,318)],BLUE)
  rect(730,244,240,182);text(850,288,'1',30,BLUE);text(850,337,'00:00:00,000',22);text(850,386,'歡迎使用 SRT',25,GREEN)
 elif i==2:
  doc(240,220);line([(460,330),(650,330),(632,313)],BLUE);play(735,240)
 elif i==3:
  for k,(s,v) in enumerate([('編號','1'),('時間碼','00:00:00,000'),('字幕文字','歡迎使用 SRT！')]):
   x=180+k*315;rect(x,253,290,175);text(x+145,294,s,29,BLUE);text(x+145,366,v,25)
 elif i==4:
  circle(310,333,83);line([(310,276),(310,333),(349,354)],BLUE)
  text(800,310,'00 : 00 : 26 , 000',43,BLUE)
  for x,s in [(590,'時'),(715,'分'),(839,'秒'),(1010,'毫秒')]:text(x,386,s,25)
 elif i==5:
  for y,s in [(286,'影片'),(389,'字幕')]:
   text(235,y,s,28);line([(330,y),(1080,y)],INK,3)
   rect(490,y-24,300,48,BLUE if y==286 else GREEN)
  line([(640,240),(640,439)],GREEN,3);text(640,476,'同步',29,GREEN)
 elif i==6:
  rect(200,230,880,220);text(640,303,'字幕文字清楚易讀',48)
  line([(340,389),(365,414),(405,365)],GREEN,7);text(690,396,'看得清楚，讀得輕鬆',31,GREEN)
 elif i==7:
  for x,s in [(225,'編寫'),(540,'對時'),(855,'儲存')]:
   rect(x,257,200,150);text(x+100,330,s,36,BLUE)
  for x in [450,765]:line([(x,330),(x+65,330),(x+48,313)],GREEN)
  text(640,470,'字幕完成.srt',30,GREEN)
 else:
  circle(640,327,106,GREEN);line([(583,324),(626,367),(702,282)],GREEN,10)
  for x,y in [(430,240),(855,260),(412,400),(870,419)]:
   line([(x-10,y),(x+10,y)],BLUE,3);line([(x,y-10),(x,y+10)],BLUE,3)
 # Reveal paths in order at a constant drawing speed.
 budget=min(1,max(0,q)/2)*sum(len(p)-1 for p,c,w in strokes);tip=None
 for p,c,w in strokes:
  for u,v in zip(p,p[1:]):
   if budget<=0:break
   z=min(1,budget);tip=(u[0]+(v[0]-u[0])*z,u[1]+(v[1]-u[1])*z)
   d.line([u,tip],fill=c,width=w);budget-=1
  if budget<=0:break
 if q>.7:
  for x,y,s,n,c in labels:d.text((x,y),s,font=font(n),fill=c,anchor='mm')
 if tip and q<2:
  x,y=tip;d.polygon([(x,y),(x+14,y-6),(x+74,y+64),(x+59,y+78)],fill='#f2bd87',outline=INK)
  d.line([(x+6,y+4),(x+57,y+63)],fill=INK,width=9)
 d.text((640,541),tag,font=font(27),fill=INK,anchor='mm')
 d.line([(90,584),(1190,584)],fill='#dadbd3',width=2)
 if a<=t<b:d.text((640,633),subtitle,font=font(31),fill=INK,anchor='mm')
 d.line([(90,685),(90+1100*t/DURATION,685)],fill=BLUE,width=4)
 return im

def main():
 out=ROOT/'work'/'srt-intro';out.mkdir(parents=True,exist_ok=True)
 video=out/'srt-intro-whiteboard.mp4'
 p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
 try:
  for k in range(FPS*DURATION):p.stdin.write(frame(k/FPS).tobytes())
 finally:p.stdin.close()
 if p.wait():raise RuntimeError('FFmpeg failed')
 preview=Image.new('RGB',(1280,720),'white')
 for i,c in enumerate(CUES):preview.paste(frame(c[0]+3).resize((426,240)),((i%3)*426,(i//3)*240))
 preview.save(out/'srt-intro-preview.jpg')
 def tc(t):
  ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
 (out/'srt-intro.srt').write_text('\n\n'.join(f'{i}\n{tc(a)} --> {tc(b)}\n{s}' for i,(a,b,s,*_) in enumerate(CUES,1))+'\n',encoding='utf-8')
 print(video)

if __name__=='__main__':main()
