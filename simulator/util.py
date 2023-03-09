import numpy as np
from PySide6.QtGui import QPainter, QTransform, QVector2D, QMouseEvent

Vec2 = tuple[float, float]

def vec2_to_array(v: Vec2) -> np.ndarray:
    return np.array(v, dtype="float32")

def array_to_vec2(a: np.ndarray) -> Vec2:
    assert a.size == 2
    return (a[0], a[1])

def vec2_to_qvector2d(v: Vec2) -> QVector2D:
    return QVector2D(*v)
