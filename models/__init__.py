from models.base import Shape2D
from models.circle import Circle
from models.rectangle import Rectangle
from models.triangle import Triangle

models: dict[str, type[Shape2D]] = {
    'circle': Circle,
    'rectangle': Rectangle,
    'triangle': Triangle,
}
