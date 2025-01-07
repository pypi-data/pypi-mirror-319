"""Module that defines the PictorPoint class."""
from decimal import Decimal

from dataclasses import dataclass
from src.pictor_lib.pictor_type import DecimalUnion
from src.pictor_lib.pictor_size import PictorSize


@dataclass(kw_only=True)
class PictorPoint:
    """Wrap 2d point (x, y)."""

    _x: Decimal
    _y: Decimal

    def __init__(self, x: DecimalUnion = 0, y: DecimalUnion = 0):
        self._x = x
        self._y = y

    @property
    def x(self) -> Decimal:
        """The x property."""

        return self._x

    @property
    def y(self) -> Decimal:
        """The y property."""

        return self._y

    @property
    def raw_tuple(self) -> tuple[int, int]:
        """Convert to rounded int tuple which can be used in raw Pillow APIs."""

        return round(self.x), round(self.y)

    def copy(self) -> 'PictorPoint':
        """Create a new point instance by copying all fields."""

        return PictorPoint(self._x, self._y)

    def set_x(self, x: DecimalUnion) -> 'PictorPoint':
        """Set the x property and return a new instance."""

        self._x = x
        return self

    def set_y(self, y: DecimalUnion) -> 'PictorPoint':
        """Set the y property and return a new instance."""

        self._y = y
        return self

    def move(self, offset: PictorSize) -> 'PictorPoint':
        """Move self by the given offset."""

        self._x += offset.width
        self._y += offset.height
        return self

    def move_x(self, offset: DecimalUnion) -> 'PictorPoint':
        """Move the x field by given offset."""

        self._x += offset
        return self

    def move_y(self, offset: DecimalUnion) -> 'PictorPoint':
        """Return a new instance by moving the y field of given offset."""

        self._y += offset
        return self


PictorPoint.ORIGIN = PictorPoint(0, 0)
