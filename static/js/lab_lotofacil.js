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
  const tpl = document.getElementById('tpl-head-num');
  for(let n=1;n<=25;n++){
    const d=document.createElement('button'); // Mudou para button
    d.className="h-8 rounded border border-purple-900/40 text-[11px] text-center cursor-pointer transition-all duration-200 hover:bg-purple-600/20";
    d.textContent = n.toString().padStart(2,'0');
    d.dataset.num = n;
    
    // Adicionar funcionalidade de seleção no cabeçalho
    d.addEventListener('click', ()=>{
      const num = parseInt(d.dataset.num,10);
      if(SELECIONADOS.has(num)){
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
        SELECIONADOS.add(num);
        d.classList.add('ring','ring-green-400','bg-green-600/30');
        d.classList.remove('border-purple-900/40');
      }
      atualizarKpis();
    }, {passive:true});
    
    tpl.parentNode.insertBefore(d, tpl);
  }
  tpl.remove();
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
  const grade = document.getElementById('gradeWrap');
  grade.innerHTML = "";

  // INVERTER A ORDEM: último concurso na primeira linha
  const MATRIZ_INVERTIDA = [...MATRIZ].reverse();

  MATRIZ_INVERTIDA.forEach(linha=>{
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
        d.style.background = "rgba(234,179,8,.15)";  // amarelo (saiu)
        d.style.color = "#fde68a";
      }
      // SEM seleção - apenas visualização dos resultados históricos
      row.appendChild(d);
    }
    grade.appendChild(row);
  });

  // Linhas F/P/M/x3/Repetido
  const pad = document.getElementById('linhasPadroes');
  pad.innerHTML = "";
  pad.appendChild(linhaPadrao("Fibonacci", n=> FIBO.has(n) ? "F" : ""));
  pad.appendChild(linhaPadrao("Primos",    n=> PRIMOS.has(n)? "P" : ""));
  pad.appendChild(linhaPadrao("Moldura",   n=> MOLD.has(n)  ? "M" : ""));
  pad.appendChild(linhaPadrao("Múltiplo",  n=> MULT3.has(n) ? "x3": ""));
  const repSet = new Set(ULTIMO.slice(1)); // b1..b15 do último concurso (primeira linha)
  pad.appendChild(linhaPadrao("Repetido",  n=> repSet.has(n)? "R" : ""));

  atualizarKpis();
}

function atualizarKpis(){
  const sel = [...SELECIONADOS];
  const fibo = sel.filter(n=>FIBO.has(n)).length;
  const prim = sel.filter(n=>PRIMOS.has(n)).length;
  const mold = sel.filter(n=>MOLD.has(n)).length;
  const mult = sel.filter(n=>MULT3.has(n)).length;
  const rep  = sel.filter(n=>ULTIMO.slice(1).includes(n)).length;

  // Atualizar valores e aplicar cores baseadas nos intervalos padrão
  const k_fibo = document.getElementById('k_fibo');
  const k_primos = document.getElementById('k_primos');
  const k_mold = document.getElementById('k_mold');
  const k_mult = document.getElementById('k_mult');
  const k_rep = document.getElementById('k_rep');
  
  // Definir intervalos padrão para Lotofácil (15 números)
  const intervalos = {
    fibonacci: { min: 3, max: 5 },    // 3-5 números Fibonacci (ideal)
    primos: { min: 4, max: 7 },       // 4-7 números primos (ideal)
    moldura: { min: 8, max: 12 },     // 8-12 números da moldura (ideal)
    multiplos: { min: 3, max: 6 },    // 3-6 múltiplos de 3 (ideal)
    repetidos: { min: 2, max: 5 }     // 2-5 repetidos do último (ideal)
  };
  
  // Aplicar valores e cores
  k_fibo.textContent = fibo;
  k_primos.textContent = prim;
  k_mold.textContent = mold;
  k_mult.textContent = mult;
  k_rep.textContent = rep;
  
  // Aplicar cores baseadas nos intervalos
  k_fibo.className = (fibo >= intervalos.fibonacci.min && fibo <= intervalos.fibonacci.max) ? 
    'controle-valor text-green-400' : 'controle-valor text-gray-300';
    
  k_primos.className = (prim >= intervalos.primos.min && prim <= intervalos.primos.max) ? 
    'controle-valor text-green-400' : 'controle-valor text-gray-300';
    
  k_mold.className = (mold >= intervalos.moldura.min && mold <= intervalos.moldura.max) ? 
    'controle-valor text-green-400' : 'controle-valor text-gray-300';
    
  k_mult.className = (mult >= intervalos.multiplos.min && mult <= intervalos.multiplos.max) ? 
    'controle-valor text-green-400' : 'controle-valor text-gray-300';
    
  k_rep.className = (rep >= intervalos.repetidos.min && rep <= intervalos.repetidos.max) ? 
    'controle-valor text-green-400' : 'controle-valor text-gray-300';
    
  document.getElementById('k_sel').textContent   = sel.length;

  document.getElementById('totalSel').textContent = sel.length;
  
  // Validação da quantidade de números selecionados
  const valor = valorAposta(sel.length);
  if(sel.length >= 15 && sel.length <= 20){
    // Quantidade válida para Lotofácil
    document.getElementById('valorPagar').textContent = fmtMoney(valor);
    document.getElementById('valorPagar').className = 'font-bold text-green-400';
  } else if(sel.length > 0 && sel.length < 15){
    // Quantidade insuficiente
    document.getElementById('valorPagar').textContent = `Mínimo 15 números (${sel.length}/15)`;
    document.getElementById('valorPagar').className = 'font-bold text-orange-400';
  } else if(sel.length > 20){
    // Quantidade excessiva
    document.getElementById('valorPagar').textContent = 'Máximo 20 números!';
    document.getElementById('valorPagar').className = 'font-bold text-red-400';
  } else {
    // Nenhum número selecionado
    document.getElementById('valorPagar').textContent = 'Selecione números para jogar';
    document.getElementById('valorPagar').className = 'font-bold text-gray-400';
  }
}



function abrirModal(id){ document.querySelector(id).style.display="block"; }
function fecharModal(id){ document.querySelector(id).style.display="none"; }

async function carregar(){
  montarHead();
  const r = await fetch('/api/lotofacil/matriz?limit=25');
  const data = await r.json();
  MATRIZ = data.matriz;
  ULTIMO = data.ultimo_concurso;
  render();
}

document.addEventListener('click', e=>{
  const tgt = e.target;
  if(tgt.matches('.close')) fecharModal(tgt.dataset.close);
});
document.getElementById('btnReset').onclick = ()=>{
  SELECIONADOS.clear();
  // Reset apenas no cabeçalho (onde está a seleção)
  document.querySelectorAll('.grade-header button').forEach(b=> {
    b.classList.remove('ring','ring-green-400','bg-green-600/30');
    b.classList.add('border-purple-900/40');
  });
  atualizarKpis();
};
document.getElementById('btnProximo').onclick = ()=>{
  const modal = '#modalPadroes';
  // Mostra uma comparação simples: selecionados vs último concurso (primeira linha)
  const sel = [...SELECIONADOS].sort((a,b)=>a-b);
  const prox = new Set(ULTIMO.slice(1));
  const x = sel.map((n,i)=>i+1);
  const y = sel.map(n=> prox.has(n)? 1: 0);
  Plotly.newPlot('chartPadroes', [{
    x, y, type:'bar', text: sel.map(n=>n.toString().padStart(2,'0')),
    textposition:'auto', hoverinfo:'text', marker:{line:{width:1}}
  }], {yaxis:{tickvals:[0,1], ticktext:['não sai','sai']}, margin:{t:20,r:10,l:40,b:30},
       paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}} ,{displayModeBar:false});
  abrirModal(modal);
};
document.getElementById('btnGraficos').onclick = ()=>{
  // Gráfico 3D e Heatmap (POC) derivados da MATRIZ
  const rows = MATRIZ.length;
  const Z = [];
  // Usar a mesma ordem invertida para manter consistência visual
  const MATRIZ_INVERTIDA = [...MATRIZ].reverse();
  for(let i=0;i<rows;i++){
    const linha = MATRIZ_INVERTIDA[i];
    const z = [];
    for(let n=1;n<=25;n++) z.push(linha[n]>0 ? 1 : 0); // 1 quando saiu
    Z.push(z);
  }
  const x = [...Array(25)].map((_,i)=>i+1);
  const y = MATRIZ_INVERTIDA.map(l=> l[0]);

  Plotly.newPlot('chart3d', [{
    type:'surface', x, y, z: Z, showscale:false
  }], {scene:{xaxis:{title:'Dezenas'}, yaxis:{title:'Concurso'}, zaxis:{title:'Saída'}},
       margin:{t:10,r:10,l:10,b:10}, paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}},
       {displayModeBar:false});

  Plotly.newPlot('heatmap', [{
    type:'heatmap', x, y, z: Z, colorscale:'Turbo', showscale:true
  }], {margin:{t:10,r:10,l:60,b:30}, paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}},
     {displayModeBar:false});

  abrirModal('#modalGraficos');
};

carregar();

