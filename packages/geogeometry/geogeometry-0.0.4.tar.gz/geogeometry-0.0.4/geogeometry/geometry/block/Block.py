from typing import Optional, Union, List

import numpy as np

from geogeometry.geometry.block.components.BlockProperties import BlockProperties
from geogeometry.geometry.shared.explicit_geometry.ExplicitGeometry import ExplicitGeometry


class Block(ExplicitGeometry, BlockProperties):

    def __init__(self,
                 corners: Union[List, np.ndarray],
                 name: Optional[str] = None):
        super().__init__(name=name)

        corners = np.array([np.min(corners, axis=0), np.max(corners, axis=0)])

        self.setCorners(corners=corners)
        self.setNodes(nodes=corners)

