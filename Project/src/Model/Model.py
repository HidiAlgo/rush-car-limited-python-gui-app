class Model:

    def __init__(self, modelName, modelID=None):
        self.__modelID = modelID
        self.__modelName = modelName

    def getModelID(self):
        return self.__modelID

    def setModelID(self, modelID):
        self.__modelID = modelID

    def getModelName(self):
        return self.__modelName

    def setModelName(self, modelName):
        self.__modelName = modelName

