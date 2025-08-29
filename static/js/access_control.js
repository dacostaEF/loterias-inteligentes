/**
 * 🔐 Sistema de Controle de Acesso Frontend
 * Gerencia acesso às páginas premium e exibe modal de upgrade quando necessário
 */

class AccessControl {
    constructor() {
        this.currentUser = null;
        this.isInitialized = false;
        this.upgradeModal = null;
    }

    /**
     * Inicializa o sistema de controle de acesso
     */
    init() {
        if (this.isInitialized) return;
        
        console.log('🔐 Inicializando sistema de controle de acesso...');
        
        // Verificar acesso da página atual
        this.checkPageAccess();
        
        // Interceptar links premium
        this.interceptPremiumLinks();
        
        // Adicionar estilos do modal
        this.addModalStyles();
        
        this.isInitialized = true;
        console.log('✅ Sistema de controle de acesso inicializado');
    }

    /**
     * Verifica se o usuário tem acesso à página atual
     */
    async checkPageAccess() {
        const routeName = this.getRouteNameFromPath();
        if (!routeName) return;

        try {
            const response = await fetch(`/check_access/${routeName}`);
            const data = await response.json();

            if (!data.has_access) {
                if (data.reason === 'premium_required') {
                    this.showUpgradeModal(data.message);
                } else if (data.reason === 'not_logged_in') {
                    // Redirecionar para login
                    window.location.href = '/login';
                }
            }
        } catch (error) {
            console.error('Erro ao verificar acesso:', error);
        }
    }

    /**
     * Extrai o nome da rota do caminho atual
     */
    getRouteNameFromPath() {
        const path = window.location.pathname;
        const route = path.substring(1); // Remove a barra inicial
        
        // Mapear rotas para nomes de verificação
        const routeMapping = {
            'aposta_inteligente_premium': 'aposta_inteligente_premium',
            'aposta_inteligente_premium_MS': 'aposta_inteligente_premium_MS',
            'aposta_inteligente_premium_quina': 'aposta_inteligente_premium_quina',
            'aposta_inteligente_premium_lotofacil': 'aposta_inteligente_premium_lotofacil',
            'lotofacil_laboratorio': 'lotofacil_laboratorio',
            'boloes': 'boloes_loterias',
            'dashboard_MS': 'dashboard_megasena',
            'dashboard_lotofacil': 'dashboard_lotofacil'
        };

        return routeMapping[route] || null;
    }

    /**
     * Intercepta cliques em links premium
     */
    interceptPremiumLinks() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (!link) return;

            if (this.isPremiumLink(link.href)) {
                e.preventDefault();
                this.checkLinkAccess(link.href);
            }
        });
    }

    /**
     * Verifica se um link é para página premium
     */
    isPremiumLink(href) {
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

        return premiumRoutes.some(route => href.includes(route));
    }

    /**
     * Verifica acesso a um link específico
     */
    async checkLinkAccess(href) {
        try {
            const routeName = this.getRouteNameFromPath();
            if (!routeName) return;

            const response = await fetch(`/check_access/${routeName}`);
            const data = await response.json();

            if (data.has_access) {
                window.location.href = href;
            } else {
                if (data.reason === 'premium_required') {
                    this.showUpgradeModal(data.message);
                } else if (data.reason === 'not_logged_in') {
                    window.location.href = '/login';
                }
            }
        } catch (error) {
            console.error('Erro ao verificar acesso ao link:', error);
        }
    }

    /**
     * Exibe modal de upgrade
     */
    showUpgradeModal(message = 'Esta página requer uma assinatura premium.') {
        if (this.upgradeModal) {
            this.upgradeModal.style.display = 'block';
            return;
        }

        this.createUpgradeModal(message);
        this.upgradeModal.style.display = 'block';
    }

    /**
     * Cria o modal de upgrade
     */
    createUpgradeModal(message) {
        const modal = document.createElement('div');
        modal.className = 'upgrade-modal-overlay';
        modal.innerHTML = `
            <div class="upgrade-modal">
                <div class="upgrade-modal-header">
                    <h3>⭐ Acesso Premium Necessário</h3>
                    <button class="upgrade-modal-close" onclick="accessControl.closeUpgradeModal()">&times;</button>
                </div>
                <div class="upgrade-modal-body">
                    <div class="upgrade-icon">🔒</div>
                    <p class="upgrade-message">${message}</p>
                    <div class="upgrade-benefits">
                        <h4>Com o plano Premium você terá acesso a:</h4>
                        <ul>
                            <li>✅ Todas as loterias disponíveis</li>
                            <li>✅ Análises estatísticas avançadas</li>
                            <li>✅ Geração de apostas inteligentes</li>
                            <li>✅ Laboratório de simulações</li>
                            <li>✅ Participação em bolões</li>
                            <li>✅ Suporte prioritário</li>
                        </ul>
                    </div>
                </div>
                <div class="upgrade-modal-footer">
                    <button class="btn-upgrade" onclick="accessControl.selectPlan()">
                        Ver Planos Premium
                    </button>
                    <button class="btn-login" onclick="accessControl.redirectToLogin()">
                        Fazer Login
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.upgradeModal = modal;
    }

    /**
     * Fecha o modal de upgrade
     */
    closeUpgradeModal() {
        if (this.upgradeModal) {
            this.upgradeModal.style.display = 'none';
        }
    }

    /**
     * Redireciona para página de planos
     */
    selectPlan() {
        this.closeUpgradeModal();
        window.location.href = '/upgrade_plans';
    }

    /**
     * Redireciona para página de login
     */
    redirectToLogin() {
        this.closeUpgradeModal();
        window.location.href = '/login';
    }

    /**
     * Adiciona estilos CSS para o modal
     */
    addModalStyles() {
        if (document.getElementById('access-control-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'access-control-styles';
        styles.textContent = `
            .upgrade-modal-overlay {
                display: none;
                position: fixed;
                z-index: 10000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(5px);
                animation: fadeIn 0.3s ease-out;
            }

            .upgrade-modal {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                margin: 5% auto;
                border: 2px solid #A855F7;
                border-radius: 20px;
                width: 90%;
                max-width: 500px;
                box-shadow: 0 20px 40px rgba(168, 85, 247, 0.3);
                animation: slideIn 0.3s ease-out;
            }

            .upgrade-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 25px;
                border-bottom: 1px solid rgba(168, 85, 247, 0.3);
            }

            .upgrade-modal-header h3 {
                color: #A855F7;
                margin: 0;
                font-size: 1.5rem;
                font-weight: 600;
            }

            .upgrade-modal-close {
                background: none;
                border: none;
                color: #A855F7;
                font-size: 28px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.3s ease;
            }

            .upgrade-modal-close:hover {
                background: rgba(168, 85, 247, 0.2);
                transform: scale(1.1);
            }

            .upgrade-modal-body {
                padding: 25px;
                text-align: center;
            }

            .upgrade-icon {
                font-size: 4rem;
                margin-bottom: 20px;
            }

            .upgrade-message {
                color: #cbd5e1;
                font-size: 1.1rem;
                margin-bottom: 25px;
                line-height: 1.6;
            }

            .upgrade-benefits {
                text-align: left;
                background: rgba(168, 85, 247, 0.1);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(168, 85, 247, 0.3);
            }

            .upgrade-benefits h4 {
                color: #A855F7;
                margin-bottom: 15px;
                font-size: 1.1rem;
                text-align: center;
            }

            .upgrade-benefits ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            .upgrade-benefits li {
                color: #cbd5e1;
                padding: 8px 0;
                border-bottom: 1px solid rgba(168, 85, 247, 0.2);
                font-size: 0.95rem;
            }

            .upgrade-benefits li:last-child {
                border-bottom: none;
            }

            .upgrade-modal-footer {
                padding: 20px 25px;
                border-top: 1px solid rgba(168, 85, 247, 0.3);
                display: flex;
                gap: 15px;
                justify-content: center;
            }

            .btn-upgrade, .btn-login {
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }

            .btn-upgrade {
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                color: white;
                flex: 2;
            }

            .btn-upgrade:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(168, 85, 247, 0.4);
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
                transform: translateY(-2px);
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 768px) {
                .upgrade-modal {
                    margin: 10% auto;
                    width: 95%;
                }

                .upgrade-modal-header {
                    padding: 15px 20px;
                }

                .upgrade-modal-header h3 {
                    font-size: 1.3rem;
                }

                .upgrade-modal-body {
                    padding: 20px;
                }

                .upgrade-modal-footer {
                    padding: 15px 20px;
                    flex-direction: column;
                }

                .btn-upgrade, .btn-login {
                    width: 100%;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

// Instância global do sistema de controle de acesso
const accessControl = new AccessControl();

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    accessControl.init();
});

// Inicializar o sistema de controle de acesso
