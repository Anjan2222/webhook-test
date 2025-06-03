from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received webhook:", data)
    return "Webhook received!", 200

if __name__ == "__main__":
    app.run(port=5000) 
