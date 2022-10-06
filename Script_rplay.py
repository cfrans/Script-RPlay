import os
import os.path
import getpass
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from distutils.dir_util import copy_tree


def check_quit(inp):
    if inp == 'exit':
        sys.exit(0)


def gerarQrCode(content):
    code = pyqrcode.create(
        "0" + str(content), error='M', version=1, mode='numeric')
    code.png(str(content) + ".png", scale=4)


def gerarPdf(content, nFinal):
    c.setPageSize((113.5, 227.2))
    c.drawInlineImage(str(content) + ".png", 10.196,
                      124.974, width=94.368, height=94.368)
    c.setFont("Arial-Bold", 12)
    c.drawCentredString(57.273, 123.063, "0" + str(content))
    c.setFont("Arial", 11)
    c.drawCentredString(57.273, 105, "__________")
    c.showPage()
    if content == nFinal:
        c.save()
        print(f"{(Fore.LIGHTBLACK_EX)}Salvando PDF...")


def atualizarLog(nInicial, nFinal, numeroOP):
   computerName = getpass.getuser()
   timeNow = (datetime.now().strftime('%d-%m-%Y %H:%M:%S')) # pega o horário atual para salvar no log
   logFile = open("Log.txt","a")
   logFile.write(f"{nInicial} ao {nFinal}. OP{numeroOP}. {timeNow}. {computerName}. \n")
   logFile.close()


def atualizarLastCode(nFinal):
    lastCode = open("lastcode.txt", "w")
    lastCode.write(str(nFinal))
    lastCode.close()


def verificaCodeCorreto(nInicial, nFinal, qtdFinal):
    if modoTeste == False:
        lastCode = open("lastcode.txt", "r")
        conteudoLastCode = lastCode.read()
        if nInicial <= int(conteudoLastCode):
            print(Back.RED + Fore.WHITE)
            print(f"ATENÇÃO: O número inicial é menor do que o último código já gerado ({conteudoLastCode}).")
            sys.exit(0)
        elif nInicial == (int(conteudoLastCode) + 1):
            print(Fore.GREEN)
            print(f"Sequência informada: {nInicial} ao {nFinal} ({qtdFinal} un.)")
            input("Aperte enter para confirmar")
        elif nInicial > (int(conteudoLastCode) + 1):
            print(Back.RED + Fore.WHITE)
            print(f"ATENÇÃO: O número inicial não é o próximo do último código já gerado ({conteudoLastCode}).")
            sys.exit(0)
        lastCode.close()
    else:
        print(f"Sequência informada: {nInicial} ao {nFinal} ({qtdFinal} un.)")
        input("Aperte enter para confirmar")


def instaladorDependencias():
    print("--------------------------------------------------")
    print("As bibliotecas Colorama, Reportlab, PyQRCode e pypng serão instaladas")
    input("Pressione enter para continuar")

    print("--------------------------------------------------")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'colorama'])
    print("--------------------------------------------------")
    print("Colorama instalado com sucesso.")

    print("--------------------------------------------------")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'reportlab'])
    print("--------------------------------------------------")
    print("Reportlab instalado com sucesso.")

    print("--------------------------------------------------")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'pyqrcode'])
    print("--------------------------------------------------")
    print("PyQRCode instalado com sucesso.")

    print("--------------------------------------------------")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'pypng'])
    print("--------------------------------------------------")
    print("Pypng instalado com sucesso.")
    print("Todas as tarefas foram concluídas.")
    print("--------------------------------------------------")

    print("Inicie novamente o script")
    sys.exit(0)


try:
    import pyqrcode
    from colorama import Back, Fore, Style, init
    from reportlab.pdfbase.pdfmetrics import registerFont
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ModuleNotFoundError:
        print('Algum módulo necessário não foi encontrado. Iniciando o instalador de dependências...')
        instaladorDependencias()

temp_dir = tempfile.TemporaryDirectory()  # define uma variavel para o temp dir
destinationOpFolder = os.getcwd()
defaultFilesPath = destinationOpFolder + "\\CODES_EM_BRANCO\\defaults_nao_alterar"
version = "2.0"
modoTeste = False

init() # inicializa as cores

print(Fore.GREEN + "----------------------------------------------")
print("Script RPlay " + Fore.LIGHTBLACK_EX + version + Fore.WHITE + " -- made by " + Fore.LIGHTRED_EX + "CFRANS " + Fore.BLUE + "(2022)")
print(Fore.GREEN + "----------------------------------------------")

if modoTeste == True:
    print(Back.WHITE, Fore.BLACK + "EXECUTANDO EM MODO DE TESTE " + Style.RESET_ALL)

numeroOPCorreto = False
while numeroOPCorreto == False:
    print(Fore.WHITE)
    numeroOP = input("Insira o número da OP: ")
    check_quit(numeroOP)
    try:
        string_int = int(numeroOP)
        numeroOPCorreto = True
    except ValueError:
        print((Back.RED) + (Fore.WHITE))
        print("Informe somente o número, sem letras.")
        print(Style.RESET_ALL)

nInicial = int(input("Insira o número inicial do QR Code: "))
nFinal = int(input("Insira o número final do QR Code: "))
qtdFinal = ((nInicial - nFinal) - 1) * -1

verificaCodeCorreto(nInicial, nFinal, qtdFinal)

start = time.time()

print(Fore.LIGHTBLACK_EX)

#cria as pastas da OP caso não existam
pastaOP = destinationOpFolder + "/OP" + str(numeroOP) + "/"
if not os.path.exists(pastaOP):
    print("Criando pasta da OP...")
    os.makedirs(pastaOP)

# copia os arquivos padrao para a pasta da OP
print("Copiando arquivos padrão...")
copy_tree(defaultFilesPath, pastaOP)
os.chdir(pastaOP)
os.rename("rplay.job", "rplay_OP" + str(numeroOP) + ".job")

os.chdir(temp_dir.name)  # muda o current dir para o temp dir
registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))  # registra a arial bold
registerFont(TTFont('Arial', 'arial.ttf'))  # registra a arial
c = canvas.Canvas(f"{nInicial} ao {nFinal} (OP{numeroOP}).pdf") # inicia a página do canvas

print(Fore.WHITE)
print(f"Gerando {qtdFinal} códigos. Favor aguardar...")

for code in range(nInicial, (nFinal + 1)):
    porcentagem = (100 * ((code - nInicial) + 1)) / qtdFinal
    print(f"Gerando código {(code - nInicial) + 1} de {qtdFinal} {Fore.GREEN}({porcentagem:.2f}%){Style.RESET_ALL}...")
    gerarQrCode(code)
    gerarPdf(code, nFinal)

shutil.move((f"{nInicial} ao {nFinal} (OP{numeroOP}).pdf"), pastaOP)

os.chdir(destinationOpFolder)
if modoTeste == False:
    atualizarLog(nInicial, nFinal, numeroOP)
    atualizarLastCode(nFinal)

temp_dir.cleanup()

end = time.time()

print(Fore.LIGHTBLACK_EX)
print(f"Conclúido em {end - start:.2f} segundos.")
print("De qualquer forma lembre-se de conferir o conteúdo gerado.")
