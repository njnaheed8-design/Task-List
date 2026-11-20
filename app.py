import os, sqlite3
from flask import Flask, request, redirect
app = Flask(__name__)
DB = "tasks.db"
def get_db():
    db=sqlite3.connect(DB); db.row_factory=sqlite3.Row; return db
def init_db():
    db=get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, done INTEGER DEFAULT 0, due TEXT, priority TEXT, category TEXT, alarm TEXT DEFAULT '')""")
    # Purono DB te alarm column na thakle add koro
    try: db.execute("ALTER TABLE tasks ADD COLUMN alarm TEXT DEFAULT ''")
    except: pass
    db.commit(); db.close()
init_db()

@app.route('/')
def home():
    q=request.args.get('q','').lower(); cat=request.args.get('cat','')
    db=get_db(); rows=db.execute("SELECT * FROM tasks ORDER BY done ASC, due ASC").fetchall(); db.close()
    total=len(rows); done=sum(1 for r in rows if r['done']); pct=int(done/total*100) if total else 0
    t_html=""; alarms=[]
    for r in rows:
        if q and q not in r['text'].lower(): continue
        if cat and cat!="All" and r['category']!=cat: continue
        style="text-decoration:line-through;opacity:0.5" if r['done'] else ""
        check="✅" if r['done'] else "⬜"
        pcol={"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"}.get(r['priority'],"#999")
        if r['alarm'] and not r['done']:
            alarms.append(f"{r['due']} {r['alarm']}|{r['text']}")
        t_html+=f"<div class='task'><div style='flex:1'><a href='/toggle/{r['id']}'>{check}</a> <b style='{style}'>{r['text']}</b><br><small>📅 {r['due'] or 'No date'} ⏰ {r['alarm'] or 'No alarm'} | <b style='color:{pcol}'>{r['priority']}</b> | 🏷️ {r['category']}</small></div><div><a href='/edit/{r['id']}'>✏️</a> <a href='/del/{r['id']}'>❌</a></div></div>"
    alarm_js = str(alarms)
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='manifest' href='/manifest.json'>
<style>body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);min-height:100vh;margin:0;padding:16px}} .card{{background:white;max-width:520px;margin:auto;padding:22px;border-radius:24px}} body.dark .card{{background:#1e1e2e;color:white}} body.dark input,body.dark select{{background:#2d2d3a;color:white}} input,select{{padding:12px;width:100%;margin-top:8px;border:1.5px solid #ddd;border-radius:12px}} .row{{display:flex;gap:8px}} .row select{{flex:1}} .btn{{padding:13px;background:linear-gradient(135deg,#7c3aed,#db2777);color:white;border:none;border-radius:12px;margin-top:10px;width:100%;font-weight:bold}} .task{{display:flex;gap:10px;padding:13px;background:#f8fafc;margin-top:10px;border-radius:14px;border-left:5px solid #7c3aed}} body.dark .task{{background:#2d2d3a}} .task a{{text-decoration:none;font-size:18px}} .bar{{background:#eee;height:13px;border-radius:20px;overflow:hidden}} .fill{{background:#22c55e;height:100%;width:{pct}%}} .cat{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}} .cat a{{padding:6px 12px;background:#eef2ff;border-radius:20px;text-decoration:none;color:#4338ca;font-size:13px}} .cat a.on{{background:#7c3aed;color:white}} #alarmBox{{display:none;background:#fef3c7;border:2px solid #f59e0b;padding:15px;border-radius:14px;margin-bottom:12px;text-align:center}} #alarmBox button{{padding:10px 20px;background:#f59e0b;border:none;border-radius:10px;font-weight:bold;margin-top:8px}}</style></head><body>
<div class='card'>
<div id='alarmBox'><h3>⏰ ALARM!</h3><p id='alarmText'></p><button onclick='stopAlarm()'>Stop / Done ✅</button></div>
<div style='display:flex;justify-content:space-between'><h2>✔ Amar Task List</h2><button onclick='document.body.classList.toggle("dark")' style='background:none;border:none;font-size:20px'>🌙</button></div>
<p><b>{done}/{total} Done - {pct}%</b></p><div class='bar'><div class='fill'></div></div>
<form action='/add' method='post'><input name='task' placeholder='✨ Notun task...' required>
<div class='row'><input type='date' name='due'><input type='time' name='alarm'></div>
<div class='row'><select name='priority'><option>High 🔴</option><option selected>Medium 🟡</option><option>Low 🟢</option></select><select name='category'><option>Bazar</option><option>Pora</option><option>Kaj</option><option selected>Onno</option></select></div><button class='btn'>+ Add Task ⏰</button></form>
<form method='get'><input name='q' value='{q}' placeholder='🔍 Search...'><button class='btn' style='background:#111827'>Search</button></form>
<div class='cat'><a href='/?cat=All' class='{"on" if cat in ["","All"] else ""}'>All</a><a href='/?cat=Bazar' class='{"on" if cat=="Bazar" else ""}'>🛒 Bazar</a><a href='/?cat=Pora' class='{"on" if cat=="Pora" else ""}'>📚 Pora</a><a href='/?cat=Kaj' class='{"on" if cat=="Kaj" else ""}'>💼 Kaj</a><a href='/?cat=Onno' class='{"on" if cat=="Onno" else ""}'>📌 Onno</a></div>
<div>{t_html if t_html else '<p style="text-align:center;color:#888">Kono task nai 😴</p>'}</div></div>
<script>
let alarms={alarm_js};
let audio=null; let ringing=false;
function beep(){{ try{{ let ctx=new (window.AudioContext||window.webkitAudioContext)(); let o=ctx.createOscillator(); o.connect(ctx.destination); o.frequency.value=880; o.start(); setTimeout(()=>o.stop(),800); }}catch(e){{}} }}
function stopAlarm(){{ document.getElementById('alarmBox').style.display='none'; ringing=false; if(audio){{clearInterval(audio)}} }}
function checkAlarm(){{ let now=new Date(); let today=now.toISOString().slice(0,10); let hm=now.toTimeString().slice(0,5); for(let a of alarms){{ let parts=a.split('|'); let dt=parts[0].trim(); let txt=parts[1]; if(dt===today+' '+hm && !ringing){{ ringing=true; document.getElementById('alarmText').innerText=txt+' er somoy hoye gese!'; document.getElementById('alarmBox').style.display='block'; audio=setInterval(beep,1000); if(Notification.permission==='granted') new Notification('⏰ Task Alarm',{{body:txt}}); }} }} }}
if(Notification.permission==='default') Notification.requestPermission();
setInterval(checkAlarm, 10000); checkAlarm();
</script></body></html>"""

@app.route('/add', methods=['POST'])
def add():
    db=get_db(); pri=request.form['priority'].split()[0]
    db.execute("INSERT INTO tasks (text,due,priority,category,alarm) VALUES (?,?,?,?,?)", (request.form['task'], request.form['due'], pri, request.form['category'], request.form.get('alarm',''))); db.commit(); db.close(); return redirect('/')
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
        db.execute("UPDATE tasks SET text=?, due=?, priority=?, category=?, alarm=? WHERE id=?", (request.form['task'], request.form['due'], pri, request.form['category'], request.form.get('alarm',''), i)); db.commit(); db.close(); return redirect('/')
    r=db.execute("SELECT * FROM tasks WHERE id=?", (i,)).fetchone(); db.close()
    if not r: return redirect('/')
    return f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px}} .card{{background:white;max-width:480px;margin:auto;padding:22px;border-radius:20px}} input,select{{padding:12px;width:100%;margin-top:8px;border:1px solid #ddd;border-radius:10px}} button{{padding:12px;width:100%;margin-top:10px;background:#7c3aed;color:white;border:none;border-radius:10px}} a{{display:block;text-align:center;margin-top:10px;color:#666}}</style></head><body><div class='card'><h2>✏️ Edit + ⏰ Alarm</h2>
<form method='post'><input name='task' value='{r['text']}' required><input type='date' name='due' value='{r['due'] or ""}'><input type='time' name='alarm' value='{r['alarm'] or ""}'><select name='priority'><option {'selected' if r['priority']=='High' else ''}>High 🔴</option><option {'selected' if r['priority']=='Medium' else ''}>Medium 🟡</option><option {'selected' if r['priority']=='Low' else ''}>Low 🟢</option></select><select name='category'><option {'selected' if r['category']=='Bazar' else ''}>Bazar</option><option {'selected' if r['category']=='Pora' else ''}>Pora</option><option {'selected' if r['category']=='Kaj' else ''}>Kaj</option><option {'selected' if r['category']=='Onno' else ''}>Onno</option></select><button>Save ✅</button></form><a href='/'>Cancel</a></div></body></html>"""
@app.route('/manifest.json')
def man(): return open('manifest.json').read(), 200, {'Content-Type':'application/json'}
@app.route('/icon.png')
def icon(): return open('icon.png','rb').read(), 200, {'Content-Type':'image/png'}
if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
