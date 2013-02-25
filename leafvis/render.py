"""
Rendering module, responsible for *fast* png creation.
"""

import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def draw_tile(grid, cmap='gray', dpi=80, alpha=0.5, vmin=0, vmax=2500):
    """ Draws a tile """

    fig = Figure(dpi=dpi, edgecolor='none')
    fig.patch.set_alpha(0.0)

    # Form the graphic
    ax = fig.add_axes((0,0,1,1))
    ax.matshow(grid, interpolation='nearest', alpha=alpha, vmin=vmin, vmax=vmax)
    ax.contour(grid, level=[500])
    ax.axis('off')
    ax.axis('tight')

    # Write the PNG file to a string.
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output, transparent=True)
    
    return png_output.getvalue()