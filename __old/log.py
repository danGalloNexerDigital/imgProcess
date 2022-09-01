class Log:
    def __init__(self, filename, mode ="a") -> None:
        print("LOG FILE OPENED")
        self.__filename = filename
        self.__myFile = open(filename, mode)

    # OPENS FILE IN WRITE THEN REOPENS IN APPEND MODE THIS ESSENTIALLY CLEARS THE FILE (caps?)
    def clearFile(self) -> None:
        self.__myFile.close()
        self.__myFile = open(self.__filename, "w")
        self.__myFile.close()
        self.__myFile = open(self.__filename, "a")
        print("LOG FILE CLEARED")

    def write(self, inp, end= "\n") -> None: # TODO: Rework args here
        print(inp, end=end)
        self.__myFile.write(inp)
        self.__myFile.write(end)

    def __del__(self): # Destructor
        self.__myFile.close()
        print("LOG FILE CLOSED")
