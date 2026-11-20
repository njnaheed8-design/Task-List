import os, sqlite3
from flask import Flask, request, redirect
app = Flask(__name__)
DB = "tasks.db"

def get_db():
    db = sqlite3.connect(DB); db.row_factory = sqlite3.Row; return db

def init_db():
    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT, done INTEGER DEFAULT 0,
        due TEXT, priority TEXT, category TEXT)""")
    db.commit(); db.close()
init_db()

@app.route('/')
def home():
    q = request.args.get('q','').lower()
    cat = request.args.get('cat','')
    db = get_db()
    rows = db.execute("SELECT * FROM tasks ORDER BY done ASC, CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, due ASC").fetchall()
    db.close()
    total=len(rows); done=sum(1 for r in rows if r['done']); pct=int(done/total*100) if total else 0
    t_html=""
    for r in rows:
        if q and q not in r['text'].lower(): continue
        if cat and cat!="All" and r['category']!=cat: continue
        style="text-decoration:line-through;opacity:0.5" if r['done'] else ""
        check="✅" if r['done'] else "⬜"
        pcol={"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"}.get(r['priority'],"#999")
        picon={"High":"🔴","Medium":"🟡","Low":"🟢"}.get(r['priority'],"")
        t_html+=f"<div class='task'><div style='flex:1'><span><a href='/toggle/{r['id']}'>{check}</a> <b style='{style}'>{r['text']}</b></span><br><small>📅 {r['due'] or 'No date'} | {picon} {r['priority']} | 🏷️ {r['category']}</small></div><div class='acts'><a href='/edit/{r['id']}'>✏️</a> <a href='/del/{r['id']}'>❌</a></div></div>"
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<link rel='manifest' href='/manifest.json'><meta name='theme-color' content='#7c3aed'>
<style>*{{box-sizing:border-box}} body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);min-height:100vh;margin:0;padding:16px}}
.card{{background:rgba(255,255,255,0.95);max-width:520px;margin:auto;padding:22px;border-radius:24px;box-shadow:0 20px 40px rgba(0,0,0,0.2)}}
body.dark .card{{background:#1e1e2e;color:white}} body.dark input,body.dark select{{background:#2d2d3a;color:white;border-color:#444}}
input,select{{padding:13px;width:100%;margin-top:8px;border:1.5px solid #e5e7eb;border-radius:12px;font-size:15px}}
.row{{display:flex;gap:8px}} .row select{{flex:1}}
.btn{{padding:13px;background:linear-gradient(135deg,#7c3aed,#db2777);color:white;border:none;border-radius:12px;margin-top:10px;width:100%;font-weight:bold;font-size:16px}}
.task{{display:flex;gap:10px;align-items:center;padding:14px;background:#f8fafc;margin-top:10px;border-radius:14px;border-left:5px solid #7c3aed}} body.dark .task{{background:#2d2d3a}}
.task a{{text-decoration:none;font-size:19px}} .acts a{{margin-left:6px}}
.bar{{background:#e5e7eb;height:14px;border-radius:20px;overflow:hidden;margin:12px 0}} .fill{{background:linear-gradient(90deg,#22c55e,#16a34a);height:100%;width:{pct}%;border-radius:20px}}
.cat{{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}} .cat a{{padding:7px 13px;background:#eef2ff;border-radius:20px;text-decoration:none;color:#4338ca;font-size:13px;font-weight:600}} .cat a.on{{background:#7c3aed;color:white}}
h2{{margin:5px 0}} .top{{display:flex;justify-content:space-between;align-items:center}}</style></head><body>
<div class='card'><div class='top'><h2>✔ Amar Task List</h2><button onclick='document.body.classList.toggle("dark");localStorage.setItem("dark",document.body.classList.contains("dark"))' style='font-size:20px;background:none;border:none'>🌙</button></div>
<p><b>{done}/{total} Done - {pct}%</b> 🎯</p><div class='bar'><div class='fill'></div></div>
<form action='/add' method='post'><input name='task' placeholder='✨ Notun task likho...' required><input type='date' name='due'><div class='row'><select name='priority'><option>High 🔴</option><option selected>Medium 🟡</option><option>Low 🟢</option></select><select name='category'><option>Bazar</option><option>Pora</option><option>Kaj</option><option selected>Onno</option></select></div><button class='btn'>+ Add Task</button></form>
<form method='get'><input name='q' value='{q}' placeholder='🔍 Search task...'><button class='btn' style='background:#111827'>Search</button></form>
<div class='cat'><a href='/?cat=All' class='{"on" if cat in ["","All"] else ""}'>All</a><a href='/?cat=Bazar' class='{"on" if cat=="Bazar" else ""}'>🛒 Bazar</a><a href='/?cat=Pora' class='{"on" if cat=="Pora" else ""}'>📚 Pora</a><a href='/?cat=Kaj' class='{"on" if cat=="Kaj" else ""}'>💼 Kaj</a><a href='/?cat=Onno' class='{"on" if cat=="Onno" else ""}'>📌 Onno</a></div>
<div>{t_html if t_html else '<p style="color:#888;text-align:center;margin-top:20px">Kono task pai nai 😴</p>'}</div>
</div><script>if(localStorage.getItem('dark')=='true')document.body.classList.add('dark')</script></body></html>"""

@app.route('/add', methods=['POST'])
def add():
    db=get_db(); pri=request.form['priority'].split()[0]
    db.execute("INSERT INTO tasks (text,due,priority,category) VALUES (?,?,?,?)", (request.form['task'], request.form['due'], pri, request.form['category'])); db.commit(); db.close(); return redirect('/')

@app.route('/toggle/<int:i>')
def toggle(i):
    db=get_db(); db.execute("UPDATE tasks SET done=1-done WHERE id=?", (i,)); db.commit(); db.close(); return redirect('/')

@app.route('/del/<int:i>')
def dele(i):
    db=get_db(); db.execute("DELETE FROM tasks WHERE id=?", (i,)); db.commit(); db.close(); return redirect('/')

@app.route('/edit/<int:i>', methods=['GET','POST'])
def edit(i):
    db=get_db()
    if request.method=='POST':
        pri=request.form['priority'].split()[0]
        db.execute("UPDATE tasks SET text=?, due=?, priority=?, category=? WHERE id=?", (request.form['task'], request.form['due'], pri, request.form['category'], i)); db.commit(); db.close(); return redirect('/')
    r=db.execute("SELECT * FROM tasks WHERE id=?", (i,)).fetchone(); db.close()
    if not r: return redirect('/')
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px}} .card{{background:white;max-width:480px;margin:auto;padding:22px;border-radius:20px}} input,select{{padding:12px;width:100%;margin-top:8px;border:1px solid #ddd;border-radius:10px}} button{{padding:12px;width:100%;margin-top:10px;background:#7c3aed;color:white;border:none;border-radius:10px;font-weight:bold}} a{{display:block;text-align:center;margin-top:10px;color:#666}}</style></head><body><div class='card'><h2>✏️ Edit Task</h2>
<form method='post'><input name='task' value='{r['text']}' required><input type='date' name='due' value='{r['due'] or ""}'><select name='priority'><option {'selected' if r['priority']=='High' else ''}>High 🔴</option><option {'selected' if r['priority']=='Medium' else ''}>Medium 🟡</option><option {'selected' if r['priority']=='Low' else ''}>Low 🟢</option></select><select name='category'><option {'selected' if r['category']=='Bazar' else ''}>Bazar</option><option {'selected' if r['category']=='Pora' else ''}>Pora</option><option {'selected' if r['category']=='Kaj' else ''}>Kaj</option><option {'selected' if r['category']=='Onno' else ''}>Onno</option></select><button>Save Change ✅</button></form><a href='/'>Cancel</a></div></body></html>"""

@app.route('/manifest.json')
def man(): return open('manifest.json').read(), 200, {'Content-Type':'application/json'}
@app.route('/icon.png')
def icon(): return open('icon.png','rb').read(), 200, {'Content-Type':'image/png'}
if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
