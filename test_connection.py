import socket
import requests

def test_local_connection():
    print("🔍 Testando conectividade local...")
    
    # Teste 1: Verificar se a porta está aberta
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    
    if result == 0:
        print("✅ Porta 5000 está aberta localmente")
    else:
        print("❌ Porta 5000 não está acessível")
        return
    
    # Teste 2: Tentar fazer uma requisição HTTP
    try:
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        print(f"✅ Servidor respondeu com status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
    
    # Teste 3: Verificar IPs disponíveis
    print("\n🌐 IPs disponíveis para acesso:")
    print("   Local: http://127.0.0.1:5000")
    print("   Rede:  http://192.168.0.9:5000")
    print("   Rede:  http://10.5.0.2:5000")

if __name__ == "__main__":
    test_local_connection() 