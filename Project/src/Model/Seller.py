class Seller:
    '''
    This is the Seller class, this class maintains the details for sellers of the company.
    --------------------------------------------------------------------------------------------

    PRIVATE ATTRIBUTES:-
    --------------------
        __sellerEmail: str
            every seller should have an email provided by the company
        __sellerPassword: str
            a password for the seller account
        __sellerName: str
            seller name

    METHODS:-
    ---------
        getSellerEmail()
        getSellerPassword()
        getSellerName()
        setSellerEmail()
        setSellerPassword()
        setSellerName()
    '''
    def __init__(self, sellerEmail, sellerPassword, sellerName):
        self.__sellerEmail = sellerEmail
        self.__sellerPassword = sellerPassword
        self.__sellerName = sellerName

    def getSellerEmail(self):
        return self.__sellerEmail

    def setSellerEmail(self, sellerEmail):
        self.__sellerEmail = sellerEmail

    def getSellerPassword(self):
        return self.__sellerPassword

    def setSellerPassword(self, sellerPassword):
        self.__sellerPassword = sellerPassword

    def getSellerName(self):
        return self.__sellerName

    def setSellerName(self, sellerName):
        self.__sellerName = sellerName