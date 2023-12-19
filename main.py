from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
import time

def timer(func):
    def wrapper(landscale, terrain_width, height=None):
        tb = time.time()
        if height != None:
            func(landscale, terrain_width, height)
        else:
            func(landscale, terrain_width)
        te = time.time() - tb
        print(f"It took {te} seconds to generate")

    return wrapper

@timer
def fillMatrix(landscale, terrain_width):
    for position in range(terrain_width ** 2):
        # вычисление высоты y в координатах (x, z)
        x = floor(position / terrain_width)
        z = floor(position % terrain_width)
        y = floor(noise([x / period, z / period]) * amp)
        landscale[int(x)][int(z)] = int(y)
    return landscale

@timer
def fillPicture(landscale, terrain_width, height):
    for position in range(terrain_width ** 2):
        x = floor(position / terrain_width)
        z = floor(position % terrain_width)
        if landscale[int(x)][int(z)] < height:
            draw.point((int(x), int(z)), (0, 149, 182))  # 85, 72, 189
        elif landscale[int(x)][int(z)] == height:
            draw.point((int(x), int(z)), (252, 186, 3))
        elif landscale[int(x)][int(z)] > height:
            draw.point((int(x), int(z)), (19, 112, 21))


octaves = 4  # однородность шума (чем больше - тем менее однородный, своего рода зум)
amp = 50  # количество возможных координат у высоты
period = 700  # переодичность пиков (чем выше - тем шум более гладкий)
terrain_width = 1024  # размер поля
seed = random.randint(1, 10000)  # сид шума
image_file = "base.png" # Базовое пустое изображение
img = Image.open(image_file).convert('RGB')
draw = ImageDraw.Draw(img)
pixdata = img.load()
print(seed)

# генерация шума
noise = PerlinNoise(octaves=octaves, seed=seed)
# генерация матрицы и ее заполнение
landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]
fillMatrix(landscale, terrain_width)
# заполнение изображения на основе значений в матрице
fillPicture(landscale, terrain_width, height=0)

img.save(f"outputs/output{seed}.png")

plt.axis("off")
plt.imshow(landscale)
plt.savefig(f'noises/pnoise{seed}.png', pad_inches=0, bbox_inches="tight")
plt.show()
