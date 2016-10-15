import cv2
import numpy as np
import utils


def recolorRC(src, dst):
    """Simulate conversion from BGR to RC (red, cyan).
    
    The source and destination images must both be in BGR format.
    
    Blues and greens are replaced with cyans
    
    Pseudocode:
    dst.b = dst.g = 0.5 * (src.b + src.g)
    dst.r = src.r
    
    """
    # Use split() to extract a source image's channels as one dimensional arrays
    b, g, r = cv2.split(src)

    """
    The arguments to addWeighted() are (in order) the first source
    array, a weight applied to the first source array, the second source array, a
    weight applied to the second source array, a constant added to the result, and
    a destination array.

    Replace the B channel values with an average of B and G
    """
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)

    # Replace the values in dst image with the modified channels. 
    cv2.merge((b, b, r), dst)