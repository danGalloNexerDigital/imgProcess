from image import Img
from log import Log

from math import floor

# NOTE: arr must contain int or float type
def sumArr(arr:list) -> int:
    ret = 0
    for elem in arr:
        ret += elem
    return ret

# NOTE: Blue is weighted 1 and a half
# NOTE: Red is weighted half
def sumRGB(RGB):
    return (RGB[0] // 2) + RGB[1] + RGB[2] + (RGB[2] // 2)

def findAverageRGB(img, startX:int, startY:int, endX:int, endY:int) -> int:
    total = 0
    area = (endX - startX) * (endY - startY)
    for x in range(startX, endX):
        for y in range(startY, endY):
            total += sumRGB(img.getRGBVal(x, y))
    if area != 0:
        return total // area
    return 0

def blackWhiteMask(imgPath:str) -> None:
    img = Img(imgPath)
    imgSize = img.getSize()
    averageRGBSum = findAverageRGB(img, 0, 0, imgSize[0], imgSize[1])
    print("IMG Width: ", imgSize[0])
    print("IMG Height: ", imgSize[1])
    print("Total average RGB Sum =", averageRGBSum)
    x = 0
    for y in range(imgSize[1]):
        if x+80 < imgSize[0] and y+50 < imgSize[1]:
            averageRGBSum = findAverageRGB(img, x, y, x + 80, y + 50)
        for x in range(imgSize[0]):
            RGBSum = sumRGB(img.getRGBVal(x, y))
            if RGBSum >= averageRGBSum:
                # Set to white
                img.setRGB(x, y, 255, 255, 255)
            else:
                # Set to black
                img.setRGB(x, y, 10, 10, 10)


    newName = "new" + imgPath # FIXME: this wont work with different paths
    img.save(newName)
    return newName

def isBlack(RGB) -> bool:
    s = sumRGB(RGB)
    if s <= 40:
        return True
    return False

def fillArea(img, startX:int, startY:int, endX:int, endY:int, RGB) -> None:
    for x in range(startX, endX):
        for y in range(startY, endY):
            img.setRGB(x, y, RGB[0], RGB[1], RGB[2])

def makeBlobsBin(imgPath:str, blobsPerRow:int, blobsPerColumn:int) -> str:
    # NOTE: 12 blobs per row
    # Here there are 122 pixels per row
    # Therefore 10 pixels across per blob

    # NOTE: 7 blobs per column
    # Here there are 66 pixels per column
    # Therefore 9 pixels up per blob

    ret = ""
    img = Img(imgPath)
    imgSize = img.getSize()
    # Dimensions of the area of the squares
    l = (imgSize[1] // blobsPerColumn)
    w = (imgSize[0] // blobsPerRow)

    print("L:", l)
    print("W:", w)

    # NOTE: global average
    #average = findAverageRGB(img, (x), (y), imgSize[0], imgSize[1])
    for y in range(blobsPerColumn):
        for x in range(blobsPerRow):
            # NOTE: local averages
            average = findAverageRGB(img, (x*w), (y*l), (x+1) * w, (y+1)* l)
            if average < (638): # TODO: 638 almost = 255*2.5
                averArr = []

                splits = 100
                i = 1
                while i < (splits + 1):
                    prev = floor((i-1) * (l / splits))
                    nex = floor(i * (l / splits))
                    tmp = findAverageRGB(img, (x*w), ((y*l) + prev), (x+1) * w, ((y*l) + nex))
                    averArr.append(tmp)
                    i += 1
                
                amountBlack = 0
                for i in range(len(averArr)):
                    #print("averArr[i]:", averArr[i])
                    if (averArr[i]) < 275:
                        amountBlack += 1

                if amountBlack > (len(averArr) // 2) - 1:
                    # BLACK TILE
                    fillArea(img, (x*w), (y*l), (x+1) * w, (y+1) * l, (0, 0, 0))
                    ret += "1"
                else:
                    # WHITE TILE
                    fillArea(img, (x*w), (y*l), (x+1) * w, (y+1) * l, (255, 255, 255))
                    ret += "0"

            else:
                # WHITE TILE
                fillArea(img, (x*w), (y*l), (x+1) * w, (y+1) * l, (255, 255, 255))
                ret += "0"
        ret += "E\n"
    img.save("squares.png")
    return ret

def main():
    #newFileName = blackWhiteMask("sample.png")
    #out = makeBlobsBin(newFileName, 12, 7)
    #newFileName = blackWhiteMask("img.jpg")
    #out = makeBlobsBin(newFileName, 80, 55)
    newFileName = blackWhiteMask("sample1.png")
    out = makeBlobsBin(newFileName, 23, 15)
    log = Log("out.txt")
    log.clearFile()
    log.write(str(out))

if __name__ == "__main__":
    main()
