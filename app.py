from flask import Flask, jsonify, Response, request
import os
from io import BytesIO

try:
    from PIL import Image, ImageDraw
    HAS_PILLOW = True
except:
    HAS_PILLOW = False

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>My Alarm Task List</title><link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2563eb">
<style>body{font-family:sans-serif;background:#111827;color:white;padding:20px}input,select,button{padding:12px;margin:5px 0;width:100%;border-radius:10px;border:none}button{background:#2563eb;color:white;font-weight:bold}.task{background:#1f2937;padding:12px;margin:8px 0;border-radius:10px;display:flex;justify-content:space-between}</style>
</head><body>
<h2>My Alarm Task List</h2>
<p>Data charao cholbe!</p>
<input id="t" placeholder="Notun kaj likho...">
<select id="p"><option>High</option><option>Medium</option><option>Low</option></select>
<button onclick="add()">Add Task</button>
<button onclick="clearAll()" style="background:#374151">Sob Delete</button>
<div id="list"></div>
<script>
let tasks = JSON.parse(localStorage.getItem('tasks')||'[]');
function render(){let h='';tasks.forEach((x,i)=>{h+=`<div class="task"><span>${x.p} - ${x.t}</span><span onclick="del(${i})" style="color:red;cursor:pointer">X</span></div>`});document.getElementById('list').innerHTML=h}
function add(){let v=document.getElementById('t').value;if(!v)return;tasks.push({t:v,p:document.getElementById('p').value});localStorage.setItem('tasks',JSON.stringify(tasks));document.getElementById('t').value='';render()}
function del(i){tasks.splice(i,1);localStorage.setItem('tasks',JSON.stringify(tasks));render()}
function clearAll(){tasks=[];localStorage.setItem('tasks','[]');render()}
render();
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}
</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"My Alarm Task List","short_name":"Alarm","start_url":"/","display":"standalone","background_color":"#111827","theme_color":"#2563eb","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]})

@app.route('/icon-<size>.png')
def icon(size):
    s = 512 if '512' in size else 192
    img = Image.new('RGB',(s,s),(37,99,235))
    d = ImageDraw.Draw(img)
    d.ellipse([s*0.15,s*0.15,s*0.85,s*0.85],outline='white',width=int(s*0.08))
    d.line([s/2,s/2,s/2,s*0.3],fill='white',width=int(s*0.06))
    d.line([s/2,s/2,s*0.68,s/2],fill='white',width=int(s*0.06))
    buf = BytesIO(); img.save(buf,'PNG'); buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/sw.js')
def sw():
    js = "self.addEventListener('install',e=>{self.skipWaiting()});self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)))})"
    return Response(js, mimetype='application/javascript')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
