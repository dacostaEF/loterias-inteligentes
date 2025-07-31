from pyngrok import ngrok

def config_token():
    print("🔧 Configurando token do Ngrok...")
    
    # Configurar o token
    ngrok.set_auth_token("30WTs8FbpWImuKyuTRXcTMQfXhD_2Hiv2hbJKTaeMBqamDt4e")
    
    print("✅ Token configurado com sucesso!")
    print("🚀 Agora você pode usar o ngrok_deploy.py")

if __name__ == "__main__":
    config_token() 