## Post-it notes :)

from image import Img
from math import atan, degrees, sin, cos, tan, radians, floor, ceil

def calcArea(startX:int, startY:int, endX:int, endY:int) -> int:
	deltaX = endX - startX
	deltaY = endY - startY
	return deltaX * deltaY

# NOTE: background is orange here so red and green should be valued at less
def getDarkness(img, x:int, y:int) -> int: # returns int (0 -> 255)
	return img.getRGBVal(x, y)[1]

def getAverageDarkness(img, startX:int, startY:int, endX:int, endY:int) -> int: # returns int (0 -> 255)
	total = 0
	for i in range((endX - startX)):
		for j in range(endY - startY):
			try: # TMP fix
				total += getDarkness(img, startX + i, startY + j)
			except:
				print("OUT OF RANGE!")
				break
	if calcArea(startX, startY, endX, endY) != 0:
		return (total // calcArea(startX, startY, endX, endY))
	else:
		print("0 AREA")
		return 0

def isCircleInRect(img, startX:int, startY:int, endX:int, endY:int) -> int: # length is length of line
	total = 0
	w = (endX - startX)
	h = (endY - startY)
	m = (h // w)
	length = (((endX - startX) ** 2) + ((endY - startY) ** 2) ** 0.5)
	centre = ((startX + (w // 2)), (startY + (h // 2)))
	for x in range(startX, w):
		y = m * x
		try:
			total += getDarkness(img, x, y) * ((((centre[0] - x) ** 2) + ((centre[1] - y) ** 2)) ** 0.5)
		except:
			total += 0
	tmp = total // length
	print(tmp)
	return tmp

# set vert to True for vertical lines and False for horizontal lines
def isLine(img, xPos:int, yPos:int, r:int, vert:bool) -> bool: # r radius of circle
	i = 0
	while i < 360:
		if getDarkness(img,xPos + (r*cos(radians(i))),yPos + (r*sin(radians(i)))) < 200:
			# TODO: look into using the angle data (line when ang = 0)
			if vert == True:
				return (floor(xPos + (r*cos(radians(i)))), i)
			return (floor(yPos + (r*sin(radians(i)))), i)
		i += 0.1
	return False

def normaliseLighting(img):
	out = Img(img.getPath())
	for x in range(img.getSize()[0]):
		for y in range(img.getSize()[1]):
			val = img.getRGBVal(x, y)
			R = (val[0]) 
			G = (val[1] // 100) * 100
			B = (val[2])
			if R + G > 255:
				R = 0
				G = 255
				B = 0
			out.setRGB(x, y, R, G, B)
	
	out.save("input/lights.jpg")
	return out

def isCenteredCircle(img, startX:int, startY:int, endX:int, endY:int) -> int:
	total = 0
	centreX = (endX - startX) // 2
	centreY = (endY - startY) // 2
	for x in range(endX - startX):
		for y in range(endY - startY):
			mod = ((centreX - x) **2)+ ((centreY - y) **2) **0.5
			#print("MOD:", mod)
			total += getDarkness(img, startX + x, startY + y)
			#total += mod
	return ((total // calcArea(startX, startY, endX, endY)))

def fillLine(img, startX:int, startY:int, ang:int, length:int, RGB:tuple) -> None:
	ang = radians(ang)
	for i in range(length):
		img.setRGB(startX + i*cos(ang), startY + i*sin(ang), RGB[0], RGB[1], RGB[2])

def centredDarkness(img, startX:int, startY:int, endX:int, endY:int, scaleFactor:int) -> int: # (0 -> 255)
	kw = (endX - startX) // scaleFactor
	kh = (endY - startY) // scaleFactor
	return getAverageDarkness(img, ((endX + startX) - kw) // 2, ((endY + startY) - kw) // 2, ((endX + startX) + kw) // 2, ((endY + startY) + kh) // 2)

def main():
	filepath = "final/in/vert.jpeg"
	img = Img(filepath)
	circleRadius = 100
	accuracy = 1 # higher for high res, lower for low res (lower is more accurate)
	sensitivity = 10 # higher for low res, lower for high res
	lineThickness = 10
	x = circleRadius
	y = circleRadius
	
	img = normaliseLighting(img)
	lines = Img("input/lights.jpg")
	out = Img("input/lights.jpg")

	# Vertical Lines
	linesX = []
	knownLines = {}
	while y < (img.getSize()[1] - (circleRadius * 2)):
		x = 0
		while x < (img.getSize()[0] - (circleRadius*2)):
			tmp = isLine(img, x, y, circleRadius, True) 
			if (tmp != False): # if it determines its a line
				if tmp[0] in knownLines: # updates dict
					knownLines[tmp[0]] += 1
				else:
					knownLines[tmp[0]] = 1
			x += accuracy # set to 1 for most accurate but least speed (best for low res imgs)
		y += circleRadius

	for elem in knownLines:
		if knownLines[elem] > sensitivity:
			lines.fillArea(elem, 0, 5, img.getSize()[1], (0, 0, 255))
			out.fillArea(elem, 0, 5, img.getSize()[1], (0, 0, 255))
			linesX.append(elem)
		
	print("-".center(60, "-"))

	# Horizontal lines
	linesY = []
	knownLines = {}
	x = circleRadius
	y = circleRadius
	while y < (img.getSize()[1] - (circleRadius * 2)):
		x = 0
		while x < (img.getSize()[0] - (circleRadius * 2)):
			tmp = isLine(img, x, y, circleRadius, False)
			if (tmp != False):
				if tmp[0] in knownLines:
					knownLines[tmp[0]] += 1
				else:
					knownLines[tmp[0]] = 1
			x += circleRadius
		y += accuracy
 
	for elem in knownLines:
		if knownLines[elem] > sensitivity:
			lines.fillArea(0, elem, img.getSize()[0], lineThickness, (255, 0, 255))
			out.fillArea(0, elem, img.getSize()[0], lineThickness, (255, 0, 255))
			linesY.append(elem)

	lines.save("input/lines.jpeg")

	print("-".center(60, "-"))

	# Line list cleanup
	linesX.insert(0, 0)
	linesY.insert(0, 0)
	linesX.append(img.getSize()[0])
	linesY.append(img.getSize()[1])
	
	# round
	for i in range(len(linesX)):
		linesX[i] = (linesX[i] // (lineThickness * 5)) * (lineThickness * 5)
	# round
	for i in range(len(linesY)):
		linesY[i] = (linesY[i] // (lineThickness * 5 )) * (lineThickness * 5)
	# remove duplicates
	linesX = list(set(linesX))
	linesY = list(set(linesY))
	linesX.sort()
	linesY.sort()

	print(len(linesX), "*", len(linesY))

	print(linesX)
	print("-".center(60, "-"))
	print(linesY)

	for i in range(len(linesX) - 1):
		for j in range(len(linesY) - 1):
			# Circle Detection
			tmp = getAverageDarkness(img, linesX[i], linesY[j], linesX[i + 1], linesY[j + 1]) 
			print(tmp)
			if tmp < 230:
				# Fill area black
				print("Black")
				out.fillArea(linesX[i], linesY[j], (linesX[i + 1] - linesX[i]), (linesY[j + 1] - linesY[j]), (0, 0, 0))
			else:
				print("White")
				out.fillArea(linesX[i], linesY[j], (linesX[i + 1] - linesX[i]), (linesY[j + 1] - linesY[j]), (255, 255, 255))

	out.save("input/out.jpeg")

if __name__ == "__main__":
	main()