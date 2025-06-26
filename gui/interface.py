import customtkinter as ctk
import webbrowser
from functools import partial
from tkinter import messagebox
import sys
import os

class Automation:

    @staticmethod
    def close_loading(config):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f'root:{root_path}')
        if root_path not in sys.path:
            sys.path.insert(0, root_path)
            print(f'sys_path: {sys.path}')
        from image.start_gif import FinishedGif
        finished = FinishedGif(config)

    @staticmethod
    def open_loading(loading):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f'root:{root_path}')
        if root_path not in sys.path:
            sys.path.insert(0, root_path)
            print(f'sys_path: {sys.path}')
        from image.start_gif import Configs
        configs = Configs(loading)
        return configs

    def open_gui(self):
        interface = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(interface))
        global JanelaCredenciais
        from credencial_interface import JanelaCredenciais
        
    def pagamento_pix(self):
        # Implementar a lógica para efetuar pagamento via chave Pix
        messagebox.showinfo('Atenção', 'Função Pix ainda não implementada.\nO recurso será desenvolvido caso a empresa aprove sua utilização.')

    def automacao(self, modo):
        # chama a automação
        Automation.open_gui(self)
        JanelaCredenciais(master=None, modo=modo)

class Interface:
    def __init__(self):
        self.janela = ctk.CTk()
        Automation.open_gui(self)
        self.configure()
        self.text()
        self.button()
        AnimationLoading(self.janela, ativar_loading=bool)

    def configure(self):

        #configuração para a janela ficar centralizada
        largura_monitor = self.janela.winfo_screenwidth()
        altura_monitor = self.janela.winfo_screenheight()
        if largura_monitor >= 1920 and altura_monitor >= 1080:
            largura = 500
            altura = 400
            x = (largura_monitor // 2) - (largura // 2)
            y = (altura_monitor // 2) - (altura // 2)
        elif largura_monitor >= 1366 and altura_monitor >= 768:
            largura = 500
            altura = 400
            x = (largura_monitor // 2) - (largura // 2)
            y = (altura_monitor // 2) - (altura // 2)
        #finaliza aqui essa configuração

        self.janela.title("Automação 2.0")
        self.janela.pack_propagate(True)
        self.janela.resizable(False, False)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")
        

    def button(self):
        self.frame_button = ctk.CTkFrame(self.janela, fg_color='transparent', width=300)
        self.frame_button.pack(pady=(125, 10))
        espaco = 6
        ctk.CTkButton(self.frame_button, text="Consultar Fatura", font=('arial', 14, 'bold'), height=30, width=240, command=partial(Automation.automacao, self, modo=1)).pack(pady=(0, espaco), fill='x')
        ctk.CTkButton(self.frame_button, text='Imprimir Boleto', font=('arial', 14, 'bold'), command=lambda: Automation.automacao(self, modo=2), height=30, width=240).pack(pady=(0, espaco), fill='x')
        ctk.CTkButton(self.frame_button, text='Baixar Boleto', font=('arial', 14, 'bold'), command=lambda: Automation.automacao(self, modo=3), height=30, width=240).pack(pady=(0, espaco), fill='x')
        ctk.CTkButton(self.frame_button, text='Efetuar Pagamento via Pix', font=('arial', 14, 'bold'), command=lambda: Automation.pagamento_pix(self), height=30, width=240).pack(pady=(0, espaco), fill='x')
        ctk.CTkButton(self.frame_button, text='Sair', font=('arial', 14, 'bold'), fg_color='red', hover_color='#B22222', height=30, width=240, command=self.janela.destroy).pack(pady=(10, 0), fill='x')
        #direciona para meu instagram
        ctk.CTkButton(self.janela, text='Criador', font=('arial', 14, 'bold'), fg_color='transparent', text_color='black', hover=False, command=lambda:webbrowser.open_new('https://www.instagram.com/h3r1ck00?igsh=M29pZms5MXAxaWU%3D&utm_source=qr'), height=30, width=50).place(x=215, y=360)

    def text(self):
        ctk.CTkLabel(self.janela, text='Automação de boleto\nCine Net', font=('arial', 30, 'bold'), text_color='black').place(y=30, x=100)

class AnimationLoading:
    def __init__(self, janela, ativar_loading):

        self.janela = janela
        self.loading = ctk.CTkLabel(self.janela, text='', font=('arial', 12, 'bold'))
        self.loading.place(x=400, y=290)

        self.configs = None

        if ativar_loading == 1:
            print('[DEBUG] Animação de carregamento ativada')
            self.configs = Automation.open_loading(self.loading)
            print(f'[DEBUG] Configs: {self.configs}')
        elif ativar_loading == 0:
            if self.configs is None:
                print('[DEBUG] Configs não inicializadas, criando nova instância')
                self.configs = Automation.open_loading(self.loading)
            print('[DEBUG] Animação de carregamento desativada')
            Automation.close_loading(self.configs)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    messagebox.showinfo('Bem-vindo', 'Informações sobre o software:\n\nEste software foi desenvolvido para automatizar a consulta de boletos da provedora Cine Net.\n\nDesenvolvido por Herick Müller.\n\nObs.: Para que o desenvolvedor seja alertado sobre falhas. Por favor, tenha o Whatsapp web conectado em seu navegador')
    Interface()