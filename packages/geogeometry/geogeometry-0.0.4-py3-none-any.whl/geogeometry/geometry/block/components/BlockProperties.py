from typing import Optional

import numpy as np


class BlockProperties(object):

    def __init__(self):
        self.corners: Optional[np.ndarray] = None

    def setCorners(self, corners: np.ndarray) -> None:
        self.corners = corners

    def getCorners(self) -> np.ndarray:
        return self.corners
