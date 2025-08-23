import time
from pyngrok import ngrok

def start_ngrok_only():
    print("🚀 Ativando Ngrok para servidor existente...")
    print("==================================================")
    
    try:
        # Criar túnel para porta 5000 (onde o Flask já está rodando)
        tunnel = ngrok.connect(5000)
        public_url = tunnel.public_url
        
        print("✅ NGROK ATIVADO COM SUCESSO!")
        print("==================================================")
        print(f"🌐 URL Pública: {public_url}")
        print("==================================================")
        print("📱 Acesse no seu celular usando a URL acima!")
        print("🇧🇷 Teste todas as páginas e funcionalidades")
        print("==================================================")
        print("⚠️  IMPORTANTE:")
        print("- Este túnel é temporário")
        print("- Funciona apenas enquanto este script estiver rodando")
        print("- Para parar: Ctrl+C")
        print("==================================================")
        
        # Manter o script rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando Ngrok...")
            ngrok.kill()
            print("✅ Ngrok parado!")
            
    except Exception as e:
        print(f"❌ Erro ao ativar Ngrok: {e}")

if __name__ == "__main__":
    start_ngrok_only() 