"""Plot templates for the module.

Notes
-----
These are template plot structures for plots and/or reports.
They are not expected to be used directly by the user.
"""

from itertools import repeat, cycle

import numpy as np

from specparam.core.modutils import safe_import, check_dependency
from specparam.plts.utils import check_ax, set_alpha
from specparam.plts.settings import PLT_FIGSIZES, PLT_COLORS, DEFAULT_COLORS

plt = safe_import('.pyplot', 'matplotlib')
#ticker = safe_import('.ticker', 'matplotlib')
#Note / ToDo: see if need to put back ticker management, or remove

###################################################################################################
###################################################################################################

@check_dependency(plt, 'matplotlib')
def plot_scatter_1(data, label=None, title=None, x_val=0, ax=None):
    """Plot a scatter plot, with a single y-axis.

    Parameters
    ----------
    data : 1d array
        Data to plot.
    label : str, optional
        Label for the data, to be set as the y-axis label.
    title : str, optional
        Title for the plot.
    x_val : int, optional, default: 0
        Position along the x-axis to plot set of data.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Notes
    -----
    Data is jittered slightly, for visualization purposes (deviations on x-axis are meaningless).
    """

    ax = check_ax(ax)

    # Create x-axis data, with small jitter for visualization purposes
    x_data = np.ones_like(data) * x_val + np.random.normal(0, 0.025, data.shape)

    ax.scatter(x_data, data, s=36, alpha=set_alpha(len(data)))

    if label:
        ax.set_ylabel(label, fontsize=16)
        ax.set(xticks=[x_val], xticklabels=[label])

    if title:
        ax.set_title(title, fontsize=20)

    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=12)

    ax.set_xlim([-0.5, 0.5])


@check_dependency(plt, 'matplotlib')
def plot_scatter_2(data_0, label_0, data_1, label_1, title=None, ax=None):
    """Plot a scatter plot, with two y-axes.

    Parameters
    ----------
    data_0 : 1d array
        Data to plot on the first axis.
    label_0 : str
        Label for the data on the first axis, to be set as the axis label.
    data_1 : 1d array
        Data to plot on the second axis.
    label_0 : str
        Label for the data on the second axis, to be set as the axis label.
    title : str, optional
        Title for the plot.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Notes
    -----
    Data is jittered slightly, for visualization purposes (deviations on x-axis are meaningless).
    """

    ax = check_ax(ax)
    ax1 = ax.twinx()

    plot_scatter_1(data_0, label_0, ax=ax)
    plot_scatter_1(data_1, label_1, x_val=1, ax=ax1)

    if title:
        ax.set_title(title, fontsize=20)

    ax.set(xlim=[-0.5, 1.5],
           xticks=[0, 1],
           xticklabels=[label_0, label_1])
    ax.tick_params(axis='x', labelsize=16)


@check_dependency(plt, 'matplotlib')
def plot_hist(data, label, title=None, n_bins=25, x_lims=None, ax=None):
    """Plot a histogram.

    Parameters
    ----------
    data : 1d array
        Data to plot.
    label : str
        Label for the data, to be set as the x-axis label.
    title : str, optional
        Title for the plot.
    n_bins : int, optional, default: 25
        Number of bins to use for the histogram.
    x_lims : list of float, optional
        Limits for the x-axis of the plot.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    ax = check_ax(ax)

    ax.hist(data[~np.isnan(data)], n_bins, range=x_lims, alpha=0.8)

    ax.set_xlabel(label, fontsize=16)
    ax.set_ylabel('Count', fontsize=16)

    if x_lims:
        ax.set_xlim(x_lims)

    if title:
        ax.set_title(title, fontsize=20)

    ax.tick_params(axis='both', labelsize=12)


@check_dependency(plt, 'matplotlib')
def plot_param_over_time(param, label=None, title=None, add_legend=True, add_xlabel=True,
                         ax=None, **plot_kwargs):
    """Plot a parameter over time.

    Parameters
    ----------
    param : 1d array
        Parameter values to plot.
    label : str, optional
        Label for the data, to be set as the y-axis label.
    add_legend : bool, optional, default: True
        Whether to add a legend to the plot.
    add_xlabel : bool, optional, default: True
        Whether to add an x-label to the plot.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **plot_kwargs
        Keyword arguments to pass into the ``style_plot``.
    """

    ax = check_ax(ax, plot_kwargs.pop('figsize', PLT_FIGSIZES['time']))

    n_windows = len(param)

    ax.plot(param, label=label,
            alpha=plot_kwargs.pop('alpha', 0.8),
            **plot_kwargs)

    if add_xlabel:
        ax.set_xlabel('Time Window')
    ax.set_ylabel(label if label else 'Parameter Value', fontsize=10)

    if label and add_legend:
        ax.legend(loc='upper left', framealpha=plot_kwargs.pop('legend_framealpha', 0.9))

    if title:
        ax.set_title(title, fontsize=20)

    #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))


@check_dependency(plt, 'matplotlib')
def plot_params_over_time(params, labels=None, title=None, colors=None, ax=None, **plot_kwargs):
    """Plot multiple parameters over time.

    Parameters
    ----------
    params : list of 1d array
        Parameter values to plot.
    labels : list of str
        Label(s) for the data, to be set as the y-axis label(s).
    colors : list of str
        Color(s) to plot data.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **plot_kwargs
        Keyword arguments to pass into the ``style_plot``.
    """

    labels = repeat(labels) if not isinstance(labels, list) else cycle(labels)
    colors = cycle(DEFAULT_COLORS) if not isinstance(colors, list) else cycle(colors)

    ax0 = check_ax(ax, plot_kwargs.pop('figsize', PLT_FIGSIZES['time']))

    n_axes = len(params)
    axes = [ax0] + [ax0.twinx() for ind in range(n_axes-1)]

    if n_axes >= 3:
        for nax, ind in enumerate(range(2, n_axes)):
            axes[ind].spines.right.set_position(("axes", 1.1 + (.1 * nax)))

    for cax, cparams, label, color in zip(axes, params, labels, colors):
        plot_param_over_time(cparams, label, add_legend=False, color=color,
                             ax=cax, **plot_kwargs)

    if bool(labels):
        ax0.legend([cax.get_lines()[0] for cax in axes], labels,
                   loc='upper left', framealpha=plot_kwargs.pop('legend_framealpha', 0.9))

    if title:
        ax0.set_title(title, fontsize=20)

    # Puts the axis with the legend 'on top', while also making it transparent (to see others)
    ax0.set_zorder(1)
    ax0.patch.set_visible(False)
