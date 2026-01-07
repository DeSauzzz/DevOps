from app import create_app
from app.db_metrics import collect_db_metrics
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time

app = create_app()

# Создаем планировщик для периодического сбора метрик
scheduler = BackgroundScheduler()
scheduler.add_job(func=collect_db_metrics, trigger="interval", seconds=30)
scheduler.start()

# Останавливаем планировщик при выходе
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    # Первый сбор метрик
    collect_db_metrics()
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )