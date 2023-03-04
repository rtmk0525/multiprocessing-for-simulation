import math
from dataclasses import dataclass

import torch

from models.base import Shape2D


@dataclass(kw_only=True)
class Circle(Shape2D):
    radius: float
    '''[m]'''

    @property
    def computation_time(self):
        return 1.5

    def compute_area(self):
        radius = torch.tensor(self.radius, device=self.gpu)
        area = (math.pi * radius ** 2).item()
        self.wait()
        self.save_result(area=area)
        return area
