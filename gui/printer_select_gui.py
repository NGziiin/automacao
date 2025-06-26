import customtkinter as ctk
import os, sys
import subprocess
import win32print
from pathlib import Path
from tkinter import messagebox
from functools import partial
import plyer
import threading

SUMATRA_PATH = os.path.join(os.getcwd(), 'tools', 'SumatraPDF.exe')  # configure aqui o caminho para o SumatraPDF

class FPrinter:
    def __init__(self):
        pass

    def popups_finished(self):
        automation = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(automation, '..'))
        from gui.popups.finished import FinishedPopup
        self.finished_popup = FinishedPopup(master=None)

    # Função para obter o arquivo mais recente na pasta Downloads
    def get_latest_file(self, download_folder):
        files = [os.path.join(download_folder, f) for f in os.listdir(download_folder)]
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            return None
        return max(files, key=os.path.getmtime)
    
    #enviando para a impressora selecionada
    def print_with_selected_printer(self, file_path, printer_name, parent_window):
        try:
            if not os.path.exists(SUMATRA_PATH):
                raise FileNotFoundError("[ERRO] SumatraPDF não encontrado.")

            subprocess.Popen([
                SUMATRA_PATH,
                "-print-to", printer_name,
                file_path
            ], shell=True)

            plyer.notification.notify(
                title='Impressão',
                message=f'Arquivo enviado para a impressora: {printer_name}',
                timeout=10,
                toast=True
            )
            print(f"[DEBUG] Arquivo '{file_path}' enviado para impressora '{printer_name}'")
            parent_window.destroy()
            threading.Thread(target=self.popups_finished, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao imprimir: {e}")

    #onde inicia a impressão
    def start_print(self, printer_combobox, parent_window):
        printer = printer_combobox.get()
        if not printer:
            messagebox.showwarning("Aviso", "Selecione uma impressora.")
            return

        latest_file = self.get_latest_file(str(Path.home() / "Downloads"))
        if not latest_file:
            messagebox.showwarning("Aviso", "Nenhum arquivo encontrado na pasta Downloads.")
            return

        self.print_with_selected_printer(latest_file, printer, parent_window)


class Interface(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        #configurando para a janela ficar em um local específico
        largura_monitor = self.winfo_screenwidth()
        altura_monitor = self.winfo_screenheight()
        if largura_monitor >= 1920 and altura_monitor >= 1080:
            largura = 400
            altura = 200
            x = (largura_monitor // 2) - (largura // 2) + 460
            y = (altura_monitor // 2) - (altura // 2)
            #finaliza aqui essa configuração
        elif largura_monitor >= 1366 and altura_monitor >= 768:
            largura = 400
            altura = 200
            x = (largura_monitor // 2) - (largura // 2)
            y = (altura_monitor // 2) - (altura // 2)
        #finaliza aqui essa configuração

        self.title("Imprimir Arquivo")
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()

        self.fprinter = FPrinter()

        printer_list = [printer[2] for printer in win32print.EnumPrinters(2)]

        ctk.CTkLabel(self, text="Selecione uma impressora:", font=('Arial', 14)).pack(pady=10)
        self.printer_combobox = ctk.CTkComboBox(self, values=printer_list, width=300)
        self.printer_combobox.pack(pady=5, padx=20)

        ctk.CTkButton(
            self, 
            text="Imprimir", 
            command=partial(self.fprinter.start_print, self.printer_combobox, self)
        ).pack(pady=20)

    def on_closing(self):
        self.destroy()