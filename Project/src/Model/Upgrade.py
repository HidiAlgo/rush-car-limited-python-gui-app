class Upgrade:
    '''
    This is the Upgrade class, this class maintains the details for an update.
    ----------------------------------------------------------------------------------

    PRIVATE ATTRIBUTES:-
    --------------------
        __upgradeID: int
            an auto generated/ manually added ID
        __upgradeName: str
            a specific name for a model
        __upgradePrice: ing
            the cost of
            an upgrade

    METHODS:-
    ---------
        getUpgradeID()
        getUpgradeName()
        getUpgradePrice()
        setUpgradeID()
        setUpgradeName()
        setUpgradePrice()
    '''

    def __init__(self, upgradeName, upgradePrice, upgradeID=None):
        self.__upgradeName = upgradeName
        self.__upgradePrice = upgradePrice
        self.__upgradeID = upgradeID

    def getUpgradeName(self):
        return self.__upgradeName

    def setUpgradeName(self, upgradeName):
        self.__upgradeName = upgradeName

    def getUpgradePrice(self):
        return self.__upgradePrice

    def setUpgradePrice(self, upgradePrice):
        self.__upgradePrice = upgradePrice

    def getUpgradeID(self):
        return self.__upgradeID

    def setUpgradeID(self, upgradeID):
        self.__upgradeID = upgradeID