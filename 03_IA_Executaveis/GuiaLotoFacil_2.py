import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt
import datetime

# Função para calcular a média móvel ponderada
def media_movel_ponderada(data, window_size):
    weights = np.linspace(1, 2, window_size)  # Pesos lineares de 1 a 2
    weights /= weights.sum()  # Normalizar os pesos para somar 1
    return np.convolve(data, weights, mode='valid')

# Funções para filtragem
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Função para verificar a data de instalação
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

def check_validity():
    install_date = get_installation_date()
    now = datetime.datetime.now()
    validity_period = datetime.timedelta(days=30)
    if now > install_date + validity_period:
        print("Período de validade expirado. Entre em contato com o desenvolvedor para renovar a licença.")
        exit()

# Verificar a validade antes de continuar
check_validity()

# Supondo que LeExcel2.LeExcel já leu a planilha e carregou a matriz_temp corretamente.
import LeExcel2

Pulartestes = 0    # 0 não pula, n numero de concursos pulados
Nconcursos = 50000 # lendo todos os concursos da lotofacil
CEF = 'lotofácil.xlsx'  # Endereço planilha com resultados LOTOFACIL
# CEF = '../Resultados/lotofácil.xlsx'  # Endereço planilha com resultados LOTOFACIL

matriz_temp = LeExcel2.LeExcel(Pulartestes, Nconcursos, CEF)
matriz_temp = matriz_temp[matriz_temp[:, 0].argsort()[::-1]]

# Número de concursos já realizados.
num_concursos = matriz_temp.shape[0]
num_bolas = 15

# Definindo o intervalo de testes
tst_inic = 0
tst_final = 500

# Obter os números dos concursos e inverter a ordem
concursos = matriz_temp[tst_inic:tst_final, 0][::-1]

# Criar os vetores Bola01 a Bola15 e inverter a ordem
Bola01, Bola02, Bola03, Bola04, Bola05, Bola06, Bola07, Bola08, Bola09, Bola10, Bola11, Bola12, Bola13, Bola14, Bola15 = \
    matriz_temp[tst_inic:tst_final, 1][::-1], matriz_temp[tst_inic:tst_final, 2][::-1], matriz_temp[tst_inic:tst_final, 3][::-1], \
    matriz_temp[tst_inic:tst_final, 4][::-1], matriz_temp[tst_inic:tst_final, 5][::-1], matriz_temp[tst_inic:tst_final, 6][::-1], \
    matriz_temp[tst_inic:tst_final, 7][::-1], matriz_temp[tst_inic:tst_final, 8][::-1], matriz_temp[tst_inic:tst_final, 9][::-1], \
    matriz_temp[tst_inic:tst_final, 10][::-1], matriz_temp[tst_inic:tst_final, 11][::-1], matriz_temp[tst_inic:tst_final, 12][::-1], \
    matriz_temp[tst_inic:tst_final, 13][::-1], matriz_temp[tst_inic:tst_final, 14][::-1], matriz_temp[tst_inic:tst_final, 15][::-1]

# Calculando a média de cada bola
media_Bola01 = np.round(np.mean(Bola01))
media_Bola02 = np.round(np.mean(Bola02))
media_Bola03 = np.round(np.mean(Bola03))
media_Bola04 = np.round(np.mean(Bola04))
media_Bola05 = np.round(np.mean(Bola05))
media_Bola06 = np.round(np.mean(Bola06))
media_Bola07 = np.round(np.mean(Bola07))
media_Bola08 = np.round(np.mean(Bola08))
media_Bola09 = np.round(np.mean(Bola09))
media_Bola10 = np.round(np.mean(Bola10))
media_Bola11 = np.round(np.mean(Bola11))
media_Bola12 = np.round(np.mean(Bola12))
media_Bola13 = np.round(np.mean(Bola13))
media_Bola14 = np.round(np.mean(Bola14))
media_Bola15 = np.round(np.mean(Bola15))

# Lista de todas as bolas e médias
bolas = [Bola01, Bola02, Bola03, Bola04, Bola05, Bola06, Bola07, Bola08, Bola09, Bola10, Bola11, Bola12, Bola13, Bola14, Bola15]
medias = [media_Bola01, media_Bola02, media_Bola03, media_Bola04, media_Bola05, media_Bola06, media_Bola07, media_Bola08, media_Bola09, media_Bola10, media_Bola11, media_Bola12, media_Bola13, media_Bola14, media_Bola15]

# Tamanho da janela para a média móvel ponderada
window_size = 50

# Função para criar uma janela pop-up com o gráfico
def criar_grafico(bola, media, bola_num, concursos):
    fs = 1  # Frequência de amostragem (1 concurso por unidade de tempo)
    lowcut = 0.01
    highcut = 0.1

    # Filtro passa-baixa (baixa frequência)
    bola_low = lowpass_filter(bola, lowcut, fs)
    # Filtro passa-alta (alta frequência)
    bola_high = highpass_filter(bola, highcut, fs)

    # Calcular a média móvel ponderada
    if len(bola) >= window_size:
        media_movel_pond = media_movel_ponderada(bola, window_size)
        previsao = media_movel_pond[-1]  # Previsão baseada na última média móvel ponderada

    root = tk.Toplevel()
    root.title(f'Bola {bola_num}')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # Gráfico superior
    ax1.plot(concursos, bola, label=f'Bola {bola_num}', color='black')
    ax1.axhline(y=media, color='red', linestyle='--', label=f'Média {media:.2f}')
    
    if len(bola) >= window_size:
        ax1.plot(concursos[window_size - 1:], media_movel_pond, color='green', linestyle='-', label='Média Móvel Ponderada')
        ax1.annotate(f'Média: {media:.2f}', xy=(0.95, 0.95), xycoords='axes fraction', verticalalignment='top', horizontalalignment='right', fontsize=10, color='red')
        ax1.annotate(f'Média Móvel Ponderada: {media_movel_pond[-1]:.2f}', xy=(0.95, 0.85), xycoords='axes fraction', verticalalignment='top', horizontalalignment='right', fontsize=10, color='green')
        ax1.annotate(f'Previsão: {previsao:.2f}', xy=(0.95, 0.75), xycoords='axes fraction', verticalalignment='top', horizontalalignment='right', fontsize=10, color='blue')

    ax1.plot(concursos, bola_low, label='Baixa Frequência', color='blue', linestyle='--')
    
    ax1.set_title(f'Bola {bola_num}')
    ax1.set_xlabel('Concursos')
    ax1.set_ylabel('Números')
    ax1.set_yticks(np.arange(int(np.min(bola)), int(np.max(bola)) + 1, 1))
    ax1.legend()
    
    # Gráfico inferior
    ax2.plot(concursos, bola_high, label='Alta Frequência', color='orange', linestyle='--')
    ax2.axhline(y=0, color='red', linestyle='--', label='Linha de Zero')
    ax2.set_xlabel('Concursos')
    ax2.set_ylabel('Alta Frequência')
    ax2.legend()
    ax2.yaxis.tick_right()

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Criar a janela principal para iniciar o processo
main_root = tk.Tk()
main_root.withdraw()  # Ocultar a janela principal

# Criar janelas pop-up para cada gráfico
for i in range(num_bolas):
    criar_grafico(bolas[i], medias[i], i + 1, concursos)

main_root.mainloop()