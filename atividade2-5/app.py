from flask import Flask, render_template, request, make_response, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta_super_segura'

@app.route('/')
def index():
    nome = request.cookies.get('usuario_nome', 'Desconhecido')
    
    contador = request.cookies.get('contador', '0')
    novo_contador = int(contador) + 1
    
    resp = make_response(render_template('index.html', nome=nome, contador=novo_contador))
    resp.set_cookie('contador', str(novo_contador))
    return resp

@app.route('/nome/<nome>')
def salvar_nome(nome):
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('usuario_nome', nome)
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if usuario == 'teste' and senha == '123':
            session['user'] = usuario
            return redirect(url_for('perfil'))
        return "Credenciais inválidas!", 401
        
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))
    nome = request.cookies.get('usuario_nome', 'Desconhecido')
    return render_template('perfil.html', user=nome)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)