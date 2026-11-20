import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alarm Task List</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⏰</text></svg>">
<style>
body{font-family:Arial;padding:20px;transition:0.3s}
body.light{background:#f2f2f2;color:#000}
body.dark{background:#121212;color:#fff}
.box{background:white;padding:20px;border-radius:15px;max-width:500px;margin:auto}
body.dark .box{background:#1e1e1e}
input,select{padding:12px;width:95%;border-radius:10px;border:1px solid #ccc;margin:5px 0;font-size:16px}
.time-row{display:flex;gap:8px}
.time-row select{width:33%}
button{padding:12px 18px;background:#007bff;color:white;border:none;border-radius:10px;margin:5px 0;cursor:pointer}
button.stop{background:#ff3b30}
button.snooze{background:#ff9500}
li{background:#eee;padding:12px;margin:8px 0;border-radius:10px;list-style:none;display:flex;justify-content:space-between}
body.dark li{background:#333}
a{color:red;text-decoration:none;font-size:20px}
.mode{float:right;padding:8px 12px;background:#333;color:white;border-radius:20px}
body.dark .mode{background:#fff;color:#000}
</style>
</head>
<body class="light" id="body">
<div class="box">
<button class="mode" onclick="toggleMode()">🌙 Dark / ☀️ Light</button>
<h2>⏰ My Alarm Task List</h2>
<form method="POST" action="/add">
<input name="task" placeholder="Notun kaj likho..." required>
<select name="priority"><option>🔴 High</option><option>🟡 Medium</option><option>🟢 Low</option></select>
<button>Add Task</button>
</form>
<a href="/clear" style="font-size:14px">🗑️ Sob Delete</a>
<ul>
{% for t in tasks %}
<li><span>{{t}}</span> <a href="/delete/{{loop.index0}}">❌</a></li>
{% endfor %}
</ul>
<hr>
<h3>⏰ Alarm + Sound + AM/PM</h3>
<p style="font-size:14px">Ghonta - Minute - AM/PM alada kore dao:</p>
<div class="time-row">
<select id="hour">
<option>01</option><option>02</option><option>03</option><option>04</option><option>05</option><option>06</option><option>07</option><option>08</option><option>09</option><option>10</option><option>11</option><option>12</option>
</select>
<select id="minute">
<option>00</option><option>05</option><option>10</option><option>15</option><option>20</option><option>25</option><option>30</option><option>35</option><option>40</option><option>45</option><option>50</option><option>55</option>
</select>
<select id="ampm"><option>AM</option><option>PM</option></select>
</div>
<br>
<label>Sound:</label>
<select id="soundType"><option value="beep">Beep Beep</option><option value="loud">Loud Siren</option><option value="soft">Soft Bell</option></select>
<br>
<button onclick="setAlarm()">Set Alarm</button>
<button class="stop" onclick="stopAlarm()">Stop 🔇</button>
<button class="snooze" onclick="snooze()">Snooze 5 min 😴</button>
<p id="msg" style="font-weight:bold"></p>
<p id="showTime" style="color:green"></p>
</div>
<script>
let alarm=null, audioCtx=null;
function toggleMode(){
  let b=document.getElementById('body');
  b.className = b.className=='light' ? 'dark' : 'light';
  localStorage.setItem('mode', b.className);
}
if(localStorage.getItem('mode')) document.getElementById('body').className=localStorage.getItem('mode');
function playSound(){
  let type=document.getElementById('soundType').value;
  audioCtx=new (window.AudioContext||window.webkitAudioContext)();
  let freq = type=='loud'? 880 : type=='soft'? 520 : 700;
  for(let i=0;i<6;i++){
    let o=audioCtx.createOscillator(); let g=audioCtx.createGain();
    o.connect(g); g.connect(audioCtx.destination);
    o.frequency.value=freq; o.type= type=='soft'?'sine':'square';
    o.start(audioCtx.currentTime + i*0.6); o.stop(audioCtx.currentTime + i*0.6 + 0.5);
  }
}
function convertTo24(h,m,ap){
  h=parseInt(h); if(ap=='PM' && h!=12) h+=12; if(ap=='AM' && h==12) h=0;
  return String(h).padStart(2,'0')+':'+m;
}
function setAlarm(){
  let h=document.getElementById('hour').value;
  let m=document.getElementById('minute').value;
  let ap=document.getElementById('ampm').value;
  alarm=convertTo24(h,m,ap);
  document.getElementById('msg').innerText='✅ Alarm set: '+h+':'+m+' '+ap+' - Sound ON';
  document.getElementById('showTime').innerText='24h hisabe: '+alarm;
  playSound();
}
function stopAlarm(){ alarm=null; document.getElementById('msg').innerText='🔇 Alarm Bondho'; }
function snooze(){
  let d=new Date(); d.setMinutes(d.getMinutes()+5);
  alarm=d.toTimeString().slice(0,5);
  document.getElementById('msg').innerText='😴 Snooze: Abar bajbe '+alarm+' te';
}
setInterval(()=>{
  let now=new Date().toTimeString().slice(0,5);
  if(alarm && alarm==now){
    playSound();
    document.getElementById('msg').innerText='⏰ ALARM! Utho! '+now;
    navigator.vibrate && navigator.vibrate([500,200,500]);
  }
},1000);
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, tasks=tasks)
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    pri = request.form.get('priority')
    if task: tasks.append(f"{pri} - {task}")
    return redirect('/')
@app.route('/delete/<int:id>')
def delete(id):
    if 0 <= id < len(tasks): tasks.pop(id)
    return redirect('/')
@app.route('/clear')
def clear():
    tasks.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
