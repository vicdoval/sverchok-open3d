
import numpy as np
import os

from sverchok.utils.math import inverse, inverse_square, inverse_cubic

def show_welcome():
    text = """

 <|||   SVERCHOK - OPEN3D    |||>

           initialized.
"""
    can_paint = os.name in {'posix'}

    with_color = "\033[1;31m{0}\033[0m" if can_paint else "{0}"
    for line in text.splitlines():
        print(with_color.format(line))
