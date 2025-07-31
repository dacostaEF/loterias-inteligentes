from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia

try:
    resultado = analisar_frequencia(50)
    print('Tipo:', type(resultado))
    print('Vazio:', resultado == {})
    if resultado:
        print('Keys:', list(resultado.keys()))
        print('Primeira chave:', list(resultado.keys())[0] if resultado.keys() else 'Nenhuma')
    else:
        print('Resultado é None ou vazio')
except Exception as e:
    print('Erro:', e) 