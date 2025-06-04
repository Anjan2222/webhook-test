from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['webhook_db']
events = db['events']

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event', None)
    payload = request.json

    # Extract and transform event data
    if event_type == "push":
        event_data = {
            "action_type": "PUSH",
            "author": payload["pusher"]["name"],
            "to_branch": payload["ref"].split('/')[-1],
            "timestamp": datetime.utcnow(),
            "raw": payload
        }
    elif event_type == "pull_request":
        action = payload.get("action")
        if action == "opened":
            event_data = {
                "action_type": "PULL_REQUEST",
                "author": payload["pull_request"]["user"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow(),
                "raw": payload
            }
        elif action == "closed" and payload["pull_request"]["merged"]:
            event_data = {
                "action_type": "MERGE",
                "author": payload["pull_request"]["user"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow(),
                "raw": payload
            }
        else:
            return jsonify({"status": "ignored"}), 200
    else:
        return jsonify({"status": "ignored"}), 200

    events.insert_one(event_data)
    return jsonify({"status": "success"}), 201

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    # Return the latest 20 events sorted by timestamp descending
    data = list(events.find().sort("timestamp", -1).limit(20))
    for d in data:
        d['_id'] = str(d['_id'])
        d['timestamp'] = d['timestamp'].strftime('%d %b %Y - %I:%M %p UTC')
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)