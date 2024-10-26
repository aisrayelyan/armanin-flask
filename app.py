from flask import Flask, request, jsonify, send_from_directory, make_response
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__, static_folder='static')

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname='taskmanager',
        user='taskuser',
        password='password',
        host='postgres'  # Используйте имя сервиса PostgreSQL
    )
    return conn


# Создайте таблицу задач при запуске приложения, если её нет
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Middleware для добавления заголовков безопасности
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Server'] = 'Flask'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    return response

# Главная страница
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Маршруты для обслуживания статических файлов
@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# Получить список задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

# Добавить новую задачу
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Task added successfully!'}), 201
    return jsonify({'message': 'Task content is missing!'}), 400

# Удалить задачу
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Task deleted successfully!'}), 200
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task not found!'}), 404

if __name__ == '__main__':
    init_db()  # Инициализация базы данных при запуске приложения
    app.run(host='0.0.0.0', port=5000, debug=True)
