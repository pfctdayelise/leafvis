"""
Rendering module
"""

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def draw_tile(tl, br):

    grid = resample(tl, br)

    fig = Figure(dpi=80, edgecolor='none')
    fig.patch.set_alpha(0.1)
    ax = fig.add_axes((0,0,1,1))
    ax.matshow(grid, interpolation='nearest', alpha=0.5, vmin=0, vmax=2500)
    ax.contour(grid, level=[500])
    ax.axis('off')
    ax.axis('tight')
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output, transparent=True)
    
    return png_output.getvalue()