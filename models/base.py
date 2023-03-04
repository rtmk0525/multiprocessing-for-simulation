import os
import time
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from torch import device


@dataclass(kw_only=True)
class Shape2D(metaclass=ABCMeta):
    name: str
    cpu: device
    gpu: device
    save_dir: str

    @property
    @abstractmethod
    def computation_time(self):
        '''[s]'''
        ...
    
    @abstractmethod
    def compute_area(self):
        '''[m^2]'''
        ...
    
    def wait(self):
        time.sleep(self.computation_time)
    
    def save_result(self, area: float):
        with open(os.path.join(self.save_dir, 'area.txt'), 'w') as file:
            file.write(f'Area = {area:.4f}')
