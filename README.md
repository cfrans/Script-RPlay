# Script RPlay

Script feito para um serviço de um cliente específico em uma gráfica.  

O script solicita a quantidade de QR Codes que o cliente deseja gerar e move toda a próxima sequência atual na pasta predefinida, junto dos arquivos necessários para a produção dos mesmos.  

O mesmo também une todos os arquivos solicitados em um único PDF para facilitar o manuseio, e renomeia os arquivos de acordo com o número informado de Ordem de Produção.  

No final das contas o script é demasiadamente específico para o serviço que a gráfica faz, porém aqui está de qualquer forma por ter sido criado como um desafio e servindo de aprendizado na linguagem Python.  

### Dependências:  
PyPDF2 (Necessária)  
Colorama (Opcional)  

### Inputs, opções e variáveis:  
`changelog` - input a qualquer momento para ver o changelog.  
`exit` - input a qualquer momento para encerrar o script.  

`emptyCodesPath` - pasta em que os QR Codes gerados já estão salvos individualmente.  
`defaultFilesPath` - pasta em que os arquivos necessários para a produção estão salvos.  
`destinationOpFolder` - diretório em que a pasta da Ordem de Produção vai ser gerada  

`copyOrMove` - defina 'copy' para copiar os QR Codes ou 'move' para move-los.  
