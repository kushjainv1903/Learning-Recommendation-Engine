import os
from PIL import Image

# The paths to your specific diagrams
target_images = [
    "Docs/diagrams/request lifecycle.png",
    "Docs/diagrams/Project Structure.png"
]

for img_path in target_images:
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            # Calculate new size (e.g., downsizing by exactly 50%)
            # This maintains the exact aspect ratio
            new_width = int(img.width * 0.5)
            new_height = int(img.height * 0.5)
            
            # LANCZOS resampling prevents the text and lines from becoming blurry
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save it back to overwrite the blurry file
            resized_img.save(img_path, optimize=True)
            print(f"Successfully optimized and resized: {img_path}")
    else:
        print(f"File not found: {img_path}")