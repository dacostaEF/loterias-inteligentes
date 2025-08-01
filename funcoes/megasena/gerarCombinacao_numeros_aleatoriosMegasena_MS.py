import random

# Tabela de preços das apostas da Mega Sena
TABELA_PRECOS = {
    6: {"apostas": 1, "valor": 5.00},
    7: {"apostas": 7, "valor": 35.00},
    8: {"apostas": 28, "valor": 140.00},
    9: {"apostas": 84, "valor": 420.00},
    10: {"apostas": 210, "valor": 1050.00},
    11: {"apostas": 462, "valor": 2310.00},
    12: {"apostas": 924, "valor": 4620.00},
    13: {"apostas": 1716, "valor": 8580.00},
    14: {"apostas": 3003, "valor": 15015.00},
    15: {"apostas": 5005, "valor": 25025.00}
}

def gerar_aposta_personalizada(qtde_num):
    """
    Gera uma aposta personalizada da Mega Sena com base na quantidade de números escolhidos
    
    Args:
        qtde_num (int): Quantidade de números principais (6 a 15)
    
    Returns:
        tuple: (numeros, valor_aposta, qtde_apostas)
    """
    
    # Validação dos parâmetros
    if qtde_num < 6 or qtde_num > 15:
        raise ValueError("Quantidade de números deve estar entre 6 e 15")
    
    # Verificar se a quantidade existe na tabela
    if qtde_num not in TABELA_PRECOS:
        raise ValueError(f"Quantidade de {qtde_num} números não disponível")
    
    # Gerar números principais únicos entre 1 e 60 (Mega Sena)
    numeros = sorted(random.sample(range(1, 61), qtde_num))
    
    # Buscar informações da aposta
    info_aposta = TABELA_PRECOS[qtde_num]
    valor_aposta = info_aposta["valor"]
    qtde_apostas = info_aposta["apostas"]
    
    return numeros, valor_aposta, qtde_apostas

def exibir_opcoes_disponiveis():
    """
    Exibe todas as opções de apostas disponíveis da Mega Sena
    """
    print("=" * 50)
    print("🎲 OPÇÕES DE APOSTAS MEGA SENA 🎲")
    print("=" * 50)
    print(f"{'Números':<8} {'Apostas':<10} {'Valor':<15}")
    print("-" * 50)
    
    for nums, info in sorted(TABELA_PRECOS.items()):
        valor_formatado = f"R$ {info['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        print(f"{nums:<8} {info['apostas']:<10} {valor_formatado:<15}")
    
    print("=" * 50)

def gerar_e_exibir_personalizada(qtde_num):
    """
    Gera e exibe uma aposta personalizada da Mega Sena de forma organizada
    """
    try:
        numeros, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num)
        
        print("=" * 50)
        print("🎲 APOSTA MEGA SENA GERADA 🎲")
        print("=" * 50)
        print(f"Configuração: {qtde_num} números")
        print(f"Números: {numeros}")
        print(f"Quantidade de apostas: {qtde_apostas}")
        valor_formatado = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        print(f"Valor da aposta: {valor_formatado}")
        print("=" * 50)
        
        return numeros, valor, qtde_apostas
        
    except ValueError as e:
        print(f"❌ Erro: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    print("🎯 GERADOR DE APOSTAS MEGA SENA 🎯\n")
    
    # Exibir opções disponíveis
    exibir_opcoes_disponiveis()
    
    while True:
        try:
            print("\n📝 Digite sua escolha (ou 'q' para sair):")
            entrada = input(">>> ").strip().lower()
            
            if entrada == 'q':
                print("Até logo! 👋")
                break
            
            if entrada == 'opcoes' or entrada == 'o':
                exibir_opcoes_disponiveis()
                continue
            
            # Solicitar quantidade de números
            qtde_num = int(input("Quantos números? (6-15): "))
            
            # Gerar e exibir aposta
            gerar_e_exibir_personalizada(qtde_num)
            
        except ValueError:
            print("❌ Por favor, digite números válidos!")
        except KeyboardInterrupt:
            print("\n\nAté logo! 👋")
            break

# Para usar em outros programas:
# from nome_do_arquivo import gerar_aposta_personalizada
# numeros, valor, qtde_apostas = gerar_aposta_personalizada(8)
