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
<style>
body{font-family:Arial;background:#f2f2f2;padding:20px}
.box{background:white;padding:20px;border-radius:15px;max-width:500px;margin:auto}
input{padding:10px;width:70%;border-radius:8px;border:1px solid #ccc}
button{padding:10px 15px;background:#007bff;color:white;border:none;border-radius:8px}
li{background:#eee;padding:10px;margin:8px 0;border-radius:8px;list-style:none}
a{color:red;text-decoration:none}
</style>
</head>
<body>
<div class="box">
<h2>⏰ My Alarm Task List</h2>
<form method="POST" action="/add">
<input name="task" placeholder="Notun kaj likho..." required>
<button>Add</button>
</form>
<ul>
{% for t in tasks %}
<li>{{t}} <a href="/delete/{{loop.index0}}">❌</a></li>
{% endfor %}
</ul>
<h3>⏰ Alarm</h3>
<input type="time" id="alarmTime">
<button onclick="setAlarm()">Set Alarm</button>
<p id="msg"></p>
<audio id="sound" src="https://www.soundjay.com/buttons/sounds/beep-07a.mp3"></audio>
<script>
let alarm=null;
function setAlarm(){
  alarm=document.getElementById('alarmTime').value;
  document.getElementById('msg').innerText='Alarm set: '+alarm;
}
setInterval(()=>{
  let now=new Date().toTimeString().slice(0,5);
  if(alarm && alarm==now){
    document.getElementById('sound').play();
    document.getElementById('msg').innerText='⏰ ALARM! Utho!';
    alarm=null;
  }
},1000);
</script>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if 0 <= id < len(tasks):
        tasks.pop(id)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
