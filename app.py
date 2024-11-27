from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Добавьте секретный ключ для сокетов

# Инициализируем объект socketio
socketio = SocketIO(app)

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для переключения темы
@app.route('/set_theme', methods=['POST'])
def set_theme():
    theme = request.json.get('theme')  # Получаем выбранную тему от клиента
    if theme in ['rain', 'default']:
        return jsonify({'success': True, 'theme': theme})
    return jsonify({'success': False}), 400

# Другие маршруты
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

# Обработка сообщений WebSocket
@socketio.on('message')
def handle_message(msg):
    print(f'Получено сообщение: {msg}')
    send(msg, broadcast=True)  # Отправляем сообщение всем подключенным клиентам

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)
