from PIL import Image

def floyd_steinberg_dithering(image_path):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            old_pixel = pixels[x, y]
            new_pixel = 255 if old_pixel > 128 else 0
            pixels[x, y] = new_pixel
            quant_error = old_pixel - new_pixel

            if x + 1 < image.width:
                pixels[x + 1, y] = int(pixels[x + 1, y] + quant_error * 7 / 16)
            if x - 1 >= 0 and y + 1 < image.height:
                pixels[x - 1, y + 1] = int(pixels[x - 1, y + 1] + quant_error * 3 / 16)
            if y + 1 < image.height:
                pixels[x, y + 1] = int(pixels[x, y + 1] + quant_error * 5 / 16)
            if x + 1 < image.width and y + 1 < image.height:
                pixels[x + 1, y + 1] = int(pixels[x + 1, y + 1] + quant_error * 1 / 16)

    image.show()


floyd_steinberg_dithering('D:\photo\FB_IMG_1698338467550.jpg')
