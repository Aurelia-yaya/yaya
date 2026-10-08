
const side=document.getElementById('side');
document.getElementById('menu').onclick=()=>side.classList.toggle('open');
document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{navigator.clipboard.writeText(b.parentElement.querySelector('code').innerText);b.textContent='Copié';setTimeout(()=>b.textContent='Copier',1200)});
const q=document.getElementById('q'),res=document.getElementById('res');
const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
q.addEventListener('input',()=>{
  const v=norm(q.value.trim());if(v.length<2){res.style.display='none';return}
  const words=v.split(/\s+/);
  const hits=(window.IDX||[]).map(e=>{const t=norm(e.t),x=norm(e.x);
    if(!words.every(w=>t.includes(w)||x.includes(w)))return null;
    return{e,s:words.reduce((a,w)=>a+(t.includes(w)?10:0)+(x.split(w).length-1),0)}}).filter(Boolean)
    .sort((a,b)=>b.s-a.s).slice(0,12);
  res.innerHTML=hits.length?hits.map(({e})=>{const i=norm(e.x).indexOf(words[0]);
    const sn=e.x.slice(Math.max(0,i-50),i+110).replace(/</g,'&lt;');
    return `<a href="${e.p}.html#${e.id}">${e.t}<small>${e.pt} · …${sn}…</small></a>`}).join(''):'<a>Aucun résultat</a>';
  res.style.display='block'});
document.addEventListener('click',e=>{if(!e.target.closest('.search'))res.style.display='none'});
const heads=[...document.querySelectorAll('article h2[id],article h3[id]')];
if(heads.length)addEventListener('scroll',()=>{let c=null;for(const h of heads){if(h.getBoundingClientRect().top<90)c=h.id}
  document.querySelectorAll('.toc a').forEach(a=>a.classList.toggle('act',a.getAttribute('href')==='#'+c))});
