from flask import Flask, render_template, request, jsonify
import os
from tokenization import TokenizationHandler

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the tokenization handler
tokenization_handler = TokenizationHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tokenize', methods=['POST'])
def tokenize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    
    model_name = request.form.get('modelSelect')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    try:
        # Read file content

        text = file.read().decode('utf-8')
        #print(f"Text : {text}")
        
        # Use the tokenization handler to tokenize the text
        tokens, token_ids, token_bytes, num_tokens = tokenization_handler.tokenize(text, model_name)

        return jsonify({
            'original_text': print(text),
            'tokens': tokens,
            'token_ids': token_ids,
            'token_bytes': token_bytes,
            'num_tokens': num_tokens
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
