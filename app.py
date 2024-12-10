from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, send
from flask import session, flash
from flask import url_for
from flask import redirect
from db_utils import get_db_connection
import sqlite3


# Инициализация приложения и сокетов
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

# Набор для хранения активных пользователей
active_users = set()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Переключение темы
@app.route('/set_theme', methods=['POST'])
def set_theme():
    theme = request.json.get('theme')
    if theme in ['rain', 'default']:
        return jsonify({'success': True, 'theme': theme})
    return jsonify({'success': False}), 400

# Другие страницы
@app.route('/router_setup')
def router_setup():
    return render_template('router_setup.html')

@app.route('/antivirus_installation')
def antivirus_installation():
    return render_template('antivirus_installation.html')

@app.route('/pc_setup')
def pc_setup():
    return render_template('pc_setup.html')

@app.route('/other_services')
def other_services():
    return render_template('other_services.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/prices')
def prices():
    return render_template('prices.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/articles/router_setup')
def router_setup_page():
    return render_template('articles/router_setup.html')

@app.route('/articles/antivirus_installation')
def antivirus_installation_page():
    return render_template('articles/antivirus_installation.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Имя пользователя уже занято. Попробуйте другое.', 'error')
        finally:
            conn.close()

    return render_template('register.html')



# Маршрут для входа
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Неправильное имя пользователя или пароль.', 'error')

    return render_template('login.html')
'''
@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверка пользователя в базе данных
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?', 
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            # Сохраняем имя пользователя в сессии
            session['username'] = username
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('chat'))  # Переход на страницу чата
        else:
            flash('Неправильное имя пользователя или пароль.', 'error')

    # Возврат шаблона логина
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('login'))

# Обработка сообщений чата
@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    msg = data.get('msg')
    
    # Проверка имени пользователя
    if not username:
        username = data.get('username')
        if username in active_users:
            send({'error': 'Имя уже занято! Выберите другое.'}, to=request.sid)
            return
        else:
            session['username'] = username
            active_users.add(username)
            send({'username': username, 'msg': 'присоединился к чату!'}, broadcast=True)
    
    # Отправка сообщения всем пользователям
    send({'username': username, 'msg': msg}, broadcast=True)

# Обработка отключения пользователя
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in active_users:
        active_users.remove(username)
        send({'username': username, 'msg': 'покинул чат.'}, broadcast=True)



def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Проверяем, существует ли таблица users
    cursor.execute('''
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='users';
    ''')
    
    if cursor.fetchone() is None:  # Если таблица не найдена, создаём её
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        print("Таблица 'users' успешно создана.")
    else:
        print("Таблица 'users' уже существует. Пропуск создания.")

    conn.close()
# Запуск приложения
if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True)
