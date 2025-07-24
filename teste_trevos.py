from gerarCombinacao_numeros_aleatoriosMilionaria import gerar_aposta_personalizada

print("🧪 TESTE DA FUNÇÃO DE GERAÇÃO DE TREVOS")
print("=" * 50)

# Teste 1: 6 trevos (deve retornar todos os números 1-6)
print("\n1️⃣ Teste com 6 trevos (3+3):")
result = gerar_aposta_personalizada(8, 3, 3)
print(f"Trevo1: {result[1]}")
print(f"Trevo2: {result[2]}")
print(f"Todos os trevos: {sorted(result[1] + result[2])}")
print(f"✅ Todos os 6 números presentes: {len(set(result[1] + result[2])) == 6}")

# Teste 2: 4 trevos (deve retornar 4 números únicos)
print("\n2️⃣ Teste com 4 trevos (2+2):")
result = gerar_aposta_personalizada(8, 2, 2)
print(f"Trevo1: {result[1]}")
print(f"Trevo2: {result[2]}")
print(f"Todos os trevos: {sorted(result[1] + result[2])}")
print(f"✅ 4 números únicos: {len(set(result[1] + result[2])) == 4}")

# Teste 3: 5 trevos (deve retornar 5 números únicos)
print("\n3️⃣ Teste com 5 trevos (3+2):")
result = gerar_aposta_personalizada(8, 3, 2)
print(f"Trevo1: {result[1]}")
print(f"Trevo2: {result[2]}")
print(f"Todos os trevos: {sorted(result[1] + result[2])}")
print(f"✅ 5 números únicos: {len(set(result[1] + result[2])) == 5}")

print("\n�� TESTE CONCLUÍDO!") 