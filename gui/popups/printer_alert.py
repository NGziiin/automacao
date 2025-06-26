import customtkinter as ctk
from PIL import Image, ImageTk
import os

class Alerta(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.config()
        self.imagens()
        self.frame()
        self.contagem()
        self.mainloop()

    def config(self):

        #configuração para a janela ficar em local especifico
        largura_monitor = self.winfo_screenwidth()
        altura_monitor = self.winfo_screenheight()
        if largura_monitor >= 1920 and altura_monitor >= 1080:
            largura = 500
            altura = 130
            x = (largura_monitor // 2) - (largura // 2) + 8
            y = (altura_monitor // 4.6) - (altura // 4.6)
        elif largura_monitor >= 1366 and altura_monitor >= 768:
            largura = 500
            altura = 130
            x = (largura_monitor // 2) - (largura // 2) + 8
            y = (altura_monitor // 4.6) - (altura // 4.6) - 80
        #finaliza aqui essa configuração

        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()

    def frame(self):
        frame = ctk.CTkFrame(self, bg_color='red', fg_color='transparent')
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(frame, text="Possui boleto pendente!", font=('Arial', 30, 'bold'), text_color='white', fg_color='red').place(x=110, y=50)
        ctk.CTkLabel(frame, image=self.image, text='', fg_color='red').place(x= 40, y=40)

    def contagem(self):
        self.after(5000, self.destroy)

    def imagens(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, '..', '..', 'image', 'alerta.png')
        image_path = os.path.normpath(image_path)
        self.image = Image.open(image_path)
        self.image = self.image.resize((50, 50))
        self.image = ImageTk.PhotoImage(self.image)