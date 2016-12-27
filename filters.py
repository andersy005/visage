import cv2
import numpy as np 

from scipy.interpolate import UnivariateSpline



class PencilSketch:
	
	def __init__(self, (width, height), bg_gray = 'pencilsketch_bg.jpg'):
		self.width = width
		self.height = height


		# try to open background canvas (if it exists)
		self.canvas = cv2.imread(bg_gray, cv2.CV_8UC1)
		if self.canvas is not None:
			self.canvas = cv2.resize(self.canvas, (self.width, self.height))



	# a render method that will perform the pencil sketch

	def render(self, img_rgb):
		# convert RGB image to grayscale
		 img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
		 img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0 )
	   
		 img_blend = cv2.divide(img_gray, img_blur, scale=256)


		# if available, blend with background canvas
		 if self.canvas is not None:
			 img_blend = cv2.multiply(img_blend, self.canvas, scale=1./256)


		 return cv2.cvtColor(img_blend, cv2.COLOR_GRAY2RGB)



class WarmingFilter:
	"""Warming filter

	A class that applies a warming filter to an image.
	The class uses curve filters to manipulate the perceived color temperature
	of an image. The warming filter will shift the image's color spectrum
	towards red, away from blue.

	"""

	def __init__(self):
		"""Initialize look-up table for curve filter"""

		self.incr_ch_lut = self._create_LUT_8UC1([0, 64, 128, 192, 256],
												 [0, 70, 140, 210, 256])
		self.decr_ch_lut = self._create_LUT_8UC1([0, 64, 128, 192, 256],
												 [0, 30, 80, 120, 192])

	def render(self, img_rgb):
		"""Applies warming filter to an RGB image

			:param img_rgb: RGB image to be processed
			:returns: Processed RGB  image

		"""

		# warming filter: increase red, decrease blue
		c_r, c_g, c_b = cv2.split(img_rgb)
		c_r = cv2.LUT(c_r, self.incr_ch_lut).astype(np.uint8)
		c_b = cv2.LUT(c_b, self.decr_ch_lut).astype(np.uint8)
		img_rgb = cv2.merge((c_r, c_g, c_b))

		# increase color saturation
		c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
		c_s = cv2.LUT(c_s, self.incr_ch_lut).astype(np.uint8)

		return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)


	def _create_LUT_8UC1(self, x, y):
		"""Creates a look-up table using scipy's spline interpolation"""

		spl = UnivariateSpline(x, y)
		return spl(xrange(256))


class CoolingFilter:
	"""Cooling Filter

	A class that applies a cooling filter to an image. The class uses
	curve filters to manipulate the perceived color temperature of an 
	image. The warming filter will shift the image's color spectrum towards blue,
	away from red.

	"""

	def __init__(self):
		"""Initialize look-up table for curve filter"""

		self.incr_ch_lut = self._create_LUT_8UC1([0, 64, 128, 192, 256],
												 [0, 70, 140, 210, 256])
		self.decr_ch_lut = self._create_LUT_8UC1([0, 64, 128, 192, 256],
												 [0, 30, 80, 120, 192])

	def render(self, img_rgb):
		"""Applies warming filter to an RGB image

			:param img_rgb: RGB image to be processed
			:returns: Processed RGB  image

		"""

		# warming filter: increase red, decrease blue
		c_r, c_g, c_b = cv2.split(img_rgb)
		c_r = cv2.LUT(c_r, self.decr_ch_lut).astype(np.uint8)
		c_b = cv2.LUT(c_b, self.incr_ch_lut).astype(np.uint8)
		img_rgb = cv2.merge((c_r, c_g, c_b))

		# increase color saturation
		c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
		c_s = cv2.LUT(c_s, self.decr_ch_lut).astype(np.uint8)

		return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)


	def _create_LUT_8UC1(self, x, y):
		"""Creates a look-up table using scipy's spline interpolation"""

		spl = UnivariateSpline(x, y)
		return spl(xrange(256))




class Cartoonizer:
	"""Cartoonizer effect

	A class that applies a cartoon effect to an image.
	The class uses a bilateral filter and adaptive thresholding to create
	a cartoon effect.
	"""

	def __init__(self):
		pass

	def render(self, img_rgb):
		numDownSamples = 2             # Number of downscaling steps
		numBilateralFilters = 7		   # number of bilateral filtering steps

		# STEP 1
		# downsample image using Gaussian pyramid

		img_color = img_rgb
		for _ in xrange(numDownSamples):
			img_color = cv2.pyrDown(img_color)


		# repeatedly apply small bilateral filter instead of applying
		# one large filter
		for _ in xrange(numDownSamples):
			img_color = cv2.pyrUp(img_color)


		# STEPS 2 and 3
		# Convert to grayscale and apply median blur

		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
		img_blur = cv2.medianBlur(img_gray, 7)


		# STEP 4
		# detect and enhance edges

		img_edge = cv2.adaptiveThreshold(img_blur, 255,
										 cv2.ADAPTIVE_THRESH_MEAN_C,
										 cv2.THRESH_BINARY, 9, 2)


		# STEP 5
		# convert back to color so that it can bit-ANDed with color image
		img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
		return cv2.bitwise_and(img_color, img_edge)


