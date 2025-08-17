###############################################################################
#
#   FUNÇÃO QUE IMPORTA E ORGANIZA DADOS LOTOFACIL DE PLANILHA EXCEL
#   No python e um DataFrame não é uma matriz
###############################################################################

# https://didatica.tech/o-pacote-pandas-python-para-machine-learning/
# https://www.analisededados.blog.br/2020/04/importando-excel-no-python-pandas.html

#import random  # biblioteca que trabalha com numeros aleatorios
import numpy as np
import pandas as pnd    # importando biblioteca Panda 

'''
# lista de comandos PANDAS
Lotofacil.shape                 # Quantidade de linhas e colunas do DataFrame
Lotofacil.index                 # Descrição do Index
Lotofacil.columns               # Colunas presentes no DataFrame
Lotofacil.count                 # Contagem de dados não-nulos
Lotofacil['Nova Coluna'] = 0    # Criando uma nova coluna
Lotofacil.loc[0, 'Concurso']    # Selecionando a primeira linha da primeira coluna 
'''

def LeExcel(Pulartestes, Nconcursos,  excelCEF):    

#    excelCEF = '000LotoFacilResultados_CEF.xlsx'
    
    " lendo toda a planilha excel das CEF"
    #Lotofacil = pnd.read_excel('caminho_do_arquivo\\nome_do_arquivo.xlsx')
    #Lotofacil = pnd.read_excel('000LotoFacilResultados_CEF.xlsx')

    " lendo só as colunas que nos interessam da planilha excel"
    lista_colunas = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
                     'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11',
                     'Bola12', 'Bola13', 'Bola14', 'Bola15']
#    Lotofacil = pnd.read_excel('000LotoFacilResultados_CEF.xlsx', usecols = lista_colunas)
    LotofacilCompleta = pnd.read_excel(excelCEF, usecols = lista_colunas)

    tabela = 0

    if tabela == 1:
        print (" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("1 - Matriz resultados lotofacil lido da Caixa Economica Federal (CEF)")
        print(LotofacilCompleta)
    
        type(LotofacilCompleta )       # Formato dos dados lidos da CEF 
    
        print( "dimensão da Dataframe LotoFacil = ", LotofacilCompleta.shape)   # imprime dimensão da Dataframe LotoFacil
        print (" ")
    
        print (" ")
        print (" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print (" ")


    ''' Método para converter Pandas dataframe  para NumPy Array '''
    # https://www.delftstack.com/pt/howto/python-pandas/how-to-convert-pandas-dataframe-to-numpy-array/
    LotofacilMatrizCompleta=LotofacilCompleta.to_numpy()
    
    # nlinhas  = len(LotofacilMatrizCompleta)
#    ncolunas = len(LotofacilMatrizCompleta[0])  
    # print('nlinhas =  ' , nlinhas , '     ncolunas =  ', ncolunas)
    
    #   nlinhas =   2488      ncolunas =   16    

#    LotofacilMatriz =  np.ones( [Nconcursos, ncolunas], dtype=np.float16)    
#    LotofacilMatriz =  np.zerosones( [Nconcursos, ncolunas], dtype=np.float16)
    LotofacilMatriz =  LotofacilMatrizCompleta[Pulartestes :(Nconcursos+Pulartestes ) , :] 
    
    #type(" 3 - Formado dos dados arquivados (tipo) ")
    #print(LotofacilMatriz.shape)    # imprime dimensão da Matriz LotoFacilMatriz  2450 x 16

    #type("1 - Matriz com os todos resultados da Lotofacil (LotofacilMatriz)")
    #print (LotofacilMatriz)

    #print(" ")

    if tabela == 1:
        print(" MATRIZ - PLANILHA DADOS RESULTADOS LOTOFACIL - 50 ULTIMOS CONCURSOS ")
        print(LotofacilMatriz)
        
        type(LotofacilMatriz)   # Tipo de dados
    
        print (" ")
        print (" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print (" ")


    return LotofacilMatriz