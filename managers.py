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


    """enterFrame() only grabs (synchronizes) a frame,
whereas actual retrieval from a channel is postponed to a subsequent reading of
the frame variable. The implementation of exitFrame() takes the image from the
current channel, estimates a frame rate, shows the image via the window manager
(if any), and fulfills any pending requests to write the image to files."""

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
    

    """writeImage() , startWritingVideo() , and
    stopWritingVideo() , simply record the parameters for file writing operations,
    whereas the actual writing operations are postponed to the next call of exitFrame()"""


    def writeImage(self, filename):
        """Write the next exitedi frame to an image file."""
        self._imageFilename = filename


    def startwritingVideo(self, filename, encoding = cv2.cv.CV_FOURCC('I', '4', '2', '0')):
        """Start writing exited frames to a video file"""

        self._videoFilename = filename
        self._videoEnconding = encoding


    def stopWritingVideo(self):
        """Stop writing exited frames to a video file"""
        self._videoFilename = None
        self._videoEnconding = None
        self._videoWriter = None


    def _writeVideoFrame(self):

        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.cv.CV_CAP_PROP_FPS)

            if fps == 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._framesElapsed < 20:
                    # Wait until more frames elapse so that the estimate is more stable.
                    return 

                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(
                        cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                        cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

            self._videoWriter = cv2.VideoWriter(self._videoFilename,
                                                self._videoEnconding, fps, size)

            self._videoWriter.write(self._frame)


class WindowManager(object):


    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._iswindowCreated = False


    @property
    def isWindowCreated(self):
        return self._iswindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._iswindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._iswindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK

            keycode &= 0xFF
            self.keypressCallback(keycode)