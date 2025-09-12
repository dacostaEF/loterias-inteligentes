#!/usr/bin/env python3
"""
Script para converter todas as páginas HTML para usar o layout base.html
"""

import os
import re
from pathlib import Path

def convert_template(file_path):
    """Converte um template individual para usar base.html"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pular se já foi convertido
    if '{% extends "base.html" %}' in content:
        print(f"✅ {file_path} já convertido")
        return
    
    # Extrair título
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Loterias Inteligentes"
    
    # Encontrar o início do body
    body_start = content.find('<body')
    if body_start == -1:
        print(f"❌ {file_path} não tem <body>")
        return
    
    # Encontrar o início do conteúdo (após <body>)
    body_tag_end = content.find('>', body_start) + 1
    content_start = body_tag_end
    
    # Encontrar o fim do body
    body_end = content.rfind('</body>')
    if body_end == -1:
        print(f"❌ {file_path} não tem </body>")
        return
    
    # Extrair o conteúdo do body
    body_content = content[content_start:body_end].strip()
    
    # Remover scripts e links do head que já estão no base.html
    head_removals = [
        r'<link[^>]*href="https://fonts\.googleapis\.com[^"]*"[^>]*>',
        r'<link[^>]*href="https://cdnjs\.cloudflare\.com[^"]*"[^>]*>',
        r'<link[^>]*href="/static/img/Favicon_LI\.png"[^>]*>',
        r'<meta[^>]*name="theme-color"[^>]*>',
        r'<meta[^>]*name="msapplication-[^"]*"[^>]*>',
        r'<meta[^>]*name="apple-mobile-web-app-[^"]*"[^>]*>',
        r'<link[^>]*rel="manifest"[^>]*>',
        r'<link[^>]*rel="preload"[^>]*>',
        r'<noscript>[^<]*</noscript>',
    ]
    
    for pattern in head_removals:
        body_content = re.sub(pattern, '', body_content, flags=re.IGNORECASE)
    
    # Criar o novo conteúdo
    new_content = f"""{{% extends "base.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block content %}}
{body_content}
{{% endblock %}}"""
    
    # Salvar o arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {file_path} convertido")

def main():
    """Converte todos os templates"""
    
    templates_dir = Path('templates')
    
    # Lista de arquivos para converter (excluindo base.html e partials)
    files_to_convert = [
        'analise_estatistica_avancada_lotofacil.html',
        'analise_estatistica_avancada_megasena.html',
        'analise_estatistica_avancada_milionaria_OutroPgrogarad.html',
        'analise_estatistica_avancada_milionaria.html',
        'analise_estatistica_avancada_quina.html',
        'AppLotofacil_IA_adaptativa.html',
        'boloes_loterias.html',
        'checkout_transparente.html',
        'confianca_login.html',
        'cookie_banner.html',
        'dashboard_lotofacil.html',
        'dashboard_lotomania.html',
        'dashboard_milionaria.html',
        'dashboard_quina.html',
        'lotofacil_laboratorio.html',
        'politica_cookies.html',
        'premium_required.html',
    ]
    
    print("🔄 Convertendo templates para layout base...")
    
    for filename in files_to_convert:
        file_path = templates_dir / filename
        if file_path.exists():
            convert_template(file_path)
        else:
            print(f"⚠️  {file_path} não encontrado")
    
    print("\n✅ Conversão concluída!")

if __name__ == "__main__":
    main()
