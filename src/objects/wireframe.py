from dataclasses import dataclass, field
from .line import Line
from .object import Object


@dataclass
class Wireframe(Object):
    ''' Wireframe class '''
    lines: list = field(default_factory=list)

    def distance(self, point):
        min_distance = float('inf')
        for line in self.lines:
            current = line.distance(point)
            if current < min_distance:
                min_distance = current
        return min_distance

    def as_point_list(self):
        return [point for line in self.lines for point in line.as_point_list()]
