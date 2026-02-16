import argparse
import numpy as np
from PIL import Image
import sys

def convert_rgb_to_image(filename, width, height):
    # Calculate the total number of bytes expected for the target dimensions (3 channels for RGB)
    expected_bytes = width * height * 3
    
    try:
        # Read the raw data as a byte array
        with open(filename, 'rb') as f:
            raw_data = f.read()
            data_bytes = len(raw_data)
        
        # Adjust for inexact data size: crop if too large, pad if too small
        if data_bytes > expected_bytes:
            print(f"Warning: File size ({data_bytes} bytes) is larger than expected ({expected_bytes} bytes). Cropping data.")
            raw_data = raw_data[:expected_bytes]
        elif data_bytes < expected_bytes:
            print(f"Warning: File size ({data_bytes} bytes) is smaller than expected ({expected_bytes} bytes). Padding with zeros.")
            # Pad with zeros to reach the expected size
            raw_data += b'\x00' * (expected_bytes - data_bytes)
        
        # Convert the byte data to a NumPy array and reshape it to the desired dimensions
        # The data type is uint8 (unsigned 8-bit integer)
        image_array = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width, 3))
        
        # Create a PIL Image object from the NumPy array
        image = Image.fromarray(image_array, 'RGB')
        
        # Define the output filename with a new extension (e.g., .png or .jpg)
        output_filename = filename + '.png' 
        image.save(output_filename) # The save() method automatically identifies the format
        print(f"Successfully saved image to {output_filename}")

    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error reshaping image data: {e}. Check that the width and height are correct for the amount of data in the file.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a raw RGB file to a viewable image file.")
    parser.add_argument("filename", type=str, help="The path to the raw RGB input file.")
    parser.add_argument("width", type=int, help="The width of the image.")
    parser.add_argument("height", type=int, help="The height of the image.")
    
    args = parser.parse_args()
    
    convert_rgb_to_image(args.filename, args.width, args.height)

