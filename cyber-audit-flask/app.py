import os
from flask import Flask, request, jsonify, render_template
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient

app = Flask(__name__)

# Access the environment variables
google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
alloydb_connection_string = os.getenv('ALLOYDB_CONNECTION_STRING')

# Initialize Vertex AI SDK
aiplatform.init(project=google_cloud_project)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    response = call_vertex_ai_agent(question)
    return jsonify(response)

def call_vertex_ai_agent(question):
    project_id = google_cloud_project
    location = 'us-central1'  # Modify this if your model is deployed in a different region
    model_id = "text-bison@001"  # Specify your model's ID or name

    # Initialize the Prediction Service Client
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    prediction_client = PredictionServiceClient(client_options=client_options)

    # Specify the model resource name
    model_resource = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    # Create the prediction request
    instances = [{"content": question}]  # Make sure this matches your model's input format
    parameters = {}  # Adjust parameters if your model requires specific parameters

    # Make the prediction
    response = prediction_client.predict(
        endpoint=model_resource, instances=instances, parameters=parameters
    )

    # Process the response
    predictions = response.predictions
    if predictions:
        return {"response": predictions[0].get('generated_text', 'No text generated')}  # Adjust based on the output format
    else:
        return {"response": "No answer could be generated for the question."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
