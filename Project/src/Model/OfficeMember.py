class OfficeMember:
    '''
    This is the OfficeMember class, this class maintains the details for members of the company.
    --------------------------------------------------------------------------------------------

    PRIVATE ATTRIBUTES:-
    --------------------
        __officeMemberEmail: str
            every member should have an email provided by the company
        __officeMemberPassword: str
            a password for the member account
        __officeMemberName: str
            member name

    METHODS:-
    ---------
        getOfficeMemberEmail()
        getOfficeMemberPassword()
        getOfficeMemberName()
        setOfficeMemberEmail()
        setOfficeMemberPassword()
        setOfficeMemberName()
    '''

    def __init__(self, officeMemberEmail, officeMemberPassword, officeMemberName ):
        self.__officeMemberEmail = officeMemberEmail
        self.__officeMemberPassword = officeMemberPassword
        self.__officeMemberName = officeMemberName

    def getOfficeMemberEmail(self):
        return self.__officeMemberEmail

    def setOfficeMemberEmail(self, officeMemberEmail):
        self.__officeMemberEmail = officeMemberEmail

    def getOfficeMemberPassword(self):
        return self.__officeMemberPassword

    def setOfficeMemberPassword(self, officeMemberPassword):
        self.__officeMemberEmail = officeMemberPassword

    def getOfficeMemberName(self):
        return self.__officeMemberName

    def setOfficeMemberName(self, officeMemberName):
        self.__officeMemberName = officeMemberName
