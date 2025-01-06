from typing import List, Tuple, overload

import rasterio
from rasterio.crs import CRS
from rasterio.transform import array_bounds

from glidergun._grid import Grid, grid
from glidergun._stack import Stack, stack
from glidergun._types import Extent


class Mosaic:
    def __init__(self, *files: str) -> None:
        self.files = list(files)
        self.extent, self.crs = self._read_metadata()

    def _read_metadata(self) -> Tuple[Extent, CRS]:
        assert self.files, "No files provided"
        crs = None
        extent = None
        for f in self.files:
            with rasterio.open(f) as dataset:
                p = dataset.profile
                c = p["crs"]
                e = Extent(*array_bounds(p["height"], p["width"], p["transform"]))
            if crs and crs != c:
                raise ValueError("CRS mismatch")
            crs = c
            extent = e | extent
        assert extent is not None
        return extent, crs

    def _read(self, extent: Tuple[float, float, float, float], index: int):
        for f in self.files:
            try:
                yield f if isinstance(f, Grid) else grid(f, extent, index=index)
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
