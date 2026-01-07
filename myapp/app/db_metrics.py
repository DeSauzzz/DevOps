from prometheus_client import Gauge, Histogram
from app import db
from app.models import Item
import psycopg2
from sqlalchemy import text

# Метрики для БД
DB_UP = Gauge('app_database_up', 'Database connection status (1=up, 0=down)')
DB_CONNECTIONS = Gauge('app_database_connections', 'Number of database connections')
DB_QUERY_DURATION = Histogram('app_database_query_duration_seconds', 'Database query duration')
DB_SIZE = Gauge('app_database_size_bytes', 'Database size in bytes')
DB_TABLES_COUNT = Gauge('app_database_tables_total', 'Number of tables in database')

def collect_db_metrics():
    """Сбор метрик базы данных"""
    try:
        db.session.execute(text('SELECT 1'))
        DB_UP.set(1)
        
        result = db.session.execute(text(
            "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database();"
        ))
        connections = result.scalar()
        DB_CONNECTIONS.set(connections)
        
        result = db.session.execute(text(
            "SELECT pg_database_size(current_database());"
        ))
        db_size = result.scalar()
        DB_SIZE.set(db_size)
        
        result = db.session.execute(text(
            "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
        ))
        tables_count = result.scalar()
        DB_TABLES_COUNT.set(tables_count)
        
    except Exception as e:
        print(f"Error collecting DB metrics: {e}")
        DB_UP.set(0)