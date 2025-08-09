import random

# Tabela de preços das apostas da Lotomania (50 números fixos, R$ 3,00)
TABELA_PRECOS = {
    50: {"apostas": 1, "valor": 3.00}
}

def gerar_aposta_personalizada_lotomania(qtde_num=None):
    """
    Gera uma aposta personalizada da Lotomania com 50 números fixos
    
    Args:
        qtde_num (int): Quantidade de números (ignorado, sempre 50 para Lotomania)
    
    Returns:
        tuple: (numeros, valor_aposta, qtde_apostas)
    """
    
    # Para Lotomania, sempre 50 números fixos
    qtde_num = 50
    
    # Validação dos parâmetros
    if qtde_num != 50:
        raise ValueError("Lotomania aceita apenas 50 números fixos")
    
    # Verificar se a quantidade existe na tabela
    if qtde_num not in TABELA_PRECOS:
        raise ValueError(f"Quantidade de {qtde_num} números não disponível")
    
    # Gerar 50 números únicos entre 1 e 100 (Lotomania)
    numeros = sorted(random.sample(range(1, 101), qtde_num))
    
    # Buscar informações da aposta
    info_aposta = TABELA_PRECOS[qtde_num]
    valor_aposta = info_aposta["valor"]
    qtde_apostas = info_aposta["apostas"]
    
    return numeros, valor_aposta, qtde_apostas

def exibir_opcoes_disponiveis_lotomania():
    """
    Exibe todas as opções de apostas disponíveis da Lotomania
    """
    # print("=" * 50)  # DEBUG - COMENTADO
    # print("🎲 OPÇÕES DE APOSTAS LOTOMANIA 🎲")  # DEBUG - COMENTADO
    # print("=" * 50)  # DEBUG - COMENTADO
    # print(f"{'Números':<8} {'Apostas':<10} {'Valor':<15}")  # DEBUG - COMENTADO
    # print("-" * 50)  # DEBUG - COMENTADO
    # 
    # for nums, info in sorted(TABELA_PRECOS.items()):
    #     valor_formatado = f"R$ {info['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    #     print(f"{nums:<8} {info['apostas']:<10} {valor_formatado:<15}")  # DEBUG - COMENTADO
    # 
    # print("=" * 50)  # DEBUG - COMENTADO

def gerar_e_exibir_personalizada_lotomania(qtde_num=None):
    """
    Gera e exibe uma aposta personalizada da Lotomania de forma organizada
    """
    try:
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_lotomania(qtde_num)
        
        # print("=" * 50)  # DEBUG - COMENTADO
        # print("🎲 APOSTA LOTOMANIA GERADA 🎲")  # DEBUG - COMENTADO
        # print("=" * 50)  # DEBUG - COMENTADO
        # print(f"Configuração: 50 números (fixo)")  # DEBUG - COMENTADO
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
    print("🎯 GERADOR DE APOSTAS LOTOMANIA 🎯\n")
    
    # Exibir opções disponíveis
    exibir_opcoes_disponiveis_lotomania()
    
    while True:
        try:
            print("\n📝 Digite sua escolha (ou 'q' para sair):")
            entrada = input(">>> ").strip().lower()
            
            if entrada == 'q':
                print("Até logo! 👋")
                break
            
            if entrada == 'opcoes' or entrada == 'o':
                exibir_opcoes_disponiveis_lotomania()
                continue
            
            # Para Lotomania, sempre 50 números
            print("Lotomania: 50 números fixos por R$ 3,00")
            
            # Gerar e exibir aposta
            gerar_e_exibir_personalizada_lotomania()
            
        except ValueError:
            print("❌ Por favor, digite números válidos!")
        except KeyboardInterrupt:
            print("\n\nAté logo! 👋")
            break

# Para usar em outros programas:
# from nome_do_arquivo import gerar_aposta_personalizada_lotomania
# numeros, valor, qtde_apostas = gerar_aposta_personalizada_lotomania()
