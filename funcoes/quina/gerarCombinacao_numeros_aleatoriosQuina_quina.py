import random

# Tabela de preços das apostas da Quina (valores atualizados)
TABELA_PRECOS = {
    5: {"apostas": 1, "valor": 3.00},
    6: {"apostas": 6, "valor": 18.00},
    7: {"apostas": 21, "valor": 63.00},
    8: {"apostas": 56, "valor": 168.00},
    9: {"apostas": 126, "valor": 378.00},
    10: {"apostas": 252, "valor": 756.00},
    11: {"apostas": 462, "valor": 1386.00},
    12: {"apostas": 792, "valor": 2376.00},
    13: {"apostas": 1287, "valor": 3861.00},
    14: {"apostas": 2002, "valor": 6006.00},
    15: {"apostas": 3003, "valor": 9009.00}
}

def gerar_aposta_personalizada_quina(qtde_num):
    """
    Gera uma aposta personalizada da Quina com base na quantidade de números escolhidos
    
    Args:
        qtde_num (int): Quantidade de números principais (5 a 15)
    
    Returns:
        tuple: (numeros, valor_aposta, qtde_apostas)
    """
    
    # Validação dos parâmetros
    if qtde_num < 5 or qtde_num > 15:
        raise ValueError("Quantidade de números deve estar entre 5 e 15")
    
    # Verificar se a quantidade existe na tabela
    if qtde_num not in TABELA_PRECOS:
        raise ValueError(f"Quantidade de {qtde_num} números não disponível")
    
    # Gerar números principais únicos entre 1 e 80 (Quina)
    numeros = sorted(random.sample(range(1, 81), qtde_num))
    
    # Buscar informações da aposta
    info_aposta = TABELA_PRECOS[qtde_num]
    valor_aposta = info_aposta["valor"]
    qtde_apostas = info_aposta["apostas"]
    
    return numeros, valor_aposta, qtde_apostas

def exibir_opcoes_disponiveis_quina():
    """
    Exibe todas as opções de apostas disponíveis da Quina
    """
    # print("=" * 50)  # DEBUG - COMENTADO
    # print("🎲 OPÇÕES DE APOSTAS QUINA 🎲")  # DEBUG - COMENTADO
    # print("=" * 50)  # DEBUG - COMENTADO
    # print(f"{'Números':<8} {'Apostas':<10} {'Valor':<15}")  # DEBUG - COMENTADO
    # print("-" * 50)  # DEBUG - COMENTADO
    # 
    # for nums, info in sorted(TABELA_PRECOS.items()):
    #     valor_formatado = f"R$ {info['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    #     print(f"{nums:<8} {info['apostas']:<10} {valor_formatado:<15}")  # DEBUG - COMENTADO
    # 
    # print("=" * 50)  # DEBUG - COMENTADO

def gerar_e_exibir_personalizada_quina(qtde_num):
    """
    Gera e exibe uma aposta personalizada da Quina de forma organizada
    """
    try:
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_quina(qtde_num)
        
        # print("=" * 50)  # DEBUG - COMENTADO
        # print("🎲 APOSTA QUINA GERADA 🎲")  # DEBUG - COMENTADO
        # print("=" * 50)  # DEBUG - COMENTADO
        # print(f"Configuração: {qtde_num} números")  # DEBUG - COMENTADO
        # print(f"Números: {numeros}")  # DEBUG - COMENTADO
        # print(f"Quantidade de apostas: {qtde_apostas}")  # DEBUG - COMENTADO
        # valor_formatado = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        # print(f"Valor da aposta: {valor_formatado}")  # DEBUG - COMENTADO
        # print("=" * 50)  # DEBUG - COMENTADO
        
        return numeros, valor, qtde_apostas
        
    except ValueError as e:
        print(f"❌ Erro: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    print("🎯 GERADOR DE APOSTAS QUINA 🎯\n")
    
    # Exibir opções disponíveis
    exibir_opcoes_disponiveis_quina()
    
    while True:
        try:
            print("\n📝 Digite sua escolha (ou 'q' para sair):")
            entrada = input(">>> ").strip().lower()
            
            if entrada == 'q':
                print("Até logo! 👋")
                break
            
            if entrada == 'opcoes' or entrada == 'o':
                exibir_opcoes_disponiveis_quina()
                continue
            
            # Solicitar quantidade de números
            qtde_num = int(input("Quantos números? (5-15): "))
            
            # Gerar e exibir aposta
            gerar_e_exibir_personalizada_quina(qtde_num)
            
        except ValueError:
            print("❌ Por favor, digite números válidos!")
        except KeyboardInterrupt:
            print("\n\nAté logo! 👋")
            break

# Para usar em outros programas:
# from nome_do_arquivo import gerar_aposta_personalizada_quina
# numeros, valor, qtde_apostas = gerar_aposta_personalizada_quina(8)
