/**
 * 🔐 Modal de Acesso Premium
 * Exibe popup elegante quando usuário tenta acessar conteúdo premium
 */

class PremiumAccessModal {
    constructor() {
        this.isModalOpen = false;
        this.currentRoute = null;
        this.init();
    }

    /**
     * Inicializa o sistema de modal
     */
    init() {
        console.log('🔐 Inicializando modal de acesso premium...');
        
        // Interceptar navegação para páginas premium
        this.interceptPremiumNavigation();
        
        // Adicionar estilos CSS
        this.addModalStyles();
        
        // Verificar se a página atual é premium
        this.checkCurrentPage();
        
        console.log('✅ Modal de acesso premium inicializado');
    }

    /**
     * Intercepta navegação para páginas premium
     */
    interceptPremiumNavigation() {
        // Interceptar cliques em links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (!link) return;

            if (this.isPremiumRoute(link.href)) {
                e.preventDefault();
                this.showPremiumModal(link.href);
            }
        });

        // Interceptar navegação programática
        const originalPushState = history.pushState;
        history.pushState = (...args) => {
            originalPushState.apply(history, args);
            this.checkCurrentPage();
        };

        // Interceptar mudanças de hash
        window.addEventListener('hashchange', () => {
            this.checkCurrentPage();
        });
    }

    /**
     * Verifica se a página atual é premium
     */
    checkCurrentPage() {
        const currentPath = window.location.pathname;
        if (this.isPremiumRoute(currentPath)) {
            this.showPremiumModal(currentPath);
        }
    }

    /**
     * Verifica se uma rota é premium
     */
    isPremiumRoute(route) {
        const premiumRoutes = [
            '/aposta_inteligente_premium',
            '/aposta_inteligente_premium_MS',
            '/aposta_inteligente_premium_quina',
            '/aposta_inteligente_premium_lotofacil',
            '/lotofacil_laboratorio',
            '/boloes',
            '/dashboard_MS',
            '/dashboard_lotofacil'
        ];

        return premiumRoutes.some(premiumRoute => 
            route.includes(premiumRoute) || route === premiumRoute
        );
    }

    /**
     * Exibe o modal de acesso premium
     */
    showPremiumModal(route) {
        if (this.isModalOpen) return;

        this.currentRoute = route;
        this.isModalOpen = true;
        this.createModal();
        
        // Adicionar classe ao body para prevenir scroll
        document.body.style.overflow = 'hidden';
        
        // Fechar modal com ESC
        document.addEventListener('keydown', this.handleKeydown.bind(this));
        
        // Fechar modal ao clicar fora
        document.addEventListener('click', this.handleOutsideClick.bind(this));
    }

    /**
     * Cria o modal
     */
    createModal() {
        const modalHTML = `
            <div id="premiumAccessModal" class="premium-modal-overlay">
                <div class="premium-modal">
                    <div class="premium-modal-header">
                        <div class="premium-icon">🔒</div>
                        <h2>Acesso Premium Exclusivo</h2>
                        <button class="premium-modal-close" onclick="premiumModal.closeModal()">&times;</button>
                    </div>
                    
                    <div class="premium-modal-body">
                        <div class="premium-message">
                            <p>🔒 Esta página é exclusiva para assinantes premium!</p>
                            <p>Para acessar, você precisa fazer login ou criar uma conta.</p>
                        </div>
                        
                        <div class="premium-info">
                            <h3>📋 Como Funciona:</h3>
                            <div class="info-steps">
                                <div class="step-item">
                                    <span class="step-number">1</span>
                                    <span class="step-text">Faça login ou crie sua conta</span>
                                </div>
                                <div class="step-item">
                                    <span class="step-number">2</span>
                                    <span class="step-text">Escolha um plano premium</span>
                                </div>
                                <div class="step-item">
                                    <span class="step-number">3</span>
                                    <span class="step-text">Acesse todas as funcionalidades</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="premium-modal-footer">
                        <button class="btn-premium" onclick="premiumModal.openAuthModal()">
                            <span class="btn-icon">🔐</span>
                            Acessar Página Premium
                        </button>
                        <button class="btn-home" onclick="premiumModal.goToHome()">
                            <span class="btn-icon">🏠</span>
                            Voltar ao Início
                        </button>
                    </div>
                    

                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Animar entrada do modal
        setTimeout(() => {
            const modal = document.getElementById('premiumAccessModal');
            modal.classList.add('show');
        }, 10);
    }

    /**
     * Fecha o modal
     */
    closeModal() {
        const modal = document.getElementById('premiumAccessModal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => {
                modal.remove();
                this.isModalOpen = false;
                document.body.style.overflow = '';
            }, 300);
        }
    }



    /**
     * Redireciona para página inicial
     */
    goToHome() {
        this.closeModal();
        window.location.href = '/';
    }

    /**
     * Abre o modal de autenticação existente
     */
    openAuthModal() {
        this.closeModal();
        // Abre o modal de login/cadastro que agora está disponível na página
        if (typeof openModalLogin === 'function') {
            openModalLogin('login'); // Abre modal de login por padrão
        } else {
            // Fallback: redireciona para página de login
            window.location.href = '/login';
        }
    }

    /**
     * Manipula tecla ESC
     */
    handleKeydown(e) {
        if (e.key === 'Escape') {
            this.closeModal();
        }
    }

    /**
     * Manipula clique fora do modal
     */
    handleOutsideClick(e) {
        if (e.target.id === 'premiumAccessModal') {
            this.closeModal();
        }
    }

    /**
     * Adiciona estilos CSS para o modal
     */
    addModalStyles() {
        if (document.getElementById('premium-modal-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'premium-modal-styles';
        styles.textContent = `
            .premium-modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.85);
                backdrop-filter: blur(10px);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                opacity: 0;
                transform: scale(0.9);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .premium-modal-overlay.show {
                opacity: 1;
                transform: scale(1);
            }

            .premium-modal {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 3px solid #A855F7;
                border-radius: 25px;
                max-width: 600px;
                width: 100%;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 25px 50px rgba(168, 85, 247, 0.4);
                position: relative;
            }

            .premium-modal-header {
                text-align: center;
                padding: 30px 30px 20px;
                border-bottom: 2px solid rgba(168, 85, 247, 0.3);
                position: relative;
            }

            .premium-icon {
                font-size: 4rem;
                margin-bottom: 15px;
                display: block;
            }

            .premium-modal-header h2 {
                color: #A855F7;
                font-size: 2rem;
                font-weight: 700;
                margin: 0;
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .premium-modal-close {
                position: absolute;
                top: 20px;
                right: 25px;
                background: none;
                border: none;
                color: #A855F7;
                font-size: 32px;
                cursor: pointer;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                background: rgba(168, 85, 247, 0.1);
            }

            .premium-modal-close:hover {
                background: rgba(168, 85, 247, 0.2);
                transform: scale(1.1);
            }

            .premium-modal-body {
                padding: 25px 30px;
            }

            .premium-message {
                text-align: center;
                margin-bottom: 25px;
            }

            .premium-message p {
                color: #cbd5e1;
                font-size: 1.1rem;
                margin: 8px 0;
                line-height: 1.6;
            }

            .premium-info {
                margin-bottom: 25px;
            }

            .premium-info h3 {
                color: #A855F7;
                text-align: center;
                margin-bottom: 20px;
                font-size: 1.3rem;
            }

            .info-steps {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .step-item {
                display: flex;
                align-items: center;
                background: rgba(168, 85, 247, 0.1);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 12px;
                padding: 15px;
                transition: all 0.3s ease;
            }

            .step-item:hover {
                background: rgba(168, 85, 247, 0.2);
                transform: translateY(-2px);
            }

            .step-number {
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                margin-right: 15px;
                font-size: 1.1rem;
            }

            .step-text {
                color: #cbd5e1;
                font-weight: 500;
                font-size: 1rem;
            }

            .premium-modal-footer {
                padding: 25px 30px;
                border-top: 2px solid rgba(168, 85, 247, 0.3);
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }

            .btn-premium, .btn-home {
                padding: 15px 25px;
                border: none;
                border-radius: 12px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                text-decoration: none;
                min-width: 160px;
                justify-content: center;
            }

            .btn-premium {
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                color: white;
                flex: 2;
            }

            .btn-premium:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 30px rgba(168, 85, 247, 0.4);
            }

            .btn-register {
                background: linear-gradient(135deg, #10B981, #059669);
                color: white;
                flex: 1;
            }

            .btn-register:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4);
            }

            .btn-login {
                background: transparent;
                color: #A855F7;
                border: 2px solid #A855F7;
                flex: 1;
            }

            .btn-login:hover {
                background: #A855F7;
                color: white;
                transform: translateY(-3px);
            }

            .btn-home {
                background: rgba(255, 255, 255, 0.1);
                color: #cbd5e1;
                border: 1px solid rgba(255, 255, 255, 0.3);
                flex: 1;
            }

            .btn-home:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: translateY(-3px);
            }

            .btn-icon {
                font-size: 1.1rem;
            }

            .premium-modal-guarantee {
                text-align: center;
                padding: 20px 30px 30px;
                background: rgba(168, 85, 247, 0.05);
                border-top: 1px solid rgba(168, 85, 247, 0.2);
            }

            .premium-modal-guarantee p {
                color: #94a3b8;
                margin: 5px 0;
                font-size: 0.9rem;
            }

            .premium-modal-guarantee p:first-child {
                color: #10B981;
                font-weight: 600;
            }

            /* Responsividade */
            @media (max-width: 768px) {
                .premium-modal {
                    margin: 10px;
                    max-height: 95vh;
                }

                .premium-modal-header {
                    padding: 20px 20px 15px;
                }

                .premium-modal-header h2 {
                    font-size: 1.6rem;
                }

                .premium-modal-body {
                    padding: 20px;
                }

                .info-steps {
                    gap: 10px;
                }

                .premium-modal-footer {
                    padding: 20px;
                    flex-direction: column;
                }

                .btn-premium, .btn-home {
                    width: 100%;
                    min-width: auto;
                }

                .premium-modal-guarantee {
                    padding: 15px 20px 20px;
                }
            }

            /* Scrollbar personalizada */
            .premium-modal::-webkit-scrollbar {
                width: 8px;
            }

            .premium-modal::-webkit-scrollbar-track {
                background: rgba(168, 85, 247, 0.1);
                border-radius: 4px;
            }

            .premium-modal::-webkit-scrollbar-thumb {
                background: rgba(168, 85, 247, 0.5);
                border-radius: 4px;
            }

            .premium-modal::-webkit-scrollbar-thumb:hover {
                background: rgba(168, 85, 247, 0.7);
            }
        `;

        document.head.appendChild(styles);
    }
}

// Instância global do modal
const premiumModal = new PremiumAccessModal();

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    premiumModal.init();
});

// Exportar para uso global
window.premiumModal = premiumModal;
