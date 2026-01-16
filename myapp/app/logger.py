import logging
import json
from datetime import datetime
import os

def setup_metric_logger(app):
    """Настройка логгера для метрик"""
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    metric_logger = logging.getLogger('app_metrics')
    metric_logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    metric_handler = logging.FileHandler(
        os.path.join(log_dir, 'metrics.log'),
        encoding='utf-8'
    )
    metric_handler.setLevel(logging.INFO)
    metric_handler.setFormatter(formatter)
    
    metric_logger.addHandler(metric_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    metric_logger.addHandler(console_handler)
    
    return metric_logger

def log_metric(metric_name, labels, value=1, timestamp=None):
    """Логирование метрики в файл"""
    log_entry = {
        'timestamp': timestamp or datetime.utcnow().isoformat(),
        'metric': metric_name,
        'labels': labels,
        'value': value,
        'type': 'counter_increment'  # или 'gauge_set', 'histogram_observe'
    }
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    with open(os.path.join(log_dir, 'metrics.log'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"📊 METRIC: {metric_name}{labels} = {value}")