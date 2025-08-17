import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd

#############################################################################
#   DEFININDO PERIODO DE FUNCIONAMENTO DO APP - GuiaLotofacil
# Janela prompt Anaconda pea gerar executável - 
# RODAR NA PASTA => C:\Users\Public\Executável

# => pip install pyinstaller
# SALVA COM NOVO NOME GuiaLotoFacil_v0.py
# pyinstaller --onefile GuiaLotoFacil_v0.py


############### UM MES DE TESTE => É PARA CONTROLE D E VIRUS ROUBAR E COMPIAR ARQUIVO

import os
import datetime

# Define o caminho do arquivo que armazenará a data de instalação
# C:\Users\Public\Executável  - isirir finão de data ou  deixar dentro programa MAIN

# Obtém a data e hora atual 
now = datetime.datetime.now()
print ("HOJE SERÁ  O DIA DE SUA GRANDE SORTE = ", now)


installation_date_file = 'install_date.txt'
def get_installation_date():
    if os.path.exists(installation_date_file):
        with open(installation_date_file, 'r') as file:
            install_date = file.readline().strip()
            return datetime.datetime.strptime(install_date, '%Y-%m-%d')
    else:
        install_date = datetime.datetime.now()
        with open(installation_date_file, 'w') as file:
            file.write(install_date.strftime('%Y-%m-%d'))
        return install_date

def check_expiration():
    install_date = get_installation_date()
    current_date = datetime.datetime.now()
    if current_date > install_date + datetime.timedelta(weeks=4):
        print("O período de quatro semanas expirou. Por favor, entre em contato para obter uma nova versão.")
        return True
    else:
        print("O programa está dentro do período de validade.")
        return False

#########################

def main():
    if check_expiration():
        return
    # Coloque aqui o restante do seu código principal do programa
    print("Executando o programa...")

if __name__ == '__main__':
    main()

#############################################################################

def iniciar_programaPRINCIPAL():
# dentro da função está o programa que executará toda a análise estatisca dos concursos lotofacil
    global concurso_inicial
    global qdadetestes
    global ConcursosResultados
    global lotofacil_referencia
    
    nome_planilha = entry_nome_planilha.get()
    qtd_concursos = int(entry_qtd_concursos.get())
    concurso_referencia = int(entry_concurso_referencia.get())
    
    # Carregar a planilha
    planilha = pd.read_excel(nome_planilha) 
    
    # Selecionar e guardar as linhas referentes aos concursos e às colunas das bolas
    linhas_bolas = planilha[['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']]

    # Convertendo as linhas de bolas selecionadas para uma matriz temporária
    matriz_temp = linhas_bolas.values

    # Ordenar a matriz temporária pelo número do concurso (primeira coluna)
    matriz_temp = matriz_temp[matriz_temp[:, 0].argsort()[::-1]]

    # número de concurso da planilha - linhas
    total_concursos = matriz_temp.shape[0]
    
    # Dados que serão lidos na interface inicial que irá abrir para rodar o programa
    concurso_inicial = concurso_referencia
    qdadetestes = qtd_concursos
    ConcursosResultados = np.zeros([qdadetestes, 16], dtype=int)
    lotofacil_referencia = np.zeros([16], dtype=int)
    vetor_concurso_inicial = np.zeros([16], dtype=int)  # vetor concurso digitado tela e primeira linha interface grafica 

    # Loop para encontrar o concurso desejado
    # aqui o lotofacil_referencia_será usado para confrontar com NUMEROS ESCOLHIDOS
    # ESSE LOOP VAI COPIAR A PARTIR DO CONCURSO DIGITADO, OS OUTROS 25 ANTERIORES.
    # if => DEPOIS DE CHECAR E ENCONTRAR O CONCURSO, E COPIAR NA MATRIZ ConcursoResulatados, 
    # ele entra em um segundo IF para checar se o digitado é o ultimo concurso realizado e que esta 
    # do escel lotofacil da CEF.
    # => se for igual ou seja não tem concurso futuro para checar uma previsao de acertos futuros
    # ele usa o mesmo como referencia [0,:], caso contrario ele copia normalmente o lotofacil_referencia
    
    
    for i in range(total_concursos):
        if matriz_temp[i, 0] == concurso_inicial:  # SE CONCURSO DIGITADO IGUAL LOTOFACIL INICIA COPIA 25 ANTERIORES
            vetor_concurso_inicial = matriz_temp[i, :]   # SALVA E COPIA O CONCURSO - PRIMEIRA DA INTERFACE GRAFICA
            ConcursosResultados = matriz_temp[i:i+qdadetestes]
            if concurso_inicial == matriz_temp[0, 0]:  # Quando último concurso, ele mesmo será referência
                lotofacil_referencia = matriz_temp[0, :]
            else:
                lotofacil_referencia = matriz_temp[i-1, :]
            break
  
    print("Matriz Temporária:", matriz_temp)  # Imprime a matriz temporária no console
    print("ConcursosResultados" , ConcursosResultados)
    print("qdadetestes =", qdadetestes)
    print("concurso_inicial =", concurso_inicial)
    print("lotofacil_referencia =", lotofacil_referencia[0])
    # JOGO LOTOFACIL DE REFERENCIA PAR OS PLOTS
    concurso_referencia = lotofacil_referencia
    print("LOTOFACIL DE REFERENCIA =", lotofacil_referencia)

    #vetor que aparece na primeira linha da interface grafica    
    vetor_concurso_inicial = ConcursosResultados[0,:]
    print("vetor_concurso_inicial = ", vetor_concurso_inicial)

    
    
    # global qdadetestes
    # bolas   = 15 # qdade de bolas sorteadas - Pode ser Sairam 15 - NSairam 10
    #numeros = 25 # qdade numeros total do da loteria - lotofail 26, megasena 60 ...
    #qdadetestes = 25 # numero de concursos usado para analise


    # Definindo a constante de cor
    COR_PADRAO = "lightgray"
    COR_VERDE = "green"
    COR_VERMELHO = "red"


    global UltimoConcurso
    Fibonacci = [1, 2, 3, 5, 8, 13, 21]
    Primos    = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    Moldura   = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
    Multiplo  = [3, 6, 9, 12, 15, 18, 21, 24]
    UltimoConcurso = lotofacil_referencia
    #Repetido  =  lotofacil_referencia[1:16] #Usado para saber dos escolhidos qto acertados
    Repetido  =  vetor_concurso_inicial[1:16] #Usado para saber dos escolhidos qto acertados
    #print (Repetido)



    # 2 - ARQUIVOS DAS FUNÇÕES CHAMADAS PELA INERFACE GRAFICO => JANELA PRINCIPAL - ROOT

    corF  = "" # Definindo variavel de cor vazia para usar no funda da totalização Fibo 
    corP  = "" # Definindo variavel de cor vazia para usar no funda da totalização Primos
    corM  = "" # Definindo variavel de cor vazia para usar no funda da totalização Moldura
    corx3 = "" # Definindo variavel de cor vazia para usar no funda da totalização Moldura

    def preencher_matriz():
        matriz = [["0" for _ in range(25)] for _ in range(25)]
        for i in range(25):
            for j in range(15):
                numero = ConcursosResultados[i][j+1]
                matriz[i][numero-1] = str(numero)
        return matriz

    def preencher_linha_numeros_fibonacci():
        linha_fibonacci = ["F" if i+1 in Fibonacci else "" for i in range(25)]
        return linha_fibonacci

    def preencher_linha_primos():
        linha_primos = ["P" if i+1 in Primos else "" for i in range(25)]
        return linha_primos

    def preencher_linha_moldura():
        linha_moldura = ["M" if i+1 in Moldura else "" for i in range(25)]
        return linha_moldura

    def preencher_linha_multiplo():
        linha_multiplo = ["x3" if i+1 in Multiplo else "" for i in range(25)]
        return linha_multiplo

    # lINHAS EXTRAS - ABAIXO TABELA CONCURSOS - VISUALIZAÇÃO DE NUMEROS E PADROES
    def atualizar_total_fibonacci_label(root, labels_primeira_linha):
        global corF
        total_fibonacci = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE and int(label["text"]) in Fibonacci)
        # 
        #print("Total de números de Fibonacci selecionados:", total_fibonacci)
        total_fibonacci_label.config(text="Fibonacci = " + str(total_fibonacci) + " (de 7)")
        if total_fibonacci == 4 or total_fibonacci == 5:
            corF = "green"
        elif total_fibonacci == 0: 
            corF = "lightgray"
        else:
            corF = "red"
        total_fibonacci_label.config(bg=corF)  # irá atualizar a cor de fundo do rótulo da totalização Fibo

    def atualizar_total_primos_label(root, labels_primeira_linha):
        total_primos = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE and int(label["text"]) in Primos)
        total_primos_label.config(text="Primos = " + str(total_primos) + " (de 9)")
        if total_primos == 5 or total_primos == 6:
            corP = "green"
        elif total_primos == 0: 
            corP = "lightgray"
        else:
            corP = "red"
        total_primos_label.config(bg=corP)  # irá atualizar a cor de fundo do rótulo da totalização Primos

    def atualizar_total_moldura_label(root, labels_primeira_linha):
        total_moldura = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE and int(label["text"]) in Moldura)
        total_moldura_label.config(text="Moldura = " + str(total_moldura) + " (de 16)")
        if total_moldura == 8 or total_moldura == 9 or total_moldura == 10:
            corM = "green"
        elif total_moldura == 0: 
            corM = "lightgray"
        else:
            corM = "red"
        total_moldura_label.config(bg=corM)  # irá atualizar a cor de fundo do rótulo da totalização Moldura    

    def atualizar_total_multiplo_label(root, labels_primeira_linha):
        total_multiplo = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE and int(label["text"]) in Multiplo)
        total_multiplo_label.config(text="Multiplo = " + str(total_multiplo) + " (de 8)")
        if total_multiplo == 4 or total_multiplo == 5:
            corx3 = "green"
        elif total_multiplo == 0: 
            corx3 = "lightgray"
        else:
            corx3 = "red"
        total_multiplo_label.config(bg=corx3)  # irá atualizar a cor de fundo do rótulo da totalização Multiplo    

    def atualizar_total_repetido_label(root, labels_primeira_linha):
        total_repetido = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE and int(label["text"]) in Repetido)
        total_repetido_label.config(text="Repetido = " + str(total_repetido) + " (de 15)")
        if total_repetido == 7 or total_repetido == 8 or total_repetido == 9:
            corx3 = "green"
        elif total_repetido == 0: 
            corx3 = "lightgray"
        else:
            corx3 = "red"
        total_repetido_label.config(bg=corx3)  # irá atualizar a cor de fundo do rótulo da totalização Multiplo    
        
    #### FUNÇÃO TOTALIZAÇÃO DOS VALORES A SER PAGOS QDADE NUMEROS SELECIONADOS
    def calcular_valor_pago(count):
        if count == 15:
            return "R$ {:,.2f}".format(3.00)
        elif count == 16:
            return "R$ {:,.2f}".format(48.00)
        elif count == 17:
            return "R$ {:,.2f}".format(408.00)
        elif count == 18:
            return "R$ {:,.2f}".format(2448.00)
        elif count == 19:
            return "R$ {:,.2f}".format(11628.00)
        elif count == 20:
            return "R$ {:,.2f}".format(46512.00)
        else:
            return "R$ 0.00"
    
        
    #############################################################################################
    ### CRIANDO FUNÇÃO QUE ABRIRÁ NOVA JANELA GRÁFICA, ONDE SERÃO APRESENTADOS 
    ### TODAS AS ANÁLISES ESTATISTICAS E SEUS GRAFICOS.

    # Função para análise dos padrões do concurso
    def AnalisaPadroesConcurso(vetor, ultimoconcursoSelecionado):
        
        print ("ultimoconcursoSelecionado =" , ultimoconcursoSelecionado)
        # vetor => NUMEROS ESCOLHIDOS
        # ultimoconcurso => fururo de referencia

        
        # ESSA ANALISE É SOBRE O FUTUROR
        ncol = len(vetor)  # tem que ser variavael a depender das bolas esclhidas 
        #ConcactVetores = vetor
        #ncol = len(list(ultimoconcurso[1:16]))  
        #ConcactVetores = ultimoconcurso[1:16]
        ConcactVetores = vetor   # numeros selecionados

        Analise = np.zeros([6], int)
        #nalise[0, 0] = 0

        par = 0
        impar = 0
        for i in range(ncol):
            if (ConcactVetores[i] % 2) == 0:
               par += 1
            else:
               impar += 1
        
        Analise[0] = par
        Analise[1] = impar
        
        VetorPrimos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        primos = 0
        for i in range(ncol):
            for j in range(9):
                if ConcactVetores[i] == VetorPrimos[j]:
                    primos += 1
        Analise[2] = primos    
        
        VetorFibonacci = [1, 2, 3, 5, 8, 13, 21]
        fibonacci = 0
        for i in range(ncol):
            for j in range(7):
                if ConcactVetores[i] == VetorFibonacci[j]:
                    fibonacci += 1                
        Analise[3] = fibonacci
        
        VetorMoldura = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
        moldura = 0
        for i in range(ncol):
            for j in range(16):
                if ConcactVetores[i] == VetorMoldura[j]:
                   moldura += 1 
        Analise[4] = moldura

        # repetidos = 0
        # for i in range(ncol):
        #     for j in range(15):
        #         #if ConcactVetores[i] == ultimoconcurso[j+1]: # numeros [1-15] - [0,0] - concurso
        #         if ConcactVetores[i] == ultimoconcurso[j]: # numeros [1-15] - [0,0] - concurso
        #            repetidos += 1 
        # Analise[5] = repetidos
        
        # Análise de números repetidos no último concurso
        repetidos = 0
        for i in range(ncol):
            if ConcactVetores[i] in ultimoconcursoSelecionado:
                repetidos += 1
        Analise[5] = repetidos



        print (" ##################### Analise = ", Analise)
        
        return Analise

    # Função para abrir a nova janela com a lista e a análise
    def abrir_janela_validar():
        # nova_janela = tk.Toplevel(root_validar)
        nova_janela = tk.Toplevel()
        nova_janela.title("ESCOLHIDOS x FUTURO")
        
        # Caixa de texto amarela claro para o próximo concurso
        concurso_frame = tk.Frame(nova_janela, bg="lightyellow", relief=tk.SUNKEN, bd=2)
        concurso_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        proximo_concurso_label = tk.Label(concurso_frame, text=f"Próximo concurso = {UltimoConcurso[0]}", font=("Helvetica", 10, "bold"), bg="lightyellow")
        proximo_concurso_label.pack(padx=10, pady=5)
        proximo_concurso_label.config(anchor="center")
 
        numeros_frame = tk.Frame(concurso_frame, relief=tk.SUNKEN, bd=1, bg="lightyellow")
        numeros_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        lista_numeros = tk.Label(numeros_frame, text=", ".join(map(str, UltimoConcurso[1:16])), font=("Helvetica", 10, "bold"), bg="lightyellow")
        lista_numeros.pack(padx=10, pady=10)
        proximo_concurso_label.config(anchor="center")
        
        
        # ===>>>>>>>>>                    ESCOLHIDOS X PROXIMO CONCURSO
        # Análise dos padrões do concurso
        #analise = AnalisaPadroesConcurso(NumerosEscolhidos, vetor_concurso_inicial[1:16])
        analise = AnalisaPadroesConcurso(NumerosEscolhidos, lotofacil_referencia[1:16])

        analise_text = "PADRAO PROXIMO CONCURSO: \n"   # SEM PULAR LINHA ENTRE O NUMERO CONCURSO E AS BOLAS SORTEADAS
        analise_text += f"Pares       (7-8)     {analise[0]}\n"
        analise_text += f"Ímpares     (7-8)     {analise[1]}\n"
        analise_text += f"Primos      (5-6)     {analise[2]}\n"
        analise_text += f"Fibonacci   (4-5)    {analise[3]}\n"
        analise_text += f"Moldura     (9-10)   {analise[4]}\n"
        analise_label = tk.Label(nova_janela, text=analise_text, font=("Helvetica", 10))
        analise_label.pack(padx=10, pady=10)

        acertos_label = tk.Label(nova_janela, text=f"ACERTOS:     {analise[5]}", font=("Helvetica", 10, "bold"), bg="yellow")
        acertos_label.pack(padx=10, pady=10)

        # Caixa de texto roxa claro para os números escolhidos
        escolhidos_frame = tk.Frame(nova_janela, bg="lightpink", relief=tk.SUNKEN, bd=2)
        escolhidos_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        escolhidos_label = tk.Label(escolhidos_frame, text="Números Escolhidos - EM VERMELHO NÃO SAIRIAM", font=("Helvetica", 10, "bold"), bg="lightpink")
        escolhidos_label.pack(padx=10, pady=5)

        numeros_escolhidos_frame = tk.Frame(escolhidos_frame, relief=tk.SUNKEN, bd=2, bg="lightpink")
        numeros_escolhidos_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        escolhidos_text = tk.Text(numeros_escolhidos_frame, height=1, width=80, bg="lightpink", font=("Helvetica", 10))
        escolhidos_text.pack(padx=10, pady=5)
        escolhidos_text.tag_configure("center", justify='center')
        escolhidos_text.tag_configure("bold_red", font=("Helvetica", 10, "bold"), foreground="red")
        escolhidos_text.tag_configure("pink", foreground="#FF69B4")
                    
        for i, num in enumerate(NumerosEscolhidos):
            if num not in UltimoConcurso[1:16]:
                if i < len(NumerosEscolhidos) - 1:
                    escolhidos_text.insert(tk.END, f"{num}, ", "bold_red")
                else:
                    escolhidos_text.insert(tk.END, f"{num}", "bold_red")
            else:
                if i < len(NumerosEscolhidos) - 1:
                    escolhidos_text.insert(tk.END, f"{num}, ", "black")
                else:
                    escolhidos_text.insert(tk.END, f"{num}", "black")
            
        escolhidos_text.tag_add("center", "1.0", "end")
        escolhidos_text.config(state=tk.DISABLED)
      
    #############################################################################################
    ### CRIANDO FUNÇÃO QUE ABRIRÁ NOVA JANELA GRÁFICA, ONDE SERÃO APRESENTADOS 
    ### TODAS AS ANÁLISES ESTATISTICAS E SEUS GRAFICOS.

    ##   FUNÇAÕ PARA ABRIR  NOVA JANELA que mostra plot => df3D graficos
    #import tkinter as tk
    def criar_janela_analise():     
        root_nova_janela = tk.Toplevel()    # criando nova janela SECUNDÁRIA
        titulo_janela = f"Análise Estatística e Gráficos - Lotofacil = {concurso_referencia}"
        root_nova_janela.title(titulo_janela)

        import numpy as np
        import matplotlib.pyplot as plt
        #from mpl_toolkits.mplot3d import Axes3D
        #import tkinter as tk
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        global BolasMatriz
         
        # Removendo a primeira linha e coluna dos dados
        X = BolasMatriz[0, 1:]
        Y = BolasMatriz[1:, 0][::-1]
        X, Y = np.meshgrid(X, Y)
        Z = BolasMatriz[1:, 1:]

        # Configurando a figura =>  Mesmo CONCEITO DO MATLAB
        # # Aumentar o tamanho da figura 5 -> 6 
        fig = plt.figure(figsize=(10, 6))   # dimensão inical da janela
        # Configurando as cores
        cores = plt.cm.turbo(Z / float(Z.max()))  # Mapeia os valores Max-Mn, de Z, para a escala de cores turbo

        # Subplot principal  
        ax1 = fig.add_subplot(121, projection='3d')
        # Ajustando a inclinação das barras
        ax1.view_init(elev=20, azim=250)  # Você pode ajustar os valores de 'elev' e 'azim' para alterar a inclinação4
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                ax1.bar3d(X[i, j], Y[i, j], 0, 1, 1, Z[i, j], color=cores[i, j], alpha=0.8)
        #ax1.bar3d(X.ravel(), Y.ravel(), np.zeros_like(Z).ravel(), 1, 1, Z.ravel(), color='c', alpha=0.8)
        ax1.set_title('Gráfico Principal')
        ax1.set_xlabel('Bolas')
        ax1.set_ylabel('Numeros')
        ax1.set_zlabel('Frequência')
        ax1.set_xticks(np.arange(1, 16))  # Definir ticks do eixo X para começar em 1
        ax1.set_yticks(np.arange(0, 25, 2))  # Definir ticks do eixo Y com incremento de 4
        ax1.set_yticklabels(np.arange(25, 0, -2))  # Label dos ticks do eixo Y começando em 1

        # Subplot secundário
        ax2 = fig.add_subplot(122)
        # Plot da matriz como imagem com valores numéricos
        im = ax2.imshow(Z, cmap='turbo', interpolation='nearest', aspect='auto') #hot
        # Adicionando os valores numéricos sobre a imagem
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                ax2.text(j, i, Z[i, j], ha='center', va='center', color='black')
        # Configurações adicionais
        ax2.set_title('Matriz com Valores Numéricos')
        ax2.set_xlabel('Bolas')
        ax2.set_ylabel('Numeros')
        ax2.set_xticks(np.arange(15))  # Definir ticks do eixo X para começar em 1
        ax2.set_yticks(np.arange(25))  # Definir ticks do eixo Y para começar em 1
        ax2.set_xticklabels(np.arange(1, 16))  # Alterar os rótulos dos ticks do eixo X
        ax2.set_yticklabels(np.arange(1, 26))  # Alterar os rótulos dos ticks do eixo Y

        # Adicionando a barra de cores
        fig.colorbar(im, ax=ax2, label='Valores')
        plt.tight_layout()

        # Mostrando o gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=root_nova_janela)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        root_nova_janela.grid_rowconfigure(0, weight=1)
        root_nova_janela.grid_columnconfigure(0, weight=1)
        
        # Calculando os números com maior frequência para cada coluna
        max_freq_numbers = []
        selected_numbers = set()
        for col in range(Z.shape[1]):
            col_values = Z[:, col]
            sorted_indices = np.argsort(col_values)[::-1]
            for idx in sorted_indices:
                number = Y[idx, 0]
                if number not in selected_numbers:
                    max_freq_numbers.append(number)
                    selected_numbers.add(number)
                    break

        # Ordenando os números em ordem crescente
        max_freq_numbers.sort()
        

        ## TESTE REFERENCIA => FUTURO 3007 
        # Certifique-se de que TST_FUTURO seja uma lista de números
        TST_FUTURO = UltimoConcurso[1:].tolist()  # Converter para lista se for um array numpy
        print(TST_FUTURO)
    
        # Criando a janela para exibir os números
        result_frame = tk.Frame(root_nova_janela, bg="lightyellow")
        result_frame.grid(row=1, column=0, pady=10, sticky="nsew")
    
        result_label = tk.Label(result_frame, text="Números com maior frequência para cada coluna de 1 a 15:", bg="lightyellow",            font=("Helvetica", 10))
        result_label.pack(pady=5)
        
        max_freq_text = tk.Text(result_frame, height=1, width=80, bg="lightyellow", font=("Helvetica", 10))
        max_freq_text.pack(padx=10, pady=5)
        max_freq_text.tag_configure("center", justify='center')
        max_freq_text.insert(tk.END, ", ".join(map(str, max_freq_numbers)), "center")
        max_freq_text.config(state=tk.DISABLED)
        
        
        # Criando a nova janela rosa claro 
        result_frame = tk.Frame(root_nova_janela, bg="lightpink")
        result_frame.grid(row=2, column=0, pady=10, sticky="nsew")

        result_label = tk.Label(result_frame, text="Números com maior frequencia e, EM VERMELHO, não sairiam no próximo concurso:", bg="lightpink",    font=("Helvetica", 10, "bold"))
        result_label.pack(pady=5)
        
        result_text = tk.Text(result_frame, height=1, width=80, bg="lightpink", font=("Helvetica", 10))
        result_text.pack(padx=10, pady=5)
        result_text.tag_configure("center", justify='center')
        max_freq_text.insert(tk.END, ", ".join(map(str, TST_FUTURO)), "center")
        result_text.tag_configure("bold", font=("Helvetica", 10, "bold"))
        result_text.tag_configure("pink", foreground="#FF69B4")


        # # Adicionando números ao texto e configurando as tags
        # for i, num in enumerate(max_freq_numbers):
        #     if num not in TST_FUTURO:
        #         if i < len(max_freq_numbers) - 1:
        #             result_text.insert(tk.END, f"{num}, ", "bold")
        #         else:
        #             result_text.insert(tk.END, f"{num}", "bold")
        #     else:
        #         if i < len(max_freq_numbers) - 1:
        #             result_text.insert(tk.END, f"{num}, ", "pink")
        #         else:
        #             result_text.insert(tk.END, f"{num}", "pink")
        
        
        # Configurar as tags para as cores desejadas
        result_text.tag_configure("black", foreground="black")
        result_text.tag_configure("bold_red", font=("Helvetica", 10, "bold"), foreground="red")

    # Adicionando números ao texto e configurando as tags
        for i, num in enumerate(max_freq_numbers):
            if num in TST_FUTURO:
                if i < len(max_freq_numbers) - 1:
                    result_text.insert(tk.END, f"{num}, ", "black")
                else:
                    result_text.insert(tk.END, f"{num}", "black")
            else:
                if i < len(max_freq_numbers) - 1:
                    result_text.insert(tk.END, f"{num}, ", "bold_red")
                else:
                    result_text.insert(tk.END, f"{num}", "bold_red")


        result_text.tag_add("center", "1.0", "end")
        result_text.config(state=tk.DISABLED)
        
        
        
    # ##   FUNÇAÕ PARA ABRIR NOVA JANELA qque mostra graficos dos padroes
    # HISTOGRAMAS 
    def criar_janela_padroes():
        root_padroes = tk.Toplevel()     # criando nova janela SECUNDÁRIA
        titulo_janela = f"Análise Padrões - Lotofacil = {concurso_referencia}"
        root_padroes.title(titulo_janela)
        #nova_janela.geometry("400x200") - teste tamanho fixo
        # adicionar widgets e configurar nova janela    
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # passa variável global ResultdosLoterias e aqui acerta para gerar matriz c/ 25 numeros x concursos
        global ConcursosResultados
        global qdadetestes
        #bolas   = 15 # qdade de bolas sorteadas - Pode ser Sairam 15 - NSairam 10
        #numeros = 25 # qdade numeros total do da loteria - lotofail 26, megasena 60 ...
        #qdadetestes = 25 # numero de concursos usado para analise

        # Inicializando a matriz lotofacil_matriz com zeros 
        Lotofacil = np.zeros([qdadetestes, 26], dtype=int)
        # Preenchendo a matriz com os resultados dos concursos e ZEROS
        for i in range (qdadetestes):
            for j in range (16):
                if j == 0:
                    Lotofacil[i,j] = ConcursosResultados[i][j]
                else:
                    for k in range (1,26):
                        if ConcursosResultados[i][j] == k:
                           Lotofacil[i,k] = ConcursosResultados[i][j]
        ##            
        #print(Lotofacil)

        # padroes 
        # 1 - conputando quantidades de vezes que sairam os elementos 01_&_25 
        # 00_00 / 01_25 / 00_25 / 01_25
        vetor_01_25 = np.zeros([4], dtype=int)
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 0 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_01_25[0] = icont
            
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_01_25[1] = icont
               
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,2] == 0 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_01_25[2] = icont
            
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_01_25[3] = icont

        # print(vetor_01_25)
        
        # 2 - conputando quantidades de vezes que sairam os elementos 01_&_02_&_03 
        # 00_00_00 / 01_00_00 / 00_02_00 / 00_00_03
        # 01_02_00 / 01_00_03 / 00_02_03 / 01_02_03
        vetor_01_02_03 = np.zeros([8], dtype=int)
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 0 and Lotofacil[i,2] == 0 and Lotofacil[i,3] == 0:
               icont = icont + 1
            vetor_01_02_03[0] = icont

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,2] == 0 and Lotofacil[i,3] == 0:
               icont = icont + 1
            vetor_01_02_03[1] = icont    
            
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 0 and Lotofacil[i,2] == 2 and Lotofacil[i,3] == 0:
               icont = icont + 1
            vetor_01_02_03[2] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 0 and Lotofacil[i,2] == 0 and Lotofacil[i,3] == 3:
               icont = icont + 1
            vetor_01_02_03[3] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,2] == 2 and Lotofacil[i,3] == 0:
               icont = icont + 1
            vetor_01_02_03[4] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,2] == 0 and Lotofacil[i,3] == 3:
               icont = icont + 1
            vetor_01_02_03[5] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 0 and Lotofacil[i,2] == 2 and Lotofacil[i,3] == 3:
               icont = icont + 1
            vetor_01_02_03[6] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,1] == 1 and Lotofacil[i,2] == 2 and Lotofacil[i,3] == 3:
               icont = icont + 1
            vetor_01_02_03[7] = icont            

        # 3 - conputando quantidades de vezes que sairam os elementos 03_&_06_&_09 
        # 00_00_00 / 00_03_00 / 00_06_09 / 00_00_09
        # 03_06_00 / 03_00_09 / 00_06_09 / 03_06_09
        vetor_03_06_09 = np.zeros([8], dtype=int)
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 0 and Lotofacil[i,6] == 0 and Lotofacil[i,3] == 0:
               icont = icont + 1
            vetor_03_06_09[0] = icont

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 3 and Lotofacil[i,6] == 0 and Lotofacil[i,9] == 0:
               icont = icont + 1
            vetor_03_06_09[1] = icont    
            
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 0 and Lotofacil[i,6] == 6 and Lotofacil[i,9] == 0:
               icont = icont + 1
            vetor_03_06_09[2] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 0 and Lotofacil[i,6] == 0 and Lotofacil[i,9] == 9:
               icont = icont + 1
            vetor_03_06_09[3] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 3 and Lotofacil[i,6] == 6 and Lotofacil[i,9] == 0:
               icont = icont + 1
            vetor_03_06_09[4] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 3 and Lotofacil[i,6] == 0 and Lotofacil[i,9] == 9:
               icont = icont + 1
            vetor_03_06_09[5] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 0 and Lotofacil[i,6] == 6 and Lotofacil[i,9] == 9:
               icont = icont + 1
            vetor_03_06_09[6] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,3] == 3 and Lotofacil[i,6] == 6 and Lotofacil[i,9] == 9:
               icont = icont + 1
            vetor_03_06_09[7] = icont            

        # 4 - conputando quantidades de vezes que sairam os elementos 23_&_24_&_25 
        # 00_00_00 / 23_00_00 / 00_24_00 / 00_00_25
        # 23_24_00 / 23_00_25 / 00_24_25 / 23_24_25
        vetor_23_24_25 = np.zeros([8], dtype=int)
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 0 and Lotofacil[i,24] == 0 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_23_24_25[0] = icont

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 23 and Lotofacil[i,24] == 0 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_23_24_25[1] = icont    
            
        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 0 and Lotofacil[i,24] == 24 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_23_24_25[2] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 0 and Lotofacil[i,24] == 0 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_23_24_25[3] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 23 and Lotofacil[i,24] == 24 and Lotofacil[i,25] == 0:
               icont = icont + 1
            vetor_23_24_25[4] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 23 and Lotofacil[i,24] == 0 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_23_24_25[5] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 0 and Lotofacil[i,24] == 24 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_23_24_25[6] = icont            

        icont = 0
        for i in range (qdadetestes):
            if Lotofacil[i,23] == 23 and Lotofacil[i,24] == 24 and Lotofacil[i,25] == 25:
               icont = icont + 1
            vetor_23_24_25[7] = icont            

        # PLOT HISTOGRAMAS - FREQUENCIAS PADROES
        condicoes_01_25 = ['00_00', '01_00', '00_25', '01_25']  # eixo x e labels
        condicoes_01_02_03 = ['00_00_00','01_00_00','00_02_00','00_00_03','01_02_00','01_00_03','00_02_03','01_02_03']  # eixo x e labels
        condicoes_03_06_09 = ['00_00_00','03_00_00','00_06_00','00_00_09','03_06_00','03_00_09','00_06_09','03_06_09']  # eixo x e labels
        condicoes_23_24_25 = ['00_00_00','23_00_00','00_24_00','00_00_25','23_24_00','23_00_25','00_24_25','23_24_25']  # eixo x e labels
        
        fig = plt.figure(figsize=(8, 6))

        ax3 = fig.add_subplot(221)
        ax3.bar(range(len(condicoes_01_25)), vetor_01_25, color='blue', tick_label=condicoes_01_25)
        ax3.set_title('Padrões 01-25',fontsize=8)
        #ax3.set_xlabel('Padrões 01-25')
        ax3.set_ylabel('Frequência')
        ax3.tick_params(axis='x', labelsize=8)
        ax3.tick_params(axis='y', labelsize=8)
        # Rotacionando os labels do eixo x para ficarem 90 graus
        ax3.set_xticks(range(len(condicoes_01_25)))
        ax3.set_xticklabels(condicoes_01_25, rotation=90)
        # Exibindo o gráfico

        ax4 = fig.add_subplot(222)  
        ax4.bar(range(len(condicoes_01_02_03)), vetor_01_02_03, color='blue', tick_label=condicoes_01_02_03)
        ax4.set_title('Padrões 01-02-03',fontsize=8)
        #ax4.set_xlabel('Padrões 01-02-03')
        ax4.set_ylabel('Frequência')
        ax4.tick_params(axis='x', labelsize=8)
        ax4.tick_params(axis='y', labelsize=8)
        # Rotacionando os labels do eixo x para ficarem 90 graus
        ax4.set_xticks(range(len(condicoes_01_02_03)))
        ax4.set_xticklabels(condicoes_01_02_03, rotation=90)
        
        
        ax5 = fig.add_subplot(223)  
        ax5.bar(range(len(condicoes_03_06_09)), vetor_03_06_09, color='blue', tick_label=condicoes_03_06_09)
        ax5.set_title('Padrões 03-06-09',fontsize=8)
        #ax5.set_xlabel('Padrões 03-06-09')
        ax5.set_ylabel('Frequência')
        ax5.tick_params(axis='x', labelsize=8)
        ax5.tick_params(axis='y', labelsize=8)
        # Rotacionando os labels do eixo x para ficarem 90 graus
        ax5.set_xticks(range(len(condicoes_03_06_09)))
        ax5.set_xticklabels(condicoes_03_06_09, rotation=90)
        

        ax6 = fig.add_subplot(224)  
        ax6.bar(range(len(condicoes_23_24_25)), vetor_23_24_25, color='blue', tick_label=condicoes_23_24_25)
        ax6.set_title('Padrões 23-24-25',fontsize=8)
        #ax6.set_xlabel('Padrões 23-24-25')
        ax6.set_ylabel('Frequência')
        ax6.tick_params(axis='x', labelsize=8)
        ax6.tick_params(axis='y', labelsize=8)
        # Rotacionando os labels do eixo x para ficarem 90 graus
        ax6.set_xticks(range(len(condicoes_23_24_25)))
        ax6.set_xticklabels(condicoes_23_24_25, rotation=90)
        
        
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=root_padroes)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        root_padroes.grid_rowconfigure(0, weight=1)
        root_padroes.grid_columnconfigure(0, weight=1)

    #############################################################################################
    ### CRIANDO JANELA PRINCIPAL OCORRERA INTERATIVIDADE GRAFICA    
    # 3 - INTERFACE GRÁFICA -> PRINCIPAL - ROOT   
    #    3.1 - Funcionalidade de Seleção de Números: 
    #         3.1.1 - Ao clicar em um número na tabela, ele muda de cor para indicar que foi selecionado
    #         3.1.2 - As seleções (click) são refletidas em uma lista (janela), dos números selecionados
    #                 e em outra janela mostrando cálculo do valor a ser pago a depender qdade numeros selecionados.
    #    3.2 - Conrtuido uma funcionalidade de atualizaçao (RESET) das Seleção de Números e labels da interfce: 

         
    def criar_janela():
        
        # Função para fechar todas as janelas e encerrar programa
        def encerrar_programa():
            root.destroy()
        
        
        global NumerosEscolhidos # global incluido relativoao vetor dos numeros escolhidos vaiam dinamicamente a cada click
        NumerosEscolhidos = []
        
        
        matriz = preencher_matriz()
        linha_fibonacci = preencher_linha_numeros_fibonacci()
        linha_primos = preencher_linha_primos()
        linha_moldura = preencher_linha_moldura()
        linha_multiplo = preencher_linha_multiplo()
    #    linha_repetido = preencher_linha_repetido() # desnecessário incluir essa linha com a letra R

        root = tk.Tk()
        root.title("Guia LotoFacil")

        labels_primeira_linha = []
        
        #########################  fundamental para resertar display 
        def resetar_selecoes():
            
            global NumerosEscolhidos # global incluido relativoao vetor dos numeros escolhidos vaiam dinamicamente a cada click
            NumerosEscolhidos = []
            print("Numeros Escolhidos:", NumerosEscolhidos)
            
            
            for label in labels_primeira_linha:
                label.config(bg=COR_PADRAO)
            # Limpar a lista de números selecionados
            selected_numbers_listbox.delete(0, tk.END)
            # Redefinir o texto do total de selecionados
            total_selecionados_label.config(text="Total Selecionados: 0")
            # Limpar o valor a ser pago
            valor_a_ser_pago_textbox.delete("1.0", tk.END)
            valor_a_ser_pago_textbox.insert(tk.END, "0.00")            
            # Redefinir a cor de fundo e o texto das totalizações de padrões    
            total_fibonacci_label.config(text="Fibonacci = 0 (de 7)", bg=COR_PADRAO)
            total_primos_label.config(text="Primos = 0 (de 9)", bg=COR_PADRAO)
            total_moldura_label.config(text="Moldura = 0 (de 16)", bg=COR_PADRAO)
            total_multiplo_label.config(text="Multiplo = 0 (de 8)", bg=COR_PADRAO)
            total_repetido_label.config(text="Repetido = 0 (de 15)", bg=COR_PADRAO)



        # Função para atualizar a listbox com os números selecionados
        def atualizar_selected_numbers_listbox():
            selected_numbers_listbox.delete(0, tk.END)
            numeros_selecionados = [int(label["text"]) for label in labels_primeira_linha if label["bg"] == COR_VERDE]
            
            # Dividindo os números em duas linhas
            numeros_linha1 = numeros_selecionados[:15]
            numeros_linha2 = numeros_selecionados[15:]
        
            # Inserindo os números na Listbox
            selected_numbers_listbox.insert(tk.END, " ".join(map(str, numeros_linha1)))
            selected_numbers_listbox.insert(tk.END, " ".join(map(str, numeros_linha2)))
            
            # for numero in numeros_selecionados:
            #     selected_numbers_listbox.insert(tk.END, numero)
        
        def atualizar_total_selecionados():
            global numeros_selecionados
            numeros_selecionados = sum(1 for label in labels_primeira_linha if label["bg"] == COR_VERDE)
            total_selecionados_label.config(text="Total Selecionados: " + str(numeros_selecionados))

        def atualizar_valor_a_ser_pago(numeros_selecionados):
            valor = calcular_valor_pago(numeros_selecionados)
            valor_a_ser_pago_textbox.delete("1.0", tk.END)
            valor_a_ser_pago_textbox.insert(tk.END, valor)

        def alternar_cor_numeros(event, label):
            global NumerosEscolhidos # global incluido relativoao vetor dos numeros escolhidos vaiam dinamicamente a cada click
            numero = int(label["text"]) #relativoao vetor dos numeros escolhidos vaiam dinamicamente a cada click
            
            
            # Alternando as cores conforme a condição descrita
            if label["bg"] == COR_PADRAO:
                label.config(bg=COR_VERDE)
                NumerosEscolhidos.append(numero) #relativo ao vetor dos numeros escolhidos adiciona a cada click verde
                
            elif label["bg"] == COR_VERDE:
                label.config(bg=COR_VERMELHO)
                NumerosEscolhidos.remove(numero) #relativo ao vetor dos numeros escolhidos desceseliona se altraa verde a cada click
            else:
                label.config(bg=COR_PADRAO)
                NumerosEscolhidos.remove(numero) #relativo ao vetor dos numeros escolhidos desceseliona se altraa verde a cada click
                
            # Atualiza as contagens e listas na interface gráfica
            atualizar_total_fibonacci_label(root, labels_primeira_linha)
            atualizar_total_primos_label(root, labels_primeira_linha)
            atualizar_total_moldura_label(root, labels_primeira_linha)
            atualizar_total_multiplo_label(root, labels_primeira_linha)
            atualizar_total_repetido_label(root, labels_primeira_linha)
        
            atualizar_total_selecionados()
            atualizar_selected_numbers_listbox()
            atualizar_valor_a_ser_pago(numeros_selecionados)   
            
            
            NumerosEscolhidos.sort()
            print("Numeros Escolhidos:", NumerosEscolhidos) # consolida lista de escolha dinamicamente
            

        # layout dos  botoes 1-25, na primeira linha da janela principal
        for j in range(25):
            label = tk.Label(root, text=str(j+1), bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"), relief=tk.RAISED)
            label.grid(row=1, column=j+1, padx=1, pady=1)
            label.bind("<Button-1>", lambda event, label=label: alternar_cor_numeros(event, label))
            labels_primeira_linha.append(label)
        
        # display da matriz concursos na janela principal => os 25 primeiros
        for i in range(25):
            label = tk.Label(root, text=str(ConcursosResultados[i][0]), bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"))
            label.grid(row=i+2, column=0, padx=1, pady=1)
            
        # loop para colocar cor de fundo 0-roza, numero amarelo
        for i in range(25):
            for j in range(25):
                numero = matriz[i][j]
                if numero != "0":
                    label = tk.Label(root, text=numero, bg="gold", width=3, height=1, font=("Helvetica", 8, "bold"))
                else:
                    label = tk.Label(root, text=numero, bg="lightpink", width=3, height=1, font=("Helvetica", 8, "bold"))
                label.grid(row=i+2, column=j+1, padx=1, pady=1)

        # Adiciona a linha extra com os números Fibonacci
        for j in range(25):
            numero = linha_fibonacci[j]
            label = tk.Label(root, text=numero, bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"))
            label.grid(row=27, column=j+1, padx=1, pady=1)

        # Adiciona a linha extra com os números primos
        for j in range(25):
            numero = linha_primos[j]
            label = tk.Label(root, text=numero, bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"))
            label.grid(row=28, column=j+1, padx=1, pady=1)
            
            # Adiciona a linha extra com os números moldura
        for j in range(25):
            numero = linha_moldura[j]
            label = tk.Label(root, text=numero, bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"))
            label.grid(row=29, column=j+1, padx=1, pady=1)

    # Adiciona a linha extra com os números múltiplos de 3 (x3)
        for j in range(25):
            numero = linha_multiplo[j]
            label = tk.Label(root, text=numero, bg="lightgray", width=3, height=1, font=("Helvetica", 8, "bold"))
            label.grid(row=30, column=j+1, padx=1, pady=1) 
       
         

    # na linha 31, configurando as caixas com totalização padroes     
        corF = COR_PADRAO
        global total_fibonacci_label
        texto_total_fibonacci = "Fibonacci = "
        total_fibonacci_label = tk.Label(root, text=texto_total_fibonacci + " 0 ", bg=corF, font=("Helvetica", 8, "bold"))
        total_fibonacci_label.grid(row=31, column=1, columnspan=6, padx=5, pady=5)

        corP = COR_PADRAO 
        global total_primos_label
        texto_total_primos = "Primos = "
        total_primos_label = tk.Label(root, text=texto_total_primos + " 0 ", bg=corP, font=("Helvetica", 8, "bold"))
        total_primos_label.grid(row=31, column=6, columnspan=6, padx=5, pady=5)
        
        corM = COR_PADRAO 
        global total_moldura_label
        texto_total_moldura = "Moldura = "
        total_moldura_label = tk.Label(root, text=texto_total_moldura + " 0 ", bg=corM, font=("Helvetica", 8, "bold"))
        total_moldura_label.grid(row=31, column=10, columnspan=6, padx=5, pady=5)

        corx3 = COR_PADRAO 
        global total_multiplo_label
        texto_total_multiplo = "Multiplo = "
        total_multiplo_label = tk.Label(root, text=texto_total_multiplo + " 0 ", bg=corx3, font=("Helvetica", 8, "bold"))
        total_multiplo_label.grid(row=31, column=15, columnspan=6, padx=5, pady=5)
        
        #corx3 = COR_PADRAO 
        global total_repetido_label
        texto_total_repetido = "Repetido = "
        total_repetido_label = tk.Label(root, text=texto_total_repetido + " 0 ", bg=corx3, font=("Helvetica", 8, "bold"))
        total_repetido_label.grid(row=31, column=20, columnspan=6, padx=5, pady=5)    
        
        
        # CRIANDO BOTAO RESET
        # botao_reset = tk.Button(root, text="Resetar Seleções", command=resetar_selecoes, bg="yellow", font=("Helvetica", 8, "bold") )
        # botao_reset.grid(row=32, column=1, columnspan=25, padx=5, pady=5)
        
        # # CONTINUANDO A INSERIR GRAFICOS E FACILIDADES ABAIXO DO BOTAO RESERT PARA
        # # Definindo a fonte em negrito
        # fonte_negrito = ("Helvetica", 10, "bold")
        # # Criando a listbox para exibir os números selecionados
        # selected_numbers_listbox = tk.Listbox(root, width=40, height=2)
        # selected_numbers_listbox.grid(row=33, column=5, columnspan=10, padx=5, pady=5)
        
        # # Criando a caixa de texto para exibir o total de números selecionados
        # total_selecionados_label = tk.Label(root, text="Total Selecionados: 0", font=("Helvetica", 10,"bold"))
        # total_selecionados_label.grid(row=34, column=5, columnspan=10, padx=5, pady=5)
        # # Aplicando o estilo de fonte em negrito na listbox
        # selected_numbers_listbox.configure(font=fonte_negrito)
     
        # # Criando a caixa de texto para exibir o valor a ser pago
        # valor_a_ser_pago_textbox = tk.Text(root, width=10, height=2, font=("Helvetica", 10, "bold"))
        # valor_a_ser_pago_textbox.grid(row=33, column=14, columnspan=10, padx=5, pady=5)  
        
        # valor_a_ser_pago_label = tk.Label(root, text="Valor a ser pago: ", font=("Helvetica", 10,"bold"))
        # valor_a_ser_pago_label.grid(row=34, column=14, columnspan=10, padx=5, pady=5)
        
        
        
        
        
        botao_reset = tk.Button(root, text="Resetar Seleções", command=resetar_selecoes, bg="yellow", font=("Helvetica", 8, "bold") )
        botao_reset.grid(row=32, column=1, columnspan=25, padx=5, pady=5)
        
        # CONTINUANDO A INSERIR GRAFICOS E FACILIDADES ABAIXO DO BOTAO RESERT PARA
        # Definindo a fonte em negrito
        fonte_negrito = ("Helvetica", 10, "bold")
        # Criando a listbox para exibir os números selecionados
        selected_numbers_listbox = tk.Listbox(root, width=35, height=2, bg= "#FFFFE0")
        selected_numbers_listbox.grid(row=33, column=1, columnspan=10, padx=5, pady=5)
        
        # Criando a caixa de texto para exibir o total de números selecionados
        total_selecionados_label = tk.Label(root, text="Total Selecionados: 0", font=("Helvetica", 10))
        total_selecionados_label.grid(row=34, column=1, columnspan=10, padx=5, pady=5)
        # Aplicando o estilo de fonte em negrito na listbox
        selected_numbers_listbox.configure(font=fonte_negrito)
     
        # Criando a caixa de texto para exibir o valor a ser pago
        valor_a_ser_pago_textbox = tk.Text(root, width=12, height=2, font=("Helvetica", 10, "bold"), bg= "#FFFFE0")
        valor_a_ser_pago_textbox.grid(row=33, column=9, columnspan=10, padx=5, pady=5)  
        
        valor_a_ser_pago_label = tk.Label(root, text="Valor a ser pago: ", font=("Helvetica", 10))
        valor_a_ser_pago_label.grid(row=34, column=9, columnspan=10, padx=5, pady=5)
        
        #Criando o botão verde para validar escolha
        botao_validar = tk.Button(root, text="Escolhidos x Proximo Concurso", bg="red", fg="yellow", font=("Helvetica", 10, "bold"), relief="raised", command=abrir_janela_validar, )
        botao_validar.grid(row=33, column=18, columnspan=10, padx=10, pady=10) 
        
       
        

    ##################################################################################
    ################################################################################
    # AGORA INICIAREMOS A INCLUSAO DE ANÁLISE DOS DADOS PARA DAR SUPORTE A ESCOLHA
    #     estimando as frequencias para cada padrão 1-25 / 1-2-3 / 3-6-9 / 23-24-25
    ################################################################################
    ################################################################################
        global BolasMatriz # FORMATO lista +><+ USADOS NO GRAFICSO PRINCPAL E GRADICO SENCUDARIO
        # global aceesado pela função que calcual os graficos primarios e secundario

        # mudando o formaao lis para matriz
        matriz = np.zeros((32, 26), dtype=int)  #32 linhas por 26 coluunas 
        # Copiar os elementos de cada linha da lista ConcursosResultados para a matriz
        for i, linha in enumerate(ConcursosResultados):
            matriz[i, :len(linha)] = linha          #copiando cada linha para gerar matriz
        Lotofacil = matriz 

        b = np.asarray(range(25))+1
        BolasMatriz  = np.zeros( [26, 16] )  # 15 bolas sequencias BOLA01 à BOLA
        BolasMatriz = BolasMatriz.astype(np.int32)
           
        # Preenchendo as primeira linha e primeira coluna com nuMeros das bolas e lotofacil
        BolasMatriz[ 0 , 1:16] = list(range(1, 16, 1))
        BolasMatriz[ 1:26 , 0] = list(range(1, 26, 1)) 
        #calculo das frequencias dos numeros que saem por BOLA (01 a 15)
        for ibola in range (0,15):
            for inumero in range(0,25):
                soma = 0
                for iteste in range (qdadetestes):
                    if b[inumero] == Lotofacil[iteste, ibola+1]:
                       soma = soma + 1
                BolasMatriz[inumero+1 , ibola+1] = soma  # Normalizar a soma
        
        # print (BolasMatriz)

        # Adicionando um botão para análise estatística e gráficos na linha 36
        btn_analise = tk.Button(root, text="Análise Estatística e Gráficos", command=criar_janela_analise, bg="yellow", font=("Helvetica", 8, "bold") )
        btn_analise.grid(row=36, column=1, columnspan=10, padx=5, pady=5)
        
        # Adicionando o novo botão para abrir uma nova janela Padroes na linha 36
        btn_padroes_janela = tk.Button(root, text="Análise Padrões", command=criar_janela_padroes, bg="yellow", font=("Helvetica", 8, "bold"))
        btn_padroes_janela.grid(row=36, column=10, columnspan=10, padx=5, pady=5)  
              
        # Criando o botão para encerrar o programa
        encerrar_button = tk.Button(root, text="Fechar", command=encerrar_programa, font=('Arial 8 bold'), bg="red", fg='yellow', relief='groove',   overrelief='ridge')  # Cor de fundo laranja
        encerrar_button.grid(row=36, column=20, columnspan=15, padx=5, pady=5)  
       
        
        root.mainloop()

    criar_janela()




###############################################################################    
###############################################################################    
## executa uma interfac gráfica com usuário - que roda principal ao INICIAL ###    
###############################################################################    
###############################################################################    

# aqui será executada a interface gráfica, onde o usuário irá preencher os dados e valores
# das variáveis enviadas para o PROGRAMA PRINCIAL AO ACINAMENTO DO BOTÃO 
# ===> "Carregar Informações e Iniciar Programa"
# CONTIDA NA FUNÇÃO => iniciar_programaPRINCIPAL


root = tk.Tk()
root.title("Guia Lotofacil")

readonly_style = ttk.Style()
readonly_style.configure("RO.TEntry", background="#f0f0f0")   # janeça fundo cinza

label_nome_planilha = ttk.Label(root, text="Digite o nome da planilha Excel onde estão os concursos:")
label_nome_planilha.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome_planilha = ttk.Entry(root)
entry_nome_planilha.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_qtd_concursos = ttk.Label(root, text="Digite a quantidade de concursos para análise:")
label_qtd_concursos.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_qtd_concursos = ttk.Entry(root)
entry_qtd_concursos.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

label_concurso_referencia = ttk.Label(root, text="Digite o número do concurso de referência:")
label_concurso_referencia.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_concurso_referencia = ttk.Entry(root)
entry_concurso_referencia.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

def aumentar_concurso_referencia():  # seta incrementa
    valor_atual = int(entry_concurso_referencia.get())
    entry_concurso_referencia.delete(0, tk.END)
    entry_concurso_referencia.insert(0, str(valor_atual + 1))

def diminuir_concurso_referencia(): # seta reduz
    valor_atual = int(entry_concurso_referencia.get())
    entry_concurso_referencia.delete(0, tk.END)
    entry_concurso_referencia.insert(0, str(valor_atual - 1))

botao_aumentar = ttk.Button(root, text="▲", command=aumentar_concurso_referencia)
botao_aumentar.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

botao_diminuir = ttk.Button(root, text="▼", command=diminuir_concurso_referencia)
botao_diminuir.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

def preencher_campos():
    entry_nome_planilha.delete(0, tk.END)
    entry_nome_planilha.insert(0, "lotofácil.xlsx")
    entry_qtd_concursos.delete(0, tk.END)
    entry_qtd_concursos.insert(0, "25")
    entry_concurso_referencia.delete(0, tk.END)
    entry_concurso_referencia.insert(0, "3006")
botao_preencher = ttk.Button(root, text="Preencher com Sugestão", command=preencher_campos)
botao_preencher.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

botao_carregar = ttk.Button(root, text="Carregar Informações e Iniciar Programa", command=iniciar_programaPRINCIPAL)
botao_carregar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

entry_nome_planilha["style"] = "RO.TEntry"
entry_qtd_concursos["style"] = "RO.TEntry"
entry_concurso_referencia["style"] = "RO.TEntry"

root.mainloop()