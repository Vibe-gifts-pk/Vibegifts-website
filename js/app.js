(function(){
var $=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return[].slice.call((c||document).querySelectorAll(s))};
var mb=$('.mb'),nav=$('.hd nav');
if(mb)mb.onclick=function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)};
var sl=$('#sl');
if(sl){var step=function(d){sl.scrollBy({left:d*(sl.firstElementChild.offsetWidth+12),behavior:'smooth'})};$('#pv').onclick=function(){step(-1)};$('#nx').onclick=function(){step(1)}}
var so=$('#sort');
if(so)so.onchange=function(){var g=$('.grid');if(!g.dataset.o)g.dataset.o=1,$$('.card',g).forEach(function(c,i){c.dataset.i=i});
$$('.card',g).sort(function(a,b){var d=a.dataset.price-b.dataset.price;return so.value=='a'?d:so.value=='d'?-d:a.dataset.i-b.dataset.i}).forEach(function(c){g.appendChild(c)})};
var io=window.IntersectionObserver?new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vis');io.unobserve(x.target)}})},{threshold:.12}):null;
$$('.rv-a').forEach(function(el){io?io.observe(el):el.classList.add('vis')});
var pd=$('#pd');
if(pd){var D=JSON.parse(pd.textContent),mi=$('#mi'),wb=$('#wb'),hint=$('.hint'),sel=D.g.map(function(){return 0});
var show=function(i){mi.src='/images/'+D.i[i];$$('.th').forEach(function(t,k){t.classList.toggle('on',k==i)})};
var calc=function(){var p=D.p;D.g.forEach(function(g,k){var o=g.o[sel[k]];if(o.p)p=o.p});return p};
var upd=function(){var p=calc(),m="Hi Vibe Gifts! \uD83D\uDC4B I'd like to order:\n\uD83C\uDF81 Product: "+D.t+"\n";
var F=function(x){return'Rs. '+x.toLocaleString('en-US')},nw=$('.now');if(nw){nw.textContent=F(p);$$('.was,.off,.save',$('#pp')).forEach(function(el){el.hidden=D.c<=p});if(D.c>p){$('.off',$('#pp')).textContent=Math.round(100-100*p/D.c)+'% OFF';$('.save').textContent='You save '+F(D.c-p)+' on this gift'}}D.g.forEach(function(g,k){m+="\uD83C\uDFA8 "+g.n+": "+g.o[sel[k]].l+"\n"});
m+="\uD83D\uDCB0 Price: Rs. "+p.toLocaleString('en-US')+"\n\uD83D\uDD17 "+D.u+"\n\nName / design / photo to print: ";wb.href='https://wa.me/'+D.wa+'?text='+encodeURIComponent(m)};
$$('.th').forEach(function(t){t.onclick=function(){show(+t.dataset.i)}});
$$('.ops').forEach(function(box){var g=+box.dataset.g;$$('.op',box).forEach(function(b){b.onclick=function(){sel[g]=+b.dataset.i;$$('.op',box).forEach(function(x){x.classList.toggle('on',x==b)});
var o=D.g[g].o[sel[g]];if(o.i!=null){show(o.i);if(hint)hint.hidden=true}else if(hint)hint.hidden=false;upd()}})});
show(0);upd()}
var E=function(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2},sg=function(p,a,b){return Math.min(1,Math.max(0,(p-a)/(b-a)))},
onscroll=function(f){var t=0,r=function(){t=0;f()};addEventListener('scroll',function(){if(!t){t=1;requestAnimationFrame(r)}},{passive:true});addEventListener('resize',r);f()},
seen=function(el,cb,th){if(!window.IntersectionObserver){cb(true);return}var o=new IntersectionObserver(function(es){cb(es[0].isIntersecting)},{threshold:th||.45});o.observe(el)};
var st=$('#story');
if(st){var g=function(i){return document.getElementById(i)},sc=function(el,x,y,cx,cy){el.setAttribute('transform','translate('+cx+','+cy+') scale('+x+','+y+') translate('+-cx+','+-cy+')')},
K=$$('.k',st),dots=$$('.dots i',st),cap=$('.cap',st),rp=$('.rp',st),last=-1,run=0,
C=[['Printed with love','Your name, photo or design is printed in sharp, lasting quality.'],['Set in a frame','The print is set neatly in place.'],['Wrapped beautifully','Nafees gift wrapping on every order.'],['Ribbon tied','A finishing ribbon for a special look.'],['A card goes with it','Your gift carries a little Vibe Gifts card.'],['On its way to you','Delivered to your door in 3-5 business days.']];
var draw=function(p){var e1=E(sg(p,0,.08)),fa=sg(p,.08,.14),e2=E(sg(p,.1,.19)),b=E(sg(p,.36,.41)),ta=E(sg(p,.42,.49)),t1=E(sg(p,.49,.64)),dr=E(sg(p,.64,.7)),go=E(sg(p,.7,1));
g('pp').setAttribute('transform','translate('+240*e2+','+(-120*e1+75*e2)+')');g('pp').style.opacity=p>.22?0:1;
sc(g('fr'),.9+.1*fa,.9+.1*fa,400,190);g('fr').style.opacity=fa;g('pr').style.opacity=1-.7*sg(p,.19,.24);
sc(g('wr'),1,E(sg(p,.2,.3)),400,98);sc(g('rv'),1,E(sg(p,.3,.35)),400,190);sc(g('rh'),E(sg(p,.32,.37)),1,400,190);sc(g('bw'),b,b,400,190);
g('tg').setAttribute('transform','rotate('+(-60*(1-ta))+' 400 192)');g('tg').style.opacity=ta;
g('tk').setAttribute('transform','translate('+(-300+615*t1+585*go)+',0)');
var T='translate('+(400+585*go)+','+(190+85*dr)+') scale('+(1-.55*dr)+') translate(-400,-190)';K.forEach(function(k){k.setAttribute('transform',T)});
g('road').setAttribute('stroke-dashoffset',-p*500);
var i=[.1,.2,.3,.42,.49].filter(function(x){return p>=x}).length;
if(i!=last){last=i;$('.num',cap).textContent='STEP 0'+(i+1);$('h3',cap).textContent=C[i][0];$('p',cap).textContent=C[i][1];dots.forEach(function(d,k){d.classList.toggle('on',k<=i)})}};
var play=function(){if(run)return;run=1;rp.hidden=true;var t0=0,D=13000,f=function(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/D);draw(p);if(p<1)requestAnimationFrame(f);else{run=0;rp.hidden=false}};requestAnimationFrame(f)};
draw(0);var started=0;seen(st,function(v){if(v&&!started){started=1;play()}},.5);rp.onclick=play}
var sh=$('#show'),setShow=function(){};
if(sh){var ALL=$$('.pc',sh),BG=$$('.bgl',sh),pcs=[],bgs=[],N=0,cur=0,timer=0,done=0,touched=0,vis=0,sw=0,cn=$('#sc'),sn=$('#sn'),dt=$('.sdt',sh),stg=$('.stg',sh),
SL=[[.13,.3,-8],[.87,.32,7],[.12,.76,6],[.88,.74,-6],[.5,.88,0]];
var render=function(){var W=stg.clientWidth,H=stg.clientHeight;
pcs.forEach(function(c,i){var l=SL[i%SL.length],tx=0,ty=0,s=1,rt=0,op=1,bl=0;
if(i<cur){tx=(l[0]-.5)*W;ty=(l[1]-.5)*H;s=.2;rt=l[2];op=.55;bl=2}else if(i>cur){s=.75;ty=70;op=0;bl=8}
c.style.opacity=op;c.style.transform='translate(-50%,-50%) translate('+tx+'px,'+ty+'px) scale('+s+') rotate('+rt+'deg)';c.style.filter=bl?'blur('+bl+'px)':'none';
c.style.pointerEvents=i<=cur?'auto':'none';c.classList.toggle('bgd',i<cur);bgs[i].style.opacity=i==cur?.6:0});
cn.textContent=cur+1;$$('i',dt).forEach(function(d,k){d.classList.toggle('on',k==cur)})};
var go=function(k){cur=Math.max(0,Math.min(N-1,k));render()},stop=function(){touched=1;clearTimeout(timer);timer=0};
var tick=function(){timer=0;if(cur<N-1){go(cur+1);timer=setTimeout(tick,3400)}else done=1},start=function(){if(!timer&&!done&&!touched)timer=setTimeout(tick,2600)};
setShow=function(list){clearTimeout(timer);timer=0;pcs=[];bgs=[];ALL.forEach(function(c){c.hidden=list.indexOf(c.dataset.slug)<0});BG.forEach(function(x){x.hidden=list.indexOf(x.dataset.slug)<0;x.style.opacity=0});
list.forEach(function(s){var c=ALL.filter(function(x){return x.dataset.slug==s})[0],g=BG.filter(function(x){return x.dataset.slug==s})[0];if(c&&g){pcs.push(c);bgs.push(g)}});
N=pcs.length;sn.textContent=N;cur=0;done=0;touched=0;dt.innerHTML=new Array(N+1).join('<i></i>');$$('i',dt).forEach(function(d,k){d.onclick=function(){stop();go(k)}});render();if(vis)start()};
$('.sbp',sh).onclick=function(){stop();go(cur-1)};$('.sbn',sh).onclick=function(){stop();go(cur+1)};
var x0=null;stg.addEventListener('dragstart',function(e){e.preventDefault()});stg.addEventListener('pointercancel',function(){x0=null});stg.addEventListener('pointerdown',function(e){x0=e.clientX});
stg.addEventListener('pointerup',function(e){if(x0===null)return;var d=e.clientX-x0;x0=null;if(Math.abs(d)>45){sw=1;setTimeout(function(){sw=0},80);stop();go(cur+(d<0?1:-1))}});
stg.addEventListener('click',function(e){if(sw){e.preventDefault();e.stopPropagation()}},true);
ALL.forEach(function(c){c.addEventListener('click',function(e){var i=pcs.indexOf(c);if(i>=0&&i<cur){e.preventDefault();stop();go(i)}})});
addEventListener('resize',render);seen(sh,function(v){vis=v;if(v)start();else{clearTimeout(timer);timer=0}},.45)}
$$('.tb').forEach(function(b){b.onclick=function(){var t=b.closest('.tm'),o=t.classList.toggle('open');b.setAttribute('aria-expanded',o);$('.mr',b).textContent=o?'Tap to close':'Tap to read more'}});
var bar=document.createElement('div');bar.className='sp';document.body.appendChild(bar);
onscroll(function(){var h=document.documentElement;bar.style.width=(100*h.scrollTop/((h.scrollHeight-innerHeight)||1))+'%'});
var LKD=$('#looks'),LK=LKD?JSON.parse(LKD.textContent):{},NM={her:'Her',him:'Him',any:'Surprise me'},pk=$('#pk'),toast;
var getLook=function(){try{return localStorage.getItem('look')}catch(e){return null}},putLook=function(l){try{localStorage.setItem('look',l)}catch(e){}};
var apply=function(l){document.documentElement.setAttribute('data-look',l);$$('.sty b').forEach(function(b){b.textContent=NM[l]});var d=LK[l];if(!d)return;
var h=$('.look-h');if(h)h.textContent=d.h;var st=$('.sl-t');if(st)st.textContent=d.st;
$$('.fan img').forEach(function(im,i){if(d.fan[i]){im.src='/images/'+d.fan[i][0];im.alt=d.fan[i][1]}});
var sl=$('#sl');if(sl){$$('.card',sl).forEach(function(c){var k=d.sl.indexOf(c.dataset.slug);c.style.order=k<0?99:k;c.hidden=k<0});sl.scrollLeft=0}
setShow(d.sh)};
var openPk=function(){pk.hidden=false;pk.classList.add('open');document.body.style.overflow='hidden';var f=$('.pk-o',pk);if(f)f.focus()},
closePk=function(){pk.classList.remove('open');pk.hidden=true;document.body.style.overflow=''};
var say=function(l){if(toast)toast.remove();toast=document.createElement('div');toast.className='toast';toast.setAttribute('role','status');toast.innerHTML='Style set to <b>'+NM[l]+'</b>. You can change it anytime from the menu: <b>Style</b>.';document.body.appendChild(toast);
$$('.sty').forEach(function(b){b.classList.add('pulse')});setTimeout(function(){toast.classList.add('out');$$('.sty').forEach(function(b){b.classList.remove('pulse')})},5200);setTimeout(function(){toast.remove()},5800)};
if(pk){$$('.pk-o',pk).forEach(function(b){b.onclick=function(){var l=b.dataset.look;putLook(l);apply(l);closePk();say(l)}});
$('.pk-x',pk).onclick=function(){if(!getLook()){putLook('any');apply('any')}closePk()};
pk.addEventListener('click',function(e){if(e.target==pk)$('.pk-x',pk).click()});
addEventListener('keydown',function(e){if(e.key=='Escape'&&pk.classList.contains('open'))$('.pk-x',pk).click()});
$$('.sty').forEach(function(b){b.onclick=function(){if(nav)nav.classList.remove('open');openPk()}})}
var saved=getLook();apply(saved||'any');if(pk&&!saved&&document.body.classList.contains('home'))setTimeout(openPk,450);
})();
