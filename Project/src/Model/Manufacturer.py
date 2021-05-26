class Manufacturer:
    '''
    This is the Manufacturer class, this class maintains the details of a manufacturer.
    ----------------------------------------------------------------------------------

    PRIVATE ATTRIBUTES:-
    --------------------
        __manufactureID: int
            an auto generated/ manually added ID
        __manufactureName: str
            a specific name for a manufacturer

    METHODS:-
    ---------
        getManufacturerID()
        getManufacturerName()
        setManufacturerID()
        setManufacturerName()
    '''
    def __init__(self, manufacturerName, manufacturerID=None):
        self.__manufacturerID = manufacturerID
        self.__manufacturerName = manufacturerName

    def getManufacturerID(self):
        return self.__manufacturerID

    def setManufacturerID(self, manufacturerID):
        self.__manufacturerID = manufacturerID

    def getManufacturerName(self):
        return self.__manufacturerName

    def setManufacturerName(self, manufacturerName):
        self.__manufacturerName = manufacturerName

