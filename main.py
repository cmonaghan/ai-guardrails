from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
import boto3
import os
import json


load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

# Initialize AWS Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
)

bedrock_blah = boto3.client(
    'bedrock',
    # region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    # aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    # aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/api/guardrail', methods=['POST'])
def guardrail():
    try:
        # Get the prompt from the request body
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Make a request to AWS Bedrock
        response = bedrock_client.apply_guardrail(
            guardrailIdentifier=os.getenv('GUARDRAIL_IDENTIFIER'),
            guardrailVersion=os.getenv('GUARDRAIL_VERSION'),
            source='INPUT',
            content=[
                {
                    'text': {
                        'text': prompt,
                        'qualifiers': [
                            # 'grounding_source',
                            # 'query',
                            'guard_content',
                        ]
                    },
                },
            ]
        )

        return jsonify({
            # allowlist specific elements to pass along to the browser
            "action": response['action'],
            "assessments": response['assessments'],
            "outputs": response['outputs'],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
