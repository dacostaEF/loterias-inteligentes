import random

def gerar_numeros_aleatorios():
    """
    Gera 3 listas de números aleatórios:
    - N_milionaria: 6 números únicos entre 1 e 50
    - trevo1: 1 número trevo entre 1 e 6
    - trevo2: 1 número trevo entre 1 e 6
    
    Returns:
        tuple: (N_milionaria, trevo1, trevo2)
    """
    # Lista com 6 números únicos entre 1 e 50
    N_milionaria = sorted(random.sample(range(1, 51), 6))
    
    # Primeiro trevo (1 a 6)
    trevo1 = random.randint(1, 6)
    
    # Segundo trevo (1 a 6)
    trevo2 = random.randint(1, 6)
    
    return N_milionaria, trevo1, trevo2

def gerar_e_exibir():
    """
    Função para gerar e exibir os números de forma organizada
    """
    N_milionaria, trevo1, trevo2 = gerar_numeros_aleatorios()
    
    print("=" * 40)
    print("🎲 NÚMEROS GERADOS ALEATORIAMENTE 🎲")
    print("=" * 40)
    print(f"N_milionaria: {N_milionaria}")
    print(f"trevo1: {trevo1}")
    print(f"trevo2: {trevo2}")
    print("=" * 40)
    
    return N_milionaria, trevo1, trevo2

# Exemplo de uso
if __name__ == "__main__":
    # Simulando cliques no botão
    print("Pressione Enter para gerar números (ou 'q' para sair)")
    
    while True:
        entrada = input("\n>>> ")
        if entrada.lower() == 'q':
            print("Até logo! 👋")
            break
        
        # Gera e exibe os números
        gerar_e_exibir()

# Para usar em outros programas, importe assim:
# from nome_do_arquivo import gerar_numeros_aleatorios
# N_milionaria, trevo1, trevo2 = gerar_numeros_aleatorios()