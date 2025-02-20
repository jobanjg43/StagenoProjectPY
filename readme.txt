Image Steganography Tool

## Setup
1. Install required libraries: `pip install opencv-python cryptography`

## Usage
### Encoding (encoder.py)
1. Run `python encoder.py`
2. Provide the image path (e.g., `dog.jpg`)
3. Input the message or provide a text file (e.g., `msg.txt`)
4. Set a password
5. Encoded image is saved in the `encoded` folder

### Decoding (decoder.py)
1. Run `python decoder.py`
2. Provide the encoded image path
3. Enter the password
4. Hidden message is saved in the `output` folder

Enjoy hiding messages securely!
