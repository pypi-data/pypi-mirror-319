from typing import Dict, List, Tuple, overload

import rasterio
from rasterio.transform import array_bounds

from glidergun._grid import Grid, grid
from glidergun._stack import Stack, stack
from glidergun._types import Extent


class Mosaic:
    def __init__(self, *files: str) -> None:
        assert files, "No files provided"
        self.files: Dict[str, Extent] = {}
        crs = None
        for f in files:
            with rasterio.open(f) as dataset:
                p = dataset.profile
                c = p["crs"]
                e = Extent(*array_bounds(p["height"], p["width"], p["transform"]))
            if crs is None:
                crs = c
            elif crs != c:
                raise ValueError("CRS mismatch")
            self.files[f] = e

    def _read(self, extent: Tuple[float, float, float, float], index: int):
        for f, e in self.files.items():
            try:
                if e.intersects(*extent):
                    yield grid(f, extent, index=index)
            except ValueError:
                pass

    @overload
    def clip(
        self, xmin: float, ymin: float, xmax: float, ymax: float, index: int = 1
    ) -> Grid: ...

    @overload
    def clip(
        self, xmin: float, ymin: float, xmax: float, ymax: float, index: Tuple[int, ...]
    ) -> Stack: ...

    def clip(self, xmin: float, ymin: float, xmax: float, ymax: float, index=None):
        if not index or isinstance(index, int):
            grids: List[Grid] = [
                g for g in self._read((xmin, ymin, xmax, ymax), index or 1) if g
            ]
            return mosaic(*grids)
        return stack(*(self.clip(xmin, ymin, xmax, ymax, index=i) for i in index))


@overload
def mosaic(*grids: str) -> Mosaic: ...


@overload
def mosaic(*grids: Grid) -> Grid: ...


def mosaic(*grids):
    g = grids[0]
    if isinstance(g, str):
        return Mosaic(*grids)
    return g.mosaic(*grids[1:])
