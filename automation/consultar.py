from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import datetime
import plyer
from tkinter import messagebox
import pywhatkit
from cryptography.fernet import Fernet
import os
import sys
import time
import threading


class Utils:
    def __init__(self, chave):
        self.chave = chave

    def proc_log(self):
        self.chave = Fernet.generate_key()
        f = Fernet(self.chave)
        self.login = f.encrypt(self.login.encode())

    def dec_log(self):
        f = Fernet(self.chave)
        self.login = f.decrypt(self.login).decode()

    def select_printer(self):
        janelaPrinter = getattr(sys, '__MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        os.path.join(janelaPrinter, 'gui')
        from gui.printer_select_gui import Interface
        interface = Interface(master=None)

    def verificar_download(self, web):
        pasta_downloads = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        arquivos_antes = set(os.listdir(pasta_downloads))  # arquivos antes do download começar
        tempo_inicial = time.time()
        timeout = 60  # segundos
        print('[DEBUG] Aguardando término do download...')
        while True:
            arquivos_atual = set(os.listdir(pasta_downloads))
            novos_arquivos = arquivos_atual - arquivos_antes
            arquivos_pdf = [f for f in novos_arquivos if f.lower().endswith('.pdf')]
            arquivos_crdownload = [f for f in arquivos_atual if f.lower().endswith('.crdownload')]
            if arquivos_pdf and not arquivos_crdownload:
                print(f'[DEBUG] Download finalizado: {arquivos_pdf[0]}')
                plyer.notification.notify(
                    title='Download Concluído',
                    message=f'Arquivo baixado: {arquivos_pdf[0]}',
                    app_icon=None,
                    timeout=3,
                    toast=True
                )
                web.quit()
                break
            if time.time() - tempo_inicial > timeout:
                print('[ERRO] Tempo limite atingido aguardando download.')
                break
            time.sleep(1)

    def popups_alert(self):
        automation = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(automation, '..'))
        from gui.popups.printer_alert import Alerta
        self.printer_alert = Alerta(master=None)

    def popups_finished(self):
        automation = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(automation, '..'))
        from gui.popups.finished import FinishedPopup
        self.finished_popup = FinishedPopup(master=None)

    @staticmethod
    def animacao_loading(self):
        initial_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f'[DEBUG] Caminho inicial: {initial_path}')
        ativar_loading = self.ativar_loading
        if initial_path not in sys.path:
            sys.path.insert(0, initial_path)
            print(f'[DEBUG] Caminho adicionado ao sys.path: {initial_path}')
        from gui.interface import AnimationLoading
        animacao = AnimationLoading(None, ativar_loading)
        print(f'[DEBUG] variável ativar_loading: {ativar_loading}')

class Consultar_boleto:

    def __init__(self, valor, master):
        self.ativar_loading = 1
        threading.Thread(target=Utils.animacao_loading, args=(self,), daemon=True).start()
        self.url = 'https://cinenetcb.sgp.net.br/accounts/central/login'
        self.login = valor
        self.master = master
        Utils.proc_log(self)
        print(f'[DEGUB] Iniciando consulta para: {self.login}')
        plyer.notification.notify(title='Automação', message='Iniciando a consulta!', app_icon=None, timeout=2, toast=True)
        self.Settings_webBrowser()
        self.starting()

    def Settings_webBrowser(self):
        print(f'[DEBUG] consultando fatura: {self.login}')
        self.options = Options()
        self.options.add_argument('--headless')
        self.web = webdriver.Chrome(options=self.options)
        self.dia_atual = datetime.datetime.now()
        self.mes_atual = self.dia_atual.strftime('%m')

    def starting(self):
        try:
            print(f'[DEBUG] Iniciando o acesso ao site: {self.url}')
            self.web.get(self.url)
            print(f'[DEBUG] Acessando o site com a variável: {self.login}')
            Utils.dec_log(self)
            self.login = self.web.find_element(By.ID, 'cpfcnpj').send_keys(self.login)
            self.login = self.web.find_element(By.TAG_NAME, 'button').click()
            self.web.implicitly_wait(10)
            try:
                self.web.find_element(By.XPATH, '//div[@class="alert text-light bg-danger fade show"]')
                print(f'[DEBUG] Erro ao logar, verifique o CPF ou CNPJ')
                self.ativar_loading = 0
                threading.Thread(target=Utils.animacao_loading, args=(self,), daemon=True).start()
                messagebox.showerror('Erro', 'CPF ou CNPJ inválido ou não cadastrado.')
                return
            except NoSuchElementException:
                pass
            print(f'[DEBUG] Logado com sucesso')
            self.web.implicitly_wait(10)
            self.payment = self.web.find_element(By.XPATH, '//h6[@class="font-size-sm mb-0"]')
            self.payment = self.payment.text
            print(f'[DEBUG] Boleto encontrado: {self.payment}')
            print(f'[DEBUG] Variável mes_atual: {self.mes_atual}')

            if self.mes_atual in self.payment:
                print('[DEBUG] boleto encontrado')
                verificar_pagamento = self.web.find_element(By.XPATH, '//span[@class="small text-primary"]').text
                if verificar_pagamento == 'pendente' or verificar_pagamento == 'Aberto':
                    print('[DEBUG] boleto pendente')
                    threading.Thread(target=Utils.popups_alert, args=(self,), daemon=True).start()
                    self.master.after(5000, self.confirmacao)

            elif self.mes_atual != self.payment:
                print(f'[DEBUG] Boleto do mês posterior')
                messagebox.showinfo('Dados', 'Só possui o boleto do Mês posterior')

        except Exception as e:
            print(f'[ERRO] o sistema deu erro na parte - {e}')
            pywhatkit.sendwhatmsg_instantly('+5562994780976', '[SISTEMA] O sistema de verificar boleto deu erro')
            try:
                os.remove('PyWhatKit_DB.txt')
                sys.exit(0)
            except FileNotFoundError:
                sys.exit(0)

    def confirmacao(self):
        download = messagebox.askyesno("Automação", "Deseja imprimir o boleto?\n\nSIM ---> para imprimir\n\nNÃO ---> para continuar.")
        print(f'[DEBUG] download: {download}')
        if download == True:
            print("[DEBUG] iniciando a impressão do boleto")
            self.imprimir_boleto()
            pass
        elif download == False:
            download = messagebox.askyesno("Automação", "Deseja baixar o boleto?\n\nSIM ---> para baixar\n\nNÃO ---> para sair.")
            if download == True:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.abspath(os.path.join(base_dir, '..',  'image', 'finalizado.ico'))
                print("[DEBUG] iniciando o download do boleto")
                self.download_boleto()
                plyer.notification.notify(
                    title='Finalizado com Sucesso',
                    message='Obrigado por utilizar o meu software\nAss.: Herick Müller',
                    app_icon=image_path,
                    timeout=15,
                )
            elif download == False:
                print("[DEBUG] Saindo do sistema")
                self.web.quit()
                self.ativar_loading = 0
                threading.Thread(target=Utils.animacao_loading, args=(self,), daemon=True).start()

    #inicia a impressão do boleto    
    def imprimir_boleto(self):
        try:
            print(f'[DEBUG] Iniciando o download do boleto')
            self.web.find_element(By.XPATH, '//a[@class="btn btn-xs btn-primary"]').click()
            print(f'[DEBUG] Download iniciado')
            Utils.verificar_download(self, self.web)
            self.ativar_loading = 0
            threading.Thread(target=Utils.animacao_loading, args=(self,), daemon=True).start()
            Utils.select_printer(self)

        except Exception as e:
            print(f'[ERRO] erro ao baixar boleto - {e}')
            pywhatkit.sendwhatmsg_instantly('+5562994780976', f'[SISTEMA] O sistema de baixar boleto deu erro ----- ({e})')
            try:
                os.remove('PyWhatKit_DB.txt')
                sys.exit(0)
            except FileNotFoundError:
                sys.exit(0)

    def download_boleto(self):
        try:
            plyer.notification.notify(
                title='Automação',
                message='Iniciando o download do boleto!',
                app_icon=None,
                timeout=5,
                toast=True
            )
            print(f'[DEBUG] Iniciando o download do boleto')
            self.web.find_element(By.XPATH, '//a[@class="btn btn-xs btn-primary"]').click()
            print(f'[DEBUG] Download iniciado')
            Utils.verificar_download(self, self.web)
            self.ativar_loading = 0
            threading.Thread(target=Utils.animacao_loading, args=(self,), daemon=True).start()
            self.web.quit()
            os.startfile(os.path.join(os.path.expanduser('~'), 'Downloads'))

        except Exception as e:
            print(f'[ERRO] erro ao baixar boleto - {e}')
            pywhatkit.sendwhatmsg_instantly('+5562994780976', f'[SISTEMA] O sistema de baixar boleto deu erro {e}')
            try:
                os.remove('PyWhatKit_DB.txt')
                sys.exit(0)
            except FileNotFoundError:
                sys.exit(0)