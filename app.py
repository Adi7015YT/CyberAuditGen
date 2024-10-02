import os
from flask import Flask, request, jsonify, render_template
from google.cloud import aiplatform

app = Flask(__name__)

# Initialize Vertex AI SDK
aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT_ID'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    response = call_vertex_ai_agent(question)
    return jsonify(response)

def call_vertex_ai_agent(question):
    # Replace these variables with your Vertex AI model details
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    location = 'us-central1'  # or your specific location
    endpoint_id = 'YOUR_ENDPOINT_ID'  # replace with your endpoint ID

    # Initialize the endpoint client
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Set up the endpoint path
    endpoint = client.endpoint_path(
        project=project_id,
        location=location,
        endpoint=endpoint_id,
    )

    # Create the prediction request
    instances = [{"question": question}]
    parameters = {}

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    # Process the response
    predictions = response.predictions
    if predictions:
        return {"response": predictions[0]}
    else:
        return {"response": "No answer could be generated for the question."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
