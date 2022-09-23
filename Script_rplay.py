import glob
import importlib.util
from PyPDF2 import PdfFileMerger
from distutils.dir_util import copy_tree
import shutil
import os.path
import tempfile
import sys
import os
emptyCodesPath = "D:/CLIENTES/RPlay/CODES_EM_BRANCO/codes_em_branco/"
defaultFilesPath = "D:/CLIENTES/RPlay/CODES_EM_BRANCO/defaults_nao_alterar/"
destinationOpFolder = "D:/CLIENTES/RPlay/"
copyOrMove = "copy"

version = "1.3"


def check_changelog(inp):
    if inp == "changelog":
        print("1.0 - First release.")
        print("1.1 - Added color support as optional, added loops when values are not expected.")
        print("1.2 - Implemented a temp folder.")
        print("1.3 - Template now is renaming itself, added warning if running in copy mode.")


temp_dir = tempfile.TemporaryDirectory()

colors = True

try:
    from colorama import Back, Fore, Style, init
except Exception:
    colors = False

if colors == True:
    init()
    print(Fore.LIGHTBLACK_EX)

# confirma se o módulo necessário está instalado
if "PyPDF2" in sys.modules:
    print("Módulo PyPDF2 já está carregado.")
elif (spec := importlib.util.find_spec("PyPDF2")) is not None:
    # If you choose to perform the actual import ...
    module = importlib.util.module_from_spec(spec)
    sys.modules["PyPDF2"] = module
    spec.loader.exec_module(module)
    # if colors == True:
    #     print(Fore.GREEN)
    # print("Módulo PyPDF2 carregado com sucesso.")
else:
    if colors == True:
        print(Fore.RED)
    print("Módulo PyPDF2 não encontrado, o programa nao irá funcionar corretamente. Contate o administrador.")
    print("Encerrando script")
    sys.exit(0)

# função para fechar o script a qualquer momento


def check_quit(inp):
    if inp == 'exit':
        sys.exit(0)


# -----------------------------------------------------------------------------------------------------


if colors == True:
    print(Fore.GREEN + "----------------------------------------------")
    print("Script RPlay " + Fore.LIGHTBLACK_EX + version + Fore.WHITE +
          " -- made by " + Fore.LIGHTRED_EX + "CFRANS " + Fore.BLUE + "(2022)")
    print(Fore.GREEN + "----------------------------------------------")
else:
    print("----------------------------------------------")
    print("Script RPlay " + version + " -- made by CFRANS (2022)")
    print("----------------------------------------------")

numeroOPCorreto = False

if copyOrMove == "copy":
    if colors == True:
        print(Back.WHITE, Fore.BLACK + "ATENÇÃO - SCRIPT EM MODO COPY")
        print(Style.RESET_ALL)
    else:
        print("ATENÇÃO - SCRIPT EM MODO COPY")

while numeroOPCorreto == False:
    if colors == True:
        print(Fore.WHITE)
    numeroOP = input("Insira o número da OP: ")
    check_quit(numeroOP)
    check_changelog(numeroOP)
    try:
        string_int = int(numeroOP)
        numeroOPCorreto = True
    except ValueError:
        if colors == True:
            print(Back.RED)
            print(Fore.WHITE)
        print("Informe somente o número, sem letras.")
        if colors == True:
            print(Style.RESET_ALL)

if colors == True:
    print(Fore.WHITE)
nCodes = int(input("Informe a quantidade de codes: "))
check_quit(nCodes)
nCodesConfirma = int(input("Confirme a quantidade de codes: "))
check_quit(nCodesConfirma)

# confirmaçao de numero de códigos para tentar barrar erro de digitaçao
while nCodes != nCodesConfirma:
    if colors == True:
        print(Back.RED)
        print(Fore.WHITE)
    print("A quantidade confirmada não é a mesma.")
    if colors == True:
        print(Style.RESET_ALL)
    nCodes = int(input("Informe a quantidade de codes: "))
    check_quit(nCodes)
    nCodesConfirma = int(input("Confirme a quantidade de codes: "))
    check_quit(nCodesConfirma)

# confirma a divisibilidade de 250, que é a quantidade mais comum de pedidos
if (nCodes % 250) != 0:
    if colors == True:
        print(Fore.YELLOW)
    print("A quantidade não é divisível por 250. Deseja continuar mesmo assim?")
    if colors == True:
        print(Fore.WHITE)
    input("Aperte enter para continuar...")

# confirma se existe a quantidade solicitada já gerada na pasta
filelist = glob.glob(emptyCodesPath + "*.pdf")
quantidadeCodesDisponiveis = (len(filelist))
if quantidadeCodesDisponiveis < nCodes:
    if colors == True:
        print(Back.RED)
        print(Fore.WHITE)
    print("ERRO: A quantidade de códigos gerados na pasta é menor do que a quantidade solicitada.")
    sys.exit(0)

# alerta se a quantidade de codes disponiveis for menos de 500
if quantidadeCodesDisponiveis <= 500:
    if colors == True:
        print(Fore.YELLOW)
    print("Aviso: a quantidade de codes disponíveis está abaixo de 500. Considere gerar mais.")
    if colors == True:
        print(Fore.WHITE)
    input("Aperte enter para continuar...")

if colors == True:
    print(Fore.GREEN)
print("Executando...")

# cria as pastas da OP caso não existam
pasta = destinationOpFolder + "OP" + str(numeroOP)
if not os.path.exists(pasta):
    os.makedirs(pasta)

# verifica se já existe o arquivo dos codes em branco na pasta da op
if glob.glob(destinationOpFolder + "OP" + str(numeroOP) + "/Codes_sem_logo_OP" + str(numeroOP) + ".pdf"):
    print("Já existe um arquivo com os códigos em branco para esta OP.")
    sys.exit(0)

copy_tree(defaultFilesPath, destinationOpFolder + "OP" + str(numeroOP) + "/")

# código para copiar a quantidade informada de codes
p1 = emptyCodesPath
p2 = (temp_dir.name)

for path, folders, files in os.walk(p1):

    for file_ in files[:nCodes]:
        # if not files: continue

        src = os.path.join(path, file_)
        dst_path = path.replace(p1, '') + os.sep
        dst_folder = p2 + dst_path

        # create dst file with only the first file
        dst = p2 + dst_path + file_

        # copy or move the file
        if copyOrMove == "move":
            shutil.move(src, dst)
        if copyOrMove == "copy":
            shutil.copy2(src, dst)

# merge function
# muda o current work directory
os.chdir(temp_dir.name)

x = [a for a in os.listdir() if a.endswith(".pdf")]

merger = PdfFileMerger(strict=False)

for pdf in x:
    merger.append(open(pdf, 'rb'))

# muda o current work directory
os.chdir(destinationOpFolder + "OP" + str(numeroOP) + "/")

with open("Codes_sem_logo_OP" + str(numeroOP) + ".pdf", "wb") as fout:
    merger.write(fout)

# remove os arquivos temporários
temp_dir.cleanup()

# renomeia o arquivo do template
os.rename("rplay.job", "rplay_OP" + str(numeroOP) + ".job")

if colors == True:
    print(Fore.BLUE + "---------------------------------------")
    print("Concluído.")
    print("---------------------------------------")
    print(Fore.YELLOW + "De qualquer forma, lembre-se de conferir se a numeração dos códigos está correta!")
    print("---------------------------------------")
    print(Back.WHITE, Fore.BLACK + "Pressione enter para fechar esta janela")
else:
    print("---------------------------------------")
    print("Concluído.")
    print("---------------------------------------")
    print("De qualquer forma, lembre-se de conferir se a numeração dos códigos está correta!")
    print("---------------------------------------")
    print("Pressione enter para fechar esta janela")
