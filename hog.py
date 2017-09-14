from PIL import Image
import math

grad_x = [[1, 0, -1],
		[2, 0, -2],
		[1, 0, -1]]

ones = [[1, 2, 3],
		[4, 5, 6],
		[7, 8, 9]]

grad_y = [[1, 2, 1],
		[0, 0, 0],
		[-1, -2, -1]]

def apply_filter(a, b):
	ans = 0
	for i in xrange(len(a)):
		for j in xrange(len(b)):
				ans += 	(a[len(a) - i - 1][ len(a) - j - 1] * b[i][j])	
	return ans

def seg_rgb_image(pixels, h, w, r, g, b):
	for i in xrange(h):
		for j in xrange(w):
			tr, tg, tb = pixels[i,j]
			r[i, j] = (tr, 0, 0)
			g[i, j] = (0, tg, 0)
			b[i, j] = (0, 0, tb)
	return r, g, b

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

def find_sobel(pixels, h, w, display=False):
	r, g, b = seg_rgb(pixels, h, w)
	msrx = []
	msry = []
	msgx = []
	msgy = []
	msbx = []
	msby = []
	
	if display:
		irx =  Image.new( 'RGB', (h, w), "black")
		srx = irx.load()
		iry =  Image.new( 'RGB', (h, w), "black")
		sry = iry.load()
		
		igx =  Image.new( 'RGB', (h, w), "black")
		sgx = igx.load()
		igy =  Image.new( 'RGB', (h, w), "black")
		sgy = igy.load()

		ibx =  Image.new( 'RGB', (h, w), "black")
		sbx = ibx.load()
		iby =  Image.new( 'RGB', (h, w), "black")
		sby = iby.load()
	
	msrx.append([])
	msry.append([])
	msgx.append([])
	msgy.append([])
	msbx.append([])
	msby.append([])		
	for i in xrange(w):
		msrx[-1].append(0)
		msry[-1].append(0)
		msgx[-1].append(0)
		msgy[-1].append(0)
		msbx[-1].append(0)
		msby[-1].append(0)

	for i in xrange(1, h-1):
		msrx.append([0])
		msry.append([0])
		msgx.append([0])
		msgy.append([0])
		msbx.append([0])
		msby.append([0])
		for j in xrange(1, w-1):
			
			red = [[r[i-1][j - 1], r[i-1][j], r[i-1][j + 1]],
				[r[i][j - 1], r[ i][ j], r[i][j + 1]],
				[r[i+1][ j - 1], r[i+1][j], r[i+1][j + 1]]]
			#srx.append(( int(math.ceil(math.sqrt((apply_filter(grad_x, red) * apply_filter(grad_x, red)) + (apply_filter(grad_y, red) * apply_filter(grad_y, red))))), 0, 0))
			trX = apply_filter(grad_x, red)
			trY = apply_filter(grad_y, red)
			msrx[-1].append(trX)
			msry[-1].append(trY)
			
			if display:	
				srx[i, j] = (trX, 0, 0)
				sry[i, j] = (trY, 0, 0)

			green = [[g[i-1][ j - 1], g[i-1][j], g[i-1][ j + 1]],
				[g[i][ j - 1], g[i][ j], g[i][ j + 1]],
				[g[i+1][ j - 1], g[i+1][ j], g[i+1][ j + 1]]]
			#sgx.append((0, int(math.ceil(math.sqrt((apply_filter(grad_x, green) * apply_filter(grad_x, green)) + (apply_filter(grad_y, green) * apply_filter(grad_y, green))))), 0))
			tgX = apply_filter(grad_x, green)
			tgY = apply_filter(grad_y, green)
			msgx[-1].append(tgX)
			msgy[-1].append(tgY)
			
			if display:
				sgx[i,j] = (0, tgX, 0)
				sgy[i,j] = (0, tgY, 0)

			blue = [[b[i-1][ j - 1], b[i-1][ j], b[i-1][ j + 1]],
				[b[i][ j - 1], b[i][ j], b[i][j + 1]],
				[b[i+1][ j - 1], b[i+1][ j], b[i+1][ j + 1]]]
			#sbx.append((0, 0, int(math.ceil(math.sqrt((apply_filter(grad_x, blue) * apply_filter(grad_x, blue)) + (apply_filter(grad_y, blue) * apply_filter(grad_y, blue)))))))
			tbX = apply_filter(grad_x, blue)
			tbY = apply_filter(grad_y, blue)
			msbx[-1].append(tbX)
			msby[-1].append(tbY)
			
			if display:
				sbx[i, j] = (0, 0, tbX)
				sby[i, j] = (0, 0, tbY)

		msrx[-1].append(0)
		msry[-1].append(0)
		msgx[-1].append(0)
		msgy[-1].append(0)
		msbx[-1].append(0)
		msby[-1].append(0)

	msrx.append([])
	msry.append([])
	msgx.append([])
	msgy.append([])
	msbx.append([])
	msby.append([])		
	for i in xrange(w):
		msrx[-1].append(0)
		msry[-1].append(0)
		msgx[-1].append(0)
		msgy[-1].append(0)
		msbx[-1].append(0)
		msby[-1].append(0)

		
	if display:
		irx.show()
		iry.show()
		igx.show()
		igy.show()
		ibx.show()
		iby.show()

	return msrx, msry, msgx, msgy, msbx, msby

def get_max(arr):
	maxVal = 0
	maxPos = 0
	for i, a in enumerate(arr):
		if a > maxVal:
			maxVal = a
			maxPos = i
	return maxPos
			
def get_mag_angle(rx, ry, gx, gy, bx, by, h, w):
	mag = []
	angle = []
	stream = ''
	for i in xrange(h):
		mag.append([])
		angle.append([])
		for j in xrange(w):
			tx = 0
			ty = 0
			sel = get_max([math.sqrt((rx[i] [j] * rx[i][j]) + (ry[i][j] * ry[i][j])), math.sqrt((gx[i][j] * gx[i][j]) + (gy[i][j] * gy[i][j])), math.sqrt((bx[i][j] * bx[i][j]) + (by[i][j]* by[i][j]))])
			#print sel
			
			if sel == 0:
				tx = rx[i][j]
				ty = ry[i][j]
			elif sel == 1:
				tx = gx[i][j]
				ty = gy[i][j]
			elif sel == 2:
				tx = bx[i][j]
				ty = by[i][j]
					
			tempAngle = 0

			if tx != 0:
				tempAngle = math.atan(ty/tx)
			else:
				if ty >= 0:
					tempAngle = 3.14/2
				else :
					tempAngle = - 3.14/2

			tempAngle *= 57.2958
			if tempAngle < 0:
				tempAngle += 180
			
			mag[-1].append(math.sqrt((tx * tx) + (ty * ty)))
			angle[-1].append(tempAngle)
			
	return mag, angle

def get_histogram(mag, angle, h, w):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in xrange(h):
		for j in xrange(w):
			bin1 = (int(angle[i][j]/20)) % 9
			bin2 = (bin1 + 1) % 9
			if angle[i][j] == 180:
				bins[8] += mag[i][j]
			else:	
				temp = angle[i][j] - (bin1 * 20)
				per1 = temp/20
				per2 = 1 - per1
				bins[bin1] += (mag[i][j] * per2)
				bins[bin2] += (mag[i][j] * per1)
	return bins

def histogram(mag, angle, h, w):
	hist = []
	i = 0
	while i < h:
		hist.append([])
		j = 0
		while j < w:
			tempMag = []
			tempAngle = []
			k   =  0
			while k < 8:
				tempMag.append([])
				tempAngle.append([])
				l = 0
				while l < 8:
					tempMag[-1].append(mag[i+k][j+l])
					tempAngle[-1].append(angle[i+k][j+l])
					l += 1
				k += 1	
			hist[-1].append(get_histogram(tempMag, tempAngle, k, l))
			j += 8			
		i += 8	
	return hist

def normalize(hists):
	maxVal = 0
	for hist in hists:
		for val in hist:
			maxVal += (val * val)
	maxVal = math.sqrt(maxVal)
	feature_vector = []
	for hist in hists:
		for val in hist:
			if maxVal == 0:
				print hists
			else:	
				feature_vector.append(val/maxVal)

	return feature_vector

def normalized_bins(histograms):
	feature_vector = []
	for i in xrange(len(histograms)-1):
		for j in xrange(len(histograms[i])-1):
			tempHist = []
			k = 0
			while k < 2:
				l = 0
				while l < 2:
					tempHist.append(histograms[i+k][j+l])
					l += 1
				k += 1
			feature_vector.extend(normalize(tempHist))
	return feature_vector			

def get_features(name):
	im = Image.open(name)
	pixels = im.load()
	h, w = im.size
	r =  Image.new( 'RGB', (h, w), "black")
	rp = r.load()
	g =  Image.new( 'RGB', (h, w), "black")
	gp = g.load()
	b =  Image.new( 'RGB', (h, w), "black")
	bp = b.load()

	rp, gp, bp = seg_rgb_image(pixels, h , w,  rp, gp, bp)
	
	#im.show()	
	#r.show()
	#g.show()
	#b.show()

	rx, ry, gx, gy, bx, by = find_sobel(pixels, h, w)
	mag, angle = get_mag_angle(rx, ry, gx, gy, bx, by, h, w)
	hists = histogram(mag, angle, h, w)
	feature_vector = normalized_bins(hists)
	return feature_vector

if __name__ == '__main__':	
	vector = get_features("train/1.png")
	print vector