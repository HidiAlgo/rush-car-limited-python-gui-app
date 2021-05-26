class Car:
    '''
    This is the Car class, this class maintains the details for a car.
    ------------------------------------------------------------------

    PRIVATE ATTRIBUTES:-
    --------------------
        __registrationNumber: int
            the registration number for the car
        __carName: str
            this might be generated according to the model
        __color: str
            the color of the car
        __price: int
        __numberOfDoors: int
            this could be 3 or 5
        __carModel: Model
        __carManufacturer: Manufacturer
        __upgrade: Upgrade
            this is not necessary
        __status: boolean
            this indicates whether the car is available or not

    METHODS:-
    ---------
        getRegistrationNumber()
        getCarName()
        getColor()
        getPrice()
        getNumberOfDoors()
        getCarModel()
        getCarManufacturer()
        getUpgrades()
        getStatus
        setRegistrationNumber()
        setCarName()
        setColor()
        setPrice()
        setNumberOfDoors()
        getCarModel()
        setCarManufacturer()
        setUpgrades()
        setStatus
    '''
    def __init__(self, rNumber, cName, color, price, numOfDoors, cModel, cManufacturer, upgrades=None, status=0 ):
        self.__registrationNumber = rNumber
        self.__carName = cName
        self.__color = color
        self.__price = price
        self.__numberOfDoors = numOfDoors
        self.__carModel = cModel
        self.__carManufacturer = cManufacturer
        self.__upgrades = upgrades
        self.__status = status

    def getRegistrationNumber(self):
        return self.__registrationNumber

    def setRegistrationNumber(self, rNumber):
        self.__registrationNumber = rNumber

    def getCarName(self):
        return self.__carName

    def setCarName(self, cName):
        self.__carName = cName

    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color

    def getPrice(self):
        return self.__price

    def setPrice(self, price):
        self.__price = price

    def getNumberOfDoors(self):
        return self.__numberOfDoors

    def setNumberOfDoors(self, numOfDoors):
        self.__numberOfDoors = numOfDoors

    def getCarModel(self):
        return self.__carModel

    def setCarModel(self, cModel):
        self.__carModel = cModel

    def getCarManufacturer(self):
        return self.__carManufacturer

    def setCarManufacturer(self, cManufacturer):
        self.__carManufacturer = cManufacturer

    def getUpgrades(self):
        return self.__upgrades

    def setUpgrades(self, upgrades):
        self.__upgrades = upgrades

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status

