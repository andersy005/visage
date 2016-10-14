import cv2
import numpy as np
import time

class CaptureManager(object):

    # Most of the member variables are private, as denoted by the underscore prefix
    # These private variables relate to the state of the current frame and any file writing operations

    def __init__(self, capture, previewWindowManager= None, shouldMirrorPreview = False):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEnconding = None
        self._videoWriter = None


        self._startTime = None
        self._framesElapsed = long(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(channel = self.channel)

        return self._frame

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None



    def enterFrame(self):
        """Capture the next frame, if any"""

        # First, check that any previous frame was exited
        assert not self._enteredFrame, 'previous enterFrame() had no matching exitFrame()'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()


    def exitFrame(self):
        """Draw to the window. Write to files. Release the frame"""
        # check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame

        if self.frame is None:
            self.enterFrame = False
            return 


    # Update the FPS estimate and related variables.
    if self._framesElapsed == 0:
        self._startTime = time.time()

    else:
        timeElapsed = time.time() - self._startTime
        self._fpsEstimate = self._framesElapsed / timeElapsed

    self._framesElapsed += 1


    # Draw to the window, if any
    if self.previewWindowManager is not None:
        if self.shouldMirrorPreview:
            mirroredFrame = np.fliplr(self._frame).copy()
            self.previewWindowManager.show(mirroredFrame)


        else:
            self.previewWindowManager.show(self._frame)


    # Write to the image file, if any
    if self.isWritingImage:
        cv2.imwrite(self._imageFilename, self._frame)
        self._imageFilename = None


    # Write to the video file, if any
    self._writeVideoFrame()


    # Release the frame
    self._frame = None
    self._enteredFrame = False
    