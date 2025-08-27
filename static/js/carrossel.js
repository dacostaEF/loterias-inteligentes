/**
 * Carrossel de Loterias - Carrega dados dinamicamente da API
 * Segue o padrão visual estabelecido para cada loteria
 */

class CarrosselLoterias {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.data = [];
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        this.init();
    }

    async init() {
        try {
            await this.loadData();
            this.render();
            this.startAutoPlay();
            this.setupEventListeners();
        } catch (error) {
            console.error('Erro ao inicializar carrossel:', error);
            this.showError();
        }
    }

    async loadData() {
        try {
            console.log('Carregando dados do carrossel...');
            const response = await fetch('/api/carousel_data');
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error('Falha ao carregar dados do carrossel.');
            }
            
            this.data = await response.json();
            console.log('Dados carregados:', this.data);
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            throw error;
        }
    }

    render() {
        if (!this.container || this.data.length === 0) return;

        this.container.innerHTML = '';
        
        // Container principal do carrossel
        const carouselWrapper = document.createElement('div');
        carouselWrapper.className = 'carousel-wrapper';
        
        // Container dos slides com movimento dinâmico
        const slidesContainer = document.createElement('div');
        slidesContainer.className = 'carousel-slides';
        slidesContainer.style.animation = 'scrollLeft 30s linear infinite'; // Movimento contínuo como filme
        
        // Renderiza cada slide
        this.data.forEach((item, index) => {
            const slide = this.createSlide(item, index);
            slidesContainer.appendChild(slide);
        });
        
        // Duplica os slides para movimento infinito
        this.data.forEach((item, index) => {
            const slide = this.createSlide(item, index);
            slidesContainer.appendChild(slide);
        });
        
        carouselWrapper.appendChild(slidesContainer);
        
        // Sem navegação manual - apenas movimento automático
        this.container.appendChild(carouselWrapper);
    }

            createSlide(item, index) {
            const slide = document.createElement('div');
            slide.className = 'carousel-slide';
            
            // ⚡ NOVO: Dimensões responsivas baseadas no tamanho da tela
            const isMobile = window.innerWidth <= 768;
            const isSmallMobile = window.innerWidth <= 480;
            
            if (isSmallMobile) {
                slide.style.width = '140px';
                slide.style.height = '60px'; /* ⚡ REDUZIDO: 140px → 60px para eliminar espaço */
            } else if (isMobile) {
                slide.style.width = '160px';
                slide.style.height = '70px'; /* ⚡ REDUZIDO: 160px → 70px para eliminar espaço */
            } else {
                slide.style.width = '127px';
                slide.style.height = '105px';
            }
        
        // TRANSPARÊNCIA TOTAL - sem cores de fundo
        slide.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        slide.style.backgroundColor = 'transparent';
        slide.style.color = item.cor_texto;
        
        // Estrutura do slide seguindo o layout da imagem
        // "Airbag" para campos vazios/null
        const valor = (item.valor ?? '').toString();
        const unidade = (item.unidade ?? '').toString();
        const texto_destaque = (item.texto_destaque ?? '').toString();
        const loteria = (item.loteria ?? '').toString();
        
        // Verifica se é a Loteca para aplicar cores especiais
        const isLoteca = loteria.toLowerCase().includes('loteca');
        
        // Verifica se é o Dia de Sorte para aplicar cores especiais
        const isDiaDeSorte = loteria.toLowerCase().includes('dia de sorte');
        
        // Verifica se é o Super Sete para aplicar cores especiais
        const isSuperSete = loteria.toLowerCase().includes('super sete');
        
        // Verifica se é Lotofácil para aplicar cores especiais
        const isLotofacil = loteria.toLowerCase().includes('lotofacil');
        
        // Verifica se é Lotomania para aplicar cores especiais
        const isLotomania = loteria.toLowerCase().includes('lotomania');
        
        // Verifica se é Mega Sena para aplicar cores especiais
        const isMegaSena = loteria.toLowerCase().includes('mega-sena');
        
        // Verifica se é Quina para aplicar cores especiais
        const isQuina = loteria.toLowerCase().includes('quina');
        
        // Verifica se é +Milionária para aplicar cores especiais
        const isMilionaria = loteria.toLowerCase().includes('milionaria') || loteria.toLowerCase().includes('+milionaria');
        
        // Verifica se é Timemania para aplicar cores especiais
        const isTimemania = loteria.toLowerCase().includes('timemania');
        
        // Verifica se é Dupla Sena para aplicar cores especiais
        const isDuplaSena = loteria.toLowerCase().includes('dupla sena');
        
        // Cores especiais para Loteca (50% de transparência) - Rosa/Magenta
        let labelBg = isLoteca ? 'rgba(255, 0, 255, 0.5)' : 'rgba(255, 255, 255, 0.15)';
        let nameBg = isLoteca ? 'rgba(255, 0, 255, 0.5)' : 'rgba(255, 255, 255, 0.15)';
        
        // Cores especiais para Dia de Sorte (50% de transparência) - Dourado
        if (isDiaDeSorte) {
            labelBg = 'rgba(255, 215, 0, 0.5)';
            nameBg = 'rgba(255, 215, 0, 0.5)';
        }
        
        // Cores especiais para Super Sete (50% de transparência) - RGB correto
        if (isSuperSete) {
            labelBg = 'rgba(168, 207, 69, 0.5)'; // RGB(168, 207, 69) com 50% de transparência
            nameBg = 'rgba(168, 207, 69, 0.5)'; // RGB(168, 207, 69) com 50% de transparência
        }
        
        // Cores especiais para Lotofácil (50% de transparência) - Roxo #930089
        if (isLotofacil) {
            labelBg = 'rgba(147, 0, 137, 0.5)'; // #930089 com 50% de transparência
            nameBg = 'rgba(147, 0, 137, 0.5)'; // #930089 com 50% de transparência
        }
        
        // Cores especiais para Lotomania (50% de transparência) - Laranja #FF8C00
        if (isLotomania) {
            labelBg = 'rgba(255, 140, 0, 0.5)'; // #FF8C00 com 50% de transparência
            nameBg = 'rgba(255, 140, 0, 0.5)'; // #FF8C00 com 50% de transparência
        }
        
        // Cores especiais para Mega Sena (50% de transparência) - Verde #9ACD32
        if (isMegaSena) {
            labelBg = 'rgba(154, 205, 50, 0.5)'; // #9ACD32 com 50% de transparência
            nameBg = 'rgba(154, 205, 50, 0.5)'; // #9ACD32 com 50% de transparência
        }
        
        // Cores especiais para Quina (50% de transparência) - Verde-azulado #008B8B
        if (isQuina) {
            labelBg = 'rgba(0, 139, 139, 0.5)'; // #008B8B com 50% de transparência
            nameBg = 'rgba(0, 139, 139, 0.5)'; // #008B8B com 50% de transparência
        }
        
        // Cores especiais para +Milionária (50% de transparência) - Azul #3B82F6
        if (isMilionaria) {
            labelBg = 'rgba(59, 130, 246, 0.5)'; // #3B82F6 com 50% de transparência
            nameBg = 'rgba(59, 130, 246, 0.5)'; // #3B82F6 com 50% de transparência
        }
        
        // Cores especiais para Timemania (50% de transparência) - Verde-limão RGB(0, 255, 72)
        if (isTimemania) {
            labelBg = 'rgba(0, 255, 72, 0.5)'; // RGB(0, 255, 72) com 50% de transparência
            nameBg = 'rgba(0, 255, 72, 0.5)'; // RGB(0, 255, 72) com 50% de transparência
        }
        
        // Cores especiais para Dupla Sena (50% de transparência) - Vermelho RGB(166, 19, 36)
        if (isDuplaSena) {
            labelBg = 'rgba(166, 19, 36, 0.5)'; // RGB(166, 19, 36) com 50% de transparência
            nameBg = 'rgba(166, 19, 36, 0.5)'; // RGB(166, 19, 36) com 50% de transparência
        }
        
        slide.innerHTML = `
            <div class="slide-content">
                <div class="slide-label" style="background-color: ${labelBg}; color: ${item.cor_texto};">
                    ${texto_destaque}
                </div>
                <div class="slide-value">
                    <span class="main-value">${valor}</span>
                    <span class="unit">${unidade}</span>
                </div>
                <div class="slide-name" style="background-color: ${nameBg};">${loteria}</div>
            </div>
        `;
        
        // Adiciona evento de clique para navegação
        slide.addEventListener('click', () => {
            this.goToSlide(index);
        });
        
        return slide;
    }

    // Navegação manual removida - apenas movimento automático

    // Funções de navegação manual removidas - apenas movimento automático

    startAutoPlay() {
        // Movimento contínuo automático - sem intervalos
        // A animação CSS cuida de tudo
    }

    stopAutoPlay() {
        // Não é mais necessário parar o movimento
    }

    setupEventListeners() {
        // ⚡ NOVO: Listener para redimensionamento da janela
        window.addEventListener('resize', () => {
            this.updateSlideDimensions();
        });
    }
    
    // ⚡ NOVO: Método para atualizar dimensões dos slides
            updateSlideDimensions() {
            const slides = this.container.querySelectorAll('.carousel-slide');
            const isMobile = window.innerWidth <= 768;
            const isSmallMobile = window.innerWidth <= 480;
            
            slides.forEach(slide => {
                if (isSmallMobile) {
                    slide.style.width = '140px';
                    slide.style.height = '60px'; /* ⚡ REDUZIDO: 140px → 60px para eliminar espaço */
                } else if (isMobile) {
                    slide.style.width = '160px';
                    slide.style.height = '70px'; /* ⚡ REDUZIDO: 160px → 70px para eliminar espaço */
                } else {
                    slide.style.width = '127px';
                    slide.style.height = '105px';
                }
            });
        }

    showError() {
        if (this.container) {
            this.container.innerHTML = `
                <div class="carousel-error">
                    <p>Erro ao carregar dados das loterias</p>
                    <button onclick="window.reloadCarousel()">Tentar novamente</button>
                </div>
            `;
        }
    }

    destroy() {
        this.stopAutoPlay();
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// Inicializa o carrossel quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM carregado, procurando container do carrossel...');
    const carouselContainer = document.getElementById('carousel-container');
    console.log('Container encontrado:', carouselContainer);
    
    if (carouselContainer) {
        console.log('Inicializando carrossel...');
        window.lotteryCarousel = new CarrosselLoterias('carousel-container');
    } else {
        console.error('Container do carrossel não encontrado!');
    }
});

// Função global para reinicializar o carrossel (útil para debugging)
window.reloadCarousel = () => {
    if (window.lotteryCarousel) {
        window.lotteryCarousel.destroy();
        window.lotteryCarousel = new CarrosselLoterias('carousel-container');
    }
};
