# routes/home.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import itens, doacoes  # 🔹 já está importando

home_route = Blueprint('home', __name__)

@home_route.route('/')
def index():
    return render_template('index.html')

@home_route.route('/<categoria_nome>')
def mostrar_categoria(categoria_nome):
    itens_categoria = itens.get(categoria_nome, [])
    return render_template('categoria.html', categoria=categoria_nome, itens=itens_categoria)

# Rota de doação
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

        # ✅ SALVAR a doação na lista global 'doacoes'
        doacoes.append({
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "item": item['nome'],
            "mensagem": mensagem
        })

        flash(f"Obrigado, {nome}! Sua doação de {item['nome']} foi registrada.", "success")
        return redirect(url_for('home.agradecimento', nome=nome, item=item['nome']))

    return render_template('doar.html', categoria=categoria_nome, item=item)


@home_route.route('/agradecimento')
def agradecimento():
    nome = request.args.get('nome')
    item = request.args.get('item')
    return render_template('agradecimento.html', nome=nome, item=item)
