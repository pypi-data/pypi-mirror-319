import math
from pathlib import Path

import numpy as np

import numpy_turtle as np_turtle

AXIOM = "F-G-G"
RULES = {
    "F": "F-G+F+G-F",
    "G": "GG",
}

COLOR = 42, 69, 222, 255
ANGLE0 = math.tau / 4
ANGLE = math.tau / 3

COLS = 512
ROWS = math.ceil(COLS * math.sin(ANGLE / 2))
ITER = 6

OUT = Path(__file__).parent / "images" / (Path(__file__).stem + ".png")


def main() -> None:
    """
    Draw the Sierpinski triangle.

    https://wikipedia.org/wiki/Sierpinski_triangle
    """
    array = np.zeros((ROWS, COLS, len(COLOR)), dtype=np.uint8)
    system = np_turtle.l_system.grow(AXIOM, RULES, ITER)

    turtle = np_turtle.Turtle(array, color=COLOR, aa=False).rotate(ANGLE0)
    turtle.position = ROWS - 1, 0

    for s_n in system:
        if s_n in {"F", "G"}:
            turtle.forward(COLS / (1 << ITER))
        elif s_n == "-":
            turtle.rotate(ANGLE)
        elif s_n == "+":
            turtle.rotate(-ANGLE)

    turtle.save_image(OUT)


if __name__ == "__main__":
    main()
