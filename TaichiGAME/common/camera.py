from TaichiGAME.math.matrix import Matrix
from typing import List, Dict, Optional, Tuple

import numpy as np


class Camera():
    class Viewport():
        def __init__(self,
                     top_left: Matrix = Matrix([0.0, 600.0], 'vec'),
                     bot_right: Matrix = Matrix([800.0, 0.0], 'vec')):
                    
            assert top_left.x < bot_right.x
            assert top_left.y > bot_right.y

            self._top_left: Matrix = top_left
            self._bot_right: Matrix = bot_right

        @property
        def width(self) -> float:
            return self._bot_right.x - self._top_left.x

        @width.setter
        def width(self, width: float):
            self._bot_right.x = self._top_left.x + width

        @property
        def height(self) -> float:
            return self._top_left.y - self._bot_right.y

        @height.setter
        def height(self, height: float):
            self._top_left.y = self._bot_right.y + height

        def set_value(self, width: float, height: float):
            self.width = width
            self.height = height


    def __init__(self):
        self._visible: bool = True
        self._aabb_visible: bool = True
        self._joint_visible:bool = True
        self._body_visible: bool = True
        self._axis_visible: bool = True
        self._dbvh_visible: bool = False
        self._tree_visible: bool = False
        self._grid_scale_line_visible: bool = False
        self._rotation_line_visible: bool = False
        self._center_visible: bool = False
        self._contact_visible: bool = False

        
        self._meter_to_pixel: float = 50.0
        self._pixel_to_meter: float = 0.02

        self._target_meter_to_pixel: float = 80.0
        self._target_pixel_to_meter: float = 0.02
        
        self._transform: Matrix = Matrix([0.0, 0.0], 'vec')
        self._origin: Matrix = Matrix([0.0, 0.0], 'vec')
        self._viewport: Camera.Viewport = Camera.Viewport()

        PhysicsWorld *m_world = nullptr
        Body *m_targetBody = nullptr
        DBVH* m_dbvh = nullptr
        Tree* m_tree = nullptr
        ContactMaintainer* m_maintainer = nullptr

        m_zoomFactor = 1.0f
        m_restitution = 2.0f
        m_deltaTime = 15.0f
        m_axisPointCount = 20.0f

