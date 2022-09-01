from PIL import Image, ImageOps, ImageEnhance

class Img:
    def __init__(self, imgPath:any) -> None:
        if isinstance(imgPath, str): # str constructor
            self.__imgPath = imgPath
            self.__img = Image.open(imgPath)
            self.__pix = self.__img.load()
            self.__grayScale = False
        elif isinstance(imgPath, Image.Image): # overload constructor if Image.Image is passed in
            self.__img = imgPath
            self.__pix = self.__img.load()
            self.__grayScale = False # TODO: should first convert it to 'RGB' format

    def convRGB(self) -> None:
        self.__img = self.__img.convert('RGB')
        self.__pix = self.__img.load()
        self.__grayScale = False

    def getSize(self) -> tuple: # (width, height) format
        return self.__img.size

    def getRGBVal(self, xPos:int, yPos:int) -> tuple: # (R, G, B) format
        if isinstance(self.__pix[xPos, yPos], tuple):
            return self.__pix[xPos, yPos]
        return(self.__pix[xPos, yPos] // 3, self.__pix[xPos, yPos] // 3, self.__pix[xPos, yPos] // 3)

    def setRGB(self, xPos:int, yPos:int, newR:int, newG:int, newB:int) -> None:
        if self.__grayScale == False:
            self.__pix[xPos, yPos] = (newR, newG, newB)
        else:
            self.__pix[xPos, yPos] = (newR + newG + newB) // 3

    def getDarkness(self, xPos:int, yPos:int) -> int:
        if self.__grayScale == False:
            return (self.__pix[xPos, yPos][0] + self.__pix[xPos, yPos][1] + self.__pix[xPos, yPos][2]) // 3
        return self.__pix[xPos, yPos]

    def setDarkness(self, xPos:int, yPos:int, newDark:int) -> None:
        if self.__grayScale == False:
            self.__pix[xPos, yPos] = (newDark, newDark, newDark)
        else:
            self.__pix[xPos, yPos] = (newDark)

    def fillArea(self, startX:int, startY:int, width:int, height:int, RGB:tuple) -> None:
        for i in range(startX, startX + width):
            for j in range(startY, startY + height):
                self.setRGB(i, j, RGB[0], RGB[1], RGB[2])

    def getPath(self) -> str:
        return self.__imgPath

    def save(self, newImgName:str) -> None:
        self.__img.save(newImgName)

    def grayScale(self) -> None: # This will change the format of the image to only black and white
        self.__grayScale = True
        self.__img = (ImageOps.grayscale(self.__img))
        self.__pix = self.__img.load()

    def invert(self) -> None:
        self.__img = (ImageOps.invert(self.__img))
        self.__pix = self.__img.load()

    def equalise(self) -> None:
        self.__img = (ImageOps.equalize(self.__img))
        self.__pix = self.__img.load()

    def solarise(self, threshold:int) -> None: # maybe should always be called after gray scale?
        self.__img = (ImageOps.solarize(self.__img, threshold))
        self.__pix = self.__img.load()

    def normalise(self) -> None:
        self.__img = (ImageOps.autocontrast(self.__img)) # think this is normalisation?
        self.__pix = self.__img.load()

    def enhance(self, color:float, contrast:float, brightness:float, sharpness:float) -> None:
        enhancer = ImageEnhance.Color(self.__img)
        self.__img = enhancer.enhance(color)
        self.__pix = self.__img.load() # not sure if this should just be called once at the end?
        enhancer = ImageEnhance.Contrast(self.__img)
        self.__img = enhancer.enhance(contrast)
        self.__pix = self.__img.load()
        enhancer = ImageEnhance.Brightness(self.__img)
        self.__img = enhancer.enhance(brightness)
        self.__pix = self.__img.load()
        enhancer = ImageEnhance.Sharpness(self.__img)
        self.__img = enhancer.enhance(sharpness)
        self.__pix = self.__img.load()

    # TODO: fix
    def findLinearLightingGradient(self) -> int:
        self.equalise()
        return self.getDarkness(0, 0) - self.getDarkness(self.getSize()[0] - 1, self.getSize()[1] - 1) / (self.getSize()[0])

    # TODO: fix
    def linearLightingCorrection(self) -> None: # should correct for the lighting gradient assuming that lighting is a linear function dependent on the x or y position of the image
        gradient = self.findLinearLightingGradient()
        baseVal = -1 * (self.sumRGB(self.findAverageRGB()) - 255)
        for x in range(1, self.getSize()[0]):
            for y in range(self.getSize()[1]):
                self.setDarkness(x, y, int((self.getDarkness(x, y)) * ((x / self.getSize()[0])* gradient)))

    def sumRGB(self, RGB:tuple) -> int: # 0 -> 255
        return (RGB[0] + RGB[1] + RGB[2]) // 3

    def findAverageRGB(self, startX:int = 0, startY:int = 0, width:int = "WIDTH", height:int = "HEIGHT") -> tuple: # (R, G, B) where R, G and B are 0 -> 255
        if width == "WIDTH":
            width = self.getSize()[0]
        if height == "HEIGHT":
            height = self.getSize()[1]
        R = G = B = 0
        x = startX
        y = startY
        while x < startX + width:
            y = startY
            while y < startY + height:
                R += (self.getRGBVal(x, y)[0])
                G += (self.getRGBVal(x, y)[1])
                B += (self.getRGBVal(x, y)[2])
                y += 1
            x += 1
        R = R // (width * height)
        G = G // (width * height)
        B = B // (width * height)
        return (R, G, B)

    def blackWhiteMask(self, averageRGB:tuple, threshold:int = 20) -> None:
        x = 0
        while x < self.getSize()[0]:
            y = 0
            while y < self.getSize()[1]:
                if (self.getDarkness(x, y)) > (self.sumRGB(averageRGB)) - threshold:
                    self.setRGB(x, y, 0, 0, 0)
                else:
                    self.setRGB(x, y, 255, 255, 255)
                y += 1
            x += 1
