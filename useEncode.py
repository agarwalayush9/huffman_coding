from flask import Flask, render_template, request
from encode import HuffmanCoding
import os

app = Flask(__name__)

def get_file_size(file_path):
    return os.path.getsize(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error_message="No file part")

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error_message="No selected file")

        # Save the uploaded file
        upload_path = "uploads/" + file.filename
        file.save(upload_path)

        # Calculate file sizes
        original_size = get_file_size(upload_path)

        # Perform compression and decompression
        h = HuffmanCoding(upload_path)
        compressed_path = h.compress()
        decompressed_path = h.decompress(compressed_path)

        compressed_size = get_file_size(compressed_path)
        decompressed_size = get_file_size(decompressed_path)

        # Provide the file sizes and paths to the frontend
        return render_template('index.html', 
                               original_size=original_size,
                               compressed_path=compressed_path,
                               compressed_size=compressed_size,
                               decompressed_path=decompressed_path,
                               decompressed_size=decompressed_size)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
