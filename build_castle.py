"""Dense glyph-rendered castle courtyard, inspired by the supplied video.
Run with Python and Pillow; writes a self-hosted autoplaying README GIF.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parent
W, H, N = 1200, 920, 96
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 9)
GRASS_FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
rng = random.Random(63)
BG = (7, 9, 19)
stone = Image.new('RGB', (W, H), BG)
s = ImageDraw.Draw(stone)

# Elevated view: a deep courtyard, receding side walls, and solid stone towers.
s.polygon([(217, 414), (775, 301), (1063, 548), (559, 706)], fill=(19, 30, 31))
s.polygon([(202, 224), (242, 204), (242, 534), (202, 557)], fill=(53, 79, 75))
s.polygon([(242, 204), (423, 292), (423, 599), (242, 534)], fill=(39, 58, 59))
s.polygon([(740, 236), (788, 219), (1090, 418), (1048, 440)], fill=(117, 142, 132))
s.polygon([(740, 236), (1048, 440), (1048, 589), (740, 389)], fill=(53, 76, 74))
s.polygon([(1048, 440), (1090, 418), (1090, 567), (1048, 589)], fill=(35, 51, 57))

windows = []
def tower(x, y, width, height):
    depth = int(width * .45)
    # Main face, side face, and the crenellated upper platform.
    s.rectangle((x, y, x + width, y + height), fill=(78, 102, 99))
    s.polygon([(x + width, y), (x + width + depth, y - depth // 2), (x + width + depth, y + height - depth // 2), (x + width, y + height)], fill=(39, 57, 65))
    s.polygon([(x, y), (x + depth, y - depth // 2), (x + width + depth, y - depth // 2), (x + width, y)], fill=(125, 145, 134))
    for dx in range(0, width, 22):
        s.rectangle((x + dx, y - 20, x + dx + 12, y + 4), fill=(116, 135, 129))
    for wy in range(y + 42, y + height - 22, 61):
        for wx in range(x + 18, x + width - 8, 43):
            s.rectangle((wx, wy, wx + 10, wy + 24), fill=BG)
            s.pieslice((wx, wy - 9, wx + 10, wy + 9), 180, 360, fill=BG)
            windows.append((wx, wy))
    # Weathered joints and occasional missing stones are coherent, not noise.
    for wy in range(y + 12, y + height, 18):
        s.line((x, wy, x + width, wy), fill=(55, 78, 77))
        for wx in range(x + ((wy // 18) % 2) * 13, x + width, 26):
            s.line((wx, wy, wx, min(wy + 17, y + height)), fill=(55, 76, 75))

# Distant keep, chapel and flanking towers.
tower(533, 178, 160, 253)
tower(560, 103, 72, 220)
s.polygon([(540, 103), (597, 36), (650, 103)], fill=(89, 110, 111))
s.line((597, 17, 597, 45), fill=(119, 133, 130), width=3)
tower(737, 203, 93, 242)
tower(179, 238, 112, 324)
tower(932, 364, 105, 218)
# Gatehouse forms the far courtyard wall, with an open arched entrance.
s.rectangle((336, 294, 699, 462), fill=(73, 94, 89))
for x in range(336, 698, 25):
    s.rectangle((x, 274, x + 13, 299), fill=(124, 142, 127))
s.rectangle((450, 355, 541, 490), fill=BG)
s.pieslice((450, 305, 541, 407), 180, 360, fill=BG)
s.arc((441, 297, 550, 410), 180, 360, fill=(141, 145, 124), width=9)
s.line((441, 354, 441, 465), fill=(114, 122, 107), width=9)
s.line((550, 354, 550, 465), fill=(69, 89, 83), width=9)
for x in range(459, 537, 13):
    s.line((x, 325, x, 352), fill=(90, 98, 91), width=2)
# Stairway, chapel buttresses, broken columns and a small well.
for j in range(10):
    yy = 468 + j * 8
    s.polygon([(438 - j * 4, yy), (548 + j * 5, yy), (557 + j * 5, yy + 5), (441 - j * 4, yy + 5)], fill=(43 + j * 2, 61 + j * 2, 62 + j))
for x in [358, 590, 668]:
    s.polygon([(x, 329), (x + 11, 329), (x + 25, 466), (x - 9, 466)], fill=(94, 113, 101))
s.ellipse((723, 505, 787, 540), fill=(89, 110, 105))
s.rectangle((723, 519, 787, 550), fill=(53, 77, 73))
s.ellipse((728, 508, 782, 532), fill=BG)
for x, y in [(275, 593), (1020, 665), (908, 749), (188, 693)]:
    s.rectangle((x, y, x + 23, y + 41), fill=(49, 65, 64))
    s.ellipse((x, y - 10, x + 23, y + 10), fill=(71, 86, 77))
# Thorny shrubs are volumes filled with letters, as in the reference.
for x, y, radius in [(124, 385, 63), (1113, 508, 66), (989, 799, 85), (160, 819, 91), (338, 639, 42), (855, 448, 42)]:
    for _ in range(22):
        xx, yy = x + rng.randrange(-radius, radius), y + rng.randrange(-radius // 2, radius // 2)
        rr = rng.randrange(13, 32)
        s.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=rng.choice([(48, 90, 72), (62, 107, 83), (35, 65, 58)]))

base = Image.new('RGB', (W, H), BG)
b = ImageDraw.Draw(base)
glyphs = ' .,:;iIl!+ox%#@MW'
# Dense five-pixel grid: each letter carries the light of the solid geometry.
for y in range(22, 890, 8):
    for x in range(20, W - 20, 5):
        c = stone.getpixel((x, y))
        if c == BG:
            continue
        light = max(c)
        g = glyphs[min(len(glyphs) - 1, int(light / 145 * (len(glyphs) - 1)))]
        if rng.random() < .65:
            g = rng.choice('Q0opdbw#%&@MNH=+:')
        shade = .66 + rng.random() * .48
        b.text((x, y), g, font=FONT, fill=tuple(min(255, int(v * shade)) for v in c))
# Courtyard cobbles fade into dense grass along the approach.
for y in range(475, 898, 9):
    for x in range(55, 1150, 7):
        if stone.getpixel((x, y)) != BG:
            continue
        path = abs(x - (501 + (y - 485) * .30)) < 47 + (y - 485) * .10
        if path:
            b.text((x, y), rng.choice('.:=o'), font=FONT, fill=rng.choice([(31, 43, 48), (46, 61, 63), (58, 71, 68)]))

# Sprite silhouettes become shaded glyph figures rather than stick drawings.
def sprite(kind, pose):
    shape = Image.new('RGB', (42, 77), BG)
    q = ImageDraw.Draw(shape)
    if kind == 'knight':
        q.polygon([(17, 3), (25, 3), (29, 10), (29, 20), (14, 20), (12, 11)], fill=(143, 163, 154))
        q.rectangle((14, 12, 28, 15), fill=(31, 43, 48))
        q.polygon([(11, 24), (30, 24), (33, 42), (28, 51), (13, 51), (8, 38)], fill=(129, 153, 141))
        q.rectangle((3, 25, 10, 43), fill=(87, 114, 112))
        q.polygon([(30, 27), (39, 29), (38, 48), (32, 53), (28, 42)], fill=(111, 130, 117))
        q.line((2, 26, 2, 60), fill=(162, 177, 164), width=2)
    else:
        q.polygon([(20, 1), (31, 21), (9, 21)], fill=(101, 141, 143) if kind == 'mage' else (126, 131, 97))
        q.rectangle((16, 18, 26, 28), fill=(140, 153, 134))
        q.polygon([(13, 29), (29, 29), (35, 56), (6, 56)], fill=(61, 105, 116) if kind == 'mage' else (97, 113, 88))
        q.line((38, 18, 38, 70), fill=(119, 138, 116), width=2)
    stride = [-4, 0, 4, 0][pose]
    q.line((15, 49, 13 + stride, 72), fill=(95, 115, 109), width=6)
    q.line((26, 49, 28 - stride, 72), fill=(113, 134, 120), width=6)
    out = Image.new('RGBA', shape.size)
    od = ImageDraw.Draw(out)
    for y in range(0, 76, 4):
        for x in range(0, 42, 3):
            c = shape.getpixel((x, y))
            if c != BG:
                od.text((x, y), '#%+=@'[int((x + y) / 3) % 5], font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 6), fill=(*tuple(min(230, int(v * 1.22)) for v in c), 255))
    return out
sprites = {(kind, pose): sprite(kind, pose) for kind in ['knight', 'mage', 'wanderer'] for pose in range(4)}
grass = []
for _ in range(15000):
    x, y = rng.randrange(34, 1170), rng.randrange(477, 894)
    if stone.getpixel((x, y)) != BG:
        continue
    path = abs(x - (501 + (y - 485) * .30)) < 51 + (y - 485) * .12
    if not path:
        grass.append((x, y, rng.random() * math.tau, rng.choice([(41, 89, 68), (56, 112, 79), (68, 124, 91), (29, 69, 60)]), rng.random() < .075))
embers = [(rng.random(), rng.randrange(-24, 25)) for _ in range(30)]
frames = []
namefont = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 22)
for f in range(N):
    phase = f / N * math.tau
    out = base.copy().convert('RGBA')
    d = ImageDraw.Draw(out)
    # Roaming courtyard inhabitants and two knights crossing the arch.
    walkers = [
        ('knight', 812 + 95 * math.sin(phase), 604, 1.1),
        ('wanderer', 363 + 76 * math.sin(phase + 2), 716, 1.4),
        ('mage', 885 + 57 * math.sin(phase + 4), 766, 1.4),
        ('knight', 661 + 54 * math.sin(phase + 3), 415, .60),
    ]
    for offset, side in [(0, -1), (math.pi, 1)]:
        depth = (1 - math.cos(phase + offset)) / 2
        if depth > .035:
            walkers.append(('knight', 494 + side * depth * 73, 367 + depth * 263, .55 + depth * .75))
    for x, y, wave, color, flower in grass:
        bend = math.sin(phase * 2 + wave + x / 85) + .35 * math.sin(phase * 3 + y / 70)
        near = min((math.hypot(x - wx, (y - wy) * .75) for _, wx, wy, _ in walkers), default=100)
        if near < 34:
            bend += (34 - near) / 14
        d.text((x + bend * 1.3, y), '/' if bend > .45 else ('\\' if bend < -.45 else '|'), font=GRASS_FONT, fill=color)
        if flower:
            d.text((x, y - 2), 'o' if wave > 3 else '*', font=FONT, fill=(128, 155, 138))
    for kind, x, y, size in sorted(walkers, key=lambda w: w[2]):
        actor = sprites[kind, (f // 3) % 4]
        actor = actor.resize((int(actor.width * size), int(actor.height * size)), Image.Resampling.NEAREST)
        # Soft ground shadow anchors the body to the environment.
        d.ellipse((x - 14 * size, y - 3, x + 16 * size, y + 4), fill=(8, 13, 19))
        out.alpha_composite(actor, (int(x - actor.width / 2), int(y - actor.height)))
    d = ImageDraw.Draw(out)
    for number, (x, y) in enumerate(windows):
        light = .72 + .2 * math.sin(phase * 5 + number)
        d.text((x, y + 7), ':', font=FONT, fill=(int(163 * light), int(120 * light), 66))
    for x, y in [(439, 392), (552, 392), (674, 705)]:
        d.text((x, y), '*', font=FONT, fill=(231, int(153 + 23 * math.sin(phase * 8 + x)), 72))
    # Bonfire, sword and rising embers.
    d.text((666, 680), '|', font=GRASS_FONT, fill=(160, 176, 165))
    d.text((660, 690), '-+-', font=FONT, fill=(160, 176, 165))
    d.text((657, 721), '/###\\', font=FONT, fill=(114, 91, 66))
    for offset, spread in embers:
        rise = (f / N * 3 + offset) % 1
        d.text((672 + spread * rise, 724 - rise * 65), '.+*'[int(offset * 3)], font=FONT, fill=(int(221 - rise * 80), int(158 - rise * 87), 68))
    # Ground-level mist trails, kept low contrast over the dense text.
    for j in range(65):
        x = 200 + j * 13 + 17 * math.sin(phase + j / 8)
        y = 577 + 11 * math.sin(j / 6)
        d.text((x, y), '~', font=FONT, fill=(42, 60, 66))
    # Only the owner's name is displayed, without video overlay captions.
    d.rounded_rectangle((28, 19, 390, 65), radius=6, fill=(*BG, 240))
    d.text((44, 31), 'KUSHAL M ANVEKAR', font=namefont, fill=(190, 204, 188))
    frames.append(out.convert('RGB'))

palette = frames[0].quantize(colors=128)
indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
path = ROOT / 'assets' / 'ascii-castle.gif'
indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=100, loop=0, optimize=True, disposal=1)
frames[0].save(ROOT / 'assets' / 'ascii-castle.png')
frames[24].save(ROOT / 'assets' / 'ascii-castle-preview.png')
with Image.open(path) as check:
    assert check.n_frames == N and check.info['loop'] == 0
    check.seek(0); first = check.convert('RGB')
    check.seek(48)
    assert ImageChops.difference(first, check.convert('RGB')).getbbox()
print(f'{N} frames, {W}x{H}, {path.stat().st_size / 1000000:.2f} MB')
