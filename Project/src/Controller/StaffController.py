from src.Controller import DatabaseController as DB


class StaffController:
    def searchCarsByModelOrManufacturer(self, key):
        return DB.searchCar(key)

    def addAnOfficeMember(self, officeMember):
        try:
            DB.registerMember(officeMember.getOfficeMemberEmail(),
                              officeMember.getOfficeMemberPassword(), officeMember.getOfficeMemberName())
            return True
        except Exception as e:
            return False

    def addAnSeller(self, seller):
        try:
            DB.registerSeller(seller.getSellerEmail(),seller.getSellerPassword(), seller.getSellerName())
            return True
        except Exception as e:
            return False


    def viewAvailableManufacturers(self):
        return DB.selectAllManufacturers()

    def viewAvailableModels(self):
        return DB.selectAllModels()

    def viewAvailableCars(self):
        rows = DB.selectAllCars()
        result = list(filter(lambda x: x[5] == 0, rows))
        return result

    def viewUpgrades(self):
        return DB.selectAllUpgrades()