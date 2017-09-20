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

def find_multiply(pixels, multiply_times):
	multiply = []
	for x in xrange(len(pixels)):
		multiply.append([])
		for y in xrange(len(pixels[x])):
			multiply[-1].append(multiply_times * pixels[x][y])
	return multiply

def multiply(pic='lena.bmp', multiply_times=2, img=None):
	im = None
	if img != None:
		im = img
	else:	
		im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)

	sr = find_multiply(r, multiply_times) 
	sg = find_multiply(g, multiply_times)
	sb = find_multiply(b, multiply_times)

	multiply_image =  Image.new( 'RGB', (h, w), "black")
	si = multiply_image.load()
	for i in xrange(h):
		for j in xrange(w):
			si[i, j] = (sr[i][j], sg[i][j], sb[i][j])
	multiply_image.show()
	return multiply_image

if __name__ == '__main__':
	multiply()