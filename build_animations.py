"""Generate the looping, self-hosted animated GIF assets for a GitHub profile."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random
A=Path(__file__).resolve().parent/'assets'; A.mkdir(exist_ok=True)
W=920
BG=(8,9,20); COLD=(119,159,169); DIM=(67,85,101); WHITE=(223,221,218); ORANGE=(255,157,78)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
fonts={s:ImageFont.truetype(FONT,s) for s in [10,11,12,13,14,15,16,18,20,24,27]}
fonts.update({'large':ImageFont.truetype(BOLD,34),'title':ImageFont.truetype(BOLD,20)})
rng=random.Random(11)
# Fixed scattered floating rune particles
particles=[(rng.randint(20,900),rng.randint(26,366),rng.choice('.:|*+o0/\\%#@'),rng.randint(0,100),rng.uniform(.3,1.6)) for _ in range(190)]
embers=[(rng.randint(255,735),rng.randint(125,310),rng.randint(0,40),rng.uniform(.7,2.3)) for _ in range(57)]

def canvas(h):
 im=Image.new('RGB',(W,h),BG); d=ImageDraw.Draw(im)
 for y in range(h):
  t=y/max(1,h-1); d.line([(0,y),(W,y)],fill=(int(8+4*t),int(9+4*t),int(20+9*t)))
 return im

def glow(im, x,y,rad,color):
 lay=Image.new('RGBA',im.size,(0,0,0,0)); dl=ImageDraw.Draw(lay)
 dl.ellipse((x-rad/4,y-rad/4,x+rad/4,y+rad/4),fill=(*color,150))
 lay=lay.filter(ImageFilter.GaussianBlur(rad/2)); im.paste(Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB')) if False else None
 return Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB')

def border(draw,h,caption):
 draw.rectangle([7,7,W-8,h-8],outline=(43,52,65),width=1)
 draw.line([(7,39),(W-8,39)],fill=(41,50,63))
 for x,c in zip([24,40,56],[(255,147,95),(211,166,106),(155,174,176)]):draw.ellipse([x,19,x+7,26],fill=c)
 draw.text((W-24,20),caption,font=fonts[11],anchor='ra',fill=(113,128,142))

def encode(name, frames, dur=90):
 # adaptive quantization for reasonable archive size without global dither shimmer
 frames[0].save(A/name,save_all=True,append_images=frames[1:],duration=dur,loop=0,optimize=True,disposal=2)
 print(name,(A/name).stat().st_size)

def draw_hero(t,N=36):
 h=410; im=canvas(h); d=ImageDraw.Draw(im); border(d,h,'ARCHIVE / 001 : ANOMALOUS LANDSCAPE')
 # drifting symbols in deep space; parallax
 for x,y,g,phase,speed in particles:
  xx=(x+math.sin(t/N*2*math.pi+phase)*6)%W
  yy=((y+t*speed*.63)%320)+42
  br= .48+.52*math.sin(2*math.pi*t/N+phase)**2
  clr=tuple(int(v*br) for v in (83,114,130))
  d.text((xx,yy),g,font=fonts[11],fill=clr)
 # ASCII forests and rolling ground. Text is actual monospaced characters.
 grid=rng.__class__(19)
 glyphs=':;.,/\\|^i!lIl+*x'
 for row in range(8):
  yy=232+row*16
  for col in range(102):
   xx=12+col*9
   terrain=285+29*math.sin(xx/92)+16*math.sin(xx/35)
   if yy>terrain and grid.random()>.21:
    g=grid.choice(glyphs)
    c=(32+row*3,67+row*3,70+row*3)
    d.text((xx,yy),g,font=fonts[11],fill=c)
 # brighter ASCII thicket at sides
 for sign in (-1,1):
  for q in range(15):
   x= (90+q*10) if sign<0 else (720+q*10)
   top=185+int(24*math.sin(q*.9))
   for y in range(top,300,15):
    g='/' if sign==-1 else '\\'
    d.text((x+int(math.sin(y+q)*5),y),g,font=fonts[13],fill=(66,95,100))
 # wandering fireflies
 phase=t*2*math.pi/N
 for x,y,o,speed in embers:
  xx=x+math.sin(phase+o)*14; yy=y+math.cos(phase*1.4+o)*11
  intensity=max(0,math.sin(phase*2+o))
  if intensity>.24:
   c=(int(128+116*intensity),int(62+95*intensity),int(31+42*intensity))
   d.text((xx,yy),rng.choice(['*','+','.',':']),font=fonts[12],fill=c)
 # central amber orb glow
 cx=462+math.sin(phase)*8; cy=228+math.cos(phase)*6
 im=glow(im,cx,cy,60,(250,120,42)); d=ImageDraw.Draw(im)
 d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=(255,218,155))
 for k in range(24):
  ang=k*2.399963+phase*.5; radius=16+9*math.sin(k*2+phase)
  x=cx+math.cos(ang)*radius*2; y=cy+math.sin(ang)*radius
  d.text((x,y),'+*o.'[k%4],font=fonts[13],fill=(255,145+(k%5)*12,71+(k%4)*17))
 # Main identity remains above background via tint black rectangle
 d.rounded_rectangle((155,77,765,173),radius=8,fill=(8,10,21),outline=(48,53,62),width=1)
 d.text((W/2,94),'K U S H A L   /   T H E   A S C I I   A R C H I V E',font=fonts[14],fill=(255,173,116),anchor='mt')
 d.text((W/2,121),'KUSHAL M ANVEKAR',font=fonts['large'],fill=(239,232,225),anchor='mt')
 d.text((W/2,163),'AI SYSTEMS   //   OPEN SOURCE   //   RESEARCH',font=fonts[12],fill=(120,164,170),anchor='mt')
 d.text((21,377),'visitor@archive:~$ ./explore_world',font=fonts[13],fill=(172,194,193))
 if t%12<8:d.rectangle((353,381,362,394),fill=(246,153,86))
 d.text((W-21,381),'[ LIVE TRANSMISSION ]',anchor='ra',font=fonts[11],fill=(197,134,88))
 return im

PROJ=[('01','SENTINEL','local-first security tooling'),('02','BEDROCK','model-agnostic agent runtime'),('03','VAKIL AI','open-source legal intelligence'),('04','MESH','multi-agent coordination'),('05','OPENCONNECT','remote development access')]
def draw_projects(t,N=36):
 h=327; im=canvas(h); d=ImageDraw.Draw(im); border(d,h,'ARCHIVE / 002 : KNOWN ENTITIES')
 d.text((30,57),'$ ls -la ~/systems/',font=fonts[18],fill=(244,154,94))
 d.text((30,86),'drwxr-xr-x    5 entries   //   signal stable',font=fonts[12],fill=(105,150,156))
 for k,(idx,n,desc) in enumerate(PROJ):
  y=122+k*35
  active=(t//7)%5==k
  if active:d.rectangle((22,y-5,W-23,y+27),fill=(23,33,43),outline=(63,79,87))
  d.text((32,y),f'[{idx}]',font=fonts[15],fill=(244,149,86) if active else (123,133,148))
  d.text((106,y),n.lower()+'/',font=fonts[16],fill=(232,219,206) if active else (158,193,194))
  d.text((344,y+2),'.. '+desc,font=fonts[13],fill=(131,145,154))
  if active:d.text((864,y+1),'<',font=fonts[16],fill=ORANGE)
 for i in range(6):
  x=748+i*27; v=int(9+11*math.sin((t+i)*.27)**2)
  d.line((x,70-v,x,70+v),fill=(75,119+7*i,129+4*i),width=2)
 return im

def draw_signal(t,N=36):
 h=164; im=canvas(h); d=ImageDraw.Draw(im); border(d,h,'ARCHIVE / 003 : SIGNAL FROM THE OPERATOR')
 d.text((33,57),'visitor@kushal:~$ echo $MANIFESTO',font=fonts[16],fill=(248,161,99))
 line='building systems, breaking assumptions, learning in public.'
 shown=int(len(line)*min(1,(t%N)/(N*.7)))
 d.text((33,89),line[:shown],font=fonts[15],fill=(218,223,214))
 if t%8<5:
  tw=d.textbbox((0,0),line[:shown],font=fonts[15])[2]
  d.rectangle((35+tw,88,43+tw,106),fill=(236,156,96))
 d.text((33,133),'connection: persistent  /  curiosity: unlimited',font=fonts[12],fill=(96,139,147))
 return im

if __name__=='__main__':
 encode('ascii-world.gif',[draw_hero(t) for t in range(36)],85)
 encode('project-archive.gif',[draw_projects(t) for t in range(36)],110)
 encode('operator-signal.gif',[draw_signal(t) for t in range(36)],110)

def draw_panel(t, label, command, lines, h=210):
 im=canvas(h); d=ImageDraw.Draw(im);border(d,h,label)
 d.text((29,57),'$ '+command,font=fonts[16],fill=(240,153,94))
 for i,(lead,val) in enumerate(lines):
  y=94+i*27
  d.text((34,y),lead,font=fonts[14],fill=(114,166,172))
  d.text((248,y),val,font=fonts[14],fill=(214,215,210))
 # moving trace, slow scan and offset flicker
 x=665+(t%36)*5
 for j in range(16):
  xx=690+j*14
  y=65+math.sin((t+j*2)*.3)*5
  d.text((xx,y),('.:+|*'[int((j+t)/3)%5]),font=fonts[12],fill=(88,96+int(35*math.sin(j+t)**2),102))
 d.line([(22, h-19),(22+int((W-44)*(t%36)/36),h-19)],fill=(178,101,63),width=1)
 return im

if __name__=='__main__':
 panels=[
  ('identity.gif','ARCHIVE / 004 : IDENTITY','cat identity.log', [('operator','Kushal M Anvekar'),('base','Bengaluru, India'),('field','AI/ML · software engineering'),('status','open to internships / open source')]),
  ('research.gif','ARCHIVE / 005 : RESEARCH','cat research.log', [('01 spatial','scene understanding & depth'),('02 MUTE','mask-free image editing concepts'),('03 agents','memory, execution and tool policy'),('04 build','experiments into working software')]),
  ('toolkit.gif','ARCHIVE / 006 : INSTRUMENTS','tree ~/toolkit', [('languages','Python · Java · JavaScript · SQL'),('intelligence','PyTorch · NLP · RAG · LLMs'),('services','FastAPI · Node.js · Docker'),('systems','Linux · Git · WSL · MCP')]),
  ('contact.gif','ARCHIVE / 007 : UPLINK','cat uplink.txt', [('website','kushalmanvekar.runs-on.dev'),('code','github.com/Kushalongit-hub'),('network','linkedin.com/in/kushal-m-anvekar'),('signal','open to projects & collaboration')])]
 for name,label,command,rows in panels:
  encode(name,[draw_panel(t,label,command,rows) for t in range(36)],110)
