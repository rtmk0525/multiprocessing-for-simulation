from dataclasses import dataclass

import torch

from models.base import Shape2D


@dataclass(kw_only=True)
class Triangle(Shape2D):
    base: float
    '''[m]'''
    height: float
    '''[m]'''

    @property
    def computation_time(self):
        return 5.0

    def compute_area(self):
        base = torch.tensor(self.base, device=self.gpu)
        height = torch.tensor(self.height, device=self.gpu)
        area = ((1/2) * base * height).item()
        self.wait()
        self.save_result(area=area)
        return area
