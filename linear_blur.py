from PIL import Image

def blur_it(kernel):
	sum_ele = 0
	for x in xrange(len(kernel)):
		for y in xrange(len(kernel[x])):
			sum_ele += (kernel[3 - x - 1][3 - y - 1] * 1)
	return sum_ele/9
		
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

def find_linear_blur(pixels, kernel_size):
	linear_blur = []
	for x in xrange(len(pixels)):
		linear_blur.append([])
		for y in xrange(len(pixels[x])):
			kernel = []
			mid = int(kernel_size/2)
			for i in xrange(kernel_size):
				kernel.append([])
				for j in xrange(kernel_size):
					if (i + x - mid) < 0 or (j + y - mid) < 0 or (i + x - mid) >= len(pixels) or (j + y - mid) >= len(pixels[x]):
						kernel[-1].append(0)
					else:
						kernel[-1].append(pixels[i + x - mid][j + y - mid])
			linear_blur[-1].append(blur_it(kernel))
	return linear_blur

def linear_blur(pic='lena.bmp', kernel_size=5, img=None):
	im = None
	if img != None:
		im = img
	else:
		im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)

	lbr = find_linear_blur(r, kernel_size) 
	lbg = find_linear_blur(g, kernel_size)
	lbb = find_linear_blur(b, kernel_size)

	linear_blur_image =  Image.new( 'RGB', (h, w), "black")
	lbi = linear_blur_image.load()
	for i in xrange(h):
		for j in xrange(w):
			lbi[i, j] = (lbr[i][j], lbg[i][j], lbb[i][j])
	linear_blur_image.show()
	return linear_blur_image

if __name__ == '__main__':
	linear_blur()