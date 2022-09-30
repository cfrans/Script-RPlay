# Script RPlay 2.0

Script feito para um serviço de um cliente específico em uma gráfica.  

O script gera os QR Codes de acordo com a última sequência feita (conferindo o último número no arquivo `lastcode.txt`), e com a quantidade que o cliente deseja e também copia arquivos necessários para a pré impressão. 

O mesmo também une todos os códigos gerados em um único PDF para facilitar o manuseio, e renomeia os arquivos de acordo com o número informado de Ordem de Produção.  

O script por padrão gera um log contendo a sequência gerada, o número da OP, o dia e horário e o nome do usuário da máquina.

No final das contas o script é demasiadamente específico para o serviço que a gráfica faz, porém aqui está de qualquer forma por ter sido criado como um desafio e servindo de aprendizado na linguagem Python.  

### Dependências:  
(O script possui um instalador integrado de dependências necessárias, usando o PIP.)

Reportlab  
Colorama  
PyQRCode  

### Inputs, opções e variáveis:  
`exit` - input a qualquer momento para encerrar o script.  

`defaultFilesPath` - pasta em que os arquivos necessários para a impressão estão salvos.  

`modoTeste` - faz com que o script ignore o processo de verificação do último code, e também não crie um registro no "Log.txt".  
