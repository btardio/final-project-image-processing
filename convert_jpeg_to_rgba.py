import sys
from PIL import Image

def convert_jpeg_to_rgba(input_path):
    try:
        # 1. Open the image
        with Image.open(input_path) as img:
            # 2. Print width and height
            width, height = img.size
            print(f"Width: {width}, Height: {height}")

            # 3. Convert to RGBA
            rgba_img = img.convert("RGBA")

            # 4. Save as raw binary file
            output_path = input_path.rsplit('.', 1)[0] + ".raw"
            with open(output_path, "wb") as f:
                f.write(rgba_img.tobytes())
            
            print(f"Saved raw RGBA data to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename.jpg>")
    else:
        convert_jpeg_to_rgba(sys.argv[1])
