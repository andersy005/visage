import cv2
from managers import WindowManager, CaptureManager


class Visage(object):

    def __init__(self):
        self._windowManager = WindowManager('Visage', 
                                            self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, True)


    def run(self):
        """Run the main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame

            frame = self._captureManager.frame

            # TODO: filter the frame


            self._captureManager.exitFrame()
            self._windowManager.processEvents()


    def onKeypress(self, keycode):
        """ Handle a keypress
        
        space   -> Take a screenshot.
        Tab     -> Start/Stop recording a screencast
        esacape -> Quit
        
        """

        if keycode == 32: # space
            self._captureManager.writeImage('screenshot.png')\

        elif keycode == 9: # TabError
            if not self._captureManager.isWritingVideo:
                self._captureManager.startwritingVideo('screencast.avi')

            else:
                self._captureManager.stopWritingVideo()

        elif keycode == 27: # escape
            self._windowManager.destroyWindow()


if __name__ == "__main__":
    Visage().run()


        