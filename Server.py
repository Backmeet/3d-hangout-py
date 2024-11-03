import os
import threading
import time
from flask import Flask, jsonify
from engine import Renderer3D

r = Renderer3D((900, 600))

app = Flask(__name__)
app.secret_key = 'some_secret_key'

players = []

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

def getPlayerNames(lis):
    return [info["name"] for info in lis]

@app.route('/add-player/<name>', methods=['POST'])
def addPlayer(name):
    players.append({
        "name": name,
        "x": 0,
        "y": 0,
        "z": 0,
        "colour": [(255, 255, 255) for _ in range(6)],
        "orientation": [0, 0, 0]
    })
    return "Player added", 200

@app.route('/remove-player/<name>', methods=['DELETE'])
def removePlayer(name):
    if name in getPlayerNames(players):
        players[:] = [player for player in players if player["name"] != name]
        return "Player removed", 200
    return "Player not found", 404

@app.route('/change-value/<name>/<value_name>/<new_value>', methods=['POST'])
def changeValue(name, value_name, new_value):
    if name in getPlayerNames(players):
        for info in players:
            if info["name"] == name:
                try:
                    if value_name in ["x", "y", "z"]:
                        info[value_name] = float(new_value)
                    elif value_name == "orientation":
                        info[value_name] = [float(v) for v in new_value.split(",")]
                    else:
                        info[value_name] = new_value
                except Exception as e:
                    return str(e), 400
        return "Value changed", 200
    return "Player not found", 404

@app.route('/get-scene/<in_respect_to>', methods=['GET'])
def getScene(in_respect_to):
    scene = []
    for player in players:
        if player['name'] == in_respect_to:
            continue
        scene.extend(r.generate_cube(
            (player["x"], player["y"], player["z"]),
            player["colour"],
            100, 100, 100, 0
        ))
    scene.extend(r.generate_cube((0, 0, 0), colors))
    return jsonify({"scene": scene})

if __name__ == '__main__':
    app.run(port=8080)
