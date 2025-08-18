/**
 * Laboratório de Simulação Lotofácil - LAYOUT CORRETO
 * JavaScript completo com matriz de concursos e indicadores
 * ORDEM INVERTIDA: último concurso na primeira linha
 * SELEÇÃO: apenas no cabeçalho 1-25 (números para jogar)
 */

const FIBO   = new Set([1,2,3,5,8,13,21]);
const PRIMOS = new Set([2,3,5,7,11,13,17,19,23]);
const MOLD   = new Set([1,2,3,4,5,6,10,11,15,16,20,21,22,23,24,25]);
const MULT3  = new Set([3,6,9,12,15,18,21,24]);

// TESTE: Verificar se as constantes estão definidas corretamente
console.log('🧪 TESTE: Constantes definidas:', {
  FIBO: Array.from(FIBO),
  PRIMOS: Array.from(PRIMOS),
  MOLD: Array.from(MOLD),
  MULT3: Array.from(MULT3)
});

let MATRIZ = [];        // [[conc, c1..c25], ...]
let ULTIMO = [];        // [conc, b1..b15]
let SELECIONADOS = new Set();

function fmtMoney(v){ return v.toLocaleString('pt-BR', {style:'currency', currency:'BRL'}); }
function valorAposta(q){
  // Tabela de valores correta da Lotofácil (igual ao dashboard)
  const valoresLotofacil = {
    15: 3.50,
    16: 56.00,
    17: 476.00,
    18: 2856.00,
    19: 13566.00,
    20: 54264.00
  };
  
  // Retorna o valor se estiver no intervalo válido (15-20), senão 0
  return (q >= 15 && q <= 20) ? valoresLotofacil[q] : 0;
}

function montarHead(){
  console.log('🔧 Montando cabeçalho...');
  const tpl = document.getElementById('tpl-head-num');
  
  if (!tpl) {
    console.error('❌ Template do cabeçalho não encontrado!');
    return;
  }
  
  console.log('✅ Template encontrado, criando botões...');
  
  for(let n=1;n<=25;n++){
    const d=document.createElement('button'); // Mudou para button
    d.className="h-8 rounded border border-purple-900/40 text-[11px] text-center cursor-pointer transition-all duration-200 hover:bg-purple-600/20";
    d.textContent = n.toString().padStart(2,'0');
    d.dataset.num = n;
    
    // Adicionar funcionalidade de seleção no cabeçalho
    d.addEventListener('click', ()=>{
      const num = parseInt(d.dataset.num,10);
      console.log('🖱️ Botão clicado:', num);
      console.log('📊 SELECIONADOS antes:', [...SELECIONADOS]);
      
      if(SELECIONADOS.has(num)){
        console.log('➖ Removendo número:', num);
        SELECIONADOS.delete(num);
        d.classList.remove('ring','ring-green-400','bg-green-600/30');
        d.classList.add('border-purple-900/40');
      } else {
        // Verificar limite máximo de 20 números
        if(SELECIONADOS.size >= 20){
          alert('❌ Máximo de 20 números permitido na Lotofácil!');
          return;
        }
        // Selecionar número
        console.log('➕ Adicionando número:', num);
        SELECIONADOS.add(num);
        d.classList.add('ring','ring-green-400','bg-green-600/30');
        d.classList.remove('border-purple-900/40');
      }
      
      console.log('📊 SELECIONADOS depois:', [...SELECIONADOS]);
      console.log('📊 Tamanho do conjunto:', SELECIONADOS.size);
      
      atualizarKpis();
    }, {passive:true});
    
    tpl.parentNode.insertBefore(d, tpl);
  }
  
  tpl.remove();
  console.log('✅ Cabeçalho montado com sucesso!');
}

function linhaPadrao(titulo, fnSet){
  const wrap = document.createElement('div');
  wrap.className = "grid grid-cols-[80px_repeat(25,minmax(24px,1fr))] gap-[2px] text-xs";
  const lab = document.createElement('div');
  lab.className = "text-center text-gray-300";
  lab.textContent = titulo;
  wrap.appendChild(lab);
  for(let n=1;n<=25;n++){
    const c = document.createElement('div');
    c.className = "h-6 rounded text-center grid place-items-center";
    c.textContent = fnSet(n);
    wrap.appendChild(c);
  }
  return wrap;
}

function render(){
  console.log('🎨 Renderizando grade...');
  const grade = document.getElementById('gradeWrap');
  
  if (!grade) {
    console.error('❌ Container da grade não encontrado!');
    return;
  }
  
  grade.innerHTML = "";

  // INVERTER A ORDEM: último concurso na primeira linha
  const MATRIZ_INVERTIDA = [...MATRIZ].reverse();
  console.log('📊 Renderizando', MATRIZ_INVERTIDA.length, 'linhas da matriz');

  MATRIZ_INVERTIDA.forEach((linha, index) => {
    const row = document.createElement('div');
    row.className = "grid grid-cols-[80px_repeat(25,minmax(24px,1fr))] gap-[2px]";
    const conc = document.createElement('div');
    conc.className="h-8 grid place-items-center text-xs text-gray-300";
    conc.textContent = linha[0];
    row.appendChild(conc);

    for(let n=1;n<=25;n++){
      const val = linha[n];
      const d = document.createElement('div'); // Mudou para div (sem seleção)
      d.className = "h-8 rounded border border-purple-900/40 text-[11px] flex items-center justify-center";
      if(val===0){
        d.textContent = "0";
        d.style.background = "rgba(156,163,175,.15)"; // cinza transparente (não saiu)
        d.style.color = "#9ca3af";
      }else{
        d.textContent = val.toString().padStart(2,'0');
        d.style.background = "rgba(34,197,94,.15)";  // verde limão transparente (saiu)
        d.style.color = "#86efac";
      }
      // SEM seleção - apenas visualização dos resultados históricos
      row.appendChild(d);
    }
    grade.appendChild(row);
  });

  // Linhas F/P/M/x3/Repetido
  console.log('🔍 Renderizando linhas de padrões...');
  const pad = document.getElementById('linhasPadroes');
  
  if (!pad) {
    console.error('❌ Container das linhas de padrões não encontrado!');
    return;
  }
  
  pad.innerHTML = "";
  pad.appendChild(linhaPadrao("Fibonacci", n=> FIBO.has(n) ? "F" : ""));
  pad.appendChild(linhaPadrao("Primos",    n=> PRIMOS.has(n)? "P" : ""));
  pad.appendChild(linhaPadrao("Moldura",   n=> MOLD.has(n)  ? "M" : ""));
  pad.appendChild(linhaPadrao("Múltiplo",  n=> MULT3.has(n) ? "x3": ""));
  
  if (ULTIMO && ULTIMO.length > 1) {
    const repSet = new Set(ULTIMO.slice(1)); // b1..b15 do último concurso (primeira linha)
    pad.appendChild(linhaPadrao("Repetido",  n=> repSet.has(n)? "R" : ""));
    console.log('✅ Linha de repetidos renderizada');
  } else {
    console.log('⚠️ ULTIMO não disponível para linha de repetidos');
  }

  console.log('✅ Grade renderizada, atualizando KPIs...');
  atualizarKpis();
  console.log('✅ Renderização concluída!');
}

function atualizarKpis(){
  const sel = [...SELECIONADOS];
  const fibo = sel.filter(n=>FIBO.has(n)).length;
  const prim = sel.filter(n=>PRIMOS.has(n)).length;
  const mold = sel.filter(n=>MOLD.has(n)).length;
  const mult = sel.filter(n=>MULT3.has(n)).length;
  const rep  = sel.filter(n=>ULTIMO.slice(1).includes(n)).length;

  console.log('📊 KPIs calculados:', { fibo, prim, mold, mult, rep, total: sel.length });

  // Atualizar valores e aplicar cores baseadas nos intervalos padrão
  const k_fibo = document.getElementById('k_fibo');
  const k_primos = document.getElementById('k_primos');
  const k_mold = document.getElementById('k_mold');
  const k_mult = document.getElementById('k_mult');
  const k_rep = document.getElementById('k_rep');
  
  // Verificar se os elementos foram encontrados
  if (!k_fibo || !k_primos || !k_mold || !k_mult || !k_rep) {
    console.error('❌ Elementos KPI não encontrados:', {
      k_fibo: !!k_fibo,
      k_primos: !!k_primos,
      k_mold: !!k_mold,
      k_mult: !!k_mult,
      k_rep: !!k_rep
    });
    return;
  }
  
  // Definir intervalos padrão para Lotofácil (15 números)
  const intervalos = {
    fibonacci: { min: 3, max: 5 },    // 3-5 números Fibonacci (ideal)
    primos: { min: 4, max: 7 },       // 4-7 números primos (ideal)
    moldura: { min: 8, max: 12 },     // 8-12 números da moldura (ideal)
    multiplos: { min: 3, max: 6 },    // 3-6 múltiplos de 3 (ideal)
    repetidos: { min: 2, max: 5 }     // 2-5 repetidos do último (ideal)
  };
  
  // Aplicar valores
  k_fibo.textContent = fibo;
  k_primos.textContent = prim;
  k_mold.textContent = mold;
  k_mult.textContent = mult;
  k_rep.textContent = rep;
  
  // Aplicar cores baseadas nos intervalos (usando classes Tailwind existentes)
  k_fibo.className = `text-xl font-bold ${(fibo >= intervalos.fibonacci.min && fibo <= intervalos.fibonacci.max) ? 'text-green-400' : 'text-gray-300'}`;
  k_primos.className = `text-xl font-bold ${(prim >= intervalos.primos.min && prim <= intervalos.primos.max) ? 'text-green-400' : 'text-gray-300'}`;
  k_mold.className = `text-xl font-bold ${(mold >= intervalos.moldura.min && mold <= intervalos.moldura.max) ? 'text-green-400' : 'text-gray-300'}`;
  k_mult.className = `text-xl font-bold ${(mult >= intervalos.multiplos.min && mult <= intervalos.multiplos.max) ? 'text-green-400' : 'text-gray-300'}`;
  k_rep.className = `text-xl font-bold ${(rep >= intervalos.repetidos.min && rep <= intervalos.repetidos.max) ? 'text-green-400' : 'text-gray-300'}`;
  
  // Atualizar total de selecionados
  const k_sel = document.getElementById('k_sel');
  if (k_sel) k_sel.textContent = sel.length;

  const totalSel = document.getElementById('totalSel');
  if (totalSel) totalSel.textContent = sel.length;
  
  // Validação da quantidade de números selecionados
  const valor = valorAposta(sel.length);
  const valorPagarEl = document.getElementById('valorPagar');
  
  if (valorPagarEl) {
    if(sel.length >= 15 && sel.length <= 20){
      // Quantidade válida para Lotofácil
      valorPagarEl.textContent = fmtMoney(valor);
      valorPagarEl.className = 'font-bold text-green-400';
    } else if(sel.length > 0 && sel.length < 15){
      // Quantidade insuficiente
      valorPagarEl.textContent = `Mínimo 15 números (${sel.length}/15)`;
      valorPagarEl.className = 'font-bold text-orange-400';
    } else if(sel.length > 20){
      // Quantidade excessiva
      valorPagarEl.textContent = 'Máximo 20 números!';
      valorPagarEl.className = 'font-bold text-red-400';
    } else {
      // Nenhum número selecionado
      valorPagarEl.textContent = 'Selecione números para jogar';
      valorPagarEl.className = 'font-bold text-gray-400';
    }
  }
  
  console.log('✅ KPIs atualizados com sucesso!');
}

function abrirModal(id){ 
  console.log('🔍 Abrindo modal:', id);
  
  const modal = document.querySelector(id);
  if(modal){
    console.log('✅ Modal encontrado, abrindo...');
    
    // Usar as classes CSS corretas
    modal.style.display = "flex";
    modal.classList.add('show');
    
    console.log('🎯 Modal aberto com sucesso!');
  } else {
    console.log('❌ Modal não encontrado:', id);
    alert('Erro: Modal não encontrado!');
  }
}

function fecharModal(id){ 
  const modal = document.querySelector(id);
  if(modal) {
    modal.style.display = "none";
    modal.classList.remove('show');
  }
}

async function carregar(){
  console.log('🚀 Carregando laboratório...');
  console.log('🔍 DOM ready state:', document.readyState);
  
  // Verificar se os elementos essenciais existem
  const elementosEssenciais = [
    'tpl-head-num',
    'gradeWrap',
    'linhasPadroes',
    'k_fibo',
    'k_primos',
    'k_mold',
    'k_mult',
    'k_rep',
    'k_sel',
    'valorPagar'
  ];
  
  console.log('🔍 Verificando elementos essenciais...');
  elementosEssenciais.forEach(id => {
    const el = document.getElementById(id);
    console.log(`  ${id}: ${el ? '✅' : '❌'}`);
  });
  
  montarHead();
  
  try {
    console.log('🔍 Fazendo fetch da API...');
    const r = await fetch('/api/lotofacil/matriz?limit=25');
    console.log('📡 Resposta da API:', r.status, r.statusText);
    
    if (!r.ok) {
      throw new Error(`HTTP ${r.status}: ${r.statusText}`);
    }
    
    const data = await r.json();
    console.log('📊 Dados brutos da API:', data);
    
    if (!data.matriz || !data.ultimo_concurso) {
      throw new Error('Dados da API incompletos');
    }
    
    MATRIZ = data.matriz;
    ULTIMO = data.ultimo_concurso;
    
    console.log('📊 MATRIZ carregada:', MATRIZ.length, 'linhas');
    console.log('📊 ULTIMO concurso:', ULTIMO);
    console.log('📊 Primeira linha da matriz:', MATRIZ[0]);
    console.log('📊 Estrutura da primeira linha:', {
      concurso: MATRIZ[0][0],
      numeros: MATRIZ[0].slice(1).filter(n => n > 0)
    });
    
    render();
    
    // Configurar event listeners após carregar
    configurarEventListeners();
    
    console.log('✅ Laboratório carregado com sucesso!');
  } catch (error) {
    console.error('❌ Erro ao carregar dados:', error);
    alert('Erro ao carregar dados do laboratório!');
  }
}

function configurarEventListeners(){
  console.log('🔧 Configurando event listeners...');
  
  const btnReset = document.getElementById('btnReset');
  const btnGraficos = document.getElementById('btnGraficos');
  
  console.log('🔍 Botões encontrados:', {
    btnReset: !!btnReset,
    btnGraficos: !!btnGraficos
  });
  
  if(btnReset){
    btnReset.onclick = ()=>{
      console.log('🔄 Resetando seleções...');
      SELECIONADOS.clear();
      // Reset apenas no cabeçalho (onde está a seleção)
      document.querySelectorAll('.grade-header button').forEach(b=> {
        b.classList.remove('ring','ring-green-400','bg-green-600/30');
        b.classList.add('border-purple-900/40');
      });
      atualizarKpis();
    };
    console.log('✅ Event listener do Reset configurado');
  }
  
  // Botão Próximo removido - funcionalidade redundante
  
  if(btnGraficos){
    btnGraficos.onclick = async ()=>{
      console.log('📊 Abrindo modal de gráficos...');
      
      // Abrir modal primeiro
      abrirModal('#modalGraficos');
      
      // Limpar gráfico anterior
      const plotlyGraphDiv = document.getElementById('plotly-graph');
      if (plotlyGraphDiv) {
        plotlyGraphDiv.innerHTML = 'Carregando dados...';
      }
      
      try {
        // Fazer requisição para a nova API
        console.log('📡 Fazendo requisição para /estatisticas-frequencia...');
        const response = await fetch('/estatisticas-frequencia?num_concursos=25');
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const frequencyData = await response.json();
        console.log('📊 Dados de frequência recebidos:', frequencyData);
        
        // Desenhar visualização 3D por padrão
        draw3DHistogram(frequencyData);
        
        // Preencher caixas informativas
        preencherCaixasInformativas(frequencyData);
        
        console.log('✅ Gráficos carregados com sucesso!');
      } catch (error) {
        console.error('❌ Erro ao carregar gráficos:', error);
        if (plotlyGraphDiv) {
          plotlyGraphDiv.innerHTML = `Erro ao carregar gráficos: ${error.message}`;
        }
      }
    };
    console.log('✅ Event listener do Gráficos configurado');
  }
  
  console.log('🎯 Todos os event listeners configurados!');
}

// Event listener para fechar modais
document.addEventListener('click', e=>{
  const tgt = e.target;
  if(tgt.matches('.close')) fecharModal(tgt.dataset.close);
});

// Inicializar quando a página carregar
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', carregar);
} else {
  // DOM já carregado
  carregar();
}

// ===== FUNÇÕES AUXILIARES PARA GRÁFICOS =====

// Calcular frequências dos números em cada posição
function calcularFrequencias() {
  console.log('🔢 Calculando frequências...');
  
  if (!MATRIZ || MATRIZ.length === 0) {
    throw new Error('Matriz de dados não disponível');
  }
  
  const frequencyData = {};
  
  // Inicializar estrutura de dados
  for (let num = 1; num <= 25; num++) {
    frequencyData[num] = {};
    for (let pos = 1; pos <= 15; pos++) {
      frequencyData[num][pos] = 0;
    }
  }
  
  // Calcular frequências
  MATRIZ.forEach(linha => {
    const numeros = linha.slice(1); // Pular o concurso (primeiro elemento)
    numeros.forEach((valor, index) => {
      if (valor > 0 && valor <= 25) {
        const pos = index + 1; // Posição (1-15)
        frequencyData[valor][pos]++;
      }
    });
  });
  
  console.log('📊 Frequências calculadas:', frequencyData);
  return frequencyData;
}

// Desenhar histograma 3D REAL
function draw3DHistogram(data) {
  console.log('🎨 Desenhando histograma 3D REAL...');
  
  // Preparar dados para gráfico 3D de barras
  const traces = [];
  
  // Criar uma barra 3D para cada número em cada posição
  for (let num = 1; num <= 25; num++) {
    for (let pos = 1; pos <= 15; pos++) {
      const frequencia = data[num][pos];
      
      if (frequencia > 0) { // Só mostrar barras com frequência > 0
        const trace = {
          type: 'mesh3d',
          x: [num-0.4, num+0.4, num+0.4, num-0.4, num-0.4, num+0.4, num+0.4, num-0.4],
          y: [pos-0.4, pos-0.4, pos+0.4, pos+0.4, pos-0.4, pos-0.4, pos+0.4, pos+0.4],
          z: [0, 0, 0, 0, frequencia, frequencia, frequencia, frequencia],
          i: [0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
          j: [1, 2, 3, 1, 5, 6, 7, 5, 6, 2, 7, 3],
          k: [2, 3, 0, 4, 6, 7, 4, 7, 0, 3, 1, 0],
          opacity: 0.8,
          color: 'rgba(26, 115, 232, 0.8)',
          name: `N${num}P${pos}`
        };
        traces.push(trace);
      }
    }
  }
  
  const layout = {
    title: 'Frequência dos Números por Posição (Visão 3D Real)',
    scene: {
      xaxis: { 
        title: 'Número (1-25)', 
        range: [0, 26],
        tickmode: 'linear',
        tick0: 1,
        dtick: 1
      },
      yaxis: { 
        title: 'Posição/Bola (1-15)', 
        range: [0, 16],
        tickmode: 'linear',
        tick0: 1,
        dtick: 1
      },
      zaxis: { 
        title: 'Frequência', 
        range: [0, 25] // Ajustar baseado nos dados reais
      },
      camera: {
        eye: {x: 1.5, y: 1.5, z: 1.5}
      }
    },
    autosize: true,
    margin: { t: 50, r: 20, l: 80, b: 60 }, // Aumentei left margin para 80px e bottom para 60px
    height: 500
  };

  const plotlyGraphDiv = document.getElementById('plotly-graph');
  if (plotlyGraphDiv) {
    Plotly.newPlot(plotlyGraphDiv, traces, layout, { 
      displayModeBar: true,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
    });
    
    // Forçar resize automático para corrigir dimensões na primeira abertura
    setTimeout(() => {
      Plotly.Plots.resize(plotlyGraphDiv);
      console.log('🔄 Resize automático aplicado ao gráfico 3D');
    }, 100);
    
    console.log('✅ Histograma 3D REAL desenhado!');
  }
}

// Desenhar mapa de calor (visão superior)
function drawHeatmap(data) {
  console.log('🔥 Desenhando mapa de calor...');
  
  const z_values = [];
  for (let pos = 1; pos <= 15; pos++) {
    const row = [];
    for (let num = 1; num <= 25; num++) {
      row.push(data[num][pos]);
    }
    z_values.push(row);
  }

  const trace = {
    z: z_values,
    x: Array.from({length: 25}, (_, i) => i + 1),
    y: Array.from({length: 15}, (_, i) => i + 1),
    type: 'heatmap',
    colorscale: [
      [0, 'rgb(25, 25, 112)'],      // Roxo escuro (0)
      [0.125, 'rgb(72, 61, 139)'],  // Roxo médio
      [0.25, 'rgb(70, 130, 180)'],  // Azul
      [0.375, 'rgb(100, 149, 237)'], // Azul claro
      [0.5, 'rgb(34, 139, 34)'],    // Verde
      [0.625, 'rgb(50, 205, 50)'],  // Verde claro
      [0.75, 'rgb(255, 215, 0)'],   // Dourado
      [0.875, 'rgb(255, 140, 0)'],  // Laranja
      [1, 'rgb(139, 0, 0)']         // Vermelho escuro (20)
    ],
    showscale: true,
    hoverongaps: false,
    hovertemplate: 'Número: %{x}<br>Posição: %{y}<br>Frequência: %{z}<extra></extra>'
  };

  const layout = {
    title: 'Frequência dos Números por Posição (Mapa de Calor)',
    xaxis: { 
      title: 'Número (1-25)', 
      dtick: 1,
      tickmode: 'linear',
      tick0: 1
    },
    yaxis: { 
      title: 'Posição/Bola (1-15)', 
      dtick: 1,
      tickmode: 'linear',
      tick0: 1
    },
    autosize: true,
    margin: { t: 50, r: 20, l: 80, b: 60 }, // Aumentei left margin para 80px e bottom para 60px
    height: 500,
    coloraxis: {
      colorbar: {
        title: 'Frequência',
        titleside: 'right',
        thickness: 20,
        len: 0.8
      }
    }
  };

  const plotlyGraphDiv = document.getElementById('plotly-graph');
  if (plotlyGraphDiv) {
    Plotly.newPlot(plotlyGraphDiv, [trace], layout, { 
      displayModeBar: true,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
    });
    
    // Forçar resize automático para corrigir dimensões na primeira abertura
    setTimeout(() => {
      Plotly.Plots.resize(plotlyGraphDiv);
      console.log('🔄 Resize automático aplicado ao mapa de calor');
    }, 100);
    
    console.log('✅ Mapa de calor desenhado!');
  }
}

// Preencher caixas informativas
function preencherCaixasInformativas(data) {
  console.log('📝 Preenchendo caixas informativas...');
  
  // Caixa amarela: Números com maior frequência por posição
  const numerosFrequencia = document.getElementById('numerosFrequencia');
  if (numerosFrequencia) {
    const numerosPorPosicao = [];
    const frequenciasPorPosicao = [];
    
    for (let pos = 1; pos <= 15; pos++) {
      let maxFreq = 0;
      let numeroMax = 0;
      
      for (let num = 1; num <= 25; num++) {
        if (data[num][pos] > maxFreq) {
          maxFreq = data[num][pos];
          numeroMax = num;
        }
      }
      
      numerosPorPosicao.push(numeroMax);
      frequenciasPorPosicao.push(maxFreq);
    }
    
    // Mostrar números com suas frequências
    const numerosComFreq = numerosPorPosicao.map((num, index) => 
      `${num}(${frequenciasPorPosicao[index]})`
    ).join(', ');
    
    numerosFrequencia.textContent = numerosComFreq;
    console.log('✅ Caixa amarela preenchida:', numerosPorPosicao);
    console.log('📊 Frequências:', frequenciasPorPosicao);
  }
  

}

// Configurar event listeners dos botões de visualização
function configurarBotoesVisualizacao() {
  const btn3DView = document.getElementById('btn-3d-view');
  const btnTopView = document.getElementById('btn-top-view');
  
  if (btn3DView) {
    btn3DView.onclick = async () => {
      console.log('🔄 Alternando para visualização 3D...');
      try {
        const response = await fetch('/estatisticas-frequencia?num_concursos=25');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const frequencyData = await response.json();
        draw3DHistogram(frequencyData);
      } catch (error) {
        console.error('❌ Erro ao alternar para 3D:', error);
      }
    };
  }
  
  if (btnTopView) {
    btnTopView.onclick = async () => {
      console.log('🔄 Alternando para mapa de calor...');
      try {
        const response = await fetch('/estatisticas-frequencia?num_concursos=25');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const frequencyData = await response.json();
        drawHeatmap(frequencyData);
      } catch (error) {
        console.error('❌ Erro ao alternar para mapa de calor:', error);
      }
    };
  }
  
  console.log('✅ Botões de visualização configurados!');
}

// Configurar botões de visualização quando o modal abrir
document.addEventListener('DOMContentLoaded', () => {
  // Aguardar um pouco para garantir que o modal foi renderizado
  setTimeout(() => {
    configurarBotoesVisualizacao();
  }, 1000);
});

