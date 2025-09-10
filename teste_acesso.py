#!/usr/bin/env python3
"""
Script para testar o controle de acesso das rotas da Mega Sena
"""
import requests
import time

def testar_rota(url, descricao):
    """Testa uma rota e mostra o resultado"""
    print(f"\n🔍 Testando: {descricao}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print(f"Redirecionamento para: {response.headers.get('Location', 'N/A')}")
        elif response.status_code == 200:
            print("✅ Página carregou diretamente (PROBLEMA!)")
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def main():
    print("🚀 Iniciando teste de controle de acesso...")
    print("⚠️  Certifique-se de que o servidor está rodando em http://localhost:5000")
    
    # Aguardar um pouco para o servidor inicializar
    time.sleep(2)
    
    # Testar rotas da Mega Sena
    testar_rota("http://localhost:5000/dashboard_MS", "Dashboard Mega Sena")
    testar_rota("http://localhost:5000/aposta_inteligente_premium_MS", "Aposta Inteligente Premium MS")
    testar_rota("http://localhost:5000/analise_estatistica_avancada_megasena", "Análise Estatística Avançada MS")
    
    # Testar rota gratuita para comparação
    testar_rota("http://localhost:5000/dashboard_quina", "Dashboard Quina (Gratuito)")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    main()

