from PIL import Image
import numpy as np

# Открываем изображение
image = Image.open("back_off.png")

# Конвертируем в RGB (если нужно) и в массив NumPy
image_rgb = image.convert("RGB")
pixel_array = np.array(image_rgb)


r, g, b = [255, 255, 255]
color4 = [r, g, b]
color3 = [r-38, g-38, b-38]
color2 = [r-50, g-50, b-50]
color1 = [r-63, g-63, b-63]
colors = [color1, color2, color3, color4]
for color in colors:
    for i in range(len(color)):
        if color[i]<0:
            color[i]=0
        elif color[i]>255:
            color[i]=255
print(colors)
map = []

for x in range(pixel_array.shape[0]):
    string = []
    for y in range(pixel_array.shape[1]):
        r, g, b, _ = image.getpixel((y,x))
        print(r,g,b)
        if [r, g, b] in colors:
            string.append(colors.index([r, g, b]) + 1)
        else:
            string.append(0)
    map.append(string)
print(map)
