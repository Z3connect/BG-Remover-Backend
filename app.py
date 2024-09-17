from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img_byte_arr = file.read()
        result = remove(img_byte_arr)
        
        processed_image = Image.open(io.BytesIO(result))

        img_io = io.BytesIO()
        processed_image.save(img_io, format='PNG') 
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='processed_image.png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)