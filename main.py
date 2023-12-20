import random
from PIL import Image, ImageDraw  # Depends on the Pillow lib
import opensimplex as simplex
import matplotlib.pyplot as plt
import time
from os import makedirs

WIDTH = 1024
HEIGHT = 512
scale = .007
seed = None

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


def sumOctave(num_iterations, z, x, persistence, scale, low, high):
    maxAmp = 0
    amp = 1
    freq = scale
    noise = 0
    for i in range(0, num_iterations):
        noise += simplex.noise2(z * freq, x * freq) * amp
        maxAmp += amp
        amp *= persistence
        freq *= 2
    noise /= maxAmp
    noise = noise * (high - low) / 2 + (high + low) / 2

    return noise


@timer
def fillMatrix(landscale, height, width):
    seed = random.randint(1, 10000)
    simplex.seed(seed)
    for z in range(0, height):
        for x in range(0, width):
            landscale[z][x] = sumOctave(16, z, x, .5, scale, 0, 255)
    return landscale, seed


landscale = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
fillMatrix(landscale, HEIGHT, WIDTH)

plt.axis("off")
plt.imshow(landscale)
plt.show()

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
pixdata = img.load()
for z in range(0, HEIGHT):
    for x in range(0, WIDTH):
        if landscale[z][x] < 140:
            draw.point((x, z), (0, 0, 255))  # океан
        elif landscale[z][x] < 150:
            draw.point((x, z), (0, 191, 255))  # прибрежные воды
        elif landscale[z][x] < 155:
            draw.point((x, z), (244, 164, 96))  # берег
        elif landscale[z][x] < 170:
            draw.point((x, z), (34, 139, 34))  # низменность
        elif landscale[z][x] < 190:
            draw.point((x, z), (0, 128, 0))  # равнина
        elif landscale[z][x] < 200:
            draw.point((x, z), (0, 100, 0))  # предгорье
        elif landscale[z][x] < 235:
            draw.point((x, z), (128, 128, 128))  # горы
        else:
            draw.point((x, z), (255, 250, 250))  # снега
print(f'current seed if {seed}')
makedirs(f'outputs', exist_ok=True)
img.save(f"outputs/output{seed}.png")
