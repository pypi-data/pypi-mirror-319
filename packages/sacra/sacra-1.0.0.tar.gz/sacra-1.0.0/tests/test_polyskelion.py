"""Polyskelion tests."""

from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt
import pytest
from matplotlib.figure import Figure

import sacra.polyskelion as ps
from sacra import polyskelion


@pytest.fixture()
def params() -> ps.PolyskelionParams:
    """Create a default instance of PolyskelionParams."""
    return ps.PolyskelionParams()


@pytest.mark.parametrize("bad_val", (0, -1))
def test_params_raise_on_bad_numeric_input(
    params: ps.PolyskelionParams, bad_val: int
) -> None:
    """Tests that the PolyskelionParams dataclass raises on bad numeric input."""
    fields = params._get_numeric_fields()
    for field in fields:
        with pytest.raises(ValueError, match=f"{field}={bad_val}"):
            ps.PolyskelionParams(**{field: bad_val})  # type: ignore


def test_params_raise_on_bad_color_input() -> None:
    """Tests that the PolyskelionParams dataclass raises on bad color input."""
    with pytest.raises(ValueError, match="At least one color must be provided."):
        ps.PolyskelionParams(colors=[])


def test_plot_with_default_params(params: ps.PolyskelionParams) -> None:
    """Tests that a polyskelion is successfully plotted with default parameters."""
    fig = ps.plot_polyskelion(params)

    assert len(fig.axes) == 1

    ax = fig.axes[0]
    assert ax.get_title() == ""
    assert ax.get_xlabel() == ""
    assert ax.get_ylabel() == ""
    assert ax.get_legend() is None

    lines = ax.get_lines()
    assert len(lines) == params.spirals * 2  # There are two lines per spiral
    plt.close(fig)


def test_point_calculation_raises_on_bad_n(params: ps.PolyskelionParams) -> None:
    """Tests that the point calculation raises on bad input."""
    n = -1
    with pytest.raises(ValueError, match=f"n must be 0 or a positive integer. n={n}"):
        ps.calculate_spiral_points(n, params)


def test_point_calculation_differs_for_internal(params: ps.PolyskelionParams) -> None:
    """Tests that the internal branch is "always" smaller (for a reasonable maximum)."""
    for n in range(10):
        ex_x, ex_y = ps.calculate_spiral_points(n, params)
        in_x, in_y = ps.calculate_spiral_points(n, params, internal_branch=True)

        assert ex_x.shape == ex_y.shape
        assert in_x.shape == in_y.shape

        assert ex_x.shape > in_x.shape
        assert ex_y.shape > in_y.shape


def test_defaults(params: ps.PolyskelionParams) -> None:
    """Tests that the same defaults are used everywhere."""
    with patch("sys.argv", ["polyskelion"]):
        args = ps._parse_args()
        for field, value in params.__dict__.items():
            _d = getattr(ps._D, field)
            if field == "antialiased":
                # cli flag _only_ disables antialiasing
                arg = not args.no_antialias
            else:
                arg = getattr(args, field)

            assert _d == arg == value, f"field={field}"


@pytest.mark.parametrize("bad_args", (["--dt", "-1.0"], ["--spirals", "0"]))
def test_bad_cli_args_print_and_exit(bad_args: list[str]) -> None:
    """Tests that bad arguments to the cli print from fail() and then exit."""
    with (
        patch("sys.argv", ["polyskelion"] + bad_args),
        patch("sacra.polyskelion.fail") as mock_fail,
        patch("sys.exit", side_effect=SystemExit) as mock_exit,
    ):
        with pytest.raises(SystemExit):
            polyskelion._main()
        mock_fail.assert_called_once_with(
            "All numerical input arguments must be positive numbers: "
            f"{bad_args[0][2:]}={bad_args[1]}"
        )
        mock_exit.assert_called_once_with(1)


def test_good_cli_args_save_to_output() -> None:
    """Tests good arguments saving to output.

    In particular that the cli calls savefig(), prints from okay(), and then
    exits.
    """
    outfile = "output.png"
    mock_figure = MagicMock(spec=Figure)
    with (
        patch("sys.argv", ["polyskelion", "-o", outfile]),
        patch(
            "sacra.polyskelion.plot_polyskelion", return_value=mock_figure
        ) as mock_plot_poly,
        patch("sacra.polyskelion.okay") as mock_okay,
        patch("matplotlib.pyplot.show") as mock_show,
    ):
        polyskelion._main()
        mock_plot_poly.assert_called_once()
        mock_figure.savefig.assert_called_once_with(
            outfile, dpi=300, bbox_inches="tight", transparent=True
        )
        mock_okay.assert_called_once_with(f"saved to {outfile}")
        mock_show.assert_not_called()


def test_good_cli_args_with_preview() -> None:
    """Tests good arguments that just preview the plot."""
    mock_figure = MagicMock(spec=Figure)
    with (
        patch("sys.argv", ["polyskelion"]),
        patch(
            "sacra.polyskelion.plot_polyskelion", return_value=mock_figure
        ) as mock_plot_poly,
        patch("sacra.polyskelion.info") as mock_info,
        patch("matplotlib.pyplot.show") as mock_show,
    ):
        polyskelion._main()
        mock_plot_poly.assert_called_once()
        mock_figure.savefig.assert_not_called()
        mock_info.assert_called_once_with("previewing plot ...", stderr=True)
        mock_show.assert_called_once()
