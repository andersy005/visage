import numpy as np 
import cv2
import wx

from gui import BaseLayout

from filters import PencilSketch, WarmingFilter, CoolingFilter, Cartoonizer


class FilterLayout(BaseLayout):
    """Custom layout for filter effects

        This class implements a custom layout for applying diverse filter
        effects to a camera feed. The layout is based on an abstract base
        class BaseLayout. It displays the camera feed (passed to the class as
        a cv2.VideoCapture object) in the variable self.panels_vertical.
        Additional layout elements can be added by using the Add method (e.g.,
        self.panels_vertical(wx.Panel(self, -1))).
    """

	

    def _init_custom_layout(self):
        """Initializes image filter effects"""
        self.pencil_sketch = PencilSketch((self.imgWidth, self.imgHeight))
        self.warm_filter = WarmingFilter()
        self.cool_filter = CoolingFilter()
        self.cartoonizer = Cartoonizer()




    def _create_custom_layout(self):
    	"""Layout showing a row of radio buttons below the camera feed"""

    	# create a horizontal layout with all filter modes as radio buttons
    	pnl = wx.Panel(self, -1)
        self.mode_warm = wx.RadioButton(pnl, -1, 'Warming Filter', (10, 10),
                                        style=wx.RB_GROUP)

        self.mode_cool = wx.RadioButton(pnl, -1, 'Cooling Filter', (10, 10))
    	self.mode_sketch = wx.RadioButton(pnl, -1, 'Pencil Sketch', (10, 10))
        self.mode_cartoon = wx.RadioButton(pnl, -1, 'Cartoon', (10, 10))
    	hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.mode_warm, 1)
        hbox.Add(self.mode_cool, 1)
    	hbox.Add(self.mode_sketch, 1)
        hbox.Add(self.mode_cartoon, 1)
    	pnl.SetSizer(hbox)



    	# add a panel with radio buttons to existing panels in a vertical
    	# arrangement

    	self.panels_vertical.Add(pnl, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=1)


    def _process_frame(self, frame_rgb):
    	"""Processes the current RGB camera frame

    	Returns: The processed RGB frame to be displayed

    	"""

    	# choose filter effect based on radio buttons setting
        if self.mode_warm.GetValue():
            frame = self.warm_filter.render(frame_rgb)

        elif self.mode_cool.GetValue():
            frame = self.cool_filter.render(frame_rgb)

    	elif self.mode_sketch.GetValue():
    		frame = self.pencil_sketch.render(frame_rgb)

        elif self.mode_cartoon.GetValue():
            frame = self.cartoonizer.render(frame_rgb)


    	return frame


def main():
	# open webcam 
	capture = cv2.VideoCapture(0)
	if not(capture.isOpened()):
		capture.open()

	capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)


	# start graphical user interface
	app = wx.App()
	layout = FilterLayout(None, -1, 'Visage App, Fun with Filters', capture)
	layout.Show(True)
	app.MainLoop()


if __name__ == '__main__':
	main()