from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from app import db
from app.models import Item
from app.forms import ItemForm
from prometheus_client import Counter, Histogram
import time

main = Blueprint('main', __name__)

ITEMS_CREATED = Counter('app_items_created_total', 'Total items created')
ITEMS_DELETED = Counter('app_items_deleted_total', 'Total items deleted')            # Will be supported in close (or not) future
API_REQUESTS  = Counter('app_api_requests_total', 'Total API requests', ['endpoint'])

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
        
        ITEMS_CREATED.inc()

        flash('Элемент успешно добавлен!', 'success')
        return redirect(url_for('main.items'))
    return render_template('add_item.html', form=form)

@main.route('/api/items')
def api_items():
    API_REQUESTS.labels(endpoint='/api/items').inc()
    
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@main.route('/api/items/<int:id>')
def api_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@main.route('/health')
def health():
    API_REQUESTS.labels(endpoint='/health').inc()
    
    try:
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'timestamp': time.time()
    })