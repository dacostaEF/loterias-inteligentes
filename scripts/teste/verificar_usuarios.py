import sqlite3
import hashlib

conn = sqlite3.connect('database/loterias_simples.db')
cursor = conn.cursor()

print("=== USUÁRIOS MASTER NO BANCO ===")
cursor.execute('SELECT id, nome_completo, email, tipo_plano, senha_hash FROM usuarios WHERE email LIKE "master_%"')
for row in cursor.fetchall():
    print(f"ID: {row[0]}")
    print(f"Nome: {row[1]}")
    print(f"Email: {row[2]}")
    print(f"Plano: {row[3]}")
    print(f"Senha Hash: {row[4]}")
    print("-" * 50)

print("\n=== TESTE DE SENHA ===")
senha_teste = "Tete&2602"
senha_hash_teste = hashlib.sha256(senha_teste.encode()).hexdigest()
print(f"Senha de teste: {senha_teste}")
print(f"Hash da senha: {senha_hash_teste}")

# Verificar se algum usuário tem esse hash
cursor.execute('SELECT email FROM usuarios WHERE senha_hash = ?', (senha_hash_teste,))
usuarios_com_senha = cursor.fetchall()
print(f"Usuários com essa senha: {len(usuarios_com_senha)}")
for user in usuarios_com_senha:
    print(f"  - {user[0]}")

conn.close()
