from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.wrappers import response
from chat import get_response

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# --------------------------------------  Chatbot  --------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        text = request.get_json().get('message')
        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)

# -------------------------------------- app.run --------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port='5001')