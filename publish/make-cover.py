# SPDX-FileCopyrightText: 2026 5thlayer
# SPDX-License-Identifier: MIT

# Cover and icon in the style of the mods' publish/make-cover.py: one strip of each Module's cover,
# behind the suite's name. Run from the repo root with Pillow installed, with the Module checkouts
# beside this one (../groundworks and so on).
from PIL import Image, ImageDraw, ImageFont
# Each Module with the row of its 1280x640 cover the strip is centred on, clear of its title band
MODULES=[('groundworks',50),('beltworks',110),('pipeworks',50),('wireworks',430),('craftworks',50),('fieldworks',100),
         ('voidworks',555),('gearworks',55)]
BG=(24,26,32)
ACCENT=(240,160,50)
FADE=110
FONTS='~/.local/share/fonts/msfonts/'
def strip(m,cy,W,h):
    c=Image.open(f'../{m}/publish/{m}-cover.png').convert('RGBA')
    ch=int(1280*h/W); cy=max(cy,ch//2)
    return c.crop((0,cy-ch//2,1280,cy-ch//2+ch)).resize((W,h),Image.LANCZOS)
def make(W,H,out,title_size):
    import os
    img=Image.new('RGBA',(W,H),BG+(255,))
    bh=int(title_size*2.3); half=(H-bh)//2
    # The first half of the Modules above the title, the rest below, each half shared out among its own
    n=(len(MODULES)+1)//2
    for mods,y0 in ((MODULES[:n],0),(MODULES[n:],H-half)):
        sh=half//len(mods); gap=max(2,sh//16)
        for i,(m,cy) in enumerate(mods):
            img.alpha_composite(strip(m,cy,W,sh-gap),(0,y0+i*sh+gap//2))
    img=Image.alpha_composite(img,Image.new('RGBA',(W,H),BG+(FADE,)))
    band=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(band).rectangle([0,half,W,H-half],fill=(16,17,22,235))
    img=Image.alpha_composite(img,band)
    d=ImageDraw.Draw(img); lt=max(3,title_size//25)
    d.rectangle([0,half,W,half+lt],fill=ACCENT); d.rectangle([0,H-half-lt,W,H-half],fill=ACCENT)
    fd=os.path.expanduser(FONTS)
    f1=ImageFont.truetype(fd+'impact.ttf',title_size)
    f2=ImageFont.truetype(fd+'ariblk.ttf',int(title_size*0.62))
    f3=ImageFont.truetype(fd+'ariblk.ttf',int(title_size*0.36))
    a,w='FACTORY','works'
    b1=d.textbbox((0,0),a,font=f1); b2=d.textbbox((0,0),w,font=f2)
    w1=b1[2]-b1[0]; h1=b1[3]-b1[1]; w2=b2[2]-b2[0]; h2=b2[3]-b2[1]
    px=int(title_size*0.16); g=int(title_size*0.1); bw=w2+2*px
    sub='SHOWCASE'; b3=d.textbbox((0,0),sub,font=f3,); h3=b3[3]-b3[1]
    sg=int(title_size*0.28); block=h1+sg+h3
    x=(W-(w1+g+bw))//2; top=(H-block)//2; s=max(3,title_size//20)
    d.text((x+s-b1[0],top+s-b1[1]),a,font=f1,fill=(0,0,0))
    d.text((x-b1[0],top-b1[1]),a,font=f1,fill=ACCENT)
    bx=x+w1+g; bt=top; bb=top+h1
    d.rounded_rectangle([bx+s,bt+s,bx+bw+s,bb+s],radius=px,fill=(0,0,0))
    d.rounded_rectangle([bx,bt,bx+bw,bb],radius=px,fill=(240,240,236))
    d.text((bx+px-b2[0],bt+(h1-h2)//2-b2[1]),w,font=f2,fill=BG)
    sx=(W-(b3[2]-b3[0]))//2-b3[0]; sy=top+h1+sg-b3[1]
    d.text((sx,sy),sub,font=f3,fill=(240,240,236))
    img.convert('RGB').save(out)
make(1280,640,'publish/showcase-cover.png',130)
make(512,512,'publish/showcase-icon.png',68)
