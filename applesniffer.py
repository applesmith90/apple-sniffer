import argparse
import requests
from PIL import Image
from io import BytesIO


def fetch_image_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AppleSniffer/1.0)"}
    response = requests.get(url, headers=headers)
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
    parser.add_argument("url", nargs="?", help="URL of the image to analyze")
    args = parser.parse_args()

    test_urls = [
        # Apple images
        "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f4/Honeycrisp.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Golden_Delicious_apples.jpg/500px-Golden_Delicious_apples.jpg",

        # Non-apple images
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Kiwifruit_cross_section.jpg/500px-Kiwifruit_cross_section.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Bananas.jpg/500px-Bananas.jpg", 
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Oranges_-_whole-halved-segment.jpg/960px-Oranges_-_whole-halved-segment.jpg"
    ]

    urls_to_check = [args.url] if args.url else test_urls

    for url in urls_to_check:
        print(f"\nChecking URL: {url}")
        try:
            image = fetch_image_from_url(url)
            if detect_apple(image):
                print("\U0001F34E Apple detected!")
            else:
                print("\u274C No apple found.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
