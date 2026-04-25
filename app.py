from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import get_connection, init_db, encrypt_password, decrypt_password
import secrets
import string

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

MASTER_PASSWORD = 'admin123'

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(chars) for _ in range(length))

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    passwords = conn.execute('SELECT * FROM passwords ORDER BY site').fetchall()
    conn.close()
    decrypted = []
    for p in passwords:
        decrypted.append({
            'id': p['id'],
            'site': p['site'],
            'username': p['username'],
            'password': decrypt_password(p['password']),
            'category': p['category'],
            'notes': p['notes']
        })
    return render_template('index.html', passwords=decrypted)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == MASTER_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Wrong master password!'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = encrypt_password(request.form['password'])
        category = request.form['category']
        notes = request.form['notes']
        conn = get_connection()
        conn.execute('''
            INSERT INTO passwords (site, username, password, category, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (site, username, password, category, notes))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    conn.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/generate')
def generate():
    return jsonify({'password': generate_password()})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)