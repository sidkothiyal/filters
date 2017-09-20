import gaussian
import sobel
from PIL import Image

def canny(pic='lena.bmp', kernel=11, img=None):
	im = None
	if img != None:
		im = img
	else:
		im = Image.open(pic)

	im = gaussian.gaussian(img=im)
	rx, ry, gx, gy, bx, by = sobel.sobel(max=False, img=im)
	
	pixels = im.load()
	h, w = im.size

if __name__ == '__main__':
	canny()