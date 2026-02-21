
import requests
import io
from PIL import Image, ImageDraw, ImageFont
import time

# --- CONFIGURATION ---
# STEP1: huggingface.co/login STEP2: Settings -> Access Tokens -> Create new token -> Read -> Token Name (Copy the Token)
MY_HF_TOKEN = "PASTE HERE" 
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {MY_HF_TOKEN}"}

def add_text_overlay(image, text):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    try:
        font = ImageFont.truetype("../fonts/BebasNeue-Regular.ttf", 40)
    except:
        font = ImageFont.load_default()

    # 2. Calculate text size to draw a background box
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    x = (width - text_w)/2
    y = height - text_h - 50

    padding = 10
    draw.rectangle(
        [x - padding, y - padding, x + text_w + padding, y + text_h + padding],
        fill = (0, 0, 0, 170)
    )

    draw.text((x, y), text, font=font, fill="white")
    return image

def generate_banner(prompt_text, headline_text, filename = "generated_ad.png"):
    print(f"Sending prompt to Cloud GPU: {prompt_text}")

    # --- THIS IS THE MISSING VARIABLE ---
    payload = {
        "inputs": prompt_text,
        "parameters":{
            "negative_prompt": "blurry, low resolution, low quality, cartoon, illustration, CGI, 3d render, text, watermark, logo, cluttered background, distorted, oversaturated, underexposed, overexposed",
            "width": 1024,
            "height": 1024
        }
    }

    # API Call with Retry Logic
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 503:
        time.sleep(5)
        response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.text}")
    
    # Load Image
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))

    # Apply the Overlay
    final_image = add_text_overlay(image, headline_text)

    final_image.save(filename)
    return filename