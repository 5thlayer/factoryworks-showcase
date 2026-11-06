# SPDX-FileCopyrightText: 2026 5thlayer
# SPDX-License-Identifier: MIT

# Cover, icon and title screen in the style of the mods' publish/make-cover.py: one strip of each
# Module's cover, behind the suite's name. Run from the repo root with Pillow installed, with the
# Module checkouts beside this one (../groundworks and so on).
#
# The title screen's pieces go to config/fancymenu/assets/showcase_menu_*, apart, for FancyMenu to lay
# out at any window's size: the strips with no band; a slice of the band, which FancyMenu stretches
# across the screen; the lettering on nothing; the buttons' backgrounds; and the window's icon at 16
# and 32 pixels. It prints the lettering's and the band's sizes against the screen's height, for
# config/fancymenu/customization/title_screen.txt.
from PIL import Image, ImageDraw, ImageFont
# Each Module with the row of its 1280x640 cover the strip is centred on, clear of its title band
MODULES=[('groundworks',50),('beltworks',110),('pipeworks',50),('wireworks',430),('craftworks',50),('fieldworks',100),
         ('railworks',410),('voidworks',555),('gearworks',55)]
BG=(24,26,32)
ACCENT=(240,160,50)
FADE=110
PILL=(240,240,236)
FONTS='~/.local/share/fonts/msfonts/'
def strip(m,cy,W,h):
    c=Image.open(f'../{m}/publish/{m}-cover.png').convert('RGBA')
    ch=int(1280*h/W); cy=max(cy,ch//2)
    return c.crop((0,cy-ch//2,1280,cy-ch//2+ch)).resize((W,h),Image.LANCZOS)
def strips(W,H,mods,y0,h):
    # mods' strips shared out down h pixels of an image W wide from y0, a small gap between each
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    sh=h//len(mods); gap=max(2,sh//16)
    for i,(m,cy) in enumerate(mods):
        img.alpha_composite(strip(m,cy,W,sh-gap),(0,y0+i*sh+gap//2))
    return img
def band(img,top,bottom,title_size):
    # the band across img from top to bottom, ruled top and bottom in the accent
    b=Image.new('RGBA',img.size,(0,0,0,0))
    ImageDraw.Draw(b).rectangle([0,top,img.width,bottom],fill=(16,17,22,235))
    img.alpha_composite(b)
    d=ImageDraw.Draw(img); lt=max(3,title_size//25)
    d.rectangle([0,top,img.width,top+lt],fill=ACCENT); d.rectangle([0,bottom-lt,img.width,bottom],fill=ACCENT)
def lettering(img,title_size,cy):
    # FACTORY, the works pill and SHOWCASE under them, centred across img on cy
    import os
    d=ImageDraw.Draw(img); W=img.width
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
    x=(W-(w1+g+bw))//2; top=cy-block//2; s=max(3,title_size//20)
    d.text((x+s-b1[0],top+s-b1[1]),a,font=f1,fill=(0,0,0))
    d.text((x-b1[0],top-b1[1]),a,font=f1,fill=ACCENT)
    bx=x+w1+g; bt=top; bb=top+h1
    d.rounded_rectangle([bx+s,bt+s,bx+bw+s,bb+s],radius=px,fill=(0,0,0))
    d.rounded_rectangle([bx,bt,bx+bw,bb],radius=px,fill=PILL)
    d.text((bx+px-b2[0],bt+(h1-h2)//2-b2[1]),w,font=f2,fill=BG)
    sx=(W-(b3[2]-b3[0]))//2-b3[0]; sy=top+h1+sg-b3[1]
    d.text((sx,sy),sub,font=f3,fill=PILL)
def make(W,H,out,title_size):
    img=Image.new('RGBA',(W,H),BG+(255,))
    bh=int(title_size*2.3); half=(H-bh)//2
    # The first half of the Modules above the title, the rest below, each half shared out among its own
    n=(len(MODULES)+1)//2
    img.alpha_composite(strips(W,H,MODULES[:n],0,half)); img.alpha_composite(strips(W,H,MODULES[n:],H-half,half))
    img=Image.alpha_composite(img,Image.new('RGBA',(W,H),BG+(FADE,)))
    band(img,half,H-half,title_size)
    lettering(img,title_size,H//2)
    img.convert('RGB').save(out)
def menu(W,H,title_size):
    # The background: every Module's strip down the whole screen, faded further than the cover's so the
    # buttons over it read
    img=Image.new('RGBA',(W,H),BG+(255,))
    img.alpha_composite(strips(W,H,MODULES,0,H))
    img=Image.alpha_composite(img,Image.new('RGBA',(W,H),BG+(MENU_FADE,)))
    img.convert('RGB').save(MENU+'background.png')
    # The lettering on nothing, cropped to it, and a slice of the band as tall as the cover's
    bh=int(title_size*2.3)//2*2
    title=Image.new('RGBA',(W,bh),(0,0,0,0))
    lettering(title,title_size,bh//2)
    box=title.getbbox(); title.crop(box).save(MENU+'title.png')
    sl=Image.new('RGBA',(16,bh+1),(0,0,0,0)); band(sl,0,bh,title_size); sl.save(MENU+'band.png')
    print(f'band: {bh/H:.4f} of the height; title: {(box[2]-box[0])/H:.4f} x {(box[3]-box[1])/H:.4f} of it, {box[1]/H:.4f} below the band\'s top')
    # The buttons' backgrounds, which FancyMenu nine-slices to any button's size, one texture pixel to
    # a GUI pixel: the band's dark, edged in grey, in the accent while hovered, and dimmer while off
    for name,fill,edge in [('button',(20,21,26),(70,72,80)),('button_hover',(36,30,22),ACCENT),
                           ('button_off',(12,13,16),(40,42,48))]:
        im=Image.new('RGBA',(16,16),edge+(255,))
        ImageDraw.Draw(im).rectangle([1,1,14,14],fill=fill+(235,))
        im.save(MENU+name+'.png')
    # The window's icon, at the 16 and 32 pixels FancyMenu asks for: the suite's F in the accent on the
    # band's dark, since the cover's lettering doesn't read that small
    import os
    for n in (16,32):
        im=Image.new('RGBA',(n*8,n*8),BG+(255,)); d=ImageDraw.Draw(im)
        d.rectangle([0,0,n*8-1,n*8-1],outline=ACCENT,width=n*8//10)
        f=ImageFont.truetype(os.path.expanduser(FONTS)+'impact.ttf',int(n*8*0.8))
        b=d.textbbox((0,0),'F',font=f)
        d.text(((n*8-(b[2]-b[0]))//2-b[0],(n*8-(b[3]-b[1]))//2-b[1]),'F',font=f,fill=ACCENT)
        im.resize((n,n),Image.LANCZOS).save(f'{MENU}icon_{n}.png')
MENU='config/fancymenu/assets/showcase_menu_'
MENU_FADE=150
make(1280,640,'publish/showcase-cover.png',130)
make(512,512,'publish/showcase-icon.png',68)
menu(1920,1080,120)
