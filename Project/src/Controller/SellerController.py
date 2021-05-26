from src.Controller import StaffController as admin, DatabaseController as DB


class SellerController(admin.StaffController):

    def sell(self, regNumber, upgrades, price, email, date, time):
        DB.sellCar(regNumber, upgrades, price, email, date, time)


