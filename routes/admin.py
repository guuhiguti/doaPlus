# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database.db import itens, doacoes

admin_route = Blueprint('admin', __name__)

USER = {"email": "teste@gmail.com", "senha": "123"}

@admin_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email == USER['email'] and senha == USER['senha']:
            session['logado'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Credenciais inválidas', 'danger')
    return render_template('login.html')

@admin_route.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('home.index'))

@admin_route.route('/')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('admin.login'))
    return render_template('dashboard.html', itens=itens)

@admin_route.route('/doacoes')
def ver_doacoes():
    if not session.get('logado'):
        return redirect(url_for('admin.login'))
    return render_template('lista_doacoes.html', doacoes=doacoes)

# CRUD
@admin_route.route('/<categoria>/add', methods=['GET', 'POST'])
def add_item(categoria):
    if not session.get('logado'):
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        novo_item = {
            "id": len(itens[categoria]) + 1,
            "nome": request.form['nome'],
            "descricao": request.form['descricao']
        }
        itens[categoria].append(novo_item)
        flash('Item adicionado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_item.html', categoria=categoria)

@admin_route.route('/<categoria>/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(categoria, item_id):
    if not session.get('logado'):
        return redirect(url_for('admin.login'))

    item = next((i for i in itens[categoria] if i['id'] == item_id), None)
    if not item:
        flash('Item não encontrado', 'danger')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        item['nome'] = request.form['nome']
        item['descricao'] = request.form['descricao']
        flash('Item atualizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('edit_item.html', categoria=categoria, item=item)

@admin_route.route('/<categoria>/<int:item_id>/delete')
def delete_item(categoria, item_id):
    if not session.get('logado'):
        return redirect(url_for('admin.login'))
    itens[categoria] = [i for i in itens[categoria] if i['id'] != item_id]
    flash('Item deletado com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))
