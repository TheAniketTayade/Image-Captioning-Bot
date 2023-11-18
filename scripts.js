document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const resultSection = document.getElementById('result-section');
    const uploadedImage = document.getElementById('uploaded-image');
    const generatedCaption = document.getElementById('generated-caption');
    const feedbackForm = document.getElementById('feedback-form');
    const feedbackSection = document.getElementById('feedback-section');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const imageUrl = document.getElementById('image_url').value;
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_url: imageUrl }),
        })
        .then(response => response.json())
        .then(data => {
            uploadedImage.src = imageUrl;
            generatedCaption.textContent = data.caption;
            resultSection.style.display = 'block';
            feedbackSection.style.display = 'block';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    feedbackForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const feedback = document.getElementById('feedback').value;
        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ feedback: feedback }),
        })
        .then(response => response.json())
        .then(data => {
            alert('Thank you for your feedback!');
            feedbackForm.reset();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
