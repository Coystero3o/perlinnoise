from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw

octaves = 4 # однородность шума (чем больше - тем менее однородный, своего рода зум)
amp = 10 # количество возможных координат у высоты
period = 700 # переодичность пиков (чем выше - тем шум более гладкий)
terrain_width = 1024 # размер поля
seed = random.randint(1,10000) # сид шума
print(seed)

# генерация шума
noise = PerlinNoise(octaves=octaves, seed=seed)
# генерация матрицы
landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

for position in range(terrain_width**2):
   # вычисление высоты y в координатах (x, z)
   x = floor(position / terrain_width)
   z = floor(position % terrain_width)
   y = floor(noise([x/period, z/period])*amp)
   landscale[int(x)][int(z)] = int(y)

image_file = "base.png"
img = Image.open(image_file).convert('RGB')
draw = ImageDraw.Draw(img)

pixdata = img.load()
height = 0

#http://flag.kremlin.ru/anthem/
for position in range(0, terrain_width//3):
   x = floor(position / terrain_width)
   z = floor(position % terrain_width)
   draw.point((int(x), int(z)), (255,255,255))
for position in range(terrain_width//3, terrain_width//3*2):
   x = floor(position / terrain_width)
   z = floor(position % terrain_width)
   draw.point((int(x), int(z)), (0,0,255))
for position in range(terrain_width//3*2, terrain_width):
   x = floor(position / terrain_width)
   z = floor(position % terrain_width)
   draw.point((int(x), int(z)), (255,0,0))

img.save(f"outputs/output{seed}.png")

plt.axis("off")
plt.imshow(landscale)
plt.savefig(f'noises/pnoise{seed}.png', pad_inches=0, bbox_inches="tight")
plt.show()
