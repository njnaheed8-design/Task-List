import os
from flask import Flask, request, redirect
app = Flask(__name__)
tasks = []

@app.route('/')
def home():
    t = "".join([f"<div class='task'><span>{x}</span><a href='/del/{i}'>❌</a></div>" for i,x in enumerate(tasks)])
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<link rel='manifest' href='/manifest.json'><meta name='theme-color' content='#ff5e62'>
<style>
body{{font-family:sans-serif;background:linear-gradient(135deg,#ff9966,#ff5e62);min-height:100vh;margin:0;padding:20px}}
body.dark{{background:#1a1a1a !important}}
.card{{background:white;max-width:500px;margin:auto;padding:20px;border-radius:20px}}
body.dark .card{{background:#2d2d2d;color:white}}
body.dark input{{background:#333;color:white}}
input{{padding:12px;width:70%;border:1px solid #ddd;border-radius:10px}}
button{{padding:12px 18px;background:#ff5e62;color:white;border:none;border-radius:10px}}
.task{{display:flex;justify-content:space-between;padding:12px;background:#f9f9f9;margin-top:10px;border-radius:10px}}
body.dark .task{{background:#444;color:white}}
.task a{{text-decoration:none}}
</style></head><body>
<div class='card'>
<button onclick="document.body.classList.toggle('dark');localStorage.setItem('dark',document.body.classList.contains('dark'))" style='float:right;border:none;background:#eee;font-size:18px;border-radius:50%;width:38px;height:38px'>🌙</button>
<h2>✅ Amar Task List</h2>
<form action='/add' method='post'><input name='task' placeholder='Notun task likho...' required><button>Add +</button></form>
<div>{t if t else '<p style="color:#888">Ekhono kono task nai</p>'}</div>
</div><script>if(localStorage.getItem('dark')=='true')document.body.classList.add('dark')</script></body></html>"""

@app.route('/add', methods=['POST'])
def add():
    tasks.append(request.form['task'])
    return redirect('/')

@app.route('/del/<int:i>')
def dele(i):
    if 0 <= i < len(tasks): tasks.pop(i)
    return redirect('/')

@app.route('/manifest.json')
def mani():
    return open('manifest.json').read(), 200, {'Content-Type':'application/json'}

@app.route('/icon.png')
def icon():
    return open('icon.png','rb').read(), 200, {'Content-Type':'image/png'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
