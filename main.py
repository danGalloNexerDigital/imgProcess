# Dan Gallo
# danGalloNexerDigital

from math import cos, sin, radians, pi
from image import Img

def findArea(startX:int, startY:int, endX:int, endY:int) -> int:
    return (endX - startX) * (endY - startY)

def convToBin(img:Img, amountX:int, amountY:int, threshold:int, lineWidth:int = 5) -> tuple:
    ret = ""
    x = 0
    y = 0
    while y <= int(img.getSize()[1] - 1): # -1 so it doesn't hit bounds (maybe just use <)
        x = 0
        while x <= int(img.getSize()[0] - 1):
            if (img.sumRGB(img.findAverageRGB(int(x), int(y), (img.getSize()[0] // amountX), (img.getSize()[1] // amountY)))) > threshold: # if the average RGB is higher then
                ret += "1" # circle is present
            else:
                ret += "0" # circle is not present
            for j in range(lineWidth): # Draws lines
                for i in range(int(img.getSize()[1] / amountY)):
                    img.setRGB(x + j, y + i, 255, 0, 0)
                for k in range(int(img.getSize()[0] / amountX)):
                    img.setRGB(x + k, y + j, 255, 0, 0)
            x += (img.getSize()[0] / amountX)
        y += (img.getSize()[1] / amountY)
        ret += "\n"
    return (ret, img)

def regenImg(img:Img, inp:str, RGB:tuple) -> None: # NOTE: input str must be XXX\nXXX
    inp = inp.split("\n")
    radiusX = (img.getSize()[0] / (len(inp[0]) * 2))
    radiusY = (img.getSize()[1] / ((len(inp) - 1) * 2)) # len(inp) - 1 because extra '\n' on the end
    loop = radiusY
    if radiusX < radiusY:
        loop = radiusX
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            if inp[y][x] == "1":
                i = 0
                while i < (2 * pi): # i is in radians
                    for j in range(int(loop)): # to fill the circle
                        img.setRGB((x * radiusX * 2) + (j * cos(i)) + radiusX, (y *  radiusY * 2) + (radiusY * sin(i)) + radiusY, RGB[0], RGB[1], RGB[2])
                    i += 0.01 # the smaller this value the longer it takes but the more accurate the circle
    return img

def main():
    #filepath = input("Enter the file path of the input image: ")
    filepath = "in/test.jpeg"
    img = Img(filepath)
    img.solarise(255)
    #img.save("out/sol.jpeg")
    img.normalise()
    #img.save("out/norm.jpeg")
    img.invert()
    #img.save("out/invert.jpeg")
    img.enhance(0.5, 0.7, 1, 2)
    #img.save("out/enhance.jpeg")
    img.grayScale()
    img.convRGB()
    img.blackWhiteMask(img.findAverageRGB(), 5)
    img.save("out/out.png")

    #amountX = int(input("How many accross?:  "))
    amountX = 48
    #amountY = int(input("How many vertical?: "))
    amountY = 7
    binary = convToBin(img, amountX, amountY, 50) # binary[0] is the output string, binary[1] is the image with the lines added in (for testing)
    print(binary[0]) # Binary output
    binary[1].save("out/lines.png")
    regenImg(img, binary[0], (255, 0, 255)).save("out/finalOut.png")

if __name__ == "__main__":
    main()
