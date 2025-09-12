#!/usr/bin/env python3
"""
Script para implementar rodapé em todas as páginas restantes
"""

import os
import re
from pathlib import Path

def add_footer_to_template(file_path):
    """Adiciona rodapé a um template específico"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pular se já tem rodapé
    if 'site-footer' in content:
        print(f"✅ {file_path} já tem rodapé")
        return
    
    # CSS do rodapé
    footer_css = """
  <!-- CSS do Rodapé -->
  <style>
    body {
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    
    .main-content {
      flex: 1;
    }
    
    .site-footer{
      background: linear-gradient(135deg, rgba(30,27,41,.95), rgba(42,35,64,.95));
      border-top: 1px solid rgba(255,255,255,0.08);
      padding: 10px 16px;
      font-size:.84rem;
      color:#cbd5e1;
      margin-top: auto;
    }
    .site-footer .footer-row{
      max-width:1200px;
      margin:0 auto;
      display:grid;
      grid-template-columns:1fr auto;
      gap:10px;
      align-items:center;
    }
    .site-footer strong{
      color:#A855F7;
      font-weight:700;
    }
    .site-footer a{
      color:#10b981;
      text-decoration:none;
      border-bottom:1px dotted rgba(16,185,129,.35);
    }
    .site-footer a:hover{
      color:#059669;
      border-bottom-color:transparent;
    }
    .footer-meta{
      opacity:.9;
    }
    .footer-toggle{
      background:transparent;
      border:1px solid rgba(168,85,247,.6);
      color:#A855F7;
      font-weight:600;
      padding:6px 10px;
      border-radius:8px;
      cursor:pointer;
      transition:transform .15s ease,background .2s,border-color .2s;
    }
    .footer-toggle:hover{
      transform:translateY(-1px);
      background:rgba(168,85,247,.1);
    }
    .footer-more{
      max-width:1200px;
      margin:8px auto 0;
      padding:10px 12px;
      background:rgba(168,85,247,.06);
      border:1px solid rgba(168,85,247,.25);
      border-radius:10px;
      line-height:1.55;
      font-size:.9rem;
    }
    @media (max-width:768px){
      .site-footer{
        padding:10px 12px;
        font-size:.8rem;
      }
      .site-footer .footer-row{
        grid-template-columns:1fr;
        gap:6px;
      }
      .footer-meta{
        font-size:.78rem;
      }
    }
    
    /* CSS do Modal */
    .footer-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    
    .footer-modal .modal-content {
      background: linear-gradient(135deg, #1e1b29, #2a2340);
      border-radius: 15px;
      max-width: 800px;
      width: 100%;
      max-height: 80vh;
      overflow-y: auto;
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .footer-modal .modal-header {
      padding: 20px 25px 15px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .footer-modal .modal-header h4 {
      color: #A855F7;
      font-size: 1.2rem;
      margin: 0;
    }
    
    .footer-modal .modal-close {
      background: none;
      border: none;
      color: #cbd5e1;
      font-size: 24px;
      cursor: pointer;
      padding: 0;
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: background 0.2s;
    }
    
    .footer-modal .modal-close:hover {
      background: rgba(255, 255, 255, 0.1);
    }
    
    .footer-modal .modal-body {
      padding: 20px 25px 25px;
      color: #cbd5e1;
      line-height: 1.6;
    }
    
    .footer-modal details {
      margin: 15px 0;
      border: 1px solid rgba(168, 85, 247, 0.2);
      border-radius: 8px;
      padding: 10px;
      background: rgba(168, 85, 247, 0.05);
    }
    
    .footer-modal details summary {
      cursor: pointer;
      padding: 8px 0;
      color: #A855F7;
      font-weight: 600;
      list-style: none;
    }
    
    .footer-modal details summary::-webkit-details-marker {
      display: none;
    }
    
    .footer-modal details summary::before {
      content: "▶ ";
      margin-right: 8px;
      transition: transform 0.2s;
    }
    
    .footer-modal details[open] summary::before {
      transform: rotate(90deg);
    }
    
    .footer-modal details ul {
      margin: 10px 0 0 20px;
      padding: 0;
    }
    
    .footer-modal details li {
      margin: 8px 0;
      color: #e2e8f0;
    }
    
    .footer-modal a {
      color: #10b981;
      text-decoration: none;
      border-bottom: 1px dotted rgba(16, 185, 129, 0.5);
    }
    
    .footer-modal a:hover {
      color: #059669;
      border-bottom-color: transparent;
    }
    
    @media (max-width: 768px) {
      .footer-modal {
        padding: 10px;
      }
      
      .footer-modal .modal-content {
        max-height: 90vh;
      }
      
      .footer-modal .modal-header,
      .footer-modal .modal-body {
        padding: 15px 20px;
      }
      
      .footer-modal .modal-header h4 {
        font-size: 1.1rem;
      }
    }
  </style>"""

    # HTML do rodapé
    footer_html = """
  <!-- RODAPÉ -->
  <footer class="site-footer" role="contentinfo">
    <div class="footer-row">
      <div class="footer-text">
        <strong>Política de Honestidade & Jogo Responsável.</strong>
        Loterias Inteligentes é uma plataforma independente de análise estatística,
        sem vínculo com a Caixa Econômica Federal. Nossas ferramentas oferecem
        insights baseados em dados, mas loterias envolvem sorte e aleatoriedade —
        não há garantias de ganhos. Jogue com responsabilidade.
      </div>
      <div class="footer-actions">
        <button class="footer-toggle" id="footerToggle" onclick="openFooterModal()">
          Ver detalhes
        </button>
      </div>
    </div>
  </footer>

  <!-- MODAL DO RODAPÉ -->
  <div id="footer-modal" class="footer-modal" style="display: none;">
    <div class="modal-content">
      <div class="modal-header">
        <h4 style="margin:0 0 .6rem 0;">Política de Honestidade & Jogo Responsável — Detalhes</h4>
        <button class="modal-close" onclick="closeFooterModal()">&times;</button>
      </div>
      <div class="modal-body">
        <p style="opacity:.9;margin:.3rem 0 1rem 0;">
          Somos uma plataforma independente de <strong>análise estatística</strong> para loterias. 
          Nosso objetivo é oferecer <em>insights</em> úteis — sem prometer resultados. Jogue com responsabilidade.
        </p>

        <details>
          <summary><strong>1) Como nossas ferramentas funcionam</strong></summary>
          <ul>
            <li><strong>Fontes de dados:</strong> resultados oficiais públicos.</li>
            <li><strong>Métodos estatísticos:</strong> frequência, distribuição, padrões sequenciais, correlações/clusterização, sazonalidade e testes simples de aleatoriedade.</li>
            <li><strong>Atualização:</strong> os painéis são atualizados periodicamente conforme novos concursos são publicados.</li>
            <li><strong>Objetivo:</strong> reduzir ruídos e apoiar escolhas mais conscientes; <u>não</u> prever o futuro.</li>
          </ul>
        </details>

        <details>
          <summary><strong>2) Limites e incertezas (disclaimer)</strong></summary>
          <ul>
            <li>Loterias são jogos de <strong>sorte e aleatoriedade</strong>. Não existe garantia de acerto ou lucro.</li>
            <li>Análises baseadas em dados passados <strong>não determinam</strong> resultados futuros.</li>
            <li>Use as ferramentas como <em>apoio</em> à decisão — a escolha final e os riscos são seus.</li>
          </ul>
        </details>

        <details>
          <summary><strong>3) Jogo responsável</strong></summary>
          <ul>
            <li>Defina <strong>limite de gasto</strong> e <strong>frequência</strong> antes de apostar; não tente "recuperar perdas".</li>
            <li><strong>Sinais de alerta:</strong> apostar com dinheiro reservado a contas essenciais; esconder gastos; ansiedade ao não apostar; comprometer relações/prazo de trabalho.</li>
            <li><strong>Se precisar de apoio:</strong> procure serviços de saúde locais ou grupos de ajuda para comportamentos de jogo. Cuidar de si é prioridade.</li>
          </ul>
        </details>

        <details>
          <summary><strong>4) Privacidade & LGPD</strong></summary>
          <ul>
            <li>Tratamos dados pessoais conforme a <strong>LGPD</strong> (Lei 13.709/2018).</li>
            <li>Usamos cookies para funcionalidades essenciais e métricas de uso do site.</li>
            <li><strong>Seus direitos:</strong> confirmação de tratamento, acesso, correção, anonimização/eliminação, portabilidade e revogação de consentimento.</li>
            <li><strong>Contato do DPO/Suporte:</strong> <a href="mailto:support@seudominio.com">support@seudominio.com</a></li>
          </ul>
        </details>

        <details>
          <summary><strong>5) Independência e marcas</strong></summary>
          <ul>
            <li>Plataforma <strong>independente</strong>, sem vínculo, patrocínio ou endosso da Caixa Econômica Federal.</li>
            <li>Marcas e logos de terceiros pertencem aos seus respectivos proprietários.</li>
          </ul>
        </details>

        <details>
          <summary><strong>6) Transparência técnica</strong></summary>
          <ul>
            <li><strong>Metodologia:</strong> cada estudo mostra o <em>critério</em> usado (ex.: janela de concursos, regras de cálculo, filtros aplicados).</li>
            <li><strong>Relato de desempenho:</strong> quando exibimos acertos ou simulações, indicamos o <em>período</em>, <em>parâmetros</em> e <em>limitações</em> — sem "cherry-picking".</li>
          </ul>
        </details>

        <details>
          <summary><strong>7) Documentos legais & contato</strong></summary>
          <ul>
            <li><a href="/politica-de-honestidade">Política de Honestidade</a> • <a href="/termos">Termos de Uso</a> • <a href="/privacidade">Política de Privacidade</a></li>
            <li><strong>CNPJ:</strong> 00.000.000/0000-00 • <strong>WhatsApp:</strong> <a href="https://wa.me/55SEUNUMERO" target="_blank" rel="noopener">fale com a equipe</a></li>
            <li><strong>Atendimento:</strong> seg–sex, 9h–18h (horário local)</li>
          </ul>
        </details>

        <p style="opacity:.7;margin-top:.8rem;font-size:.9em;">Última atualização: <em>agosto/2025</em></p>
      </div>
    </div>
  </div>

  <!-- JavaScript do modal do rodapé -->
  <script>
    function openFooterModal() {
      const modal = document.getElementById('footer-modal');
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Previne scroll do body
      }
    }
    
    function closeFooterModal() {
      const modal = document.getElementById('footer-modal');
      if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaura scroll do body
      }
    }
    
    // Fechar modal ao clicar fora dele
    document.addEventListener('click', function(event) {
      const modal = document.getElementById('footer-modal');
      if (event.target === modal) {
        closeFooterModal();
      }
    });
    
    // Fechar modal com tecla ESC
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape') {
        closeFooterModal();
      }
    });
  </script>"""

    # Adicionar CSS após o último link de CSS
    css_pattern = r'(<link[^>]*rel="stylesheet"[^>]*>[\s\n]*)+'
    css_matches = list(re.finditer(css_pattern, content))
    
    if css_matches:
        last_css = css_matches[-1]
        content = content[:last_css.end()] + footer_css + content[last_css.end():]
    else:
        # Se não encontrar CSS, adicionar antes do </head>
        content = content.replace('</head>', footer_css + '\n</head>')
    
    # Envolver conteúdo em main-content
    body_pattern = r'<body[^>]*>'
    body_match = re.search(body_pattern, content)
    if body_match:
        body_end = body_match.end()
        content = content[:body_end] + '\n  <div class="main-content">\n' + content[body_end:]
    
    # Adicionar rodapé antes do </body>
    content = content.replace('</body>', '  </div> <!-- Fim do main-content -->\n' + footer_html + '\n</body>')
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} - Rodapé implementado")

def main():
    """Implementa rodapé em todas as páginas restantes"""
    
    templates_dir = Path('templates')
    
    # Páginas que já têm rodapé
    already_done = [
        'landing.html',
        'dashboard_milionaria.html',
        'analise_estatistica_avancada_milionaria.html',
        'dashboard_megasena.html'
    ]
    
    # Páginas para implementar
    pages_to_do = [
        'analise_estatistica_avancada_megasena.html',
        'dashboard_quina.html',
        'analise_estatistica_avancada_quina.html',
        'dashboard_lotofacil.html',
        'analise_estatistica_avancada_lotofacil.html',
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
    
    print("🚀 Implementando rodapé em todas as páginas...")
    
    for filename in pages_to_do:
        file_path = templates_dir / filename
        if file_path.exists():
            add_footer_to_template(file_path)
        else:
            print(f"⚠️  {file_path} não encontrado")
    
    print("\n✅ Implementação concluída!")

if __name__ == "__main__":
    main()
