from PIL import Image
import math
import sys

def gaussian_func(x, y, sigma=2.84089642):
	result = math.exp(-((x*x) + (y*y))/(2 * sigma * sigma))/(2 * sigma * sigma * math.pi)
	return result

def kernel_calculation(kernel):
	ele_sum = 0
	for x in xrange(len(kernel)):
		for y in xrange(len(kernel[x])):
			#print (len(kernel) - x - 1), (len(kernel[x]) - y - 1)
			ele_sum += (gaussian_func(len(kernel) - x - 1, len(kernel[x]) - y - 1) * kernel[x][y])
	#print kernel
	#print ele_sum
	return int(ele_sum)

def seg_rgb(pixels, h, w):
	r = []
	g = []
	b = []
	for i in xrange(h):
		r.append([])
		g.append([])
		b.append([])
		for j in xrange(w):
			tr, tg, tb = pixels[i,j]
			r[-1].append(tr)
			g[-1].append(tg)
			b[-1].append(tb)
	return r, g, b

def find_gaussian(pixels, kernel_size):
	gaussian = []
	for i in xrange(len(pixels)):
		gaussian.append([])
		for j in xrange(len(pixels[i])):
			kernel = []
			mid = int(kernel_size/2)
			for x in xrange(kernel_size):
				kernel.append([])
				for y in xrange(kernel_size):
					l = x - mid
					m = y - mid
					pos_x = i + l
					pos_y = j + m
					#print pos_x, pos_y
					if pos_x < 0 or pos_x >= len(pixels) or pos_y < 0 or pos_y >= len(pixels[i]):
						kernel[-1].append(0)
					else:
						kernel[-1].append(pixels[pos_x][pos_y])						
			#print pixels[i][j], kernel_calculation(kernel)
			gaussian[-1].append(kernel_calculation(kernel))
			
	return gaussian

def gaussian(pic='lena.bmp', kernel_size=5):
	if kernel_size <= 1:
		print "Please select a bigger kernel size"
		sys.exit(0)

	elif kernel_size % 2 == 0:
		print "Please select odd kernel size"
		sys.exit(0)

	im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)
	
	gr = find_gaussian(r, kernel_size)
	gg = find_gaussian(g, kernel_size)
	gb = find_gaussian(g, kernel_size)
	
	gaussian_image =  Image.new( 'RGB', (h, w), "black")
	gi = gaussian_image.load()
	for i in xrange(h):
		for j in xrange(w):
			gi[i, j] = (gr[i][j], gg[i][j], gb[i][j])
	gaussian_image.show()

if __name__ == '__main__':
	gaussian()
	'''
	kernel = []
	for i in xrange(5):
		kernel.append([])
		for j in xrange(5):
			kernel[-1].append(1)
	print find_gaussian(kernel, 5)
	'''
