from PIL import Image

def median(kernel):
	sorted_kernal = []
	for x in xrange(len(kernel)):
		for y in xrange(len(kernel[x])):
			sorted_kernal.append(kernel[x][y])
	l = len(sorted_kernal)
	if l % 2 == 0:
		median = (sorted_kernal[int(l/2)] + sorted_kernal[int(l/2) - 1])/2
	else:
		median = sorted_kernal[int(l/2)]

	return median
	
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

def find_median_filter(pixels, kernel_size):
	median_filter = []
	for x in xrange(len(pixels)):
		median_filter.append([])
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
			median_filter[-1].append(median(kernel))
	return median_filter

def median_filter(pic='lena.bmp', kernel_size=5):
	im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)

	mfr = find_median_filter(r, kernel_size) 
	mfg = find_median_filter(g, kernel_size)
	mfb = find_median_filter(b, kernel_size)

	median_filter_image =  Image.new( 'RGB', (h, w), "black")
	mfi = median_filter_image.load()
	for i in xrange(h):
		for j in xrange(w):
			mfi[i, j] = (mfr[i][j], mfg[i][j], mfb[i][j])
	median_filter_image.show()
	return median_filter_image

if __name__ == '__main__':
	median_filter()