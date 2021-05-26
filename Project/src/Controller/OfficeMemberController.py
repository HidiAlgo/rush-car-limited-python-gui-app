from src.Controller import StaffController as admin, DatabaseController as DB
from src.Model.Car import Car
from src.Model.Model import Model
from src.Model.Manufacturer import Manufacturer


class OfficeMemberController(admin.StaffController):

    def addAModel(self, model):
        if type(model) is Model:
            DB.insertModel(model)
        else:
            print("TYPE ERROR")


    def removeAModel(self, modelID):
        try:
            DB.removeModel(modelID)
            return True
        except Exception as e:
            return False

    def updateAModel(self, modelID, name):
        DB.updateModel(modelID, name)

    def updateAManufacturer(self, manufacturerID, name):
        DB.updateManufacturer(manufacturerID, name)


    def addAManufacturer(self, manufacturer):
        if type(manufacturer) is Manufacturer:
            DB.insertManufacturer(manufacturer)
        else:
            print("TYPE ERROR")


    def removeAManufacturer(self, manufacturerID):
        try:
            DB.removeManufacturer(manufacturerID)
            return True
        except:
            return False



    def addACar(self, car, email):
        if type(car) is Car:
            try:
                DB.insertCar(car, email)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print("TYPE ERROR")



    def removeACar(self, registrationNumber):
        DB.removeCar(registrationNumber)


    def viewSoldCars(self):
        rows = DB.selectAllCars()
        result = list(filter(lambda x: x[5] == 1, rows))
        return result


    def moreDetailsForSoldCar(self, regNumber):
        return DB.selectSoldCar(regNumber)

    def addAnUpgrade(self, name, price):
        if price.isnumeric():
            DB.insertUpgrade(name, price)
            return True
        else:
            return False

    def deleteAnUpgrade(self, upgradeID):
        DB.removeUpgrade(upgradeID)

    def updateAnUpgrade(self, id, name, price):
        if price.isnumeric():
            DB.updateUpgrade(id, name, price)
            return True
        else:
            return False