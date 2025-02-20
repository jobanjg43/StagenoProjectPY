import cv2
import numpy as np
from cryptography.fernet import Fernet
import base64
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key(password):
    return base64.urlsafe_b64encode(password.ljust(32).encode('utf-8'))

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()

def extract_message_from_image(image_path, password):
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read image file")
        
        # Extract binary message from the image
        binary_message = ''
        for row in image:
            for pixel in row:
                for channel in range(3):
                    binary_message += format(pixel[channel], '08b')[-1]
        
        # Convert binary message to bytes
        encrypted_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')
        
        # Decrypt the message
        key = generate_key(password)
        message = decrypt_message(encrypted_message, key)
        
        # Save the output message
        output_message_path = "output/hidden_message.txt"
        if not os.path.exists("output"):
            os.makedirs("output")
        with open(output_message_path, 'w') as file:
            file.write(message)
        logging.info(f"Hidden message extracted and saved as {output_message_path}")
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    image_path = input("Enter the path to the encoded image file: ")
    password = input("Enter the password for decoding: ")
    extract_message_from_image(image_path, password)

if __name__ == "__main__":
    main()
