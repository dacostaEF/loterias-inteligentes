import subprocess
import sys

def open_port_5000():
    print("🔧 Abrindo porta 5000 no firewall...")
    
    try:
        # Comando para adicionar regra no firewall
        cmd = [
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name="Flask App Port 5000"',
            'dir=in',
            'action=allow',
            'protocol=TCP',
            'localport=5000'
        ]
        
        # Executar com privilégios elevados
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Porta 5000 aberta no firewall!")
            print("🚀 Agora tente acessar: http://192.168.0.9:5000")
        else:
            print("❌ Erro ao abrir porta. Tente executar como administrador.")
            print("💡 Solução: Clique com botão direito no PowerShell e escolha 'Executar como administrador'")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Execute o PowerShell como administrador e tente novamente")

if __name__ == "__main__":
    open_port_5000() 