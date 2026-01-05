import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Item

@pytest.fixture
def app():
    app = create_app('app.config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        item = Item(title='Test Item', description='Test Description')
        db.session.add(item)
        db.session.commit()
    yield

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_items_page(client, init_database):
    """Тест страницы со списком элементов"""
    response = client.get('/items')
    assert response.status_code == 200
    assert b'Test Item' in response.data

def test_add_item_page(client):
    """Тест страницы добавления элемента"""
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add new element' in response.data

def test_add_item_post(client):
    """Тест добавления элемента через POST"""
    response = client.post('/add', data={
        'title': 'New Item',
        'description': 'New Description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New element was added' in response.data

def test_api_items(client, init_database):
    """Тест API для получения всех элементов"""
    response = client.get('/api/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['title'] == 'Test Item'

def test_api_single_item(client, init_database):
    """Тест API для получения одного элемента"""
    response = client.get('/api/items/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Item'

def test_health_endpoint(client):
    """Тест endpoint health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'