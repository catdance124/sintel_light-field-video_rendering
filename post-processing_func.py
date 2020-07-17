from PIL import Image
from PIL import ImageDraw


def draw_view_point(img, point, n_angle=9):
    d = ImageDraw.Draw(img)
    size = 14
    x, y = 1024-size*n_angle, 436-size*n_angle
    for i in range(1, n_angle+1):
        for j in range(1, n_angle+1):
            d.rectangle([(x,y), (x+size,y+size)], fill='yellow', outline='green',  width=3)
            y += size
        y = 436-size*n_angle
        x += size

    # draw point
    x, y = 1024-size*n_angle, 436-size*n_angle
    d.rectangle([(x+size*point[0], y+size*point[1]), (x+size*(point[0]+1), y+size*(point[1]+1))], fill='red', outline='green',  width=3)
    return img