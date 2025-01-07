from dataclasses import dataclass
from typing import Callable, NamedTuple, Protocol, Tuple

from numpy import ndarray
from rasterio.crs import CRS
from rasterio.transform import Affine


@dataclass(frozen=True)
class GridCore:
    data: ndarray
    transform: Affine
    crs: CRS


class Extent(NamedTuple):
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def intersects(self, xmin: float, ymin: float, xmax: float, ymax: float):
        return (
            self.xmin < xmax
            and self.xmax > xmin
            and self.ymin < ymax
            and self.ymax > ymin
        )

    def intersect(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((max, max, min, min), zip(self, extent))])

    def union(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((min, min, max, max), zip(self, extent))])

    def tiles(self, cell_size: Tuple[float, float], width: int, height: int):
        xmin = self.xmin
        while xmin < self.xmax:
            xmax = xmin + width * cell_size[0]
            ymin = self.ymin
            while ymin < self.ymax:
                ymax = ymin + height * cell_size[1]
                yield Extent(xmin, ymin, xmax, ymax)
                ymin = ymax
            xmin = xmax

    __and__ = intersect
    __rand__ = __and__
    __or__ = union
    __ror__ = __or__


class CellSize(NamedTuple):
    x: float
    y: float

    def __mul__(self, n: object):
        if not isinstance(n, (float, int)):
            return NotImplemented
        return CellSize(self.x * n, self.y * n)

    def __rmul__(self, n: object):
        if not isinstance(n, (float, int)):
            return NotImplemented
        return CellSize(self.x * n, self.y * n)

    def __truediv__(self, n: float):
        return CellSize(self.x / n, self.y / n)


class PointValue(NamedTuple):
    x: float
    y: float
    value: float


class Scaler(Protocol):
    fit: Callable
    transform: Callable
    fit_transform: Callable
