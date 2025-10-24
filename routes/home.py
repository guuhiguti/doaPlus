# routes/home.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import itens

home_route = Blueprint('home', __name__)

@home_route.route('/')
def index():
    return render_template('index.html')

@home_route.route('/<categoria_nome>')
def mostrar_categoria(categoria_nome):
    itens_categoria = itens.get(categoria_nome, [])
    return render_template('categoria.html', categoria=categoria_nome, itens=itens_categoria)

# Nova rota de doação
@home_route.route('/doar/<categoria_nome>/<int:item_id>', methods=['GET', 'POST'])
def doar_item(categoria_nome, item_id):
    item = next((i for i in itens[categoria_nome] if i['id'] == item_id), None)
    if not item:
        flash('Item não encontrado', 'danger')
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        mensagem = request.form['mensagem']

        # Aqui você pode salvar os dados no banco ou enviar um e-mail, etc.
        flash(f"Obrigado, {nome}! Sua doação de {item['nome']} foi registrada.", "success")
        return redirect(url_for('home.mostrar_categoria', categoria_nome=categoria_nome))

    return render_template('doar.html', categoria=categoria_nome, item=item)
