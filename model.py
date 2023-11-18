import torch
import clip
from PIL import Image
import requests
from io import BytesIO

class ImageCaptioningModel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.transform = clip.load("ViT-B/32", device=self.device)

    def generate_caption(self, image_url):
        try:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            image = self.transform(img).unsqueeze(0).to(self.device)

            # Generate a set of candidate captions
            # You might want to increase the number of captions for better results
            candidate_captions = ["A photo of a cat", "A photo of a dog", "A photo of a bird", 
                                  "A photo of a person", "A photo of a landscape"]
            text = clip.tokenize(candidate_captions).to(self.device)

            # Calculate the similarity between the image and each candidate caption
            with torch.no_grad():
                image_features = self.model.encode_image(image)
                text_features = self.model.encode_text(text)

            # Take the caption that is most similar to the image
            similarities = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            best_caption_index = similarities.argmax(dim=-1).item()

            return candidate_captions[best_caption_index]
        except Exception as e:
            print(f"Error in generating caption: {e}")
            return None
