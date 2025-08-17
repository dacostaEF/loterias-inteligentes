/**
 * Laboratório de Simulação Lotofácil - LAYOUT CORRETO
 * JavaScript completo com matriz de concursos e indicadores
 * ORDEM INVERTIDA: último concurso na primeira linha
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
  return q===15?3: q===16?48: q===17?408: q===18?2448: q===19?11628: q===20?46512: 0;
}

function montarHead(){
  const tpl = document.getElementById('tpl-head-num');
  for(let n=1;n<=25;n++){
    const d=document.createElement('div');
    d.className="text-center";
    d.textContent = n.toString().padStart(2,'0');
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
      const d = document.createElement('button');
      d.className = "h-8 rounded border border-purple-900/40 text-[11px]";
      d.dataset.num = n;
      if(val===0){
        d.textContent = "0";
        d.style.background = "rgba(236,72,153,.15)"; // rosa (não saiu)
        d.style.color = "#fda4af";
      }else{
        d.textContent = val.toString().padStart(2,'0');
        d.style.background = "rgba(234,179,8,.15)";  // amarelo (saiu)
        d.style.color = "#fde68a";
      }
      // seleção manual (primeira linha = último concurso)
      d.addEventListener('click', ()=>{
        const num = parseInt(d.dataset.num,10);
        if(SELECIONADOS.has(num)){ SELECIONADOS.delete(num); d.classList.remove('ring','ring-green-400'); }
        else{ SELECIONADOS.add(num); d.classList.add('ring','ring-green-400'); }
        atualizarKpis();
      }, {passive:true});
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

  document.getElementById('k_fibo').textContent  = fibo;
  document.getElementById('k_primos').textContent= prim;
  document.getElementById('k_mold').textContent  = mold;
  document.getElementById('k_mult').textContent  = mult;
  document.getElementById('k_rep').textContent   = rep;
  document.getElementById('k_sel').textContent   = sel.length;

  document.getElementById('totalSel').textContent = sel.length;
  document.getElementById('valorPagar').textContent = fmtMoney(valorAposta(sel.length));
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
  document.querySelectorAll('#gradeWrap button').forEach(b=> b.classList.remove('ring','ring-green-400'));
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

