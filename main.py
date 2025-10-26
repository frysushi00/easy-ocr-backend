from flask import Flask, request, jsonify
import easyocr
import numpy as np
from PIL import Image
import io

# 1. Initialize Flask App
app = Flask(__name__)

# 2. Initialize EasyOCR Reader (ONLY RUN ONCE!)
# This step downloads and loads the models into memory, which is time-consuming.
# Add your required languages here (e.g., 'en' for English)
try:
    reader = easyocr.Reader(['en'], gpu=False) # Set gpu=True if you have a capable GPU
    print("EasyOCR models loaded successfully.")
except Exception as e:
    print(f"Error loading EasyOCR models: {e}")
    reader = None

@app.route('/ocr/read', methods=['POST'])
def read_image():
    if reader is None:
        return jsonify({"error": "EasyOCR reader not initialized"}), 500

    # Ensure an image file was uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    
    # Check if the filename is empty
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 3. Read the image data sent from the Kotlin app
        image_bytes = image_file.read()
        
        # EasyOCR can directly process bytes, or you can convert to a NumPy array:
        # image = Image.open(io.BytesIO(image_bytes))
        # image_np = np.array(image)

        # 4. Run EasyOCR on the image data (in bytes format)
        # detail=0 returns only the text string, no bounding boxes or confidence scores
        results = reader.readtext(image_bytes, detail=0) 
        
        # 5. Prepare the JSON response
        response = {
            "text": results,  # A list of the recognized text strings
            "status": "success"
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return jsonify({"error": "Error processing image for OCR"}), 500

# 6. Run the Server
if __name__ == '__main__':
    # Run on all public IPs (0.0.0.0) and use the same port (e.g., 5000)
    # as defined in your Kotlin Retrofit client.
    app.run(host='0.0.0.0', port=5000)