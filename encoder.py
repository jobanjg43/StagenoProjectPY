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

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def hide_message_in_image(image_path, message, password, output_path):
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read image file")
        
        # Encrypt the message
        key = generate_key(password)
        encrypted_message = encrypt_message(message, key)
        
        # Convert encrypted message to binary
        binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
        
        # Hide the message in the image
        data_index = 0
        for row in image:
            for pixel in row:
                for channel in range(3):
                    if data_index < len(binary_message):
                        pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                    else:
                        break
        
        # Save the output image
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_image_path = os.path.join(output_path, "encoded_image.png")
        cv2.imwrite(output_image_path, image)
        logging.info(f"Message hidden in image and saved as {output_image_path}")
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    image_path = input("Enter the path to the image file: ")
    message_option = input("Enter '1' to input the message manually or '2' to provide a text file: ")
    if message_option == '1':
        message = input("Enter the message: ")
    elif message_option == '2':
        text_file_path = input("Enter the path to the text file: ")
        with open(text_file_path, 'r') as file:
            message = file.read()
    else:
        logging.error("Invalid option")
        return
    password = input("Set a password for decoding: ")
    hide_message_in_image(image_path, message, password, "encoded")

if __name__ == "__main__":
    main()
