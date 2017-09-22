from PIL import Image
import math
import arr2image

grad_x = [[1, 0, -1],
		[2, 0, -2],
		[1, 0, -1]]

grad_y = [[1, 2, 1],
		[0, 0, 0],
		[-1, -2, -1]]

def get_max(arr):
	maxVal = 0
	maxPos = 0
	for i, a in enumerate(arr):
		if a > maxVal:
			maxVal = a
			maxPos = i
	return maxPos

def apply_filter(a, b):
	ans = 0
	for i in xrange(len(a)):
		for j in xrange(len(b)):
				ans += 	(a[len(a) - i - 1][ len(a) - j - 1] * b[i][j])	
	return ans

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

def find_sobel_max(pixels, h, w):
	r, g, b = seg_rgb(pixels, h, w)
	ix = []
	iy = []
	
	ix.append([])
	iy.append([])
	for i in xrange(w):
		ix[-1].append(0)
		iy[-1].append(0)

	for i in xrange(1, h-1):
		ix.append([0])
		iy.append([0])
		for j in xrange(1, w-1):
			
			red = [[r[i-1][j - 1], r[i-1][j], r[i-1][j + 1]],
				[r[i][j - 1], r[ i][ j], r[i][j + 1]],
				[r[i+1][ j - 1], r[i+1][j], r[i+1][j + 1]]]
			trX = apply_filter(grad_x, red)
			trY = apply_filter(grad_y, red)
			
			green = [[g[i-1][ j - 1], g[i-1][j], g[i-1][ j + 1]],
				[g[i][ j - 1], g[i][ j], g[i][ j + 1]],
				[g[i+1][ j - 1], g[i+1][ j], g[i+1][ j + 1]]]
			
			tgX = apply_filter(grad_x, green)
			tgY = apply_filter(grad_y, green)
			
			blue = [[b[i-1][ j - 1], b[i-1][ j], b[i-1][ j + 1]],
				[b[i][ j - 1], b[i][ j], b[i][j + 1]],
				[b[i+1][ j - 1], b[i+1][ j], b[i+1][ j + 1]]]
			tbX = apply_filter(grad_x, blue)
			tbY = apply_filter(grad_y, blue)
			
			pos = get_max([math.sqrt((trX*trX) + (trY*trY)), math.sqrt((tgX*tgX) + (tgY*tgY)), math.sqrt((tbX*tbX) + (tbY*tbY))])
			if pos == 0:
				ix[-1].append(trX)
				iy[-1].append(trY)
			elif pos == 1:
				ix[-1].append(tgX)
				iy[-1].append(tgY)
			elif pos == 2:
				ix[-1].append(tbX)
				iy[-1].append(tbY)
				
		ix[-1].append(0)
		iy[-1].append(0)
		
	ix.append([])
	iy.append([])
	for i in xrange(w):
		ix[-1].append(0)
		iy[-1].append(0)
		
	return ix, iy

def multiply_element_by_element(x, y):
	ans = []
	for i in xrange(len(x)):
		ans.append([])
		for j in xrange(len(x[i])):
			ans[-1].append(x[i][j] * y[i][j])
	return ans

def gaussian_func(x, y, sigma=4.0):
	result = math.exp(-((x*x) + (y*y))/(2 * sigma * sigma))/(2 * sigma * sigma * math.pi)
	return result

def kernel_calculation(kernel):
	ele_sum = 0
	mid = int(len(kernel)/2)
	for x in xrange(len(kernel)):
		for y in xrange(len(kernel[x])):
			#print (len(kernel) - x - 1), (len(kernel[x]) - y - 1)
			ele_sum += (gaussian_func(len(kernel) - x - 1 - mid, len(kernel[x]) - y - 1 - mid) * kernel[x][y])
	#print kernel
	#print ele_sum
	return int(ele_sum)

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

def harris_point(pixels, gix2, giy2, gixy, alpha=0.05):
	for i in xrange(len(gixy)):
		for j in xrange(len(gixy[i])):
			harr = (gix2[i][j] * giy2[i][j]) - (gixy[i][j] * gixy[i][j]) - (alpha * (gix2[i][j] + giy2[i][j])* (gix2[i][j] + giy2[i][j]))
			if harr < 0:
				pixels[i,j] = (255, 0, 0)

def harris(pic='lena.bmp', kernel=9, img=None):
	im = None
	if img != None:
		im = img
	else:
		im = Image.open(pic)

	im.show()
	
	h, w = im.size
	pixels = im.load()
	ix, iy = find_sobel_max(pixels, h, w)

	ix2 = multiply_element_by_element(ix, ix)
	iy2 = multiply_element_by_element(iy, iy)
	ixy = multiply_element_by_element(ix, iy)

	gix2 = find_gaussian(ix2, 3)
	giy2 = find_gaussian(iy2, 3)
	gixy = find_gaussian(ixy, 3)

	im2 = arr2image.get_image(l=gix2)
	im2.show()

	im2 = arr2image.get_image(l=giy2)
	im2.show()

	im2 = arr2image.get_image(l=gixy)
	im2.show()


	harris_point(pixels, gix2, giy2, gixy)

	im.show()

if __name__ == '__main__':
	harris()