import os, json
from flask import Flask, request, redirect
app = Flask(__name__)

FILE = "tasks.json"

def load_tasks():
    if os.path.exists(FILE):
        try:
            data = json.load(open(FILE))
            # Purono string task ke notun format e convert
            out = []
            for x in data:
                if isinstance(x, str):
                    out.append({"text": x, "done": False})
                else:
                    out.append(x)
            return out
        except:
            return []
    return []

def save_tasks():
    json.dump(tasks, open(FILE, "w"))

tasks = load_tasks()

@app.route('/')
def home():
    q = request.args.get('q', '').lower()
    filtered = [(i, t) for i, t in enumerate(tasks) if q in t['text'].lower()] if q else list(enumerate(tasks))
    total = len(tasks)
    done = sum(1 for t in tasks if t['done'])
    pct = int(done/total*100) if total else 0

    t_html = ""
    for i, x in filtered:
        style = "text-decoration:line-through;opacity:0.5" if x['done'] else ""
        check = "✅" if x['done'] else "⬜"
        t_html += f"<div class='task'><span><a href='/toggle/{i}'>{check}</a> <span style='{style}'>{x['text']}</span></span><span><a href='/del/{i}'>❌</a></span></div>"

    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<link rel='manifest' href='/manifest.json'><meta name='theme-color' content='#ff5e62'>
<style>body{{font-family:sans-serif;background:linear-gradient(135deg,#ff9966,#ff5e62);min-height:100vh;margin:0;padding:20px}}
.card{{background:white;max-width:500px;margin:auto;padding:20px;border-radius:20px}}
body.dark .card{{background:#2d2d2d;color:white}}
body.dark input{{background:#333;color:white}}
input{{padding:12px;width:68%;border:1px solid #ddd;border-radius:10px}}
button{{padding:12px 16px;background:#ff5e62;color:white;border:none;border-radius:10px}}
.task{{display:flex;justify-content:space-between;padding:12px;background:#f9f9f9;margin-top:10px;border-radius:10px}}
body.dark .task{{background:#444;color:white}}
.task a{{text-decoration:none;font-size:18px}}
.bar{{background:#eee;height:12px;border-radius:10px;overflow:hidden;margin:10px 0}}
.fill{{background:#22c55e;height:100%;width:{pct}%;transition:0.3s}}
.search{{width:100%!important;margin-top:10px}}</style></head><body>
<div class='card'>
<button onclick='document.body.classList.toggle("dark");localStorage.setItem("dark",document.body.classList.contains("dark"))'>🌙</button>
<h2>✔ Amar Task List</h2>
<p><b>{done}/{total} Done - {pct}%</b></p>
<div class='bar'><div class='fill'></div></div>
<form action='/add' method='post'><input name='task' placeholder='Notun task likho...' required><button>Add +</button></form>
<form method='get'><input class='search' name='q' value='{request.args.get('q','')}' placeholder='🔍 Search task...'><button>Search</button></form>
<div>{t_html if t_html else '<p style="color:#888">Kono task pai nai</p>'}</div>
</div><script>if(localStorage.getItem('dark')=='true')document.body.classList.add('dark')</script></body></html>"""

@app.route('/add', methods=['POST'])
def add():
    tasks.append({"text": request.form['task'], "done": False})
    save_tasks()
    return redirect('/')

@app.route('/toggle/<int:i>')
def toggle(i):
    if 0 <= i < len(tasks):
        tasks[i]['done'] = not tasks[i]['done']
    save_tasks()
    return redirect('/')

@app.route('/del/<int:i>')
def dele(i):
    if 0 <= i < len(tasks): tasks.pop(i)
    save_tasks()
    return redirect('/')

@app.route('/manifest.json')
def man():
    return open('manifest.json').read(), 200, {'Content-Type': 'application/json'}

@app.route('/icon.png')
def icon():
    return open('icon.png','rb').read(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
