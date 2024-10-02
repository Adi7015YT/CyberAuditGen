from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
  # This is a placeholder function
    response = call_vertex_ai_agent(question)
    return jsonify(response)

def call_vertex_ai_agent(question):
    # This is a placeholder function
    return {"response": f"Mock response for question: {question}"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
