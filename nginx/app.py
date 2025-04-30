from flask import Flask, jsonify
import sys

app = Flask(__name__)

counter = 0

@app.route('/counter', methods=['GET'])
def get_counter():
    global counter
    counter += 1
    return jsonify(counter=counter)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port)