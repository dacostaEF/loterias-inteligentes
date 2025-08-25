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
        slide.style.borderColor = item.cor_borda;
        slide.style.backgroundColor = item.cor_fundo;
        slide.style.color = item.cor_texto;
        
        // Estrutura do slide seguindo o layout da imagem
        // "Airbag" para campos vazios/null
        const valor = (item.valor ?? '').toString();
        const unidade = (item.unidade ?? '').toString();
        const texto_destaque = (item.texto_destaque ?? '').toString();
        const loteria = (item.loteria ?? '').toString();
        
        slide.innerHTML = `
            <div class="slide-content">
                <div class="slide-label" style="background-color: ${item.cor_borda}; color: ${item.cor_texto};">
                    ${texto_destaque}
                </div>
                <div class="slide-value">
                    <span class="main-value">${valor}</span>
                    <span class="unit">${unidade}</span>
                </div>
                <div class="slide-name">${loteria}</div>
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
        // Sem controles manuais - apenas movimento automático contínuo
        // A animação CSS cuida de tudo
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
