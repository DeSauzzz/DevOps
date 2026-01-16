import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Item
from datetime import datetime

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
        # Создаем тестовые данные
        item1 = Item(title='Test Item 1', description='Description 1')
        item2 = Item(title='Test Item 2', description='Description 2')
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()
    yield

def test_new_item():
    """Тест создания нового элемента"""
    item = Item(title='Test Title', description='Test Description')
    assert item.title == 'Test Title'
    assert item.description == 'Test Description'
    assert isinstance(item.created_at, datetime)

def test_item_to_dict():
    """Тест преобразования элемента в словарь"""
    item = Item(title='Test Title', description='Test Description')
    item_dict = item.to_dict()
    assert item_dict['title'] == 'Test Title'
    assert 'created_at' in item_dict

def test_database_connection(app, init_database):
    """Тест подключения к базе данных"""
    with app.app_context():
        items = Item.query.all()
        assert len(items) == 2
        assert items[0].title == 'Test Item 1'