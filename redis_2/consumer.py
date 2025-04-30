from flask import Flask
import redis
import time
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/process', methods=['GET'])
def process_messages():
    while True:
        messages = []

        # Извлекаем до 5 сообщений из очереди
        for _ in range(5):
            message = r.brpop('email_queue', timeout=2)
            if message:
                messages.append(message[1].decode('utf-8'))

        if messages:
            for msg in messages:
                print(f'Processing message: {msg}')
                time.sleep(5)  # Имитация времени обработки сообщения
        else:
            print('No messages to process. Waiting...')
            time.sleep(2)  # Ожидание перед следующей попыткой

def message_handler(message):
    data = json.loads(message['data'].decode('utf-8'))
    print(f"Consumer email: {data['email']}")
    print(f"Topic of message: {data['topic']}")
    print(f"Received message: {data['message']}")

p = r.pubsub()
p.subscribe(**{'my_channel': message_handler})  
p.run_in_thread(sleep_time=0.001)

if __name__ == '__main__':
    print("Consumer is ready to process messages.")
    app.run(port=5001)