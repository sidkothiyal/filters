from PIL import Image

def get_image(r=None, g=None, b=None, l=None):
	im = None
	im_type = None
	if l == None and (r != None and g!= None and b!= None):
		im = Image.new("RGB", (len(r), len(r[0])), "black")
		im_type = "rgb"
	elif l != None:
		im = Image.new("L", (len(l), len(l[0])), "black")
		im_type = "l"
	else:
		return None	

	h, w = im.size
	pixels = im.load()
	for i in xrange(h):
		for j in xrange(w):
			if im_type == "rgb":
				pixels[i, j] = (r[i][j], g[i][j], b[i][j])
			elif im_type == "l":
				pixels[i, j] = (l[i][j],)

	return im				