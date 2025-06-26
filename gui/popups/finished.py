from customtkinter import CTkToplevel, CTkFrame, CTkLabel
from PIL import Image, ImageTk
import os

class FinishedPopup(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.config()
        self.load_images()
        self.create_frame()
        self.set_timer()
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

    def create_frame(self):
        frame = CTkFrame(self, bg_color='white', fg_color='transparent')
        frame.pack(fill="both", expand=True)

        CTkLabel(frame, text="Finalizado com sucesso", font=('Arial', 25, 'bold'), text_color='green', fg_color='white').place(x=130, y=30)
        CTkLabel(frame, text='Obrigado por utilizar o meu software\nAss.: Herick Müller', font=('arial', 15, 'bold'), justify='left', text_color='black', fg_color='white').place(x=130, y=60)
        CTkLabel(frame, image=self.image, text='', fg_color='white').place(x=40, y=40)

    def set_timer(self):
        self.after(15000, self.destroy)

    def load_images(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, '..', '..', 'image', 'finalizado.png')
        image_path = os.path.normpath(image_path)
        self.image = Image.open(image_path)
        self.image = self.image.resize((50, 50))
        self.image = ImageTk.PhotoImage(self.image)