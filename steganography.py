import sys
sys.stdout.reconfigure(encoding='utf-8')
import cv2
import numpy as np

def encode_image(image_path, secret_data):
    """Encodes secret text into an image using LSB steganography."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Error: The image '{image_path}' was not found.")

   
    binary_data = ''.join(format(ord(i), '08b') for i in secret_data) + '1111111111111110'
    data_index = 0
    binary_img = img.copy()
    
    for row in binary_img:
        for pixel in row:
            for channel in range(3):  
                if data_index < len(binary_data):
                    pixel[channel] = (pixel[channel] & 254) | int(binary_data[data_index])
                    data_index += 1
                else:
                    break

    cv2.imwrite("stego_image.png", binary_img)
    print("Data successfully encoded in stego_image.png")

def decode_image(stego_path):
    """Decodes hidden text from an image using LSB extraction."""
    img = cv2.imread(stego_path)
    if img is None:
        raise FileNotFoundError(f"Error: The image '{stego_path}' was not found.")

    binary_data = ""
    
    for row in img:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)

   
    binary_chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    try:
        extracted_data = ''.join(chr(int(b, 2)) for b in binary_chars)
        extracted_data = extracted_data.split("1111111111111110")[0] 
        return extracted_data.encode("latin-1").decode("utf-8", "ignore") 
    except UnicodeDecodeError:
        print("Warning: Some characters could not be decoded properly.")
        return extracted_data


encode_image("cover_image.png", "Hello, this is a hidden message! 🚀")
print("Decoded message:", decode_image("stego_image.png"))
