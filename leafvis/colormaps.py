"""  A module that loads colormaps (from cpt files) """

import colorsys
import numpy as np
import matplotlib
import os


def colordictFromCPT(fileName):
    """
    Shameless copy of a cpt to colordict implementation from:
        http://www.scipy.org/Cookbook/Matplotlib/Loading_a_colormap_dynamically
    """

    f = open(fileName)
    lines = f.readlines()
    f.close()

    x = []
    r = []
    g = []
    b = []

    colorModel = "RGB"
    for l in lines:
        ls = l.split()
        if l[0] == "#":
            if ls[-1] == "HSV":
                colorModel = "HSV"
                continue
            else:
                continue
        if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
            pass
        else:
            x.append(float(ls[0]))
            r.append(float(ls[1]))
            g.append(float(ls[2]))
            b.append(float(ls[3]))
            xtemp = float(ls[4])
            rtemp = float(ls[5])
            gtemp = float(ls[6])
            btemp = float(ls[7])

    x.append(xtemp)
    r.append(rtemp)
    g.append(gtemp)
    b.append(btemp)

    x = np.array(x, np.float)
    r = np.array(r, np.float)
    g = np.array(g, np.float)
    b = np.array(b, np.float)

    if colorModel == "HSV":
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360., g[i], b[i])
            r[i] = rr
            g[i] = gg
            b[i] = bb
    if colorModel == "HSV":
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360., g[i], b[i])
            r[i] = rr
            g[i] = gg
            b[i] = bb
    if colorModel == "RGB":
        r = r / 255.
        g = g / 255.
        b = b / 255.

    xNorm = (x - x[0]) / (x[-1] - x[0])

    red = []
    blue = []
    green = []
    for i in range(len(x)):
        red.append([xNorm[i], r[i], r[i]])
        green.append([xNorm[i], g[i], g[i]])
        blue.append([xNorm[i], b[i], b[i]])

    colorDict = {"red": red, "green": green, "blue": blue}

    return (colorDict)


temperature = matplotlib.colors.LinearSegmentedColormap(
    'temperature',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'temperature.cpt')),
    20
    )

mslp = matplotlib.colors.LinearSegmentedColormap(
    'mslp',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'mslp.cpt')),
    20
    )


elevation = matplotlib.colors.LinearSegmentedColormap(
    'elevation',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'elevation.cpt')),
    20
    )

rainfall = matplotlib.colors.LinearSegmentedColormap(
    'rainfall',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'rainfall.cpt')),
    20
    )


precip = matplotlib.colors.LinearSegmentedColormap(
    'precip',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'precip.cpt')),
    11
    )

precip2 = matplotlib.colors.LinearSegmentedColormap(
    'precip2',
    colordictFromCPT(os.path.join(os.path.dirname(__file__), 'colortables', 'precip2.cpt')),
    17
    )
