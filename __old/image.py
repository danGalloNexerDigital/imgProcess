from PIL import Image
from numpy import array

class Img:
    def __init__(self, imgPath:str) -> None:
        self.__imgPath = imgPath
        self.__img = Image.open(imgPath)
        self.__pix = self.__img.load()

    def getSize(self) -> tuple:
        return self.__img.size

    def getRGBVal(self, xPos:int, yPos:int) -> tuple:
        return self.__pix[xPos, yPos]
    
    def setRGB(self, xPos:int, yPos:int, newR:int, newG:int, newB:int) -> None:
        self.__pix[xPos, yPos] = (newR, newG, newB)
    
    def fillArea(self, startX:int, startY:int, width:int, height:int, RGB:tuple) -> None:
        for i in range(startX, startX + width):
            for j in range(startY, startY + height):
                self.setRGB(i, j, RGB[0], RGB[1], RGB[2])

    def getPath(self):
        return self.__imgPath

    def convToNp(self):
        ret = []
        tmp = array(self.__img)
        for i in range(len(tmp)):
            ret.append([])
            for j in range(len(tmp[i])):
                ret[i].append(tmp[i, j][0] + tmp[i, j][1] + tmp[i, j][2])
        return array(ret)

    def save(self, newImgName:str) -> None:
        self.__img.save(newImgName)