from pathlib import Path
import logging
from typing import cast

logging.getLogger("matplotlib").setLevel(logging.WARNING)
import matplotlib as mpl  # NOQA

default_backend = mpl.get_backend()
mpl.use("Agg")
import matplotlib.pyplot as plt  # NOQA

from icplot.color import ColorMap, Color  # NOQA
from .series import PlotSeries, LinePlotSeries, ScatterPlotSeries, ImageSeries  # NOQA
from .plot import Plot, GridPlot, get_series_colors  # NOQA


class MatplotlibColorMap(ColorMap):
    """
    A matplotlib based colormap
    """

    def __init__(self, label: str):
        super().__init__(label, mpl.colormaps[label])


def _set_decorations(axs, plot: Plot):
    ax = axs[0]
    if plot.legend.lower() != "none":
        lines = []
        for axis in axs:
            for line in axis.lines:
                lines.append(line)
        ax.legend(handles=lines, loc=plot.legend)
    if plot.x_axis.label:
        ax.set_xlabel(plot.x_axis.label)
    for idx, y_axis in enumerate(plot.y_axes):
        axs[idx].set_yscale(y_axis.scale)
        if y_axis.label:
            axs[idx].set_ylabel(y_axis.label)
        if y_axis.ticks:
            axs[idx].set_yticks(y_axis.resolved_ticks)
    if plot.x_axis.ticks:
        ax.set_xticks(plot.x_axis.resolved_ticks)
    if plot.title:
        ax.set_title(plot.title)


def _plot_line(axs, series: LinePlotSeries, color: Color | None):
    if not series.position_right:
        ax = axs[0]
    else:
        ax = axs[1]

    if color:
        render_color: list | None = color.as_list()
    else:
        render_color = None

    ax.plot(
        series.x,
        series.y,
        label=series.label,
        color=render_color,
        marker=series.marker,
        drawstyle=series.drawstyle,
        linestyle=series.linestyle,
    )


def _plot_scatter(ax, series: ScatterPlotSeries, color: Color | None):

    if color:
        render_color: list | None = series.color.as_list()
    else:
        render_color = None

    ax.scatter(series.data, label=series.label, color=render_color)


def _plot_image(ax, series: ImageSeries):
    ax.imshow(series.data)
    ax.axis("off")


def _plot_series(axs, series: PlotSeries, color: Color | None = None):
    ax = axs[0]
    if series.series_type == "line":
        _plot_line(axs, cast(LinePlotSeries, series), color)
    elif series.series_type == "scatter":
        _plot_scatter(ax, cast(ScatterPlotSeries, series), color)
    elif series.series_type == "image":
        _plot_image(ax, cast(ImageSeries, series))


def _render(fig, path: Path | None = None):
    if path:
        fig.savefig(path)
    else:
        plt.switch_backend(default_backend)
        fig.show()
        plt.switch_backend("Agg")


def render(
    plot: Plot, path: Path | None = None, cmap=MatplotlibColorMap("gist_rainbow")
):

    colors = get_series_colors(cmap, plot)

    fig, ax = plt.subplots()
    axs = [ax]
    if len(plot.y_axes) > 1:
        axs.append(ax.twinx())

    for series, color in zip(plot.series, colors):
        _plot_series(axs, series, color)

    _set_decorations(axs, plot)

    _render(fig, path)


def render_grid(
    plot: GridPlot,
    path: Path | None = None,
    num_samples: int = 0,
):
    rows, cols, series = plot.get_subplots(num_samples)
    fig, axs = plt.subplots(rows, cols)

    for ax, series_item in zip(axs, series):
        _plot_series(ax, series_item)

    _render(fig, path)
