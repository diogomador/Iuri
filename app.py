from flask import Flask, url_for, request, render_template, flash, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar sessões

# Obter uma conexão com SQLite
def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_name' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    users = conn.execute('SELECT id, nome, email FROM users').fetchall()
    return render_template('pages/index.html', users=users)


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['password']

        if not nome or not email:
            flash('Nome e Email são obrigatórios')
        else:
            conn = get_connection()
            conn.execute("INSERT INTO users (nome, email, senha) VALUES (?,?,?)", (nome, email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('pages/create.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE email=? AND senha=?", (email, senha)).fetchone()

        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['nome']
            return redirect(url_for('index'))
        else:
            flash('Email ou senha inválidos')
            return redirect(url_for('login'))

    return render_template('pages/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/<int:id>/edit', methods=['POST','GET'])
def edit(id):
    SELECT = 'SELECT * FROM users WHERE id=?'
    conn = get_connection()
    usuario = conn.execute(SELECT, (id,)).fetchone()

    if usuario == None:
        return 'Usuário não encontrado'

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        UPDATE = 'UPDATE users SET nome=?, email=? WHERE id=?'
        conn.execute(UPDATE, (nome, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('pages/edit.html', user=usuario)


if __name__ == '__main__':
    app.run(debug=True)
