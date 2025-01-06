"""A script to generate polyskelion with some parameters.

Mathematics by JJacquelin
https://math.stackexchange.com/questions/651772/parametric-equations-and-specifications-of-a-triskelion-triple-spiral
"""

import argparse
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, fields
from typing import Final, Self, get_type_hints

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.pyplot import Figure

from ._print import fail, info, okay


class _D:
    """Default values for parameters in use in multiple places."""

    output: Final[str | None] = None
    spirals: Final[int] = 3
    whirls: Final[int] = 5
    scale: Final[float] = 1.0
    dt: Final[float] = 0.0001
    linewidth: Final[float] = 1.0
    colors: Final[list[str]] = ["black"]
    antialiased: Final[bool] = True


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="polyskelion",
        description=(
            "A simple script to draw an polyskelion (triskelion, quadskelion, etc.)"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=(
            "Filename to save the plot to (e.g., 'triskelion.png'). If no filename is "
            f"given a preview will be displayed. Default: {_D.output}"
        ),
        default=_D.output,
    )
    parser.add_argument(
        "-s",
        "--spirals",
        type=int,
        help=f"Number of polyskelion spirals. Default: {_D.spirals}",
        default=_D.spirals,
    )
    parser.add_argument(
        "-w",
        "--whirls",
        type=int,
        help=f"Number of whirls in each spiral. Default: {_D.spirals}",
        default=_D.whirls,
    )
    parser.add_argument(
        "--scale",
        type=float,
        help=f"Scaling factor for the spirals. Default: {_D.scale}",
        default=_D.scale,
    )
    parser.add_argument(
        "--dt",
        type=float,
        help=f"Increment of angle from one point to the next. Default: {_D.dt}",
        default=_D.dt,
    )
    parser.add_argument(
        "--linewidth",
        type=float,
        help=f"Linewidth of the plot. Default: {_D.linewidth}",
        default=_D.linewidth,
    )
    parser.add_argument(
        "--color",
        nargs="+",
        dest="colors",
        type=str,
        help=(
            "Provide one or two colors (e.g., '--color black' or '--color \"#f00\" "
            '"#0f0"\'. If two are given the first will color the outer line and the '
            f"second will color the inner line. Default: {_D.colors[0]}"
        ),
        default=_D.colors,
    )
    parser.add_argument(
        "--no-antialias",
        action="store_true",
        help="Disable antialiasing on the final plot",
    )

    return parser.parse_args()


@dataclass
class PolyskelionParams:
    """Parameters used for plotting a polyskelion."""

    spirals: int = _D.spirals
    """Number of polyskelion spirals."""

    whirls: int = _D.whirls
    """Number of whirls in each spiral."""

    scale: float = _D.scale
    """Scaling factor for the spirals."""

    dt: float = _D.dt
    """Increment of angle from one point to the next."""

    linewidth: float = _D.linewidth
    """Linewidth of the plot."""

    colors: Sequence[str] = field(default_factory=lambda: _D.colors)
    """A sequence of one or two colors for the line in the plot.

    If two are given, the second is used for the internal line."""

    antialiased: bool = _D.antialiased
    """Whether or not the plotted line is antialiased."""

    def _get_numeric_fields(self: Self) -> Mapping[str, int | float]:
        type_hints = get_type_hints(self.__class__)
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if type_hints[field.name] in (int, float)
        }

    def __post_init__(self: Self) -> None:
        """Validate some of the given parameters."""
        if len(self.colors) <= 0:
            raise ValueError("At least one color must be provided.")

        for k, v in self._get_numeric_fields().items():
            if v <= 0:
                raise ValueError(
                    f"All numerical input arguments must be positive numbers: {k}={v}"
                )


def calculate_spiral_points(
    n: int, p: PolyskelionParams, internal_branch: bool = False
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Calculate points along spiral number 'n'.

    Args:
        n: The spiral number points are being calculated for
        p: Instance of PolyskelionParams
        internal_branch: True if calculating the internal spiral. Default: False

    Returns:
        x, y: A tuple of the x- and y- point vectors.

    """
    if n < 0:
        raise ValueError(f"n must be 0 or a positive integer. n={n}")
    # Calculate the center of each spiral arm
    x0 = p.scale * np.cos(2 * np.pi * n / p.spirals)
    y0 = p.scale * np.sin(2 * np.pi * n / p.spirals)

    # Define angular ranges for the spiral arm
    # End angle of main segment
    t1 = 2 * np.pi * p.whirls - np.pi / p.spirals + np.pi / 2
    # End angle of additional segment
    t2 = t1 + 2 * np.pi / p.spirals

    # Calculate a constant controlling the radial growth of the spiral
    c = p.scale * np.sin(np.pi / p.spirals) * 2 / np.pi / (1 + 4 * p.whirls)

    # Generate angles and radii for the spiral arm (polar coordinates)
    ta = np.arange(p.dt, t2, p.dt)  # Angle values
    r = c * ta  # Radius values

    # The external branch of the spiral is drawn from angle t=0 to t=t2.
    # The internal branch is drawn from t=π to t=t1+π.
    if internal_branch:
        internal = ta <= t1  # Select angles within the main segment range
        t = ta[internal] + np.pi  # Filter and adjust angles to start from π
        r = r[internal]  # Filter radii
    else:
        t = ta

    x = x0 + r * np.cos(t + 2 * np.pi * n / p.spirals)
    y = y0 + r * np.sin(t + 2 * np.pi * n / p.spirals)

    return x, y


def plot_polyskelion(p: PolyskelionParams) -> Figure:
    """Plot a polyskelion using the provided parameters.

    Note that this returns a matplotlib.pyplot.Figure. This means one should call
    `plt.close(fig)` on the value returned from this if used within a long running
    application.

    Args:
        p: PolyskelionParams

    Returns:
        matplotlib.Figure: The plotted polyskelion

    """
    figure = plt.figure()
    figplot = figure.add_subplot()

    for n in range(p.spirals):
        x, y = calculate_spiral_points(n, p)
        figplot.plot(
            x,
            y,
            p.colors[0],
            linewidth=p.linewidth,
            antialiased=p.antialiased,
        )

        x, y = calculate_spiral_points(n, p, internal_branch=True)
        figplot.plot(
            x,
            y,
            p.colors[-1],
            linewidth=p.linewidth,
            antialiased=p.antialiased,
        )

    figplot.axis("equal")
    figplot.axis("off")
    return figure


def _main() -> None:
    args = _parse_args()

    try:
        params = PolyskelionParams(
            spirals=args.spirals,
            whirls=args.whirls,
            scale=args.scale,
            dt=args.dt,
            linewidth=args.linewidth,
            colors=args.colors,
            antialiased=not args.no_antialias,
        )
    except ValueError as e:
        fail(str(e))
        sys.exit(1)

    figure = plot_polyskelion(params)
    if args.output:
        figure.savefig(args.output, dpi=300, bbox_inches="tight", transparent=True)
        okay(f"saved to {args.output}")
    else:
        info("previewing plot ...", stderr=True)
        plt.show()


if __name__ == "__main__":
    _main()  # pragma: no cover
