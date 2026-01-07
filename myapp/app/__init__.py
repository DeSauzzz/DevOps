from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from prometheus_client import Counter, Histogram, Gauge
import time
import os

db = SQLAlchemy()
csrf = CSRFProtect()

ITEMS_TOTAL = Gauge('items_total', 'Total number of items')
REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['endpoint'])

def create_app(config_class='config.Config'):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_class)
    
    db.init_app(app)
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)
    
    setup_metrics(app)

    with app.app_context():
        db.create_all()
    
    return app


def setup_metrics(app):
    """Настройка сбора метрик"""
    
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time'):
            if request.path == '/metrics':
                return response
            status_code = str(response.status_code)
            duration = time.time() - request.start_time
            REQUEST_DURATION.labels(endpoint=request.path).observe(duration)
            REQUESTS_TOTAL.labels(method=request.method, endpoint=request.path, status=status_code).inc()
        
        return response
    
    @app.route('/metrics')
    def metrics():
        from prometheus_client import generate_latest
        from flask import Response
        update_app_metrics()
        return Response(generate_latest(), mimetype='text/plain')

def update_app_metrics():
    """Обновление метрик приложения"""
    from app.models import Item
    from app import db
    
    try:
        count = Item.query.count()
        ITEMS_TOTAL.set(count)
    except:
        ITEMS_TOTAL.set(-1)
