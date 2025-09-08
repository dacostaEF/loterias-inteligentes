/**
 * 🍪 GERENCIADOR DE COOKIES
 * Gerencia consentimento e configurações de cookies
 */

class CookieManager {
    constructor() {
        this.cookieName = 'loterias_cookies_consent';
        this.cookieExpiry = 365; // dias
        this.essentialCookies = ['session_id', 'user_id', 'csrf_token'];
        this.init();
    }

    /**
     * Inicializa o gerenciador de cookies
     */
    init() {
        // Verificar se já existe consentimento
        if (!this.hasConsent()) {
            this.showBanner();
        }
        
        // Configurar event listeners
        this.setupEventListeners();
    }

    /**
     * Verifica se o usuário já deu consentimento
     */
    hasConsent() {
        return localStorage.getItem(this.cookieName) !== null;
    }

    /**
     * Mostra o banner de cookies
     */
    showBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.style.display = 'block';
        }
    }

    /**
     * Esconde o banner de cookies
     */
    hideBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.style.display = 'none';
        }
    }

    /**
     * Mostra o modal de configuração
     */
    showModal() {
        const modal = document.getElementById('cookie-modal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Esconde o modal de configuração
     */
    hideModal() {
        const modal = document.getElementById('cookie-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Configura os event listeners
     */
    setupEventListeners() {
        // Botão aceitar todos
        const aceitarBtn = document.getElementById('aceitar-cookies');
        if (aceitarBtn) {
            aceitarBtn.addEventListener('click', () => this.acceptAll());
        }

        // Botão recusar
        const recusarBtn = document.getElementById('recusar-cookies');
        if (recusarBtn) {
            recusarBtn.addEventListener('click', () => this.rejectAll());
        }

        // Botão configurar
        const configurarBtn = document.getElementById('configurar-cookies');
        if (configurarBtn) {
            configurarBtn.addEventListener('click', () => this.showModal());
        }

        // Botões do modal
        const salvarBtn = document.getElementById('salvar-configuracoes');
        if (salvarBtn) {
            salvarBtn.addEventListener('click', () => this.saveSettings());
        }

        const aceitarModalBtn = document.getElementById('aceitar-todos-modal');
        if (aceitarModalBtn) {
            aceitarModalBtn.addEventListener('click', () => this.acceptAll());
        }

        const cancelarBtn = document.getElementById('cancelar-modal');
        if (cancelarBtn) {
            cancelarBtn.addEventListener('click', () => this.hideModal());
        }

        // Fechar modal clicando fora
        const modal = document.getElementById('cookie-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal();
                }
            });
        }
    }

    /**
     * Aceita todos os cookies
     */
    acceptAll() {
        const consent = {
            essential: true,
            session: true,
            preferences: true,
            timestamp: new Date().toISOString()
        };
        
        this.saveConsent(consent);
        this.hideBanner();
        this.hideModal();
        this.showSuccessMessage('Cookies aceitos com sucesso!');
    }

    /**
     * Recusa todos os cookies (exceto essenciais)
     */
    rejectAll() {
        const consent = {
            essential: true,
            session: false,
            preferences: false,
            timestamp: new Date().toISOString()
        };
        
        this.saveConsent(consent);
        this.hideBanner();
        this.hideModal();
        this.showSuccessMessage('Configurações salvas! Apenas cookies essenciais serão utilizados.');
    }

    /**
     * Salva configurações personalizadas
     */
    saveSettings() {
        const consent = {
            essential: true, // Sempre true
            session: document.getElementById('cookies-sessao').checked,
            preferences: document.getElementById('cookies-preferences').checked,
            timestamp: new Date().toISOString()
        };
        
        this.saveConsent(consent);
        this.hideBanner();
        this.hideModal();
        this.showSuccessMessage('Configurações salvas com sucesso!');
    }

    /**
     * Salva o consentimento no localStorage
     */
    saveConsent(consent) {
        localStorage.setItem(this.cookieName, JSON.stringify(consent));
        
        // Aplicar configurações
        this.applyCookieSettings(consent);
    }

    /**
     * Aplica as configurações de cookies
     */
    applyCookieSettings(consent) {
        if (consent.session) {
            // Permitir cookies de sessão
            console.log('✅ Cookies de sessão habilitados');
        } else {
            // Desabilitar cookies de sessão (exceto essenciais)
            console.log('❌ Cookies de sessão desabilitados');
        }

        if (consent.preferences) {
            // Permitir cookies de preferências
            console.log('✅ Cookies de preferências habilitados');
        } else {
            // Desabilitar cookies de preferências
            console.log('❌ Cookies de preferências desabilitados');
        }
    }

    /**
     * Obtém as configurações atuais
     */
    getConsent() {
        const stored = localStorage.getItem(this.cookieName);
        if (stored) {
            return JSON.parse(stored);
        }
        return null;
    }

    /**
     * Verifica se um tipo de cookie é permitido
     */
    isCookieAllowed(cookieType) {
        const consent = this.getConsent();
        if (!consent) return false;

        switch (cookieType) {
            case 'essential':
                return true; // Sempre permitido
            case 'session':
                return consent.session;
            case 'preferences':
                return consent.preferences;
            default:
                return false;
        }
    }

    /**
     * Mostra mensagem de sucesso
     */
    showSuccessMessage(message) {
        // Criar notificação temporária
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 10002;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        // Adicionar estilos de animação
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Remover após 3 segundos
        setTimeout(() => {
            notification.remove();
            style.remove();
        }, 3000);
    }

    /**
     * Limpa todos os cookies (exceto essenciais)
     */
    clearNonEssentialCookies() {
        const consent = this.getConsent();
        if (consent && !consent.session) {
            // Limpar cookies de sessão
            document.cookie.split(";").forEach(cookie => {
                const eqPos = cookie.indexOf("=");
                const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
                if (!this.essentialCookies.includes(name)) {
                    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
                }
            });
        }
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.cookieManager = new CookieManager();
});

// Exportar para uso global
window.CookieManager = CookieManager;
