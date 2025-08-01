#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Teste para verificar se a função de análise de frequência da Mega Sena está funcionando

from funcoes.megasena.funcao_analise_de_frequencia_MS import analisar_frequencia
from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena

def testar_analise_frequencia_megasena():
    """Testa a análise de frequência da Mega Sena."""
    try:
        print("🔍 Testando análise de frequência da Mega Sena...")
        print("=" * 50)
        
        # Carregar dados
        df_megasena = carregar_dados_megasena()
        print(f"✅ Dados carregados. Total de concursos: {len(df_megasena)}")
        
        # Testar análise de frequência
        resultado = analisar_frequencia(df_megasena=df_megasena, qtd_concursos=50)
        
        if resultado and 'numeros_quentes_frios' in resultado:
            print("✅ Análise de frequência funcionando!")
            
            # Verificar números quentes
            numeros_quentes = resultado['numeros_quentes_frios'].get('numeros_quentes', [])
            print(f"🔥 Números quentes (top 10): {numeros_quentes[:10]}")
            
            # Verificar números frios
            numeros_frios = resultado['numeros_quentes_frios'].get('numeros_frios', [])
            print(f"❄️ Números frios (top 10): {numeros_frios[:10]}")
            
            # Verificar números secos
            numeros_secos = resultado['numeros_quentes_frios'].get('numeros_secos', [])
            print(f"🌵 Números secos (top 10): {numeros_secos[:10]}")
            
        else:
            print("❌ Resultado vazio ou sem dados esperados")
            print(f"Resultado: {resultado}")
            
    except Exception as e:
        print(f"❌ Erro ao testar análise de frequência: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_analise_frequencia_megasena() 