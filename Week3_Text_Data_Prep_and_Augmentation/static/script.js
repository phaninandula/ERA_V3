document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const modelSelect = document.getElementById('modelSelect');
    const originalTextDiv = document.getElementById('original-text');
    const tokensDiv = document.getElementById('tokens');
    const tokenIdsDiv = document.getElementById('token-ids');
    const numTokensDiv = document.getElementById('num-tokens'); // New div for number of tokens
    const tokenBytesDiv = document.getElementById('token-bytes'); // New div for token bytes

    uploadButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        const selectedModel = modelSelect.value; // Get the selected model
        console.log('Selected Model:', selectedModel); // Log the selected model
        formData.append('modelSelect', selectedModel); // Append the selected model

        fetch('/tokenize', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            console.log('Tokenization Response:', data);
            originalTextDiv.textContent = fileInput.files[0].name; // Display file name
            tokensDiv.textContent = data.tokens.join(', ');
            tokenIdsDiv.textContent = data.token_ids.join(', ');
            numTokensDiv.textContent = data.num_tokens; // Display number of tokens
            tokenBytesDiv.textContent = data.token_bytes.join(', '); // Display token bytes
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the file: ' + error.message);
        });
    });
});
