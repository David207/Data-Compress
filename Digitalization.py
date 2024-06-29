from PIL import Image

def digitalize_image(image_path, threshold=128):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    binary_image = image.point(lambda p: 255 if p > threshold else 0, '1')
    binary_image.show()

digitalize_image('path_to_your_image.jpg')
