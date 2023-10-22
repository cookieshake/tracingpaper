from typing import Self

import numpy as np
from pydantic import BaseModel

class Point(BaseModel):
    x: int
    y: int


class Box(BaseModel):
    top_left: Point
    top_right: Point
    bottom_right: Point
    bottom_left: Point
    
    def is_rectangle(self) -> bool:
        if not self.top_left.x == self.bottom_left.x:
            return False
        elif not self.top_right.x == self.bottom_right.x:
            return False
        elif not self.top_left.y == self.top_right.y:
            return False
        elif not self.bottom_left.y == self.bottom_right.y:
            return False
        else:
            return True
        
    def as_np_array(self) -> np.ndarray:
        return np.array([
            [self.top_left.x, self.top_left.y],
            [self.top_right.x, self.top_right.y],
            [self.bottom_right.x, self.bottom_right.y],
            [self.bottom_left.x, self.bottom_left.y]
        ])
    
    def get_container_box(self) -> Self:
        if self.is_rectangle():
            return self
        else:
            x_list = sorted([self.top_left.x, self.top_right.x, self.bottom_left.x, self.bottom_right.x])
            y_list = sorted([self.top_left.y, self.top_right.y, self.bottom_left.y, self.bottom_right.y])
            min_x = x_list[0]
            max_x = x_list[-1]
            min_y = y_list[0]
            max_y = y_list[-1]
            return Box(
                top_left=Point(x=min_x, y=min_y),
                top_right=Point(x=max_x, y=min_y),
                bottom_left=Point(x=min_x, y=max_y),
                bottom_right=Point(x=max_x, y=max_y)
            )
    


class TextBox(BaseModel):
    text: str
    box: Box
    score: float