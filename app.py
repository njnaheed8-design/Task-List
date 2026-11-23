<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Rul's Lafalafi - Forest Waterfall</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#07130c;color:#fff;font-family:system-ui;text-align:center;overflow:hidden}
.top{padding:8px}
h1{font-size:30px;text-shadow:0 3px 0 #000} h1 span{color:#a3e635}
.badges{display:flex;justify-content:center;gap:6px;margin:7px;flex-wrap:wrap}
.badge{background:#14532d;padding:6px 13px;border-radius:20px;font-weight:800;font-size:14px;border:1px solid #22c55e}
.badge b{color:#facc15}
canvas{background:#87ceeb;display:block;margin:6px auto;max-width:98vw;width:98vw;height:520px;border-radius:16px;border:4px solid #14532d;box-shadow:0 10px 30px rgba(0,0,0,.6)}
.btn{width:94%;max-width:440px;border:none;border-radius:999px;padding:17px;font-size:21px;font-weight:900;color:#fff;margin:5px auto;display:block}
#jumpBtn{background:linear-gradient(90deg,#0ea5e9,#22c55e);box-shadow:0 6px 0 #075985}
#jumpBtn:active{transform:translateY(4px);box-shadow:none}
#startBtn{background:#f59e0b;box-shadow:0 4px 0 #92400e}
</style>
</head>
<body>
<div class="top"><h1>🌳 Rul's <span>LAFALAFI FOREST</span> 💦</h1>
<div class="badges"><div class="badge">Score: <b id="sc">0</b></div><div class="badge">🪙 Coin: <b id="coin">0</b></div><div class="badge">Best: <b id="best">0</b></div><div class="badge" id="level">Forest Level 1</div></div></div>
<canvas id="c" width="420" height="520"></canvas>
<button class="btn" id="startBtn" onclick="startGame()">▶️ PLAY - FOREST E DHUKO</button>
<button class="btn" id="jumpBtn" ontouchstart="jump(event)" onclick="jump(event)">🦘 LAF DE! WATERFALL PAR HO</button>
<p style="opacity:.7;font-size:13px">Pani te laglei ses • Coin khaile +20 • 2 bar tap = Double Laf</p>
<script>
let cv=document.getElementById('c'), ctx=cv.getContext('2d');
let p, obs, coins, treesBack, treesFront, score, coinCount, best=localStorage.getItem('forest_best')||0, gameOn=false, timer, frame=0, speed=4.5, jumps=0;
document.getElementById('best').innerText=best;
function startGame(){
 p={x:60,y:400,w:42,h:52,vy:0}; obs=[]; coins=[]; treesBack=[]; treesFront=[]; score=0; coinCount=0; speed=4.5; frame=0; jumps=0;
 for(let i=0;i<6;i++){ treesBack.push({x:i*80, h:120+Math.random()*60}); treesFront.push({x:i*90, h:80+Math.random()*40}); }
 document.getElementById('sc').innerText=0; document.getElementById('coin').innerText=0;
 gameOn=true; clearInterval(timer); timer=setInterval(draw,16);
}
function jump(e){ if(e) e.preventDefault(); if(!gameOn) startGame(); if(jumps<2){ p.vy=-15; jumps++; } }
document.addEventListener('keydown',e=>{ if(e.code==='Space'){ e.preventDefault(); jump(); }});

function drawTree(x, baseY, h, dark){
 ctx.fillStyle=dark?'#5b3a1a':'#7c4a21'; ctx.fillRect(x+18, baseY-h*0.35, 12, h*0.35);
 ctx.fillStyle=dark?'#14532d':'#15803d';
 ctx.beginPath(); ctx.moveTo(x, baseY-h*0.35); ctx.lineTo(x+24, baseY-h); ctx.lineTo(x+48, baseY-h*0.35); ctx.closePath(); ctx.fill();
 ctx.beginPath(); ctx.moveTo(x+5, baseY-h*0.6); ctx.lineTo(x+24, baseY-h*1.15); ctx.lineTo(x+43, baseY-h*0.6); ctx.closePath(); ctx.fill();
}

function draw(){
 frame++;
 // Akash
 let g=ctx.createLinearGradient(0,0,0,520); g.addColorStop(0,'#38bdf8'); g.addColorStop(0.6,'#a7f3d0'); g.addColorStop(1,'#dcfce7'); ctx.fillStyle=g; ctx.fillRect(0,0,420,520);
 // Surjo
 ctx.fillStyle='#fde047'; ctx.beginPath(); ctx.arc(360,50,28,0,7); ctx.fill(); ctx.fillStyle='rgba(253,224,71,.3)'; ctx.beginPath(); ctx.arc(360,50,45,0,7); ctx.fill();
 // Megh
 ctx.fillStyle='rgba(255,255,255,.95)'; ctx.beginPath(); ctx.ellipse((frame*0.4)%500-40,60,35,12,0,0,7); ctx.fill(); ctx.beginPath(); ctx.ellipse((frame*0.3+200)%500-40,100,28,10,0,0,7); ctx.fill();

 // PISONER FOREST - aste cholbe (3D depth)
 treesBack.forEach(t=>{ t.x-=speed*0.3; if(t.x<-60) t.x=430; drawTree(t.x, 430, t.h, true); });
 // SAMNER FOREST - jore cholbe
 treesFront.forEach(t=>{ t.x-=speed*0.7; if(t.x<-60) t.x=430; drawTree(t.x, 460, t.h, false); });

 // MATI - 3D feel er jonno perspective
 ctx.fillStyle='#8b5a2b'; ctx.fillRect(0,460,420,60);
 ctx.fillStyle='#22c55e'; ctx.fillRect(0,460,420,14);
 ctx.fillStyle='#16a34a'; for(let i=0;i<12;i++) ctx.fillRect((i*40-(frame*speed)%40),475,14,8);
 // Rasta
 ctx.fillStyle='#d9a066'; ctx.fillRect(0,485,420,20);
 ctx.fillStyle='#a16207'; for(let i=0;i<8;i++) ctx.fillRect((i*60-(frame*speed)%60),492,30,4);

 // Kangaroo + Chaya (3D feel)
 let shadowW = 34 - (400-p.y)*0.04; // Upor e uthle chaya choto
 ctx.fillStyle='rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(p.x+22, 478, Math.max(10,shadowW), 6, 0,0,7); ctx.fill();
 p.vy+=0.7; p.y+=p.vy; if(p.y>=400){ p.y=400; p.vy=0; jumps=0; }
 // Body
 ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.ellipse(p.x+22,p.y+32,20,24,0,0,7); ctx.fill();
 ctx.fillStyle='#fb923c'; ctx.beginPath(); ctx.ellipse(p.x+22,p.y+36,12,14,0,0,7); ctx.fill();
 ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.ellipse(p.x+32,p.y+8,10,18,-0.3,0,7); ctx.fill();
 ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(p.x+37,p.y+6,5,0,7); ctx.fill(); ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(p.x+38,p.y+6,2.5,0,7); ctx.fill();
 ctx.strokeStyle='#ea580c'; ctx.lineWidth=7; ctx.beginPath(); ctx.moveTo(p.x+8,p.y+44); ctx.lineTo(p.x-6,p.y+54); ctx.stroke();
 ctx.fillStyle='#ea580c'; ctx.fillRect(p.x+10,p.y+48,16,6);
 // Paa
 ctx.fillStyle='#c2410c'; ctx.fillRect(p.x+16,p.y+50,18,5);

 // WATERFALL BADHA - upor theke pani porbe
 if(frame%105===0) obs.push({x:430, gapY: 180+Math.random()*140});
 if(frame%190===0) coins.push({x:430, y:200+Math.random()*150});
 obs.forEach(o=>{
   o.x-=speed;
   // Uporer waterfall
   let topH = o.gapY-55;
   let grad=ctx.createLinearGradient(o.x,0,o.x+42,0); grad.addColorStop(0,'#0ea5e9'); grad.addColorStop(0.5,'#bae6fd'); grad.addColorStop(1,'#0369a1');
   ctx.fillStyle=grad; ctx.fillRect(o.x,0,42,topH);
   ctx.fillStyle='rgba(255,255,255,.7)'; for(let y=0;y<topH;y+=22) ctx.fillRect(o.x+10+Math.sin(y+frame*0.4)*4, y, 3, 14);
   // Nicher waterfall
   let botY = o.gapY+55;
   ctx.fillStyle=grad; ctx.fillRect(o.x,botY,42,460-botY);
   ctx.fillStyle='rgba(255,255,255,.7)'; for(let y=botY;y<460;y+=22) ctx.fillRect(o.x+10+Math.cos(y+frame*0.4)*4, y, 3, 14);
   // Paharer matha
   ctx.fillStyle='#78716c'; ctx.fillRect(o.x-4,0,50,14); ctx.fillRect(o.x-4,452,50,12);
 });
 obs=obs.filter(o=>o.x>-60);
 coins.forEach(c=>{ c.x-=speed; ctx.font='28px serif'; ctx.fillText('🪙',c.x,c.y); });
 coins=coins.filter(c=>c.x>-30);

 if(frame%8===0){ score++; document.getElementById('sc').innerText=score; }
 if(score>300){ speed=6; document.getElementById('level').innerText='Forest Level 2 - Pani Jore!'; }
 if(score>700){ speed=7.2; document.getElementById('level').innerText='Forest Level 3 - PRO! 💀'; }

 for(let c of coins){ if(Math.abs(p.x+20-c.x)<28 && Math.abs(p.y+25-c.y)<30){ coins.splice(coins.indexOf(c),1); coinCount++; score+=20; document.getElementById('coin').innerText=coinCount; document.getElementById('sc').innerText=score; } }
 for(let o of obs){
   let px=p.x+10, pw=24, py=p.y+5, ph=42;
   // Gap er majkhane thakle bachbo, naile pani lagbe
   let hitTop = py < o.gapY-55+5 && px+pw > o.x+4 && px < o.x+38;
   let hitBot = py+ph > o.gapY+55-5 && px+pw > o.x+4 && px < o.x+38;
   if(hitTop || hitBot){
     clearInterval(timer); gameOn=false;
     if(score>best){ best=score; localStorage.setItem('forest_best',best); document.getElementById('best').innerText=best; }
     alert('💦 Pani te Poira Gela! Score: '+score+' | Coin: '+coinCount); return;
   }
 }
}
</script>
</body>
</html>
