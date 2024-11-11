from flask import Flask, render_template, request, jsonify
import os
from image_processing import Image_Augmentation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Print debugging information
        print(f"Processing type: {request.form.get('type')}")
        print(f"Selected options: {list(request.form.keys())}")

        # Save uploaded file temporarily
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)

        # Process image
        processor = Image_Augmentation(file_path)
        results = {}
        
        process_type = request.form.get('type', 'processing')
        
        # Process based on type
        if process_type == 'processing':
            if 'resize' in request.form:
                results['resize'] = processor.resize_image()
            if 'grayscale' in request.form:
                results['grayscale'] = processor.convert_to_grayscale()
            if 'normalize' in request.form:
                results['normalize'] = processor.normalize_img()
            if 'center_crop' in request.form:
                results['center_crop'] = processor.center_crop()
                
        elif process_type == 'augmentation':
            if 'random_crop' in request.form:
                results['random_crop'] = processor.random_crop()
            if 'horizontal_flip' in request.form:
                results['horizontal_flip'] = processor.random_horizontal_flip()
            if 'rotation' in request.form:
                results['rotation'] = processor.random_rotation()
            if 'color_jitter' in request.form:
                results['color_jitter'] = processor.color_jitter()
            if 'random_erasing' in request.form:
                results['random_erasing'] = processor.random_erasing()
            if 'elastic_transform' in request.form:
                results['elastic_transform'] = processor.elastic_transform()
            if 'noise' in request.form:
                results['noise'] = processor.add_gaussian_noise()
                
        elif process_type == 'enhancement':
            if 'histogram_equalization' in request.form:
                results['histogram_equalization'] = processor.histogram_equalization()
            if 'adjust_brightness' in request.form:
                results['adjust_brightness'] = processor.adjust_brightness()
            if 'adjust_contrast' in request.form:
                results['adjust_contrast'] = processor.adjust_contrast()
            if 'adjust_saturation' in request.form:
                results['adjust_saturation'] = processor.adjust_saturation()
            if 'gaussian_blur' in request.form:
                results['gaussian_blur'] = processor.gaussian_blur()
            if 'solarize' in request.form:
                results['solarize'] = processor.solarize()
            if 'posterize' in request.form:
                results['posterize'] = processor.posterize()
            if 'adjust_sharpness' in request.form:
                results['adjust_sharpness'] = processor.adjust_sharpness()

        # Convert results to base64
        encoded_results = {k: processor.image_to_base64(v) for k, v in results.items()}
        
        # Print results before sending
        print(f"Number of results: {len(encoded_results)}")
        
        # Clean up
        os.remove(file_path)
        
        return jsonify(encoded_results)

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
