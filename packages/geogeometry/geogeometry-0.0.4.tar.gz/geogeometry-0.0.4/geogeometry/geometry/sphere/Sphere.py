from typing import Optional

import numpy as np

from geogeometry.geometry.shared.BaseObject import BaseObject


class Sphere(BaseObject, SphereProperties):

    def __init__(self,
                 center: np.ndarray,
                 radius: float,
                 name: Optional[str] = None):
        super().__init__(name=name)

        self.setCenter(center=center)
        self.setRadius(radius=radius)