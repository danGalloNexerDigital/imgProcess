class Log:
    def __init__(self, filename, mode ="a") -> None:
        print("LOG FILE OPENED")
        self.__filename = filename
        self.__myFile = open(filename, mode)

    def clearFile(self) -> None:
        self.__myFile.close()
        self.__myFile = open(self.__filename, "w")
        self.__myFile.close()
        self.__myFile = open(self.__filename, "a")
        print("LOG FILE CLEARED")

    def write(self, *args, end = "\n") -> None:
        for arg in args:
            print(arg, end = "")
            self.__myFile.write(arg)
        print("", end = end)
        self.__myFile.write(end)

    def __del__(self): # Destructor
        self.__myFile.close()
        print("LOG FILE CLOSED")
