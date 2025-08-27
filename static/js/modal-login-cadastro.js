// === MODAL LOGIN/CADASTRO ===
class ModalLoginCadastro {
    constructor() {
        this.modal = null;
        this.currentTab = 'login';
        this.init();
    }

    init() {
        this.createModal();
        this.bindEvents();
        this.setupValidation();
    }

    createModal() {
        // Criar o HTML do modal
        const modalHTML = `
            <div id="modal-login-cadastro" class="modal-overlay">
                <div class="modal-container">
                    <div class="modal-header">
                        <h2 class="modal-title">Acesso ao Sistema</h2>
                        <button class="modal-close" id="modal-close">&times;</button>
                    </div>
                    
                    <div class="modal-tabs">
                        <button class="tab-button active" data-tab="login">LOGIN</button>
                        <button class="tab-button" data-tab="cadastro">CADASTRO</button>
                    </div>
                    
                    <!-- ABA LOGIN -->
                    <div class="tab-content active" id="tab-login">
                        <div class="form-group">
                            <label class="form-label" for="login-email">E-mail, Celular ou CPF</label>
                            <input type="text" class="form-input" id="login-email" placeholder="Digite seu e-mail, celular ou CPF">
                            <div class="error-message" id="login-email-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="login-senha">Senha</label>
                            <input type="password" class="form-input" id="login-senha" placeholder="Digite sua senha">
                            <div class="error-message" id="login-senha-error"></div>
                        </div>
                        
                        <div class="form-link">
                            <a href="#" id="esqueceu-senha">Esqueceu a senha?</a>
                        </div>
                        
                        <button class="btn-primary" id="btn-login">ENTRAR</button>
                        
                        <div class="form-separator">
                            <span>ou</span>
                        </div>
                        
                        <button class="btn-secondary" id="btn-google-login">
                            <svg width="20" height="20" viewBox="0 0 24 24">
                                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                            </svg>
                            Entrar com Google
                        </button>
                    </div>
                    
                    <!-- ABA CADASTRO -->
                    <div class="tab-content" id="tab-cadastro">
                        <button class="btn-secondary" id="btn-google-cadastro">
                            <svg width="20" height="20" viewBox="0 0 24 24">
                                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                            </svg>
                            Cadastrar com Google
                        </button>
                        
                        <div class="form-separator">
                            <span>ou</span>
                        </div>
                        
                        <h3 style="text-align: center; margin-bottom: 20px; color: #374151;">Preencha os dados de cadastro</h3>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-nome">Nome Completo</label>
                            <input type="text" class="form-input" id="cadastro-nome" placeholder="Digite seu nome completo">
                            <div class="error-message" id="cadastro-nome-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-nascimento">Data de Nascimento</label>
                            <input type="date" class="form-input" id="cadastro-nascimento">
                            <div class="error-message" id="cadastro-nascimento-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-cpf">CPF</label>
                            <input type="text" class="form-input" id="cadastro-cpf" placeholder="000.000.000-00" maxlength="14">
                            <div class="error-message" id="cadastro-cpf-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-telefone">Telefone Celular</label>
                            <input type="tel" class="form-input" id="cadastro-telefone" placeholder="(00) 00000-0000">
                            <div class="error-message" id="cadastro-telefone-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-email">E-mail</label>
                            <input type="email" class="form-input" id="cadastro-email" placeholder="Digite seu e-mail">
                            <div class="error-message" id="cadastro-email-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-confirmar-email">Confirme seu e-mail</label>
                            <input type="email" class="form-input" id="cadastro-confirmar-email" placeholder="Confirme seu e-mail">
                            <div class="error-message" id="cadastro-confirmar-email-error"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label" for="cadastro-senha">Escolha uma senha</label>
                            <input type="password" class="form-input" id="cadastro-senha" placeholder="Digite uma senha forte">
                            <div class="error-message" id="cadastro-senha-error"></div>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" class="checkbox-input" id="termos-uso" required>
                            <label class="checkbox-label" for="termos-uso">
                                Li e aceito os <a href="#" target="_blank">termos de uso</a>.
                            </label>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" class="checkbox-input" id="receber-email" checked>
                            <label class="checkbox-label" for="receber-email">
                                Aceito receber e-mails do Loterias Inteligentes
                            </label>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" class="checkbox-input" id="receber-sms" checked>
                            <label class="checkbox-label" for="receber-sms">
                                Aceito receber SMS do Loterias Inteligentes
                            </label>
                        </div>
                        
                        <button class="btn-primary" id="btn-cadastrar">CRIAR CONTA</button>
                    </div>
                </div>
            </div>
        `;
        
        // Adicionar ao body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('modal-login-cadastro');
    }

    bindEvents() {
        // Botões para abrir o modal
        document.addEventListener('click', (e) => {
            if (e.target.id === 'btn-entrar') {
                this.openModal('login');
            } else if (e.target.id === 'btn-cadastrar-header') {
                this.openModal('cadastro');
            }
        });

        // Fechar modal
        document.getElementById('modal-close').addEventListener('click', () => {
            this.closeModal();
        });

        // Fechar ao clicar fora
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // Fechar com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) {
                this.closeModal();
            }
        });

        // Trocar abas
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });

        // Botões de ação
        document.getElementById('btn-login').addEventListener('click', () => {
            this.handleLogin();
        });

        document.getElementById('btn-cadastrar').addEventListener('click', () => {
            this.handleCadastro();
        });

        document.getElementById('btn-google-login').addEventListener('click', () => {
            this.handleGoogleLogin();
        });

        document.getElementById('btn-google-cadastro').addEventListener('click', () => {
            this.handleGoogleCadastro();
        });

        // Esqueceu senha
        document.getElementById('esqueceu-senha').addEventListener('click', (e) => {
            e.preventDefault();
            this.handleEsqueceuSenha();
        });
    }

    setupValidation() {
        // Máscara para CPF
        const cpfInput = document.getElementById('cadastro-cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            });
        }

        // Máscara para telefone
        const telefoneInput = document.getElementById('cadastro-telefone');
        if (telefoneInput) {
            telefoneInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
                value = value.replace(/(\d)(\d{4})$/, '$1-$2');
                e.target.value = value;
            });
        }
    }

    openModal(tab = 'login') {
        this.modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        this.switchTab(tab);
    }

    closeModal() {
        this.modal.classList.remove('show');
        document.body.style.overflow = '';
        this.clearErrors();
    }

    isOpen() {
        return this.modal.classList.contains('show');
    }

    switchTab(tab) {
        // Atualizar botões das abas
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        // Atualizar conteúdo das abas
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`tab-${tab}`).classList.add('active');

        this.currentTab = tab;
        this.clearErrors();
    }

    clearErrors() {
        document.querySelectorAll('.form-input').forEach(input => {
            input.classList.remove('error');
        });
        document.querySelectorAll('.error-message').forEach(error => {
            error.classList.remove('show');
            error.textContent = '';
        });
    }

    showError(inputId, message) {
        const input = document.getElementById(inputId);
        const error = document.getElementById(`${inputId}-error`);
        
        if (input && error) {
            input.classList.add('error');
            error.textContent = message;
            error.classList.add('show');
        }
    }

    validateLogin() {
        let isValid = true;
        const email = document.getElementById('login-email').value.trim();
        const senha = document.getElementById('login-senha').value.trim();

        if (!email) {
            this.showError('login-email', 'Campo obrigatório');
            isValid = false;
        }

        if (!senha) {
            this.showError('login-senha', 'Campo obrigatório');
            isValid = false;
        }

        return isValid;
    }

    validateCadastro() {
        let isValid = true;
        const nome = document.getElementById('cadastro-nome').value.trim();
        const nascimento = document.getElementById('cadastro-nascimento').value;
        const cpf = document.getElementById('cadastro-cpf').value.trim();
        const telefone = document.getElementById('cadastro-telefone').value.trim();
        const email = document.getElementById('cadastro-email').value.trim();
        const confirmarEmail = document.getElementById('cadastro-confirmar-email').value.trim();
        const senha = document.getElementById('cadastro-senha').value;
        const termos = document.getElementById('termos-uso').checked;

        if (!nome) {
            this.showError('cadastro-nome', 'Nome é obrigatório');
            isValid = false;
        }

        if (!nascimento) {
            this.showError('cadastro-nascimento', 'Data de nascimento é obrigatória');
            isValid = false;
        }

        if (!cpf) {
            this.showError('cadastro-cpf', 'CPF é obrigatório');
            isValid = false;
        } else if (cpf.replace(/\D/g, '').length !== 11) {
            this.showError('cadastro-cpf', 'CPF inválido');
            isValid = false;
        }

        if (!telefone) {
            this.showError('cadastro-telefone', 'Telefone é obrigatório');
            isValid = false;
        }

        if (!email) {
            this.showError('cadastro-email', 'E-mail é obrigatório');
            isValid = false;
        } else if (!this.isValidEmail(email)) {
            this.showError('cadastro-email', 'E-mail inválido');
            isValid = false;
        }

        if (email !== confirmarEmail) {
            this.showError('cadastro-confirmar-email', 'E-mails não coincidem');
            isValid = false;
        }

        if (!senha) {
            this.showError('cadastro-senha', 'Senha é obrigatória');
            isValid = false;
        } else if (senha.length < 6) {
            this.showError('cadastro-senha', 'Senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }

        if (!termos) {
            alert('Você deve aceitar os termos de uso');
            isValid = false;
        }

        return isValid;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    handleLogin() {
        if (!this.validateLogin()) return;

        const email = document.getElementById('login-email').value.trim();
        const senha = document.getElementById('login-senha').value.trim();

        // Aqui você implementaria a lógica de login
        console.log('Tentativa de login:', { email, senha });
        
        // Simular login bem-sucedido
        alert('Login realizado com sucesso!');
        this.closeModal();
    }

    handleCadastro() {
        if (!this.validateCadastro()) return;

        const formData = {
            nome: document.getElementById('cadastro-nome').value.trim(),
            nascimento: document.getElementById('cadastro-nascimento').value,
            cpf: document.getElementById('cadastro-cpf').value.trim(),
            telefone: document.getElementById('cadastro-telefone').value.trim(),
            email: document.getElementById('cadastro-email').value.trim(),
            senha: document.getElementById('cadastro-senha').value,
            receberEmail: document.getElementById('receber-email').checked,
            receberSMS: document.getElementById('receber-sms').checked
        };

        // Aqui você implementaria a lógica de cadastro
        console.log('Dados de cadastro:', formData);
        
        // Simular cadastro bem-sucedido
        alert('Cadastro realizado com sucesso!');
        this.closeModal();
    }

    handleGoogleLogin() {
        // Implementar login com Google
        console.log('Login com Google');
        alert('Funcionalidade de login com Google será implementada em breve!');
    }

    handleGoogleCadastro() {
        // Implementar cadastro com Google
        console.log('Cadastro com Google');
        alert('Funcionalidade de cadastro com Google será implementada em breve!');
    }

    handleEsqueceuSenha() {
        // Implementar recuperação de senha
        console.log('Esqueceu senha');
        alert('Funcionalidade de recuperação de senha será implementada em breve!');
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.modalLoginCadastro = new ModalLoginCadastro();
});

// Função global para abrir o modal (pode ser chamada de qualquer lugar)
function openModalLogin(tab = 'login') {
    if (window.modalLoginCadastro) {
        window.modalLoginCadastro.openModal(tab);
    }
}
