from math import cos, sin, radians, floor
from image import Img

def findArea(startX:int, startY:int, endX:int, endY:int) -> int:
    return (endX - startX) * (endY - startY)

def getDarkness(RGB:tuple) -> int: # 0 (least dark) -> 255 (most dark)
    sumRGB = RGB[0] + RGB[1] + RGB[2]
    ret = sumRGB // 3
    return (255 - ret)

def normaliseLighting(img:Img, r:int = 20) -> Img:
    I = getDarkness(img.getRGBVal(0, 0))
    for x in range(1, img.getSize()[0]):
        for y in range(1, img.getSize()[1]):
            if getDarkness(img.getRGBVal(x, y)) in range(I - r, I + r):
                img.setRGB(x, y, int(I // 3), int(I // 3), int(I // 3))
    return img

def greyScale(img:Img) -> Img:
    for x in range(img.getSize()[0]):
        for y in range(img.getSize()[1]):
            dark = img.getRGBVal(x, y)[0] + img.getRGBVal(x, y)[1] + img.getRGBVal(x, y)[2]
            img.setRGB(x, y, dark // 3, (dark // 3), (dark // 3))
    return img

def blackWhiteMask(img:Img, averageRGB:tuple, r:int = 20) -> Img:
    x = 0
    y = 0
    while x < img.getSize()[0]:
        y = 0
        while y < img.getSize()[1]:
            if getDarkness(img.getRGBVal(x, y)) < getDarkness(averageRGB) + r:
                img.setRGB(x, y, 0, 0, 0)
            else:
                img.setRGB(x, y, 255, 255, 255)
            y += 1
        x += 1
    return img

def convToBin(img:Img, amountX:int, amountY:int) -> tuple:
    ret = ""
    x = 0
    y = 0
    while y <= int(img.getSize()[1] - (1)):
        x = 0
        while x <= int(img.getSize()[0] - (1)):
            if (img.sumRGB(img.findAverageRGB(int(x), int(y), (img.getSize()[0] // amountX), (img.getSize()[1] // amountY)))) > 50:
                ret += "1"
            else:
                ret += "0"
            for j in range(10):
                img.setRGB(x + j, y + j, 255, 0, 0)
            x += (img.getSize()[0] / amountX)
        y += (img.getSize()[1] / amountY)
        ret += "\n"
    return (ret, img)

def regenImg(img:Img, inp:str, RGB:tuple) -> None: # NOTE: input str must be XXX\nXXX
    inp = inp.split("\n")
    radiusX = int(img.getSize()[0] / (len(inp[0]) * 2))
    radiusY = int(img.getSize()[1] / (len(inp) * 2))
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            if inp[y][x] == "1":
                i = 0
                while i < 360:
                    for j in range(radiusX): # to fill the circles (maybe need to change a radiusY also)
                        img.setRGB((x * radiusX * 2) + (radiusX) + (j * cos(radians(i))), (y * radiusY * 2) + (radiusY) + (radiusY * sin(radians(i))), RGB[0], RGB[1], RGB[2])
                    i += 0.1
    return img

# NOTE: the cards dont line up

def main():
    img = Img("in/test.jpeg")
    img.solarise(255)
    img.normalise()
    img.invert()
    img.enhance(0.5, 0.7, 1, 2)
    img.grayScale()
    img = blackWhiteMask(img, img.findAverageRGB(), 5)
    img.save("out/out.png")
    img = Img("out/out.png")
    img.convRGB()

    binary = convToBin(img, 16, 49)
    print(binary[0])
    binary[1].save("out/lines.png")
    regenImg(img, binary[0], (255, 0, 255)).save("out/finalOut.png")

if __name__ == "__main__":
    main()
