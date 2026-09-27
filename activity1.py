import requests
import io
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HF_TOKEN = "hf_YOUR_TOKEN_HERE" 
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_ai_image(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": "blurry, low quality, deformed, ugly",
            "guidance_scale": 8.0,
            "num_inference_steps": 40
        },
        "options": {"wait_for_model": True}
    }
    print(f"Generating: {prompt}...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.headers.get("Content-Type", "").startswith("image/"):
        return Image.open(io.BytesIO(response.content))
    else:
        print("Error:", response.json())
        return None
def apply_signature_look(image, style_name):
    """This is your themed enhancement pipeline"""
    print(f"Applying Signature Look: {style_name}")

    if style_name == "1": 
        image = ImageOps.colorize(ImageOps.grayscale(image), '#704214', '#C8A07A')
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        image = image.filter(ImageFilter.GaussianBlur(0.5))
        return image

    elif style_name == "2": 
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(2.0) 
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)
        return image

    elif style_name == "3": 
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.15)
        blurred = image.filter(ImageFilter.GaussianBlur(radius=5))
        image = Image.blend(image, blurred, 0.3)
        return image

    elif style_name == "4": 
        image = ImageOps.grayscale(image)
        image = ImageOps.colorize(image, black="#000000", white="#FFFFFF")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.8)
        image = image.filter(ImageFilter.SHARPEN)
        return image.convert("RGB")

    elif style_name == "5": 
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.4)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        return image

    else:
        return image

print("=== AI Image Stylist: Your Signature Look ===")

prompt = input("Enter your theme / prompt (e.g., 'a girl on a rainbow bridge'): ")
if not prompt:
    prompt = "a stylish girl on a colorful rainbow bridge, fashion photo, highly detailed"
base_image = generate_ai_image(prompt)
if base_image is None:
    exit()

base_image.save("01_base_image.png")
print("Saved 01_base_image.png")

print("\nChoose your Signature Look to enhance:")
print("1. Vintage Film - Warm, old movie look")
print("2. Cyberpunk Neon - Slay, saturated neon")
print("3. Soft Glow - Dreamy, bright, soft")
print("4. Cinematic B&W - Moody black and white")
print("5. Instagram Slay - Sharp, vibrant")

choice = input("Enter 1-5 (default 5): ") or "5"

final_image = apply_signature_look(base_image, choice)
final_image.save("02_signature_look.png")
print(f"✅ Final Image Saved as 02_signature_look.png")
final_image.show()
print("""
=== What to write in Report ===
1. Generation: Used Stable Diffusion v1-5 with prompt: '...'
2. Post-Processing Pipeline:
   - Used Pillow (PIL) library
   - Applied: Color Enhancement, Contrast, Brightness, Blur, Sharpen
   - Created 5 themed filters as 'Signature Looks'
3. Why Post-Processing? AI images are often dull/low contrast. Pillow enhances it to match your personal style.
""")