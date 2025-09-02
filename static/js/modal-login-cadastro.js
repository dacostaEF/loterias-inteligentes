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
        
        // 🔒 PROTEÇÃO: Se o usuário fechar sem fazer login, redireciona para landing page
        // Verifica se estamos em uma página premium e se o usuário não está autenticado
        if (this.isPremiumPage() && !this.isUserAuthenticated()) {
            this.redirectToLanding();
        }
    }
    
    /**
     * Verifica se a página atual é premium
     */
    isPremiumPage() {
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
        
        const currentPath = window.location.pathname;
        return premiumRoutes.some(route => currentPath.includes(route));
    }
    
    /**
     * Verifica se o usuário está autenticado
     * Por enquanto, sempre retorna false (usuário não autenticado)
     */
    isUserAuthenticated() {
        // TODO: Implementar verificação real de autenticação
        return false;
    }
    
    /**
     * Redireciona para a landing page
     */
    redirectToLanding() {
        console.log('🔒 Usuário fechou modal sem autenticação. Redirecionando para landing page...');
        setTimeout(() => {
            window.location.href = '/';
        }, 300); // Pequeno delay para suavizar a transição
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

    async handleCadastro() {
        if (!this.validateCadastro()) return;

        const formData = {
            nome_completo: document.getElementById('cadastro-nome').value.trim(),
            data_nascimento: document.getElementById('cadastro-nascimento').value,
            cpf: document.getElementById('cadastro-cpf').value.trim(),
            telefone: document.getElementById('cadastro-telefone').value.trim(),
            email: document.getElementById('cadastro-email').value.trim(),
            senha: document.getElementById('cadastro-senha').value,
            receber_emails: document.getElementById('receber-email').checked,
            receber_sms: document.getElementById('receber-sms').checked,
            aceitou_termos: true
        };

        console.log('Dados de cadastro:', formData);
        
        try {
            // Enviar dados para a nova rota de cadastro
            const response = await fetch('/salvar_cadastro', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                // ✅ Cadastro realizado com sucesso - abrir modal de confirmação
                this.closeModal();
                formData.usuario_id = data.user_id; // Adicionar ID do usuário
                this.openModalConfirmacao(formData);
            } else {
                alert('Erro ao realizar cadastro: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao enviar cadastro:', error);
            alert('Erro ao realizar cadastro. Tente novamente.');
        }
    }

    handleGoogleLogin() {
        // 🔗 Redirecionar para Google OAuth
        console.log('🔗 Iniciando login com Google...');
        try {
            // Redirecionar para rota de autenticação Google
            window.location.href = '/auth/google';
        } catch (error) {
            console.error('❌ Erro ao iniciar login Google:', error);
            alert('Erro ao conectar com Google. Tente novamente.');
        }
    }

    // 🔐 Login com Google via OAuth Direto (SOLUÇÃO DEFINITIVA)
    handleGoogleCadastro() {
        console.log('🔐 Iniciando login Google com OAuth Direto...');
        
        try {
            // Configurações OAuth corretas do Google Cloud Console
            const clientId = '109705001662-2pshc4dargmtf3chn9c9r31lfk607mr8.apps.googleusercontent.com';
            const redirectUri = 'http://localhost:5000/auth/google/callback';
            const scope = 'email profile';
            
            // Construir URL de autorização OAuth
            const authUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&response_type=code&access_type=offline&prompt=consent`;
            
            console.log('🔗 Redirecionando para Google OAuth:', authUrl);
            
            // Redirecionar para Google OAuth
            window.location.href = authUrl;
            
        } catch (error) {
            console.error('❌ Erro ao iniciar login Google:', error);
            alert('Erro ao conectar com Google. Tente novamente.');
        }
    }

    handleEsqueceuSenha() {
        // Implementar recuperação de senha
        console.log('Esqueceu senha');
        alert('Funcionalidade de recuperação de senha será implementada em breve!');
    }

    // 🎯 Abrir modal de confirmação de cadastro
    openModalConfirmacao(formData) {
        console.log('🎯 Abrindo modal de confirmação...');
        
        // Preencher dados no modal
        document.getElementById('confirmacao-email').textContent = formData.email;
        document.getElementById('confirmacao-telefone').textContent = formData.telefone;
        
        // Mostrar modal
        document.getElementById('modal-confirmacao').style.display = 'flex';
        
        // Configurar botão de envio
        this.setupEnvioCodigo(formData);
        
        // Configurar inputs do código (inicialmente ocultos)
        this.setupCodigoInputs();
        
        // Configurar botões de confirmação (inicialmente ocultos)
        this.setupConfirmacaoButtons(formData);
    }

    // 🔧 Configurar inputs do código de confirmação
    setupCodigoInputs() {
        const inputs = document.querySelectorAll('.codigo-input');
        
        inputs.forEach((input, index) => {
            // Limpar valor
            input.value = '';
            
            // Evento de digitação
            input.addEventListener('input', (e) => {
                const value = e.target.value;
                
                // Só aceita números
                if (!/^\d*$/.test(value)) {
                    e.target.value = '';
                    return;
                }
                
                // Marcar como preenchido
                if (value) {
                    input.classList.add('filled');
                    
                    // Ir para próximo input
                    if (index < inputs.length - 1) {
                        inputs[index + 1].focus();
                    }
                } else {
                    input.classList.remove('filled');
                }
            });
            
            // Evento de backspace
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !input.value && index > 0) {
                    inputs[index - 1].focus();
                }
            });
        });
    }

    // 🔧 Configurar envio de código
    setupEnvioCodigo(formData) {
        const btnEnviar = document.getElementById('btn-enviar-codigo');
        
        btnEnviar.addEventListener('click', () => {
            const tipoEnvio = document.querySelector('input[name="tipo-envio"]:checked').value;
            this.enviarCodigo(formData, tipoEnvio);
        });
    }

    // 🔧 Configurar botões do modal de confirmação
    setupConfirmacaoButtons(formData) {
        const btnConfirmar = document.getElementById('btn-confirmar-codigo');
        const btnReenviar = document.getElementById('btn-reenviar-codigo');
        
        // Botão confirmar código
        btnConfirmar.addEventListener('click', () => {
            this.validarCodigo(formData);
        });
        
        // Botão reenviar código
        btnReenviar.addEventListener('click', () => {
            const tipoEnvio = document.querySelector('input[name="tipo-envio"]:checked').value;
            this.enviarCodigo(formData, tipoEnvio);
        });
    }

    // ✅ Validar código de confirmação
    async validarCodigo(formData) {
        const inputs = document.querySelectorAll('.codigo-input');
        const codigo = Array.from(inputs).map(input => input.value).join('');
        
        if (codigo.length !== 6) {
            this.showConfirmacaoMessage('Por favor, insira o código completo de 6 dígitos.', 'error');
            return;
        }
        
        try {
            console.log('🎯 Validando código:', codigo);
            
            const response = await fetch('/validar_codigo_confirmacao', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    usuario_id: formData.usuario_id,
                    codigo: codigo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showConfirmacaoMessage('✅ Cadastro confirmado com sucesso! Bem-vindo ao Loterias Inteligentes!', 'success');
                
                console.log('🎯 Código confirmado com sucesso! Iniciando sequência...');
                
                // Fechar modal após 2 segundos e abrir modal de planos
                setTimeout(() => {
                    console.log('🔄 Fechando modal de confirmação...');
                    closeModalConfirmacao(); // Função global
                    
                    console.log('💎 Abrindo modal de planos...');
                    // Abrir modal de planos automaticamente
                    this.abrirModalPlanos();
                }, 2000);
                
            } else {
                this.showConfirmacaoMessage('❌ Código inválido ou expirado. Tente novamente.', 'error');
            }
            
        } catch (error) {
            console.error('❌ Erro ao validar código:', error);
            this.showConfirmacaoMessage('Erro ao validar código. Tente novamente.', 'error');
        }
    }

    // 📧 Enviar código de confirmação
    async enviarCodigo(formData, tipo) {
        try {
            console.log(`📧 Enviando código por ${tipo} para:`, formData[tipo === 'email' ? 'email' : 'telefone']);
            
            const response = await fetch('/enviar_codigo_confirmacao', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    usuario_id: formData.usuario_id,
                    tipo: tipo,
                    destinatario: formData[tipo === 'email' ? 'email' : 'telefone']
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showConfirmacaoMessage(`✅ Código enviado com sucesso por ${tipo}! Verifique sua caixa de entrada.`, 'success');
                
                // Mostrar campos de código e botões de confirmação
                document.querySelector('.codigo-container').style.display = 'block';
                document.querySelector('.confirmacao-actions').style.display = 'block';
                document.querySelector('.escolha-envio').style.display = 'none';
                
            } else {
                this.showConfirmacaoMessage('❌ Erro ao enviar código. Tente novamente.', 'error');
            }
            
        } catch (error) {
            console.error('❌ Erro ao enviar código:', error);
            this.showConfirmacaoMessage('Erro ao enviar código. Tente novamente.', 'error');
        }
    }

    // 💬 Mostrar mensagem no modal de confirmação
    showConfirmacaoMessage(message, type = 'info') {
        const messageBox = document.getElementById('confirmacao-message');
        messageBox.textContent = message;
        messageBox.className = `message-box ${type}`;
        messageBox.style.display = 'block';
        
        // Auto-hide após 5 segundos
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }

    // 💎 Abrir modal de planos após confirmação
    abrirModalPlanos() {
        // Abrir modal de planos
        const modal = document.getElementById('welcomePlansModal');
        if (modal) {
            modal.style.display = 'flex';
            console.log('✅ Modal de planos aberto');
        } else {
            console.error('❌ Modal de planos não encontrado');
            // Fallback: redirecionar para página
            window.location.href = '/upgrade_plans';
        }
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

// 🎯 Funções globais para o modal de confirmação
function closeModalConfirmacao() {
    document.getElementById('modal-confirmacao').style.display = 'none';
}

function alterarDadosCadastro() {
    // Fechar modal de confirmação
    closeModalConfirmacao();
    
    // Abrir modal de cadastro novamente
    openModalLogin('cadastro');
}
