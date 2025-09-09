/**
 * 🎯 SCRIPT UNIVERSAL DE VERIFICAÇÃO DE ACESSO
 * 
 * Este script verifica se o usuário tem acesso a funcionalidades premium
 * antes de executar ações, evitando modais desnecessários para usuários master.
 */

class AccessChecker {
    constructor() {
        this.init();
    }

    init() {
        // Configurar verificações automáticas quando o DOM estiver pronto
        document.addEventListener('DOMContentLoaded', () => {
            this.setupAccessChecks();
        });
    }

    /**
     * Configura verificações de acesso para botões premium
     */
    setupAccessChecks() {
        // Lista de botões premium e suas respectivas rotas
        const premiumButtons = [
            {
                id: 'abrir-modal-premium',
                route: 'aposta_inteligente_premium_MS',
                action: () => this.executeMegaSenaAction()
            },
            {
                id: 'abrir-modal-premium-lotofacil',
                route: 'aposta_inteligente_premium_lotofacil',
                action: () => this.executeLotofacilAction()
            },
            {
                id: 'abrir-modal-premium-quina',
                route: 'aposta_inteligente_premium_quina',
                action: () => this.executeQuinaAction()
            },
            {
                id: 'abrir-modal-premium-milionaria',
                route: 'aposta_inteligente_premium_milionaria',
                action: () => this.executeMilionariaAction()
            },
            {
                id: 'btn-gerar-aposta-premium',
                route: 'aposta_inteligente_premium_MS',
                action: () => this.executeMegaSenaAction()
            },
            {
                id: 'btn-gerar-aposta-lotofacil',
                route: 'aposta_inteligente_premium_lotofacil',
                action: () => this.executeLotofacilAction()
            },
            {
                id: 'btn-gerar-aposta-quina',
                route: 'aposta_inteligente_premium_quina',
                action: () => this.executeQuinaAction()
            },
            {
                id: 'btn-gerar-aposta-milionaria',
                route: 'aposta_inteligente_premium_milionaria',
                action: () => this.executeMilionariaAction()
            }
        ];

        // Configurar cada botão
        premiumButtons.forEach(button => {
            const element = document.getElementById(button.id);
            if (element) {
                element.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.checkAndProceed(button.route, button.action);
                });
            }
        });
    }

    /**
     * Verifica acesso e executa ação se permitido
     */
    async checkAndProceed(routeName, onAllowed) {
        try {
            console.log(`🔍 Verificando acesso para rota: ${routeName}`);
            
            const response = await fetch(`/check_access/${routeName}`, {
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📊 Resposta do servidor:', data);

            if (data.has_access) {
                console.log('✅ Acesso liberado:', data.reason);
                // Usuário tem acesso (master ou premium) -> executa ação
                onAllowed && onAllowed();
                return;
            }

            // Usuário não tem acesso -> decide ação
            this.handleAccessDenied(data);

        } catch (error) {
            console.error('❌ Erro ao verificar acesso:', error);
            this.showError('Não foi possível verificar o acesso. Tente novamente.');
        }
    }

    /**
     * Trata casos de acesso negado
     */
    handleAccessDenied(data) {
        console.log('🚫 Acesso negado:', data.reason);

        switch (data.reason) {
            case 'not_logged_in':
                // Usuário não logado -> redireciona para login
                console.log('🔐 Usuário não logado. Redirecionando para login...');
                this.redirectToLogin();
                break;

            case 'premium_required':
                // Precisa de plano premium -> mostra modal ou redireciona
                console.log('💎 Acesso premium necessário. Abrindo modal...');
                this.showPremiumModal(data.upgrade_url);
                break;

            default:
                // Outros casos
                this.showError(data.message || 'Acesso negado.');
        }
    }

    /**
     * Redireciona para página de login
     */
    redirectToLogin() {
        // Tentar abrir modal de login se disponível
        if (typeof window.openModalLogin === 'function') {
            window.openModalLogin('login');
        } else {
            // Fallback: redirecionar para página de login
            window.location.href = '/login';
        }
    }

    /**
     * Mostra modal de planos premium
     */
    showPremiumModal(upgradeUrl) {
        // Tentar abrir modal elegante se disponível
        if (typeof window.openWelcomeModal === 'function') {
            window.openWelcomeModal();
        } else if (upgradeUrl) {
            // Fallback: redirecionar para página de planos
            window.location.href = upgradeUrl;
        } else {
            // Último fallback
            window.location.href = '/upgrade_plans';
        }
    }

    /**
     * Mostra mensagem de erro
     */
    showError(message) {
        alert(message);
    }

    /**
     * Ações específicas para cada loteria
     */
    executeMegaSenaAction() {
        console.log('🎯 Executando ação da Mega-Sena...');
        // Abrir modal de frequência ou executar geração de aposta
        if (typeof abrirModal === 'function') {
            abrirModal('frequencia');
        } else if (typeof gerarApostaInteligentePremium === 'function') {
            gerarApostaInteligentePremium();
        } else {
            console.log('⚠️ Função de ação não encontrada para Mega-Sena');
        }
    }

    executeLotofacilAction() {
        console.log('🎯 Executando ação da Lotofácil...');
        if (typeof abrirModal === 'function') {
            abrirModal('frequencia');
        } else if (typeof gerarApostaInteligenteLotofacil === 'function') {
            gerarApostaInteligenteLotofacil();
        } else {
            console.log('⚠️ Função de ação não encontrada para Lotofácil');
        }
    }

    executeQuinaAction() {
        console.log('🎯 Executando ação da Quina...');
        if (typeof abrirModal === 'function') {
            abrirModal('frequencia');
        } else if (typeof gerarApostaInteligenteQuina === 'function') {
            gerarApostaInteligenteQuina();
        } else {
            console.log('⚠️ Função de ação não encontrada para Quina');
        }
    }

    executeMilionariaAction() {
        console.log('🎯 Executando ação da Milionária...');
        if (typeof abrirModal === 'function') {
            abrirModal('frequencia');
        } else if (typeof gerarApostaInteligenteMilionaria === 'function') {
            gerarApostaInteligenteMilionaria();
        } else {
            console.log('⚠️ Função de ação não encontrada para Milionária');
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.accessChecker = new AccessChecker();
    
    // Verificar acesso automaticamente para páginas premium
    const currentPath = window.location.pathname;
    const premiumRoutes = [
        '/dashboard_MS',
        '/aposta_inteligente_premium_MS',
        '/analise_estatistica_avancada_megasena',
        '/dashboard_lotofacil',
        '/aposta_inteligente_premium_lotofacil',
        '/lotofacil_laboratorio',
        '/aposta_inteligente_premium_quina',
        '/aposta_inteligente_premium',
        '/boloes_loterias'
    ];
    
    if (premiumRoutes.includes(currentPath)) {
        console.log('🔍 Verificando acesso automático para:', currentPath);
        window.accessChecker.checkAndProceed(currentPath.substring(1), () => {
            console.log('✅ Usuário tem acesso à página');
        });
    }
});

// Função global para verificação manual
window.checkAccess = function(routeName, onAllowed) {
    if (window.accessChecker) {
        window.accessChecker.checkAndProceed(routeName, onAllowed);
    } else {
        console.error('❌ AccessChecker não inicializado');
    }
};
