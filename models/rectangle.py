from dataclasses import dataclass

import torch

from models.base import Shape2D


@dataclass(kw_only=True)
class Rectangle(Shape2D):
    length: float
    '''[m]'''
    width: float
    '''[m]'''

    @property
    def computation_time(self):
        return 2.0

    def compute_area(self):
        length = torch.tensor(self.length, device=self.gpu)
        width = torch.tensor(self.length, device=self.gpu)
        area = (length * width).item()
        self.wait()
        self.save_result(area=area)
        return area
