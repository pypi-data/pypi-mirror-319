from typing import Optional

import numpy as np


class SphereProperties(object):

    def __init__(self):
        self.center: Optional[np.ndarray] = None
        self.radius: Optional[float] = None

    def setCenter(self, center: np.ndarray) -> None:
        self.center = center

    def setRadius(self, radius: float) -> None:
        self.radius = radius

    def getCenter(self) -> np.ndarray:
        return self.center

    def getRadius(self) -> float:
        return self.radius
