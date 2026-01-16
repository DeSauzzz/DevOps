#!/bin/bash
sudo apt update && \
sudo apt install postgresql postgresql-contrib && \
sudo apt install python3 && \
sudo apt install pip && \
sudo apt install git curl vim && \
sudo apt install systemctl && \
cd myapp && pip install -r requirements.txt && cd .. && \
echo "Создание и настройка БД" && \
service postgresql start && \
sudo systemctl enable && sudo systemctl start && \
sudo -u postgres psql <<EOF
CREATE DATABASE myapp_db;
ALTER USER postgres WITH PASSWORD 'postgres';
EOF
exit && \
echo "База данных создана"

