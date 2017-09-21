import gaussian
import sobel
from PIL import Image
import math

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
			
			mag[-1].append(math.sqrt((tx * tx) + (ty * ty)))
			angle[-1].append(tempAngle)
			
	return mag, angle

def non_maxima_suppression(mag, angle):
	localMaxima = []
	localMaximaImage =  Image.new( 'L', (len(angle), len(angle[0])), "black")
	pixels = localMaximaImage.load()
	for i in xrange(len(angle)):
		localMaxima.append([])
		for j in xrange(len(angle[i])):
			localMaxima[-1].append(0)
			if angle[i][j] <= -67.5 or angle[i][j] > 67.5:
				localMaxima[-1][-1] = mag[i][j]
				if i > 0:
					if mag[i-1][j] > mag[i][j]:
						localMaxima[-1][-1] = 0

				if i + 1 < len(angle):
					if mag[i+1][j] > mag[i][j]:
						localMaxima[-1][-1] = 0

			elif angle[i][j] <= -22.5 and angle[i][j] > -67.5:
				localMaxima[-1][-1] = mag[i][j]
				if j > 0 and i + 1 < len(angle):
					if mag[i+1][j-1] > mag[i][j]:
						localMaxima[-1][-1] = 0

				if j + 1 < len(angle[i]) and i > 0:
					if mag[i-1][j+1] > mag[i][j]:
						localMaxima[-1][-1] = 0

			elif angle[i][j] <= 22.5 and angle[i][j] > -22.5:
				localMaxima[-1][-1] = mag[i][j]
				if j > 0:
					if mag[i][j-1] > mag[i][j]:
						localMaxima[-1][-1] = 0

				if j + 1 < len(angle[i]):
					if mag[i][j+1] > mag[i][j]:
						localMaxima[-1][-1] = 0

			
			elif angle[i][j] <= 67.5 and angle[i][j] > 22.5:
				localMaxima[-1][-1] = mag[i][j]
				if i + 1 < len(angle) and j + 1 < len(angle[i]):
					if mag[i+1][j+1] > mag[i][j]:
						localMaxima[-1][-1] = 0

				if j > 0 and i > 0:
					if mag[i-1][j-1] > mag[i][j]:
						localMaxima[-1][-1] = 0
			pixels[i, j] = (int(localMaxima[-1][-1]),)
	localMaximaImage.show()
	return localMaxima					

def not_all_visited(visited):
	for i in visited:
		for j in i:
			if j != 0:
				return True
	return False
			
def hysteresis_thresholding(local_maxima, higher=30, lower=10):
	gh = []
	gl = []
	visited = []
	ghImage =  Image.new( 'L', (len(local_maxima), len(local_maxima[0])), "black")
	pixels = ghImage.load()
	
	for i in xrange(len(local_maxima)):
		gh.append([])
		gl.append([])
		visited.append([])
		for j in xrange(len(local_maxima[i])):
			visited[-1].append(0)
			if local_maxima[i][j] >= higher:
				gh[-1].append(local_maxima[i][j])
				visited[-1][-1] = 1
				pixels[i,j] = (int(local_maxima[i][j]),)
				gl[-1].append(0)
			elif local_maxima[i][j] >= lower:
				gh[-1].append(0)
				gl[-1].append(local_maxima[i][j])
			else:
				gh[-1].append(0)
				gl[-1].append(0)

	while not_all_visited(visited):
		for i in xrange(len(gh)):
			for j in xrange(len(gh[i])):
				if gh[i][j] != 0 and visited[i][j] == 1:
					visited[i][j] = 0
					for x in xrange(3):
						for y in xrange(3):
							pos_x = x - 1
							pos_y = y - 1
							if i + pos_x >= 0 and i + pos_x < len(gh) and j + pos_y >= 0 and j + pos_y < len(gh[i]):
								if gh[i+pos_x][j+pos_y] == 0 and gl[i+pos_x][j+pos_y] != 0:
									gh[i+pos_x][j+pos_y] = gl[i+pos_x][j+pos_y]
									pixels[i+pos_x,j+pos_y] = (int(gl[i+pos_x][j+pos_y]),)
									visited[i+pos_x][j+pos_y] = 1
								
	ghImage.show()
	return gh

def canny(pic='lena_top.jpg', kernel=9, img=None):
	im = None
	if img != None:
		im = img
	else:
		im = Image.open(pic)

	h, w = im.size	
	im = gaussian.gaussian(img=im)
	rx, ry, gx, gy, bx, by = sobel.sobel(max=False, img=im)
	mag, angle = get_mag_angle(rx, ry, gx, gy, bx, by, h, w)
	local_maxima = non_maxima_suppression(mag, angle)
	gh = hysteresis_thresholding(local_maxima)

if __name__ == '__main__':
	canny()