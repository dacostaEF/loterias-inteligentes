#!/usr/bin/env python3
"""
Script para corrigir o badge LOGGED IN em todas as páginas
"""

import os
import re
from pathlib import Path

def fix_logged_in_badge(file_path):
    """Corrige o badge LOGGED IN em um template específico"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pular se já tem a classe logged-in-badge
    if 'logged-in-badge' in content:
        print(f"✅ {file_path} já tem badge corrigido")
        return
    
    # CSS do badge responsivo
    badge_css = """
    /* CSS do Badge LOGGED IN */
    .logged-in-badge {
      position: fixed;
      top: 45px;
      left: 15px;
      background: #10B981;
      color: white;
      padding: 8px 12px;
      z-index: 10001;
      font-size: 14px;
      font-weight: bold;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      border: 2px solid white;
    }
    
    /* Responsividade para mobile */
    @media (max-width: 768px) {
      .logged-in-badge {
        top: 60px; /* Abaixa para alinhar com Tour Guiado */
        left: 10px;
        padding: 4px 8px; /* Reduz padding */
        font-size: 11px; /* Reduz fonte */
        border-radius: 3px;
        border: 1px solid white; /* Reduz borda */
      }
    }
    
    @media (max-width: 480px) {
      .logged-in-badge {
        top: 65px; /* Ajusta ainda mais para telas muito pequenas */
        left: 8px;
        padding: 3px 6px; /* Padding ainda menor */
        font-size: 10px; /* Fonte ainda menor */
      }
    }"""
    
    # Substituir o badge inline por classe
    old_badge = r'<div style="position: fixed; top: 45px; left: 15px; background: #10B981; color: white; padding: 8px 12px; z-index: 10001; font-size: 14px; font-weight: bold; border-radius: 4px; box-shadow: 0 2px 8px rgba\(0,0,0,0\.3\); border: 2px solid white;">'
    new_badge = '<div class="logged-in-badge">'
    
    content = re.sub(old_badge, new_badge, content)
    
    # Adicionar CSS antes do fechamento do </style>
    if '</style>' in content:
        content = content.replace('</style>', badge_css + '\n  </style>')
    else:
        # Se não encontrar </style>, adicionar antes do </head>
        content = content.replace('</head>', '<style>' + badge_css + '</style>\n</head>')
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} - Badge LOGGED IN corrigido")

def main():
    """Corrige badge LOGGED IN em todas as páginas"""
    
    templates_dir = Path('templates')
    
    # Páginas que já foram corrigidas
    already_done = ['dashboard_megasena.html']
    
    # Páginas para corrigir
    pages_to_fix = [
        'landing.html',
        'dashboard_milionaria.html',
        'analise_estatistica_avancada_milionaria.html',
        'analise_estatistica_avancada_quina.html',
        'analise_estatistica_avancada_lotofacil.html',
        'analise_estatistica_avancada_megasena.html',
        'dashboard_quina.html',
        'dashboard_lotofacil.html',
        'dashboard_lotomania.html',
        'upgrade_plans.html',
        'checkout.html',
        'checkout_transparente.html',
        'politica_cookies.html',
        'premium_required.html',
        'boloes_loterias.html',
        'lotofacil_laboratorio.html',
        'confianca_login.html',
        'AppLotofacil_IA_adaptativa.html'
    ]
    
    print("🔧 Corrigindo badge LOGGED IN em todas as páginas...")
    
    for filename in pages_to_fix:
        file_path = templates_dir / filename
        if file_path.exists():
            fix_logged_in_badge(file_path)
        else:
            print(f"⚠️  {file_path} não encontrado")
    
    print("\n✅ Correção concluída!")

if __name__ == "__main__":
    main()
