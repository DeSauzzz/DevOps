from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from app import db
from app.models import Item
from app.forms import ItemForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/items')
def items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('items.html', items=items)

@main.route('/add', methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, 
                   description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash('Элемент успешно добавлен!', 'success')
        return redirect(url_for('main.items'))
    return render_template('add_item.html', form=form)

@main.route('/api/items')
def api_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@main.route('/api/items/<int:id>')
def api_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@main.route('/health')
def health():
    return jsonify({'status': 'ok', 'database': 'connected'})