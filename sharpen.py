from PIL import Image

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

def find_sharpen(pixels, sharpen_times):
	sharpen = []
	for x in xrange(len(pixels)):
		sharpen.append([])
		for y in xrange(len(pixels[x])):
			sharpen[-1].append(sharpen_times * pixels[x][y])
	return sharpen

def sharpen(pic='lena.bmp', sharpen_times=2):
	im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)

	sr = find_sharpen(r, sharpen_times) 
	sg = find_sharpen(g, sharpen_times)
	sb = find_sharpen(b, sharpen_times)

	sharpen_image =  Image.new( 'RGB', (h, w), "black")
	si = sharpen_image.load()
	for i in xrange(h):
		for j in xrange(w):
			si[i, j] = (sr[i][j], sg[i][j], sb[i][j])
	sharpen_image.show()
	return sharpen_image

if __name__ == '__main__':
	sharpen()