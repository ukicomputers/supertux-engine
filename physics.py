from math import sqrt
from config import GRAVITY

def jumpSpeed(height):
    return sqrt(2 * GRAVITY * height)