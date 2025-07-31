#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Caminho do backup
backup_path = r"C:\Users\Dell\Dropbox\! 000 ByPass\Pessoal\99_Loterias\0 - Milionaria_backups\0 - Milionaria_V22_Versao_Alfa_MilionariaCOmpleta_ProximoMegaSena"

print("=== VERIFICANDO ESTRUTURA DO BACKUP ===")
print(f"Caminho: {backup_path}")
print(f"Existe? {os.path.exists(backup_path)}")

if os.path.exists(backup_path):
    print("\nConteúdo do backup:")
    for item in os.listdir(backup_path):
        item_path = os.path.join(backup_path, item)
        if os.path.isdir(item_path):
            print(f"📁 {item}/")
        else:
            print(f"📄 {item}")
else:
    print("❌ Pasta de backup não encontrada!") 