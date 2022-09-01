# Silk Card Process
## Code

> To run the code type 'python main.py' python also needs to be added to windows path

### Dependencies
- Python
- PIL
  - Image
  - ImageOps
  - ImageEnhance
- Math
  - cos, sin, radians, floor, pi

### __old/
Two previous attempts are stored here

There are functions here which will be useful in the future:
- isLine
  - checks if there is a line in a specified point
   - works by projecting circles then checking if a line intersects twice
- makeBlobsBin
   - previous attempt at converting image to binary
- fillArea
   - fill a specified area a specific colour
- getAverageDarkness
   - get the average darkness over an area
   - darknes is the sum of red, green and blue values divided by 3

### Img class (still working on)
> Note: this is the new Img class located in ./image.py

#### Members:
- __imgPath:str
  - path to the image being opened
- __img: Image object (Image.Image)
  - provided by PIL
  - __img.load() returns the image access object
- __pix: Image access object
  - provided by PIL
  - has overloads for [] which are used to set and get RGB values of specific pixels
- __grayScale: boolean
  - stores true if the loaded image is in grayScale

#### Methods:
- constructor(imgPath:str) -> None
- constructor(img:Image.Image) -> None
- convRGB() -> None
- getSize() -> tuple
  - returns (width, height)
- getRGBVal(xPos:int, yPos:int) -> tuple
  - returns (R, G, B) at (xPos, yPos)
- setRGB(xPos:int, yPos:int, newR:int, newG:int, newB:int) -> None
  - sets __pix[xPos, yPos] = (newR, newG, newB)
- getDarkness(xPos:int, yPos:int) -> tuple
  - returns the sum of the red, green and blue divided by 3 at xPos, yPos
- setDarkness(xPos:int, yPos:int, newDark:int) -> None
  - will set the R, G, B to newDark
- fillArea(startX:int, startY:int, width:int, height:int, RGB:tuple) -> None
  - fills the area of the rectangle with points:
    - startX
    - startY
    - startX + width
    - startY + height
  - with the specified RGB value
- getPath() -> str
  - returns __imgPath
- save(newImgName:str) -> None
  - calls a PIL function which saves the changes made on an image
- grayScale() -> None
- invert() -> None
- equalise() -> None
- solarise(threshold:int) -> None
- normalise() -> None
- enhance(color:float, contrast:float, brightness:float, sharpness: float) -> None
  - These values should be adjusted
- findLinearLightingGradient() -> int
  - fix
  - equalises the image then finds the change in darkness divided by the change in width
- linearLightingCorrection() -> None
  - fix
  - will use the gradient to correct the change in lighting as the X or Y of the image increases
- sumRGB(RGB:tuple) -> int (0 -> 255)
  - adds RGB[0], RGB[1] and RGB[2]
  - then divides by 3 and returns this
- findAverageRGB(startX:int = 0, startY:int = 0, width:int = img.getSize()[0], height:int = img.getSize()[1]) -> tuple
  - finds the average RGB over a specified area
- blackWhiteMask(averageRGB:tuple, threshold:int = 20) -> Img
  - sets all pixels with a darkness > averageDarkness + r to black
  - sets pixels that dont satisfy this condition to white
  - returns the modified Img object

### Other functions used (still working on)
- convToBin(img:Img, amountX:int, amountY:int) -> tuple
  - amountX is the amount of hole punches across
  - amountY is the amount of hole punches down
  - this will average out the RGB over a square to determine if there is a hole punch
  - the threshhold in this function can be tweaked
  - tuple is of a binary string and a modified img which has lines drawn on it for testing purposes
  - the binary string is in the format "XXXX\nXXXX\n"
  - the amount of "\n" will be the same as amountY
  - the amount of X's per row will be the same as amountX
- regenImg(img:Img, inp:str, RGB:tuple) -> None
  - This will add filled coloured circles close to the position where a 1 was recorded
  - The colour will be the RGB value specified in the parameters
  - The input string will be in the format: "XXXX\nXXXX\n"
  - "\n" denotes the start of a new row
  - uses trig to determine the poitions on the circle
 
### The order of the filters (still working on)
- `solarise(255)`
- `normalise()`
- `invert()`
- `enhance(0.5, 0.7, 1, 2)`
- `grayScale()`
- `img = blackWhiteMask(img, img.findAverageRGB(), 5)`

### Final Processing
- the image is then converted to binary
- then regenImg is called and then it is saved

## Pictures

### Lighting
- The lighting is best when it is not dim but also not bright
- There cannot be a part of the image that is siginifcantlly darker or lighter than another part
- Lighting can be checked by gray scaling then equalising then saving the result

### Background
- I have placed the cards on white paper
- This ensures good contrast between the brown card and the background
- The image taken must be straight or it will not be properly converted
- The cards also must line up

## Next Steps

### Code
- Take inputs from the user on conditions and filter such as:
  - amount across
  - amount down
  - some threshold values for `blackWhiteMask`
- Test out other filters
- Work on a lighting adjustment function
- Improve it's general accuracy
- Work on a function that will adjust the image straightness
- Work on better circle detection instead of just using averages
- Send the data to a locally hosted server to be drawn with canvas
  - Could use the same framework as teams status used (expressjs)
  - use python requests library to post to a server and then handle that through expressjs (POST and GET)
- **Improve efficiency**
  - Improve the speed
  - Replace loops
  - Look into using more library calls (they will be faster)
  - Don't save between each filter
- Fix linear gradient function
  - Take into account non-linear lighting
  - Take into account changes to lighting over both X and Y
- Potentially look at edge detection
  - used for the edge of cards
  - could help with aliigning them 
  - checking if the cards are alligned

### Pictures
- Standardising the lighting
- Different coloured background (green maybe) to constrast even more from the brown
- Using camera filters or a higher resolution camera

### Use cases
- Digitally store the cards
- Display the cards and test out different colours
