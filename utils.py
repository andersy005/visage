import cv2
import numpy as np
import scipy.interpolate


def createCurveFunc(points):
    """Return a function derived from control points."""

    if points is None:
        return None

    numPoints = len(points)
    if numPoints < 2:
        return None
    """function takes an array of (x, y) pairs
        treat x as a channel's input value
        and y as the corresponding output value. For example, (128, 160) would
        brighten a channel's midtones."""
    xs, ys = zip(*points)

    if numPoints < 4:
        kind = 'linear'
        # quadratic is not implemented

    else:
        kind = 'cubic'

    return scipy.interpolate.interp1d(xs, ys, kind, bounds_error= False)
