import numpy as np

def get_color(label):
    np.random.seed(hash(label) % 256)
    return tuple(np.random.randint(0, 256, size=3).tolist())
