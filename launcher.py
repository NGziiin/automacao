import os
import sys
import subprocess

def main():
    starting = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    start = os.path.join(starting, 'gui', 'interface.py')
    subprocess.Popen([sys.executable, start])

if __name__ == "__main__":
    main()
    # A classe Automation não é instanciada aqui, pois parece fazer parte da lógica da interface.
    # # Se necessário, você pode instanciá-la na classe Interface ou em outro lugar conforme necessário.