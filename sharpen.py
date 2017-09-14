from PIL import Image
import multiply
import linear_blur

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

def find_sharpen(multiply, linear_blur, pixels):
	sharpen = []
	for i in xrange(len(multiply)):
		sharpen.append([])
		for j in xrange(len(multiply[i])):
			sharpen[-1].append(multiply[i][j] - linear_blur[i][j] + pixels[i][j])
	return sharpen		

def sharpen(pic='lena.bmp', sharpen_times=2):
	im = Image.open(pic)
	pixels = im.load()
	h, w = im.size
	r, g, b = seg_rgb(pixels, h, w)

	multiply_image = multiply.multiply(pic, sharpen_times)
	multiply_pixels = multiply_image.load()
	mh, mw = multiply_image.size
	mr, mg, mb = seg_rgb(multiply_pixels, mh, mw)

	linear_blur_image = linear_blur.linear_blur(pic)
	linear_blur_pixels = linear_blur_image.load()
	lbh, lbw = linear_blur_image.size
	lbr, lbg, lbb = seg_rgb(linear_blur_pixels, lbh, lbw)

	sr = find_sharpen(r, mr, lbr) 
	sg = find_sharpen(g, mg, lbg)
	sb = find_sharpen(b, mb, lbb)


	sharpen_image =  Image.new( 'RGB', (mh, mw), "black")
	si = sharpen_image.load()
	for i in xrange(mh):
		for j in xrange(mw):
			si[i, j] = (sr[i][j], sg[i][j], sb[i][j])
	sharpen_image.show()
	return sharpen_image

if __name__ == '__main__':
	sharpen()