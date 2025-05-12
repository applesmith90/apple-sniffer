import argparse
import requests
from PIL import Image
from io import BytesIO


def fetch_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def detect_apple(image: Image.Image) -> bool:
    # Placeholder heuristic: Check for red pixels as a naive apple indicator
    red_threshold = 100
    red_pixel_count = 0

    image = image.convert('RGB')
    for pixel in image.getdata():
        r, g, b = pixel
        if r > red_threshold and g < 80 and b < 80:
            red_pixel_count += 1

    return red_pixel_count > 500  # Arbitrary threshold for demo purposes


def main():
    parser = argparse.ArgumentParser(description="Detect if an apple exists in an image from a URL.")
    parser.add_argument("url", help="URL of the image to analyze")
    args = parser.parse_args()

    try:
        image = fetch_image_from_url(args.url)
        if detect_apple(image):
            print("\U0001F34E Apple detected!")
        else:
            print("\u274C No apple found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
