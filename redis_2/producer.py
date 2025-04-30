from flask import Flask, request, jsonify
import redis
import json
import time
import requests
import random
import threading

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
message_iter = 0

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    email = data['email']
    topic = data['topic']
    message = data['message']
    letter = {
        'email': email,
        'topic': topic,
        'message': message
    }

    # Публикуем сообщение в канал
    r.publish('my_channel', json.dumps(letter))

    # Записываем сообщение в очередь для дальнейшей обработки
    r.rpush('email_queue', json.dumps(letter))

    print(f"Message sent: {letter}")
    return jsonify({'status': 'Message sent!'}), 200

# Функция для отправки 10 сообщений с неравномерной задержкой
def send_requests_group(start_iter):
    local_message_iter = start_iter
    for _ in range(10):
        email = f"user{random.randint(1, 100)}@example.com"
        topic = "Test Topic"
        message = "This is a test message"
        process_time = time.time() + 10  # Время, через 10 секунд после отправки
        data = {
            'email': email,
            'topic': topic + str(local_message_iter),
            'message': message,
            'process_time': process_time
        }
        
        # Случайная задержка перед отправкой
        delay = random.uniform(0.1, 1.5)  # Задержка от 0.1 до 1.5 секунд
        time.sleep(delay)  # Задержка перед отправкой
        
        response = requests.post("http://localhost:5000/send", json=data)
        print(response.json(), "Message №", local_message_iter)
        local_message_iter += 1  # Увеличиваем локальный итератор

        time.sleep(0.5)  # Задержка между запросами

@app.route('/30-requests', methods=['GET'])
def send_multiple_requests():
    global message_iter
    for _ in range(3):  # Отправляем 3 группы по 10 сообщений
        threading.Thread(target=send_requests_group, args=(message_iter,)).start()
        message_iter += 10  # Увеличиваем global message_iter для следующей группы
        time.sleep(1)  # Задержка перед отправкой следующей группы
    return jsonify({'status': 'Requests sent!'}), 200  # Ответ после отправки

if __name__ == '__main__':
    app.run(port=5000)