import cv2
import matplotlib.pyplot as plt
import numpy as np

def plot_image(image, name="", plt_show=True):
	'''
	Plots one image
	:param image: the image to plot
	:param img_shape: the shape of the image
	:param plt_show: debug parameter, if false it wont plot the image
	:param number of color channels, 1 for greyscale and 3 for color
	:param name: title of image default: ""
	'''

	img_shape = np.asarray(image).shape

	fig = plt.figure()
	fig.canvas.set_window_title(name)
	plt.title(name)
	if len(img_shape) == 4:
		cpy = image.reshape((img_shape[0], img_shape[1], 4))
		cv2.imwrite("output/cpy.png", cpy)
		cpy = cv2.imread("output/cpy.png")
		cpy = cv2.cvtColor(cpy, cv2.COLOR_BGR2RGB)
		plt.imshow(cpy, interpolation='nearest')
	elif len(img_shape) == 3:
		cpy = image.reshape((img_shape[0], img_shape[1], 3))
		cpy = cv2.cvtColor(cpy, cv2.COLOR_BGR2RGB)
		cv2.imwrite("output/cpy.png", cpy)
		cpy = cv2.imread("output/cpy.png")
		plt.imshow(cpy, interpolation='nearest')
	else:
		cv2.imwrite("output/cpy.png", image)
		cpy = cv2.imread("output/cpy.png")
		plt.imshow(cpy, interpolation='nearest', cmap='gray')

	if plt_show == True:
		plt.show()

def canny_fill(img, height, width, bottom, threshold=0):
	"""
	Fills the space between two lines on a vertical plane

	Example: If you have an image:
	OOOOOOOOOOO
	###########
	OOOOOOOOOOO
	###########
	OOOOOOOOOOO

	where
	# represents within threshold
	O represents any color
	@ represents white

	then the output image would be
	OOOOOOOOOOO
	###########
	###########
	###########
	OOOOOOOOOOO

	:param img: the image to process
	:param height: the height of the input image
	:param width: the width of the input image
	:param bottom: The highest point of search space
	:param threshold: a threshold that say how big a value can be before its detected as a white pixel, Default: 0
	:return: the processed image
	"""

	# create a copy of image to avoid editing the original image
	img = np.copy(img)

	for hor in range(width):
		found = False
		unfound = False

		for vert in range(bottom, height):

			pxl = img[vert][hor]

			# if a white pixel has been found in this column but it has not found a second pixel, make current pixel white
			if found:
				img[vert][hor] = 255


			# if current pixel is bigger than the set threshold
			if pxl > threshold:
				# then check if it is done
				if found & unfound :
					break
				# if not done then check if it is the first white pixel found
				elif (not found):
					found = True

			# lastly check if a second white pixel has been found to avoid filling all the way to the bottom of image
			elif (pxl == 0) & (found):
				unfound = True
	return img

def rm_green(img, height, width, r_threshold=80, g_threshold=90, b_threshold=80):
	"""
	Makes the any pixel within a color range white and any pixel above that pixel white.
	Can be used for removing redundant information if you have a color boundary.
	Example: If you have an image:
	OOOOOOOOOOO
	#O#########
	O#OO###OO##
	OOOOOOOOOOO
	OOOOOOOOOOO

	where
	# represents within threshold
	O represents any color
	@ represents white

	then the output image would be
	@@@@@@@@@@@
	@O@@@@@@@@@
	O@OO@@@OO@@
	OOOOOOOOOOO
	OOOOOOOOOOO


	:param img: the image to process
	:param height: the height of the input image
	:param width: the width of the input image
	:param r_threshold: the threshold for the red color range
	:param g_threshold: the threshold for the green color range
	:param b_threshold: the threshold for the blue color range
	:return: the processed image and the lowest non white pixel
	"""

	# create a copy of image to avoid editing the original image
	green = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	bottom = height
	for hor in range(width):
		found = False
		for vert in range(height):
			# reverses the range, if range(0,3) then hori and verti start at 3 and stop at 0
			hori = width - hor - 1
			verti = height - vert - 1

			# if a pixel within the threshold boundary has been found, then make the whole column white above said pixel
			if found:
				green[verti][hori] = 255
			else:
				# if the pixel is within the threshold boundary then set found to true and
				# change the pixel at that point to be white
				if green[verti][hori][0] < r_threshold:
					if green[verti][hori][1] > g_threshold:
						if green[verti][hori][2] < b_threshold:
							found = True
							green[verti][hori] = 255
							if verti < bottom:
								bottom = verti
	return green, bottom

def rm_line(img, height, width):
	"""
	Looks at the bottom line of the image and if a pixel is white, then make all pixels above it black
	:param img: the image to process
	:param height: the height of the input image
	:param width: the width of the input image
	:return: the processed image
	"""

	# create a copy of image to avoid editing the original image
	line = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	x = height - 1
	for i in range(width):
		# if the pixel at the bottom is white then remove any pixels above it
		if (line[x][i][0] == 255) & (line[x][i][0] == 255) & (line[x][i][0] == 255):
			cv2.line(line, (i, 0), (i, height), (0, 0, 0), 1)

	return line


def process(img):
	# set height and width
	height = img.shape[0]
	width = img.shape[1]

	# starts a timer
	import time
	start = time.time()

	strength = 50

	highlight = np.copy(img)
	highlight[np.where((highlight < [strength, strength, strength]).all(axis=2))] = [0, 255, 0]

	# create blur kernel
	kernel = np.ones((2, 2), np.float32) / (2 * 2)

	# blur image (Only use blur if needed. Lower resolution need less blur. Changing kernel can help too.)
	blur = cv2.filter2D(highlight, -1, kernel)


	# removes the green top of the image
	green, top = rm_green(blur, height, width)                                             # slow (cpp) = 0.148861885

	# ends the timer
	end = time.time()

	print(end-start)
	########
	# optimization notes:
	# numbers are the best of 3 attempts
	# optimized for 200x200 0.432s -> 0.314s -> 0.156s -> 0.147s -> 0.136s -> 0.132s -> 0.118
	########

	return img, highlight, blur, green


def plot_process(imgs):
	names = []
	names.append("Original image")
	names.append("Highlight edge")
	names.append("Blurred edge")
	names.append("Remove above edge")

	for i in range(len(imgs)):
		plot_image(imgs[i], names[i])

def plot_one(img, name):
	# plotting
	plot_image(img, name=name)

def get_images(path):
	import glob
	images = []
	for filename in glob.glob(path):  # assuming gif
		image = cv2.imread(filename)
		images.append(image)
	return images

def main():
	# read image from file
	images = get_images('input/*.png')


	for img in images:
		img = cv2.resize(img, (200, 200))
		imgs = process(img)
		plot_process(imgs)
		# plot_image(imgs[-1])


if __name__ == '__main__':
	main()
