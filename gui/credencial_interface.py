import customtkinter as ctk
from tkinter import messagebox
from functools import partial
import os
import sys
import threading

class JanelaCredenciais(ctk.CTkToplevel):

    def __init__(self, master, modo, callback_cancelar=None):
        super().__init__(master)
        self.modo = modo # 1 para consulta, 2 para impressão e 3 para download 
                         ## >>>>>> NÃO REMOVER DE MANEIRA ALGUMA!!! 
                         ### SE REMOVER QUEBRA O SOFTWARE 

        #configurando para a janela ficar em um local específico
        largura_monitor = self.winfo_screenwidth()
        altura_monitor = self.winfo_screenheight()
        if largura_monitor >= 1920 and altura_monitor >= 1080:
            largura = 300
            altura = 280
            x = (largura_monitor // 4) - (largura // 4)
            y = (altura_monitor // 4) - (altura // 4) + 140
            #finaliza aqui essa configuração
        elif largura_monitor >= 1366 and altura_monitor >= 768:
            largura = 300
            altura = 280
            x = (largura_monitor // 4) - (largura // 4) - 135
            y = (altura_monitor // 4) - (altura // 4) + 62

        #finaliza aqui essa configuração

        self.title("Credenciais")
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.lift()
        self.grab_set()
        

        ctk.CTkLabel(self, text="Digite o CPF ou CNPJ:", font=('Arial', 14)).pack(pady=10)
        self.entrada = ctk.CTkEntry(self, placeholder_text="000.000.000-00 ou 00.000.000/0000-00")
        self.entrada.pack(pady=5, padx=20, fill='x')

        ctk.CTkButton(self, text="Prosseguir", command=partial(self.salvar, self.entrada, self.modo)).pack(pady=5, fill='x', padx=20)
        ctk.CTkButton(self, text="Cancelar", fg_color="red", hover_color='#B22222', command=partial(self.cancelar, callback_cancelar)).pack(pady=5, fill='x', padx=20)

    def get_class(self):
        automation = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(automation, '..'))
        global Consultar_boleto
        global ImprimirBoleto
        global BaixarBoleto
        from automation.consultar import Consultar_boleto
        from automation.imprimir import ImprimirBoleto
        from automation.baixar import BaixarBoleto

    def salvar(self, entrada, modo):
        print("[DEBUG] Clique no botão INICIAR")
        valor = entrada.get()
        self.get_class()
        if valor:
            if modo == 1:
                print(f'[DEBUG] Modo de consulta: {modo}')
                self.destroy()
                threading.Thread(target=Consultar_boleto, args=(valor, self), daemon=True).start()
            elif modo == 2:
                print(f'[DEBUG] Modo de impressão: {modo}')
                self.destroy()
                threading.Thread(target=ImprimirBoleto, args=(valor, self), daemon=True).start()
            elif modo == 3:
                print(f'[DEBUG] Modo de download: {modo}')
                self.destroy()
                threading.Thread(target=BaixarBoleto, args=(valor, self), daemon=True).start()
        if not valor:
            messagebox.showerror("Erro", "O campo não pode estar vazio.")

    def cancelar(self, callback):
        if callback:
            callback()
        self.destroy()