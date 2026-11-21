from flask import Flask, jsonify, Response
import os
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>My Alarm Task List</title><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#2563eb">
<style>body{font-family:sans-serif;background:#111827;color:white;padding:20px;max-width:500px;margin:auto}input,select,button{padding:13px;margin:6px 0;width:100%;border-radius:12px;border:none;box-sizing:border-box}button{background:#2563eb;color:white;font-weight:bold;font-size:16px}.task{background:#1f2937;padding:14px;margin:10px 0;border-radius:12px}.time{color:#60a5fa;font-size:13px}h1{font-size:28px}</style></head>
<body><h1>My Alarm Task List</h1><p>Data charao cholbe!</p>
<input id="t" placeholder="Notun kaj likho...">
<input id="tm" type="time">
<select id="p"><option>High 🔴</option><option>Medium 🟡</option><option>Low 🟢</option></select>
<button onclick="add()">Add Task + Alarm Set</button>
<button onclick="clearAll()" style="background:#374151">Sob Delete</button>
<div id="list"></div><audio id="snd" src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"></audio>
<script>
let tasks=JSON.parse(localStorage.getItem('tasks')||'[]');
function render(){let h='';tasks.forEach((x,i)=>{h+=`<div class="task"><b>${x.t}</b><div class="time">${x.tm||'No time'} • ${x.p}</div><div style="margin-top:8px"><button onclick="del(${i})" style="background:#dc2626;padding:8px">Delete</button></div></div>`});document.getElementById('list').innerHTML=h||'<p style="opacity:.6">Kono kaj nai, notun kaj add koro.</p>'}
function add(){let v=document.getElementById('t').value;if(!v)return alert('Kaj likho!');tasks.push({t:v,tm:document.getElementById('tm').value,p:document.getElementById('p').value});localStorage.setItem('tasks',JSON.stringify(tasks));document.getElementById('t').value='';render()}
function del(i){tasks.splice(i,1);localStorage.setItem('tasks',JSON.stringify(tasks));render()}
function clearAll(){if(confirm('Sob delete korbo?')){tasks=[];localStorage.setItem('tasks','[]');render()}}
setInterval(()=>{let now=new Date().toTimeString().slice(0,5);tasks.forEach(x=>{if(x.tm===now&&!x.rang){x.rang=true;localStorage.setItem('tasks',JSON.stringify(tasks));document.getElementById('snd').play();alert('ALARM: '+x.t)}})},10000);
render();if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}
</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"My Alarm Task List","short_name":"Alarm","start_url":"/","display":"standalone","background_color":"#111827","theme_color":"#2563eb","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"}]})
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
