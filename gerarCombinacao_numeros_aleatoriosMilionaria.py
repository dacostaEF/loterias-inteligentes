import random

# Tabela de preços das apostas
TABELA_PRECOS = {
    (6, 2): {"apostas": 1, "valor": 6.00},
    (6, 3): {"apostas": 3, "valor": 18.00},
    (6, 4): {"apostas": 6, "valor": 36.00},
    (7, 2): {"apostas": 7, "valor": 42.00},
    (6, 5): {"apostas": 10, "valor": 60.00},
    (6, 6): {"apostas": 15, "valor": 90.00},
    (7, 3): {"apostas": 21, "valor": 126.00},
    (8, 2): {"apostas": 28, "valor": 168.00},
    (7, 4): {"apostas": 42, "valor": 252.00},
    (7, 5): {"apostas": 70, "valor": 420.00},
    (9, 2): {"apostas": 84, "valor": 504.00},
    (8, 3): {"apostas": 84, "valor": 504.00},
    (7, 6): {"apostas": 105, "valor": 630.00},
    (8, 4): {"apostas": 168, "valor": 1008.00},
    (10, 2): {"apostas": 210, "valor": 1260.00},
    (9, 3): {"apostas": 252, "valor": 1512.00},
    (8, 5): {"apostas": 280, "valor": 1680.00},
    (8, 6): {"apostas": 420, "valor": 2520.00},
    (11, 2): {"apostas": 462, "valor": 2772.00},
    (9, 4): {"apostas": 504, "valor": 3024.00},
    (10, 3): {"apostas": 630, "valor": 3780.00},
    (9, 5): {"apostas": 840, "valor": 5040.00},
    (12, 2): {"apostas": 924, "valor": 5544.00},
    (9, 6): {"apostas": 1260, "valor": 7560.00},
    (10, 4): {"apostas": 1260, "valor": 7560.00},
    (11, 3): {"apostas": 1386, "valor": 8316.00},
    (10, 5): {"apostas": 2100, "valor": 12600.00},
    (12, 3): {"apostas": 2772, "valor": 16632.00},
    (11, 4): {"apostas": 2772, "valor": 16632.00},
    (10, 6): {"apostas": 3150, "valor": 18900.00},
    (11, 5): {"apostas": 4620, "valor": 27720.00},
    (12, 4): {"apostas": 5544, "valor": 33264.00},
    (11, 6): {"apostas": 6930, "valor": 41580.00},
    (12, 5): {"apostas": 9240, "valor": 55440.00},
    (12, 6): {"apostas": 13860, "valor": 83160.00}
}

def gerar_aposta_personalizada(qtde_num, qtde_trevo1, qtde_trevo2):
    """
    Gera uma aposta personalizada com base na quantidade de números e trevos escolhidos
    
    Args:
        qtde_num (int): Quantidade de números principais (6 a 12)
        qtde_trevo1 (int): Quantidade de números para Trevo 1 (1 a 3)
        qtde_trevo2 (int): Quantidade de números para Trevo 2 (1 a 3)
    
    Returns:
        tuple: (N_milionaria, trevo1, trevo2, valor_aposta, qtde_apostas)
    """
    
    # Validação dos parâmetros
    if qtde_num < 6 or qtde_num > 12:
        raise ValueError("Quantidade de números deve estar entre 6 e 12")
    
    if qtde_trevo1 < 1 or qtde_trevo1 > 3:
        raise ValueError("Quantidade de números para Trevo 1 deve estar entre 1 e 3")
    
    if qtde_trevo2 < 1 or qtde_trevo2 > 3:
        raise ValueError("Quantidade de números para Trevo 2 deve estar entre 1 e 3")
    
    # Calcular total de trevos para verificar na tabela
    qtde_trevo_total = qtde_trevo1 + qtde_trevo2
    
    # Verificar se a combinação existe na tabela
    chave = (qtde_num, qtde_trevo_total)
    if chave not in TABELA_PRECOS:
        raise ValueError(f"Combinação ({qtde_num} números, {qtde_trevo_total} trevos) não disponível")
    
    # Gerar números principais únicos entre 1 e 50
    N_milionaria = sorted(random.sample(range(1, 51), qtde_num))
    
    # Gerar múltiplos números para Trevo 1 (1 a 6)
    trevo1 = sorted(random.sample(range(1, 7), qtde_trevo1))
    
    # Gerar múltiplos números para Trevo 2 (1 a 6)
    trevo2 = sorted(random.sample(range(1, 7), qtde_trevo2))
    
    # Buscar informações da aposta
    info_aposta = TABELA_PRECOS[chave]
    valor_aposta = info_aposta["valor"]
    qtde_apostas = info_aposta["apostas"]
    
    return N_milionaria, trevo1, trevo2, valor_aposta, qtde_apostas

def exibir_opcoes_disponiveis():
    """
    Exibe todas as opções de apostas disponíveis
    """
    print("=" * 60)
    print("🎲 OPÇÕES DE APOSTAS DISPONÍVEIS 🎲")
    print("=" * 60)
    print(f"{'Números':<8} {'Trevos':<8} {'Apostas':<10} {'Valor':<15}")
    print("-" * 60)
    
    for (nums, trevos), info in sorted(TABELA_PRECOS.items()):
        valor_formatado = f"R$ {info['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        print(f"{nums:<8} {trevos:<8} {info['apostas']:<10} {valor_formatado:<15}")
    
    print("=" * 60)

def gerar_e_exibir_personalizada(qtde_num, qtde_trevo):
    """
    Gera e exibe uma aposta personalizada de forma organizada
    """
    try:
        N_milionaria, trevo1, trevo2, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num, qtde_trevo)
        
        print("=" * 50)
        print("🎲 APOSTA PERSONALIZADA GERADA 🎲")
        print("=" * 50)
        print(f"Configuração: {qtde_num} números + {qtde_trevo} trevos")
        print(f"N_milionaria: {N_milionaria}")
        print(f"trevo1: {trevo1}")
        print(f"trevo2: {trevo2}")
        print(f"Quantidade de apostas: {qtde_apostas}")
        valor_formatado = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        print(f"Valor da aposta: {valor_formatado}")
        print("=" * 50)
        
        return N_milionaria, trevo1, trevo2, valor, qtde_apostas
        
    except ValueError as e:
        print(f"❌ Erro: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    print("🎯 GERADOR DE APOSTAS EUROMILHÕES 🎯\n")
    
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
            
            # Solicitar quantidade de números e trevos
            qtde_num = int(input("Quantos números principais? (6-12): "))
            qtde_trevo = int(input("Quantos trevos? (2-6): "))
            
            # Gerar e exibir aposta
            gerar_e_exibir_personalizada(qtde_num, qtde_trevo)
            
        except ValueError:
            print("❌ Por favor, digite números válidos!")
        except KeyboardInterrupt:
            print("\n\nAté logo! 👋")
            break

# Para usar em outros programas:
# from nome_do_arquivo import gerar_aposta_personalizada
# N_milionaria, trevo1, trevo2, valor, qtde_apostas = gerar_aposta_personalizada(8, 3)
