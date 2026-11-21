from flask import Flask, jsonify, Response
import os
from io import BytesIO
from PIL import Image, ImageDraw
app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>My Alarm Task List</title><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#2563eb">
<style>
body{font-family:sans-serif;background:#111827;color:white;padding:18px;max-width:500px;margin:auto;transition:.3s}
body.light{background:#f3f4f6;color:#111}
.card{background:#1f2937;padding:16px;border-radius:16px} body.light .card{background:white;box-shadow:0 4px 12px #0002}
input,select{padding:13px;margin:7px 0;width:100%;border-radius:12px;border:none;box-sizing:border-box;font-size:15px}
button{padding:12px 16px;border:none;border-radius:10px;font-weight:bold;cursor:pointer}
.blue{background:#2563eb;color:white}.gray{background:#6b7280;color:white}.red{background:#dc2626;color:white}
.top{display:flex;justify-content:space-between;align-items:center}
.toggle{background:white;color:#111;border-radius:20px;padding:8px 12px;font-size:13px}
.badge{background:#16a34a;color:white;padding:5px 10px;border-radius:20px;font-size:13px;display:inline-block}
.task{background:#374151;padding:12px;margin:8px 0;border-radius:10px;display:flex;justify-content:space-between;align-items:center} body.light .task{background:#e5e7eb}
.row{display:flex;gap:8px}.row select{flex:1}
</style></head><body>
<div class="top"><h2>⏰ My<br>Alarm Task List</h2><button class="toggle" onclick="document.body.classList.toggle('light')">🌙 Dark / ☀️ Light</button></div>
<span class="badge">✅ Offline Ready</span><p style="opacity:.6;font-size:13px">Data charao cholbe!</p>
<div class="card">
<input id="t" placeholder="Notun kaj likho...">
<select id="p"><option>🔴 High</option><option>🟡 Medium</option><option>🟢 Low</option></select>
<div class="row"><button class="blue" style="flex:1" onclick="add()">Add Task</button><button class="gray" style="flex:1" onclick="clearAll()">🗑️ Sob Delete</button></div>
<div id="list"></div><hr>
<h3>⏰ Alarm + AM/PM</h3>
<div class="row"><select id="hh"></select><select id="mm"></select><select id="ap"><option>AM</option><option>PM</option></select></div>
<select id="snd"><option value="beep">Beep Beep</option><option value="alarm">Alarm Clock</option><option value="ring">Ring Ring</option></select>
<div class="row"><button class="blue" style="flex:1" onclick="setAlarm()">Set Alarm</button><button class="red" style="flex:1" onclick="stopAlarm()">Stop 🔇</button></div>
<p id="astatus" style="font-size:13px;opacity:.7"></p>
</div><audio id="a" loop src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"></audio>
<script>
let tasks=JSON.parse(localStorage.getItem('tasks')||'[]');
let hh=document.getElementById('hh'),mm=document.getElementById('mm');
for(let i=1;i<=12;i++)hh.innerHTML+=`<option>${String(i).padStart(2,'0')}</option>`;
for(let i=0;i<60;i++)mm.innerHTML+=`<option>${String(i).padStart(2,'0')}</option>`;
function render(){let h='';tasks.forEach((x,i)=>{h+=`<div class="task"><span>${x.p} - ${x.t}</span><span onclick="del(${i})" style="color:#f87171;font-weight:bold;cursor:pointer;font-size:20px">❌</span></div>`});document.getElementById('list').innerHTML=h}
function add(){let v=document.getElementById('t').value;if(!v)return;tasks.push({t:v,p:document.getElementById('p').value});localStorage.setItem('tasks',JSON.stringify(tasks));document.getElementById('t').value='';render()}
function del(i){tasks.splice(i,1);localStorage.setItem('tasks',JSON.stringify(tasks));render()}
function clearAll(){tasks=[];localStorage.setItem('tasks','[]');render()}
let alarmTime=null;
function setAlarm(){let h=hh.value,m=mm.value,ap=document.getElementById('ap').value;let h24=parseInt(h)%12+(ap==='PM'?12:0);alarmTime=String(h24).padStart(2,'0')+':'+m;document.getElementById('astatus').innerText='Alarm set: '+h+':'+m+' '+ap;alert('Alarm set! '+h+':'+m+' '+ap)}
function stopAlarm(){alarmTime=null;document.getElementById('a').pause();document.getElementById('astatus').innerText='Alarm off';}
setInterval(()=>{if(!alarmTime)return;let now=new Date().toTimeString().slice(0,5);if(now===alarmTime){document.getElementById('a').play();alert('⏰ ALARM! Time hoise!')}} ,5000);
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
