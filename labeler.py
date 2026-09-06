"""Simple local YOLO labeler for kiwifruit (0) and support-post (1)."""
from __future__ import annotations
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import Image, ImageTk

class Labeler:
    def __init__(self, root):
        self.root=root; root.title('KiwiAI Labeler'); self.images=[]; self.i=0; self.boxes=[]; self.start=None; self.class_id=0
        tk.Button(root,text='انتخاب پوشهٔ عکس',command=self.choose).pack(); self.info=tk.Label(root); self.info.pack()
        self.canvas=tk.Canvas(root,width=900,height=600,bg='black'); self.canvas.pack(); self.canvas.bind('<Button-1>',self.down); self.canvas.bind('<ButtonRelease-1>',self.up)
        bar=tk.Frame(root); bar.pack(); tk.Button(bar,text='۱: کیوی',command=lambda:self.set_class(0)).pack(side='left'); tk.Button(bar,text='۲: پایه',command=lambda:self.set_class(1)).pack(side='left'); tk.Button(bar,text='ذخیره و بعدی',command=self.save_next).pack(side='left'); root.bind('1',lambda e:self.set_class(0)); root.bind('2',lambda e:self.set_class(1)); root.bind('<Return>',lambda e:self.save_next())
    def choose(self):
        folder=filedialog.askdirectory(); self.images=sorted(Path(folder).glob('*')) if folder else []; self.images=[p for p in self.images if p.suffix.lower() in {'.jpg','.jpeg','.png'}]; self.i=0; self.load()
    def set_class(self,c): self.class_id=c; self.info.config(text=f'کلاس فعال: {"کیوی" if c==0 else "پایه"}')
    def load(self):
        if not self.images:return
        p=self.images[self.i]; self.img=Image.open(p).convert('RGB'); self.scale=min(900/self.img.width,600/self.img.height); self.photo=ImageTk.PhotoImage(self.img.resize((int(self.img.width*self.scale),int(self.img.height*self.scale)))); self.canvas.delete('all'); self.canvas.create_image(0,0,anchor='nw',image=self.photo); self.boxes=[]; self.info.config(text=f'{self.i+1}/{len(self.images)} | ۱=کیوی، ۲=پایه، Enter=ذخیره')
    def down(self,e): self.start=(e.x,e.y)
    def up(self,e):
        if not self.start:return
        x1,y1=self.start; x2,y2=e.x,e.y; self.start=None
        if abs(x2-x1)<5 or abs(y2-y1)<5:return
        self.boxes.append((self.class_id,min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))); self.canvas.create_rectangle(x1,y1,x2,y2,outline='lime' if self.class_id==0 else 'cyan',width=2)
    def save_next(self):
        if not self.images:return
        p=self.images[self.i]; out=p.parent.parent/'labels'; out.mkdir(exist_ok=True); rows=[]
        for c,x1,y1,x2,y2 in self.boxes:
            rows.append(f'{c} {(x1+x2)/(2*self.scale*self.img.width):.6f} {(y1+y2)/(2*self.scale*self.img.height):.6f} {(x2-x1)/(self.scale*self.img.width):.6f} {(y2-y1)/(self.scale*self.img.height):.6f}')
        (out/(p.stem+'.txt')).write_text('\n'.join(rows)+'\n',encoding='utf-8'); self.i=(self.i+1)%len(self.images); self.load()
if __name__=='__main__': Labeler(tk.Tk()).root.mainloop()
