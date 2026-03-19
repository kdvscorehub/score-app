from flask import Flask, request, render_template, redirect, url_for, session
import os
from database import init_db, get_student, save_student

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_strong_random_key'
app.config['SESSION_PERMANENT'] = True

init_db()

CLASSES = ["open", "match", "factory", "auto"]

# Landing page
@app.route('/', methods=['GET', 'POST'])
def landing():
    print("Landing route hit")

    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == "secret123":
            session['authenticated'] = True
            return redirect(url_for('form'))
        else:
            error = "Incorrect password!"
            return render_template('landing.html', error=error)

    return render_template('landing.html', error=None)

# Form page (authenticated)
@app.route('/form', methods=['GET', 'POST'])
def form():
    if not session.get('authenticated'):
        return redirect(url_for('landing'))

    data = {
        'first_name': '',
        'last_name': '',
        'score': '',
        'xcount': '',
        'class': ''
    }

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        score = request.form['score']
        xcount = request.form['xcount']
        class_name = request.form['class']
        save_student(first_name, last_name, score, xcount, class_name)
        existing = get_student(first_name, last_name)
        if existing:
            data = {
                'first_name': existing[0],
                'last_name': existing[1],
                'score': existing[2],
                'xcount': existing[3],
                'class': existing[4]
            }
	return redirect(url_for('form', first_name=first_name, last_name=last_name))

    # GET with optional pre-fill
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    if first_name and last_name:
        existing = get_student(first_name, last_name)
        if existing:
            data = {
                'first_name': existing[0],
                'last_name': existing[1],
                'score': existing[2],
                'xcount': existing[3],
                'class': existing[4]
            }

    return render_template('form.html', data=data, classes=CLASSES)

# View all results (no password required)
@app.route('/results')
def view_results():
    from database import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT first_name, last_name, score, xcount, class FROM students ORDER BY id DESC')
    students = cur.fetchall()
    conn.close()
    return render_template('results_list.html', students=students)

# Optional logout
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('landing'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
