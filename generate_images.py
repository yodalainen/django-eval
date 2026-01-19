from PIL import Image
import os

def generate_placeholder_images():
    path = 'accounts/static/accounts/images'
    os.makedirs(path, exist_ok=True)

    # JPEG
    img_jpg = Image.new('RGB', (100, 100), color=(255, 0, 0))
    img_jpg.save(os.path.join(path, 'image.jpg'), 'JPEG')

    # PNG
    img_png = Image.new('RGBA', (100, 100), color=(0, 255, 0, 255))
    img_png.save(os.path.join(path, 'image.png'), 'PNG')

    # GIF
    img_gif = Image.new('RGB', (100, 100), color=(0, 0, 255))
    img_gif.save(os.path.join(path, 'image.gif'), 'GIF')

    # WebP
    img_webp = Image.new('RGB', (100, 100), color=(255, 255, 0))
    img_webp.save(os.path.join(path, 'image.webp'), 'WebP')

if __name__ == "__main__":
    generate_placeholder_images()
