import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from slideforge.parser import parse_document
from slideforge.generator import PresentationGenerator

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SlideForge AI - MVP')
        self.geometry('720x430')
        self.configure(padx=20,pady=20)
        self.doc=tk.StringVar(); self.banner=tk.StringVar(); self.output=tk.StringVar()
        tk.Label(self,text='SlideForge AI',font=('Segoe UI',22,'bold')).pack(pady=(0,15))
        self.row('Documento Word/TXT/MD',self.doc,self.pick_doc)
        self.row('Banner/Logo (PNG/JPG)',self.banner,self.pick_banner)
        self.row('Arquivo de saída (.pptx)',self.output,self.pick_output)
        tk.Button(self,text='GERAR APRESENTAÇÃO',command=self.generate,height=2,font=('Segoe UI',12,'bold')).pack(fill='x',pady=25)
        tk.Label(self,text='MVP: preserva o conteúdo, divide automaticamente e aplica identidade visual.',fg='#445').pack()
    def row(self,label,var,cmd):
        f=tk.Frame(self); f.pack(fill='x',pady=8)
        tk.Label(f,text=label,width=24,anchor='w').pack(side='left')
        tk.Entry(f,textvariable=var).pack(side='left',fill='x',expand=True,padx=8)
        tk.Button(f,text='Selecionar',command=cmd).pack(side='right')
    def pick_doc(self):
        p=filedialog.askopenfilename(filetypes=[('Documentos','*.docx *.txt *.md')]);
        if p:
            self.doc.set(p)
            if not self.output.get(): self.output.set(str(Path(p).with_suffix(''))+'_apresentacao.pptx')
    def pick_banner(self):
        p=filedialog.askopenfilename(filetypes=[('Imagens','*.png *.jpg *.jpeg')]);
        if p:self.banner.set(p)
    def pick_output(self):
        p=filedialog.asksaveasfilename(defaultextension='.pptx',filetypes=[('PowerPoint','*.pptx')]);
        if p:self.output.set(p)
    def generate(self):
        try:
            blocks=parse_document(self.doc.get())
            PresentationGenerator().generate(blocks,self.output.get(),banner=self.banner.get() or None)
            messagebox.showinfo('Concluído',f'Apresentação criada em:\n{self.output.get()}')
        except Exception as e:
            messagebox.showerror('Erro',str(e))

if __name__=='__main__':
    App().mainloop()
