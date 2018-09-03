#!/usr/bin/env python3
import string
from itertools import chain
from pywal.theme import list_themes, parse
from PIL import Image
import os

template = [
 ['b'] * 10,
 [ 'b', '0', '1', '2', '3', '4', '5', '6', '7', 'b'],
 ['b'] + ['f'] * 8 + ['b'],
 ['b'] + ['f'] * 8 + ['b'],
 [ 'b', '8', '9', '10', '11', '12', '13', '14', '15', 'b'],
 ['b'] * 10,
]

def to_bytes(color):
    """Convert #123ABC to [18, 58, 188]"""
    return (int(color[1:][i:i + 2], 16) for i in [0,2,4])

def get_themes(dark=True):
    return {t.name.replace('.json', ''): parse(t) for t in list_themes(dark)}

def get_color(theme, ix):
    if ix in 'bfc':
        n = {'b': 'background', 'f': 'foreground', 'c': 'cursor'}[ix]
        return theme['special'][n]
    else:
        return theme['colors']['color' + ix]

def generate_preview(theme_name, theme, dirname='preview', size=(32, 20)):
    w, h = len(template[0]), len(template)

    bs = bytes(chain.from_iterable(to_bytes(get_color(theme, c))
                                   for r in template for c in r))

    if type(size) is int or len(size) == 1:
        size = (size, size)

    image_size = (w * size[0], h * size[1])

    image = Image.frombytes('RGB', (w, h), bs).resize(size=image_size)

    with open(dirname + '/' + theme_name + '.png', 'wb') as f:
        image.save(f)

def generate_previews(themes, **kwargs):
    for t in themes:
        generate_preview(t, themes[t], **kwargs)


def generate_markdown(themes, fname, dirname='preview'):
    with open(fname + '.md', 'w') as f:
        f.write("---\ntitle: {}\n---\n\n".format("PyWal theme preview"))
        for t in themes:
            f.write("\n## " + t + '\n\n')
            f.write("![]({}/{}.png)\n".format(dirname, t))

if __name__ == '__main__':
    for name, themes in [("dark", get_themes()),
                         ("light", get_themes(dark=False))]:
        os.makedirs(name, exist_ok=True)
        generate_previews(themes, dirname=name)
        generate_markdown(themes, name + 'previews', dirname=name)
