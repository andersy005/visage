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



def recolorCMV(src, dst):
    """Simulate conversion from BGR to CMV (Cyan, magenta, value)
    The source and destination images must both be in BGR format.
    Yellows are desaturated/
    
    Pseudocode:
    dst.b = max(src.b, src.g,src.r)
    dst.g = src.g
    dst.r = src.r
    
    """

    b, g, r = cv2.split(src)
    cv2.max(b, g, r)
    cv2.max(b, r, b)
    cv2.merge((b, g, r), dst)



class VFuncFilter(object):
    """A filter that applies a function to V (or all of BGR)"""

    def __init__(self, vFunc = None, dtype = np.uint8):
        length = np.iinfo(dtype).max + 1
        self._vlookupArray = utils.createLookupArray(vFunc, length)


    def apply(self, src, dst):
        """Apply the filter with a BGR or gray source/destination."""

        srcFlatView = utils.flatView(src)
        dstFlatView = utils.flatView(dst)
        utils.applyLookupArray(self._vlookupArray, srcFlatView, dstFlatView)


class VcurveFilter(VFuncFilter):
    """A filter that applies a curve to V ( or all of BGR)."""

    def __init__(self, vPoints, dtype = np.uint8):
        VFuncFilter.__init__(self, utils.createCurveFunc(vPoints), dtype)



class BGRFuncFilter(object):
    """A filter that applies different functions to each of BGR."""

    def __init__(self, vFunc = None, bFunc = None, gFunc = None, rFunc = None, dtype = np.uint8):
        length = np.iinfo(dtype).max + 1
        self._bLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(bFunc, vFunc), length)

        self._gLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(gFunc, vFunc), length)

        self._rLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(rFunc, vFunc), length)


    def apply(self, src, dst):
        """Apply the filter with a BGR source/destination."""

        b, g, r = cv2.split(src)
        utils.applyLookupArray(self._bLookupArray, b, b)
        utils.applyLookupArray(self._gLookupArray, g, g)
        utils.applyLookupArray(self._rLookupArray, r, r)


class BGRCurveFilter(BGRFuncFilter):
    """A filter that applies different curves to each of BGR."""

    def __init__(self, vPoints = None, bPoints = None, gPoints = None, 
                 rPoints = None, dtype = np.uint8):

                 BGRFuncFilter.__init__(self,
                                     utils.createCurveFunc(vPoints),
                                     utils.createCurveFunc(bPoints),
                                     utils.createCurveFunc(gPoints),
                                     utils.createCurveFunc(rPoints), dtype)
                                     

        
           
        
