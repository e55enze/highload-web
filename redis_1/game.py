from flask import Flask, request, jsonify
import redis
import sys

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushall()

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    player_name = data['name']
    score = data['score']

    summary_score = 0
    player_stats = []
    leaderboard = r.zrevrange('leaderboard', 0, -1, withscores=True)
    for player in leaderboard:
        if player[0].decode("utf-8") == player_name:
            print(player_name, player[1])
            player_stats.append(player_name)
            player_stats.append(score)
            flag = 1
            break
    if len(player_stats) > 0:
        summary_score = r.zincrby("leaderboard",  player_stats[1], player_stats[0])
        print('summary: ',summary_score)
    else:
        r.zadd('leaderboard', {player_name: score})
    
    return {'message': 'Score added successfully'}, 200

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    # Получение топ-10 игроков из Sorted Set
    leaderboard = r.zrevrange('leaderboard', 0, -1, withscores=True)
    print(leaderboard[0], type(leaderboard[0]))
    json_data = [{'name': name.decode('utf-8'), 'score': score} for name, score in leaderboard]
    return jsonify(json_data)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port, debug=True)