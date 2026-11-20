import os, sqlite3
from flask import Flask, request, redirect, g
app = Flask(__name__)
DB = "tasks.db"

def get_db():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT, done INTEGER DEFAULT 0,
        due TEXT, priority TEXT, category TEXT)""")
    db.commit()
    # Purono tasks.json thakle niye aso
    if os.path.exists("tasks.json"):
        try:
            import json
            data = json.load(open("tasks.json"))
            for x in data:
                t = x if isinstance(x, str) else x.get("text","")
                if t:
                    db.execute("INSERT INTO tasks (text,done,due,priority,category) VALUES (?,?,?,?,?)", (t, 1 if isinstance(x,dict) and x.get("done") else 0, "", "Medium", "Onno"))
            db.commit()
            os.rename("tasks.json","tasks.json.bak")
        except: pass
    db.close()

init_db()

@app.route('/')
def home():
    q = request.args.get('q','').lower()
    cat = request.args.get('cat','')
    db = get_db()
    rows = db.execute("SELECT * FROM tasks ORDER BY done ASC, CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, due ASC").fetchall()
    db.close()
    total = len(rows)
    done = sum(1 for r in rows if r['done'])
    pct = int(done/total*100) if total else 0
    t_html = ""
    for r in rows:
        if q and q not in r['text'].lower(): continue
        if cat and cat != "All" and r['category'] != cat: continue
        style = "text-decoration:line-through;opacity:0.5" if r['done'] else ""
        check = "✅" if r['done'] else "⬜"
        pcol = {"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"}.get(r['priority'],"#999")
        t_html += f"<div class='task'><span><a href='/toggle/{r['id']}?cat={cat}&q={q}'>{check}</a> <span style='{style}'>{r['text']}</span><br><small>📅 {r['due'] or 'No date'} | <b style='color:{pcol}'>{r['priority']}</b> | 🏷️ {r['category']}</small></span><span><a href='/del/{r['id']}'>❌</a></span></div>"
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<link rel='manifest' href='/manifest.json'><meta name='theme-color' content='#ff5e62'>
<style>body{{font-family:sans-serif;background:linear-gradient(135deg,#ff9966,#ff5e62);min-height:100vh;margin:0;padding:20px}}
.card{{background:white;max-width:520px;margin:auto;padding:20px;border-radius:20px}}
body.dark .card{{background:#2d2d2d;color:white}} body.dark input,body.dark select{{background:#333;color:white}}
input,select{{padding:11px;width:100%;margin-top:8px;border:1px solid #ddd;border-radius:10px;box-sizing:border-box}}
.row{{display:flex;gap:8px}} .row select{{flex:1}}
button{{padding:12px 16px;background:#ff5e62;color:white;border:none;border-radius:10px;margin-top:10px;width:100%}}
.task{{display:flex;justify-content:space-between;padding:12px;background:#f9f9f9;margin-top:10px;border-radius:10px}} body.dark .task{{background:#444}}
.task a{{text-decoration:none;font-size:18px}}
.bar{{background:#eee;height:12px;border-radius:10px;overflow:hidden;margin:10px 0}} .fill{{background:#22c55e;height:100%;width:{pct}%}}
.cat{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}} .cat a{{padding:6px 12px;background:#eee;border-radius:20px;text-decoration:none;color:#333;font-size:13px}}
.cat a.on{{background:#ff5e62;color:white}}</style></head><body>
<div class='card'>
<button onclick='document.body.classList.toggle("dark");localStorage.setItem("dark",document.body.classList.contains("dark"))'>🌙</button>
<h2>✔ Amar Task List</h2><p><b>{done}/{total} Done - {pct}%</b></p><div class='bar'><div class='fill'></div></div>
<form action='/add' method='post'>
<input name='task' placeholder='Notun task likho...' required>
<input type='date' name='due'>
<div class='row'>
<select name='priority'><option>High 🔴</option><option selected>Medium 🟡</option><option>Low 🟢</option></select>
<select name='category'><option>Bazar</option><option>Pora</option><option>Kaj</option><option selected>Onno</option></select>
</div><button>Add +</button></form>
<form method='get'><input name='q' value='{q}' placeholder='🔍 Search task...'><button>Search</button></form>
<div class='cat'>
<a href='/?cat=All' class='{"on" if cat in ["","All"] else ""}'>All</a>
<a href='/?cat=Bazar' class='{"on" if cat=="Bazar" else ""}'>🛒 Bazar</a>
<a href='/?cat=Pora' class='{"on" if cat=="Pora" else ""}'>📚 Pora</a>
<a href='/?cat=Kaj' class='{"on" if cat=="Kaj" else ""}'>💼 Kaj</a>
<a href='/?cat=Onno' class='{"on" if cat=="Onno" else ""}'>📌 Onno</a>
</div>
<div>{t_html if t_html else '<p style="color:#888">Kono task pai nai</p>'}</div>
</div><script>if(localStorage.getItem('dark')=='true')document.body.classList.add('dark')</script></body></html>"""

@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    pri = request.form['priority'].split()[0]
    db.execute("INSERT INTO tasks (text,due,priority,category) VALUES (?,?,?,?)", (request.form['task'], request.form['due'], pri, request.form['category']))
    db.commit(); db.close()
    return redirect('/')

@app.route('/toggle/<int:i>')
def toggle(i):
    db = get_db()
    db.execute("UPDATE tasks SET done = 1-done WHERE id=?", (i,)); db.commit(); db.close()
    return redirect(f"/?cat={request.args.get('cat','')}&q={request.args.get('q','')}")

@app.route('/del/<int:i>')
def dele(i):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (i,)); db.commit(); db.close()
    return redirect('/')

@app.route('/manifest.json')
def man():
    return open('manifest.json').read(), 200, {'Content-Type': 'application/json'}
@app.route('/icon.png')
def icon():
    return open('icon.png','rb').read(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
