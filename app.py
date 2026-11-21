from flask import Flask, jsonify, Response
import os
from io import BytesIO
from PIL import Image, ImageDraw
app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>My Alarm Task List</title><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#2563eb">
<style>
body{font-family:sans-serif;background:#111827;color:white;padding:18px;max-width:500px;margin:auto}
body.light{background:#f3f4f6;color:#111}
.card{background:#1f2937;padding:16px;border-radius:16px} body.light .card{background:white;box-shadow:0 4px 12px #0002}
input,select{padding:13px;margin:7px 0;width:100%;border-radius:12px;border:none;box-sizing:border-box;font-size:15px}
button{padding:12px 16px;border:none;border-radius:10px;font-weight:bold;cursor:pointer}
.blue{background:#2563eb;color:white}.gray{background:#6b7280;color:white}.red{background:#dc2626;color:white}
.top{display:flex;justify-content:space-between;align-items:center}
.toggle{background:white;color:#111;border-radius:20px;padding:8px 12px;font-size:13px}
.badge{background:#16a34a;color:white;padding:5px 10px;border-radius:20px;font-size:13px;display:inline-block}
.task{background:#374151;padding:13px;margin:9px 0;border-radius:12px} body.light .task{background:#e5e7eb}
.task b{font-size:16px}.at{color:#60a5fa;font-weight:bold;font-size:14px;margin-top:4px}
.row{display:flex;gap:8px}.row select{flex:1}.row button{flex:1}
label{font-size:13px;opacity:.7}.box{background:#111827;padding:12px;border-radius:12px;margin-top:10px} body.light .box{background:#f3f4f6}
</style></head><body>
<div class="top"><h2>⏰ My<br>Alarm Task List</h2><button class="toggle" onclick="document.body.classList.toggle('light')">🌙 Dark / ☀️ Light</button></div>
<span class="badge">✅ Offline Ready</span><p style="opacity:.6;font-size:13px">Data charao cholbe!</p>
<div class="card">
<input id="t" placeholder="Notun kaj likho... jemon: bazar kora">
<select id="p"><option>🔴 High</option><option>🟡 Medium</option><option>🟢 Low</option></select>
<label>🕐 Task er Time Set Koro:</label>
<div class="row"><select id="hh"></select><select id="mm"></select><select id="ap"><option>AM</option><option>PM</option></select></div>
<div class="box"><label>🔊 Alarm Setting:</label>
<label>Kotokkhon bajbe?</label><select id="dur"><option value="30">30 Second</option><option value="60" selected>1 Minute</option><option value="120">2 Minute</option><option value="0">Stop na kora porjonto</option></select>
<label>Koybar bajbe?</label><select id="rep"><option value="1">1 Bar</option><option value="3" selected>3 Bar</option><option value="5">5 Bar</option></select>
<label>Sound:</label><select id="snd"><option value="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg">Beep Beep</option><option value="https://actions.google.com/sounds/v1/alarms/beep_short.ogg">Alarm Clock</option><option value="https://actions.google.com/sounds/v1/alarms/phone_ringtone.ogg">Ring Ring</option></select></div>
<div class="row"><button class="blue" onclick="add()">Add Task</button><button class="gray" onclick="clearAll()">🗑️ Sob Delete</button></div>
<div id="list"></div><hr>
<h3>⏰ Alarm Status</h3><p id="astatus" style="font-size:13px;opacity:.7">Kono alarm nai</p>
<button class="red" style="width:100%" onclick="stopAlarm()">Stop 🔇</button>
</div><audio id="a" loop></audio>
<script>
let tasks=JSON.parse(localStorage.getItem('tasks')||'[]');
let hh=document.getElementById('hh'),mm=document.getElementById('mm');
for(let i=1;i<=12;i++)hh.innerHTML+=`<option>${String(i).padStart(2,'0')}</option>`;
for(let i=0;i<60;i++)mm.innerHTML+=`<option>${String(i).padStart(2,'0')}</option>`;
hh.value='05'; mm.value='00'; document.getElementById('ap').value='PM';
function safe(x){ if(!x.rep) x.rep='3'; if(!x.dur) x.dur='60'; if(!x.durText) x.durText=x.dur==='0'?'Stop na kora porjonto':x.dur+' sec'; if(!x.sound) x.sound=document.getElementById('snd').value; return x; }
tasks=tasks.map(safe); localStorage.setItem('tasks',JSON.stringify(tasks));
function render(){let h='';tasks.forEach((x,i)=>{x=safe(x);h+=`<div class="task"><b>Task ${i+1} - ${x.t}</b><div class="at">🕐 at ${x.show} • 🔁 ${x.rep} bar • ⏱️ ${x.durText}</div><div style="display:flex;justify-content:space-between;margin-top:8px"><span style="font-size:13px;opacity:.7">${x.p}</span><span onclick="del(${i})" style="color:#f87171;font-weight:bold;cursor:pointer">❌</span></div></div>`});document.getElementById('list').innerHTML=h||'<p style="opacity:.6">Kono kaj nai</p>'}
function add(){let v=document.getElementById('t').value;if(!v)return alert('Kaj likho!');let h=hh.value,m=mm.value,ap=document.getElementById('ap').value;let h24=parseInt(h)%12+(ap==='PM'?12:0);let t24=String(h24).padStart(2,'0')+':'+m;let dur=document.getElementById('dur').value,rep=document.getElementById('rep').value;let durText=dur==='0'?'Stop na kora porjonto':dur+' sec';tasks.push({t:v,p:document.getElementById('p').value,show:h+':'+m+' '+ap,t24:t24,rang:false,dur:dur,rep:rep,durText:durText,sound:document.getElementById('snd').value});localStorage.setItem('tasks',JSON.stringify(tasks));document.getElementById('t').value='';render();document.getElementById('astatus').innerText='Alarm set: '+v+' at '+h+':'+m+' '+ap+' | '+rep+' bar bajbe, '+durText;}
function del(i){tasks.splice(i,1);localStorage.setItem('tasks',JSON.stringify(tasks));render()}
function clearAll(){if(confirm('Sob delete?')){tasks=[];localStorage.setItem('tasks','[]');render()}}
let stopped=false;
function stopAlarm(){stopped=true;document.getElementById('a').pause();document.getElementById('astatus').innerText='Alarm off';}
function ringAlarm(task){
 stopped=false;let maxRep=parseInt(task.rep||3);let durSec=parseInt(task.dur||60);let count=0;
 let audio=document.getElementById('a'); audio.src=task.sound||document.getElementById('snd').value;
 function oneRing(){
  if(stopped) return; count++; document.getElementById('astatus').innerText='🔔 BAJTASE! '+task.t+' - '+count+'/'+maxRep+' bar';
  audio.play().catch(()=>{}); alert('⏰ ALARM!\\nTask: '+task.t+'\\nTime: '+task.show+'\\n'+count+'/'+maxRep+' bar');
  if(durSec===0) return;
  setTimeout(()=>{audio.pause(); if(stopped) return; if(count<maxRep){setTimeout(oneRing,5000)} else{document.getElementById('astatus').innerText='Alarm sesh: '+task.t}},durSec*1000)}
 oneRing();}
setInterval(()=>{let now=new Date().toTimeString().slice(0,5);tasks.forEach(x=>{if(x.t24===now&&!x.rang){x.rang=true;localStorage.setItem('tasks',JSON.stringify(tasks));ringAlarm(x)}})},5000);
render();if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}
</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/manifest.json')
def manifest(): return jsonify({"name":"My Alarm Task List","short_name":"Alarm","start_url":"/","display":"standalone","background_color":"#111827","theme_color":"#2563eb","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]})
@app.route('/icon-<size>.png')
def icon(size):
    s=512 if '512' in size else 192
    img=Image.new('RGB',(s,s),(37,99,235));d=ImageDraw.Draw(img)
    d.ellipse([s*0.15,s*0.15,s*0.85,s*0.85],outline='white',width=int(s*0.08))
    d.line([s/2,s/2,s/2,s*0.3],fill='white',width=int(s*0.06));d.line([s/2,s/2,s*0.68,s/2],fill='white',width=int(s*0.06))
    buf=BytesIO();img.save(buf,'PNG');buf.seek(0);return Response(buf.getvalue(),mimetype='image/png')
@app.route('/sw.js')
def sw(): return Response("self.addEventListener('install',e=>{self.skipWaiting()});self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)))})",mimetype='application/javascript')
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
