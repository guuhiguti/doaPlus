from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import categorias, itens, doacoes  # adiciona "doacoes" para registrar doadores

home_route = Blueprint('home', __name__)

@home_route.route('/')
def index():
    return render_template('index.html', categorias=categorias)

@home_route.route('/<categoria_nome>')
def mostrar_categoria(categoria_nome):  
    itens_categoria = itens.get(categoria_nome, [])  
    return render_template('categoria.html', categoria=categoria_nome, itens=itens_categoria)

@home_route.route('/doar/<categoria_nome>/<item_nome>', methods=['GET', 'POST'])
def doar_item(categoria_nome, item_nome):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        # salva dados da doação
        doacoes.append({
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'categoria': categoria_nome,
            'item': item_nome
        })
        flash('Doação registrada com sucesso!', 'success')
        return redirect(url_for('home.agradecimento'))

    return render_template('doacao_form.html', categoria=categoria_nome, item=item_nome)

@home_route.route('/agradecimento')
def agradecimento():
    return render_template('agradecimento.html')
