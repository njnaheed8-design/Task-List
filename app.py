import os, io
from flask import Flask, render_template_string, Response, jsonify, send_file
from PIL import Image, ImageDraw

app = Flask(__name__)

def make_icon(size):
    img = Image.new('RGB', (size, size), (0, 123, 255))
    d = ImageDraw.Draw(img)
    # Boro gol circle
    d.ellipse([size*0.15, size*0.15, size*0.85, size*0.85], outline=(255,255,255), width=int(size*0.08))
    d.line([size*0.5, size*0.5, size*0.5, size*0.28], fill=(255,255,255), width=int(size*0.07))
    d.line([size*0.5, size*0.5, size*0.68, size*0.5], fill=(255,255,255), width=int(size*0.07))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/icon-192.png')
def icon192():
    return send_file(make_icon(192), mimetype='image/png')
@app.route('/icon-512.png')
def icon512():
    return send_file(make_icon(512), mimetype='image/png')

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alarm Task List</title>
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="/icon-192.png">
<meta name="theme-color" content="#007bff">
<style>
body{font-family:Arial;padding:20px} body.light{background:#f2f2f2;color:#000} body.dark{background:#121212;color:#fff}
.box{background:white;padding:20px;border-radius:15px;max-width:500px;margin:auto} body.dark .box{background:#1e1e1e}
input,select{padding:12px;width:95%;border-radius:10px;border:1px solid #ccc;margin:5px 0;font-size:16px}
.time-row{display:flex;gap:8px} .time-row select{width:33%}
button{padding:12px 18px;background:#007bff;color:white;border:none;border-radius:10px;margin:5px 0;cursor:pointer}
button.stop{background:#ff3b30} button.snooze{background:#ff9500}
li{background:#eee;padding:12px;margin:8px 0;border-radius:10px;list-style:none;display:flex;justify-content:space-between} body.dark li{background:#333}
.mode{float:right;padding:8px 12px;background:#333;color:white;border-radius:20px} body.dark .mode{background:#fff;color:#000}
</style>
</head>
<body class="light" id="body">
<div class="box">
<button class="mode" onclick="toggleMode()">Dark / Light</button>
<h2>My Alarm Task List</h2>
<p style="font-size:12px;color:gray">Offline Ready - Data charao cholbe!</p>
<input id="taskInput" placeholder="Notun kaj likho...">
<select id="priority"><option>High</option><option>Medium</option><option>Low</option></select>
<button onclick="addTask()">Add Task</button>
<button onclick="clearAll()" style="background:#666">Sob Delete</button>
<ul id="taskList"></ul>
<hr>
<h3>Alarm + AM/PM</h3>
<div class="time-row">
<select id="hour"><option>01</option><option>02</option><option>03</option><option>04</option><option>05</option><option>06</option><option>07</option><option>08</option><option>09</option><option>10</option><option>11</option><option>12</option></select>
<select id="minute"><option>00</option><option>05</option><option>10</option><option>15</option><option>20</option><option>25</option><option>30</option><option>35</option><option>40</option><option>45</option><option>50</option><option>55</option></select>
<select id="ampm"><option>AM</option><option>PM</option></select>
</div>
<select id="soundType"><option value="beep">Beep Beep</option><option value="loud">Loud Siren</option><option value="soft">Soft Bell</option></select>
<button onclick="setAlarm()">Set Alarm</button>
<button class="stop" onclick="stopAlarm()">Stop</button>
<button class="snooze" onclick="snooze()">Snooze 5 min</button>
<p id="msg" style="font-weight:bold"></p>
</div>
<script>
if('serviceWorker' in navigator){ navigator.serviceWorker.register('/sw.js'); }
let tasks = JSON.parse(localStorage.getItem('myTasks')||'[]');
let alarm = localStorage.getItem('myAlarm')||null;
function saveTasks(){ localStorage.setItem('myTasks', JSON.stringify(tasks)); render(); }
function render(){ let ul=document.getElementById('taskList'); ul.innerHTML=''; tasks.forEach((t,i)=>{ let li=document.createElement('li'); li.innerHTML='<span>'+t+'</span> <span style="color:red;cursor:pointer" onclick="delTask('+i+')">X</span>'; ul.appendChild(li); }); }
function addTask(){ let inp=document.getElementById('taskInput'); let p=document.getElementById('priority').value; if(!inp.value) return; tasks.push(p+' - '+inp.value); inp.value=''; saveTasks(); }
function delTask(i){ tasks.splice(i,1); saveTasks(); }
function clearAll(){ tasks=[]; saveTasks(); }
function toggleMode(){ let b=document.getElementById('body'); b.className=b.className=='light'?'dark':'light'; localStorage.setItem('mode',b.className); }
if(localStorage.getItem('mode')) document.getElementById('body').className=localStorage.getItem('mode');
if(alarm) document.getElementById('msg').innerText='Alarm set: '+alarm;
function playSound(){ let ctx=new (window.AudioContext||window.webkitAudioContext)(); for(let i=0;i<6;i++){ let o=ctx.createOscillator(); let g=ctx.createGain(); o.connect(g); g.connect(ctx.destination); o.frequency.value=700; o.type='square'; o.start(ctx.currentTime+i*0.6); o.stop(ctx.currentTime+i*0.6+0.5); } }
function convertTo24(h,m,ap){ h=parseInt(h); if(ap=='PM'&&h!=12)h+=12; if(ap=='AM'&&h==12)h=0; return String(h).padStart(2,'0')+':'+m; }
function setAlarm(){ let h=document.getElementById('hour').value; let m=document.getElementById('minute').value; let ap=document.getElementById('ampm').value; alarm=convertTo24(h,m,ap); localStorage.setItem('myAlarm',alarm); document.getElementById('msg').innerText='Alarm set: '+h+':'+m+' '+ap; playSound(); }
function stopAlarm(){ alarm=null; localStorage.removeItem('myAlarm'); document.getElementById('msg').innerText='Alarm Bondho'; }
function snooze(){ let d=new Date(); d.setMinutes(d.getMinutes()+5); alarm=d.toTimeString().slice(0,5); localStorage.setItem('myAlarm',alarm); document.getElementById('msg').innerText='Snooze: Abar bajbe '+alarm+' te'; }
setInterval(()=>{ let now=new Date().toTimeString().slice(0,5); if(alarm&&alarm==now){ playSound(); document.getElementById('msg').innerText='ALARM! Utho!'; } },1000);
render();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)
@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"Alarm Task List","short_name":"Alarm","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#007bff","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]})
@app.route('/sw.js')
def sw():
    js = "self.addEventListener('install', e => { e.waitUntil(caches.open('alarm-v2').then(c => c.addAll(['/','/manifest.json','/icon-192.png','/icon-512.png']))); self.skipWaiting(); }); self.addEventListener('fetch', e => { e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { let copy=res.clone(); caches.open('alarm-v2').then(c=>c.put(e.request, copy)); return res; }).catch(()=>caches.match('/')))); });"
    return Response(js, mimetype='application/javascript')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
