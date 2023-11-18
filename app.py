from flask import Flask, request, jsonify, render_template
from model import ImageCaptioningModel
from error_handler import handle_errors
from feedback import handle_feedback

app = Flask(__name__)
model = ImageCaptioningModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@handle_errors
def upload_image():
    image_url = request.form.get('image_url')
    if not image_url:
        return jsonify({'error': 'No image URL provided'}), 400

    caption = model.generate_caption(image_url)
    if not caption:
        return jsonify({'error': 'Failed to generate a caption'}), 500

    return jsonify({'caption': caption})

@app.route('/feedback', methods=['POST'])
@handle_errors
def feedback():
    feedback_data = request.get_json()
    handle_feedback(feedback_data)

    return jsonify({'message': 'Feedback received'}), 200

if __name__ == '__main__':
    app.run(debug=True)
