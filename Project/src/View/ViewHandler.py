import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from src.Controller.SellerController import SellerController
from src.Controller.StaffController import StaffController
from src.Controller.AuthenticationController import authenticateSeller, authenticateOfficeStaff
from src.Model.Car import Car
from src.Model.Manufacturer import Manufacturer
from src.Model.OfficeMember import OfficeMember
from src.Controller.OfficeMemberController import OfficeMemberController
from src.Model.Model import Model
from src.Model.Seller import Seller

from src.View.View import Ui_Rush

from datetime import date
from datetime import datetime


class Window:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_Rush()

        self.ui.setupUi(self.main_win)

        self.ui.mainStackedWidget.setCurrentWidget(self.ui.welcome_page)

        self.ui.welcome_page_register_btn.clicked.connect(self.register)
        self.ui.welcome_page_login_btn.clicked.connect(self.login)
        self.ui.login_back_btn.clicked.connect(self.home)
        self.ui.register_back_btn.clicked.connect(self.home)


        self.memberController = OfficeMemberController()
        self.sellerController = SellerController()
        self.staffController = StaffController()


    def show(self):
        self.main_win.show()

    def login(self):
        self.ui.mainStackedWidget.setCurrentWidget(self.ui.login_page)
        self.ui.login_page_login_member_btn.clicked.connect(self.memberLogin)
        self.ui.login_page_login_seller_btn.clicked.connect(self.sellerLogin)

    def sellerLogin(self):
        self.sellerEmail = self.ui.login_page_email.text().lower()
        password = self.ui.login_page_password.text()

        seller = authenticateSeller(self.sellerEmail, password)

        if seller != None:
            self.seller(seller)
        else:
            self.ui.login_error.setText("Invalid password or email")
            self.errorBox("Authentication erorr!!!", "Invalid email or password")

    def memberLogin(self):
        self.email = self.ui.login_page_email.text().lower()
        password = self.ui.login_page_password.text()

        member = authenticateOfficeStaff(self.email, password)
        if member != None:
            self.member(member)
        else:
            self.ui.login_error.setText("Invalid password or email")
            self.errorBox("Authentication erorr!!!", "Invalid email or password")


    def register(self):
        self.ui.mainStackedWidget.setCurrentWidget(self.ui.register_page)
        self.ui.register_as_a_member_btn.clicked.connect(self.registerMember)
        self.ui.register_as_a_seller_btn.clicked.connect(self.registerSeller)

    def registerSeller(self):
        sellerEmail = self.ui.register_page_emal.text()
        name = self.ui.register_page_name.text()
        password = self.ui.register_page_password.text()
        passwordConfirm = self.ui.register_page_password_confirm.text()

        if self.validateRegistration(sellerEmail, name, password, passwordConfirm):
            seller = Seller(sellerEmail, password, name)
            if self.staffController.addAnSeller(seller):
                auth_seller = authenticateSeller(sellerEmail, password)
                if auth_seller != None:
                    self.sellerEmail = auth_seller.getSellerEmail()
                    self.seller(auth_seller)
            else:
                self.ui.registration_error.setText("Sorry that email is already taken!!!")
                self.errorBox("Email error", "This email is already taken")

    def registerMember(self):
        email = self.ui.register_page_emal.text()
        name = self.ui.register_page_name.text()
        password = self.ui.register_page_password.text()
        passwordConfirm = self.ui.register_page_password_confirm.text()

        if(self.validateRegistration(email,name, password, passwordConfirm)):
            officeMember = OfficeMember(email, password, name)
            print("hello2")
            if self.staffController.addAnOfficeMember(officeMember):
                member = authenticateOfficeStaff(email, password)
                if member != None:
                    self.email = member.getOfficeMemberEmail()
                    self.member(member)
            else:
                self.ui.registration_error.setText("Sorry that email is already taken!!!")
                self.errorBox("Email error","This email is already taken")

    def home(self):
        self.ui.mainStackedWidget.setCurrentWidget(self.ui.welcome_page)

    def seller(self, seller):
        self.ui.mainStackedWidget.setCurrentWidget(self.ui.seller_page)
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_car)
        self.ui.seller_page_user_name.setText(seller.getSellerName())

        self.ui.seller_page_models_btn.clicked.connect(self.sellerCategories)
        self.ui.seller_page_upgrade_btn.clicked.connect(self.sellerUpgrades)
        self.ui.seller_page_cars_btn.clicked.connect(self.sellerCars)
        self.ui.seller_page_search_btn.clicked.connect(self.sellerSearchPage)

        self.ui.seller_page_add_upgrade_btn.clicked.connect(self.addSellUpgrades)
        self.ui.seller_selected_upgrades_delete_btn.clicked.connect(self.deleteSellUpgrade)
        self.ui.seller_page_upgrade_form_sell_btn.clicked.connect(self.sell)

        self.ui.seller_page_sell_btn.clicked.connect(self.directSell)

        result = self.sellerController.viewAvailableCars()
        self.loadSellerCarTable(result)

    def directSell(self):
        row = self.ui.seller_page_car_table.currentRow()
        if row != -1:
            self.reg = self.ui.seller_page_car_table.item(row, 0).text()
            self.name = self.ui.seller_page_car_table.item(row, 1).text()
            self.price = int(self.ui.seller_page_car_table.item(row, 3).text())
            self.soldPrice = self.price
            self.carUpgrades = []
            self.selectedUpgrades = []
            self.sell()

    def deleteSellUpgrade(self):
        row = self.ui.seller_page_sell_upgrade_table.currentRow()

        if row != -1:
            self.ui.seller_delete_upgrades_error.clear()

            price = int(self.selectedUpgrades[row][0][2])
            pound = int(self.ui.price_in_pound.text()) - price
            rs = int(self.ui.price_in_price.text()) - 248 * price
            usa = int(self.ui.price_in_usa.text()) - 1.34 * price
            euro = int(self.ui.price_in_euro.text()) - 1.12 * price

            self.soldPrice = pound

            self.ui.price_in_pound.setText(str(round(pound)))
            self.ui.price_in_price.setText(str(round(rs)))
            self.ui.price_in_usa.setText(str(round(usa)))
            self.ui.price_in_euro.setText(str(round(euro)))
            del (self.selectedUpgrades[row])
            del (self.carUpgrades[row])
            self.loadSelecteUpgradesTable()
        else:
            self.ui.seller_delete_upgrades_error.setText("Select a row first")

    def sellerUpgrades(self):
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_upgrade)
        result = self.sellerController.viewUpgrades()
        self.loadSellerUpgradeTable(result)



    def sell(self):
        print("Clicked")
        print(self.carUpgrades)
        d = date.today().strftime("%B %d, %Y")
        time = datetime.now().strftime("%H:%M:%S")
        self.sellerController.sell(self.reg, self.carUpgrades, int(self.soldPrice),self.sellerEmail,d,time)
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_sold_car_details)

        self.ui.seller_page_sold_car_reg_label.setText(self.reg)
        self.ui.seller_page_initial_pound.setText(str(self.price))
        self.ui.seller_page_sold_price_pound.setText(str(self.soldPrice))
        self.ui.seller_page_sold_date.setText(str(d))
        self.ui.seller_page_sold_time.setText(str(time))
        self.loadSoldUpgradesTable()

    def sellerCategories(self):
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_model)

        models = self.sellerController.viewAvailableModels()
        manufacturers = self.sellerController.viewAvailableManufacturers()

        self.loadSellerModelTable(models)
        self.loadSellerManufacturerTable(manufacturers)

    def sellerCars(self):
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_car)

        self.ui.car_title_2.setText("AVAILABLE CARS")

        result = self.sellerController.viewAvailableCars()
        self.loadSellerCarTable(result)

    def addSellUpgrades(self):
        row = self.ui.seller_page_car_table.currentRow()

        if row != -1:
            self.reg = self.ui.seller_page_car_table.item(row, 0).text()
            self.name = self.ui.seller_page_car_table.item(row, 1).text()
            self.price = int(self.ui.seller_page_car_table.item(row, 3).text())
            self.soldPrice = self.price

            self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_add_upgrade)

            self.carUpgrades = []
            self.selectedUpgrades = []
            upgrades = self.sellerController.viewUpgrades()
            for up in upgrades:
                self.ui.seller_page_select_upgrade_combo_box.addItem(str(up[0]) + ": " + up[1])

            self.ui.price_in_pound.setText(str(self.price))
            self.ui.price_in_price.setText(str(round(self.price*248)))
            self.ui.price_in_usa.setText(str(round(self.price*1.34)))
            self.ui.price_in_euro.setText(str(round(self.price*1.12)))

            self.ui.seller_page_select_upgrade_btn.clicked.connect(self.upgradeAdded)


        else:
            self.ui.seller_add_upgrades_error.setText("Please select a Car from the table above")


    def upgradeAdded(self):
        selectedID = int(self.ui.seller_page_select_upgrade_combo_box.currentText().split(':')[0])
        self.carUpgrades.append(int(selectedID))
        upgrades = self.sellerController.viewUpgrades()
        u = list(filter(lambda x: x[0] == selectedID, upgrades))
        self.selectedUpgrades.append(u)
        pound = int(self.ui.price_in_pound.text())+round(int(u[0][2]))
        rs = int(self.ui.price_in_price.text())+round(int(u[0][2])*248)
        usa = int(self.ui.price_in_usa.text())+round(int(u[0][2])*1.34)
        euro = int(self.ui.price_in_euro.text())+round(int(u[0][2])*1.12)

        self.soldPrice = self.soldPrice + round(int(u[0][2]))

        self.ui.price_in_pound.setText(str(pound))
        self.ui.price_in_price.setText(str(rs))
        self.ui.price_in_usa.setText(str(usa))
        self.ui.price_in_euro.setText(str(euro))

        self.loadSelecteUpgradesTable()


    def sellerSearchPage(self):
        self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_search)
        self.ui.seller_page_search_form_btn.clicked.connect(self.sellerSearch)



    def sellerSearch(self):
        key = self.ui.seller_page_search_input.text()
        result = self.memberController.searchCarsByModelOrManufacturer(key)
        if result == None:
            self.ui.seller_search_error.setText("NOT AVAILABLE")
        else:
            self.ui.sellerStackedWidget.setCurrentWidget(self.ui.seller_page_car)
            self.loadSellerCarTable(result)
            self.ui.car_title_2.setText("SEARCHED RESULTS")

    def member(self,member):
        self.ui.mainStackedWidget.setCurrentWidget(self.ui.member_page)
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_car)
        self.ui.member_page_user_name.setText(member.getOfficeMemberName())
        self.ui.member_page_car_add_btn.clicked.connect(self.addCarPage)

        self.ui.member_page_models_btn.clicked.connect(self.memberModel)
        self.ui.member_page_manufacturers_btn.clicked.connect(self.memberManufacturer)
        self.ui.member_page_upgrades_btn.clicked.connect(self.memberUpgrade)
        self.ui.member_page_cars_btn.clicked.connect(self.memberCar)
        self.ui.member_page_search_btn.clicked.connect(self.memberSearch)

        self.ui.member_page_car_delete_btn.clicked.connect(self.deleteCar)
        self.ui.member_page_car_update_btn.hide()
        self.ui.member_page_car_more_btn.clicked.connect(self.moreDetails)

        result = self.staffController.viewAvailableCars()
        self.loadCarTable(result)


        self.ui.car_title.setText("AVAILABLE CARS")

        self.ui.member_page_car_available_btn.clicked.connect(self.availableCars)
        self.ui.member_page_car_sold_btn.clicked.connect(self.soldCars)

    def moreDetails(self):
        row = self.ui.member_page_car_table.currentRow()

        if row != -1:
            id = self.ui.member_page_car_table.item(row, 0).text()
            result = self.memberController.moreDetailsForSoldCar(id)
            print(result)
            if result[1] == None:
                self.ui.member_car_error.setText("This is not for Available cars")
            else:
                print("I came here")
                self.ui.member_car_error.clear()
                self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_view_sold_car)
                self.ui.member_page_sold_car_reg.setText(result[1][1])
                self.ui.member_page_sold_car_name.setText(self.ui.member_page_car_table.item(row,1).text())

                initialPrice = int(self.ui.member_page_car_table.item(row,3).text())
                for i in result[0]:
                    initialPrice -= int(i[2])
                self.ui.member_page_sold_car_initial_price.setText(str(initialPrice))
                self.ui.member_page_sold_car_sold_price.setText(self.ui.member_page_car_table.item(row, 3).text())
                self.ui.member_page_sold_by.setText(result[1][2])
                self.ui.member_page_sold_date.setText(result[1][3])
                self.ui.member_page_sold_time.setText(result[1][4])

                self.loadMemberSoldUpgrades(result[0])
        else:
            self.ui.member_car_error.setText("Select a sold car first")

    def memberSearch(self):
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_search)
        self.ui.member_page_search_form_btn.clicked.connect(self.searchCar)

    def searchCar(self):
        key = self.ui.member_page_search_input.text()
        result = self.memberController.searchCarsByModelOrManufacturer(key)
        if result == None:
            print("None")
            self.ui.member_search_error.setText("NOT AVAILABLE")
        else:
            print("CLICKED")
            print(result)
            self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_car)
            self.ui.member_car_error.clear()
            self.ui.member_page_car_more_btn.hide()
            self.loadCarTable(result)
            self.ui.member_page_car_delete_btn.hide()
            self.ui.member_page_car_available_btn.hide()
            self.ui.member_page_car_sold_btn.hide()
            self.ui.member_page_car_add_btn.hide()

            self.ui.car_title.setText("SEARCHED RESULTS")

    def memberCar(self):
        self.ui.car_title.setText("AVAILABLE CARS")
        self.ui.member_page_car_more_btn.show()
        self.ui.member_page_car_delete_btn.show()
        self.ui.member_page_car_available_btn.show()
        self.ui.member_page_car_sold_btn.show()
        self.ui.member_page_car_sold_btn.show()
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_car)
        self.ui.member_page_car_add_btn.clicked.connect(self.addCarPage)

        result = self.staffController.viewAvailableCars()
        self.loadCarTable(result)


    def addCarPage(self):
        print("addCarPage")
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_add_car)
        manufacturers = self.staffController.viewAvailableManufacturers()
        models = self.staffController.viewAvailableModels()
        self.ui.member_page_manufacturer_combo_box.clear()
        self.ui.member_page_model_combo_box.clear()
        for manu in manufacturers:
            self.ui.member_page_manufacturer_combo_box.addItem(str(manu[0])+": "+manu[1])
        for mod in models:
            self.ui.member_page_model_combo_box.addItem(str(mod[0])+": "+mod[1])
        self.ui.member_page_add_car_form_btn.clicked.connect(self.addCar)


    def memberUpgrade(self):
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_upgrade)
        result = self.staffController.viewUpgrades()
        self.loadUpgradeTable(result)

        self.ui.upgrade_page_add_upgrade_btn.clicked.connect(self.addUpgrade)
        self.ui.upgrade_page_delete_upgrade_btn.clicked.connect(self.deleteUpgrade)
        self.ui.upgrade_page_update_upgrade_btn.clicked.connect(self.upgradeUpdate)

        self.ui.member_page_upgrade_table.itemSelectionChanged.connect(self.upgradeItemSelected)

    def memberManufacturer(self):
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_manufacturer)
        result = self.staffController.viewAvailableManufacturers()
        self.loadManufacturerTable(result)


        self.ui.model_page_add_manufacturer_add_btn.clicked.connect(self.addManufacturer)
        self.ui.model_page_delete_manufacturer_btn.clicked.connect(self.manufacturerDelete)
        self.ui.model_page_update_manufacturer_btn.clicked.connect(self.manufacturerUpdate)
        self.ui.mamber_page_manufacturer_table.itemSelectionChanged.connect(self.manufacturerItemSelected)

    def memberModel(self):
        self.ui.mamber_page_model_table.clearSelection()
        self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_model)
        result = self.staffController.viewAvailableModels()
        self.loadModelTable(result)

        self.ui.model_page_add_model_btn.clicked.connect(self.addModel)

        self.ui.model_page_delete_model_btn.clicked.connect(self.modelDelete)
        self.ui.model_page_update_model_btn.clicked.connect(self.modelUpdate)

        self.ui.mamber_page_model_table.itemSelectionChanged.connect(self.modelItemSelected)

    def modelItemSelected(self):
        row = self.ui.mamber_page_model_table.currentRow()
        modelName = self.ui.mamber_page_model_table.item(row, 1)
        if modelName != None:
            self.ui.model_page_add_model_input.setText(modelName.text())

    def manufacturerItemSelected(self):
        row = self.ui.mamber_page_manufacturer_table.currentRow()
        manufacturerName = self.ui.mamber_page_manufacturer_table.item(row, 1)
        if manufacturerName != None:
            self.ui.model_page_add_manufacturer_input.setText(manufacturerName.text())

    def upgradeItemSelected(self):
        row = self.ui.member_page_upgrade_table.currentRow()
        upgradeName = self.ui.member_page_upgrade_table.item(row, 1)
        upgradePrice = self.ui.member_page_upgrade_table.item(row, 2)
        if upgradeName != None:
            self.ui.upgrade_Page_add_upgrade_name_input.setText(upgradeName.text())
            self.ui.upgrade_page_add_upgrade_price_input.setText(upgradePrice.text())


    def loadModelTable(self, result):
        while(self.ui.mamber_page_model_table.rowCount()>0):
            self.ui.mamber_page_model_table.removeRow(0)

        for r, model in enumerate(result):
            self.ui.mamber_page_model_table.insertRow(r)
            for c, data in enumerate(model):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.mamber_page_model_table.setItem(r, c, cell)


    def loadManufacturerTable(self, result):
        while (self.ui.mamber_page_manufacturer_table.rowCount() > 0):
            self.ui.mamber_page_manufacturer_table.removeRow(0)

        for r, model in enumerate(result):
            self.ui.mamber_page_manufacturer_table.insertRow(r)
            for c, data in enumerate(model):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.mamber_page_manufacturer_table.setItem(r, c, cell)

    def loadUpgradeTable(self, result):
        while (self.ui.member_page_upgrade_table.rowCount() > 0):
            self.ui.member_page_upgrade_table.removeRow(0)

        for r, model in enumerate(result):
            self.ui.member_page_upgrade_table.insertRow(r)
            for c, data in enumerate(model):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.member_page_upgrade_table.setItem(r, c, cell)

    def loadCarTable(self, result):
        while (self.ui.member_page_car_table.rowCount() > 0):
            self.ui.member_page_car_table.removeRow(0)

        for r, car in enumerate(result):
            self.ui.member_page_car_table.insertRow(r)

            del(car[4])
            del(car[4])

            for c, data in enumerate(car):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.member_page_car_table.setItem(r, c, cell)

    def loadSellerCarTable(self, result):
        while (self.ui.seller_page_car_table.rowCount() > 0):
            self.ui.seller_page_car_table.removeRow(0)

        for r, car in enumerate(result):
            self.ui.seller_page_car_table.insertRow(r)

            del (car[4])
            del (car[4])

            for c, data in enumerate(car):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_car_table.setItem(r, c, cell)

    def loadSellerModelTable(self, result):
        while (self.ui.seller_page_model_table.rowCount() > 0):
            self.ui.seller_page_model_table.removeRow(0)

        for r, car in enumerate(result):
            self.ui.seller_page_model_table.insertRow(r)
            for c, data in enumerate(car):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_model_table.setItem(r, c, cell)

    def loadSellerManufacturerTable(self, result):
        while (self.ui.seller_page_manufacturer_table.rowCount() > 0):
            self.ui.seller_page_manufacturer_table.removeRow(0)

        for r, car in enumerate(result):
            self.ui.seller_page_manufacturer_table.insertRow(r)
            for c, data in enumerate(car):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_manufacturer_table.setItem(r, c, cell)

    def loadSellerUpgradeTable(self, result):
        while (self.ui.seller_page_upgrade_table.rowCount() > 0):
            self.ui.seller_page_upgrade_table.removeRow(0)

        for r, car in enumerate(result):
            self.ui.seller_page_upgrade_table.insertRow(r)
            for c, data in enumerate(car):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_upgrade_table.setItem(r, c, cell)


    def loadSelecteUpgradesTable(self):
        while (self.ui.seller_page_sell_upgrade_table.rowCount() > 0):
            self.ui.seller_page_sell_upgrade_table.removeRow(0)

        for r, up in enumerate(self.selectedUpgrades):
            self.ui.seller_page_sell_upgrade_table.insertRow(r)
            for c, data in enumerate(up[0]):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_sell_upgrade_table.setItem(r, c, cell)

    def loadSoldUpgradesTable(self):
        while (self.ui.seller_page_sold_upgrade_table.rowCount() > 0):
            self.ui.seller_page_sell_upgrade_table.removeRow(0)

        for r, up in enumerate(self.selectedUpgrades):
            self.ui.seller_page_sold_upgrade_table.insertRow(r)
            for c, data in enumerate(up[0]):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.seller_page_sold_upgrade_table.setItem(r, c, cell)

    def loadMemberSoldUpgrades(self, result):
        while (self.ui.member_page_sold_upgrade.rowCount() > 0):
            self.ui.member_page_sold_upgrade.removeRow(0)

        for r, up in enumerate(result):
            self.ui.member_page_sold_upgrade.insertRow(r)
            for c, data in enumerate(up):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.ui.member_page_sold_upgrade.setItem(r, c, cell)


    def modelUpdate(self):
        row = self.ui.mamber_page_model_table.currentRow()
        modelId = self.ui.mamber_page_model_table.item(row, 0)
        if modelId != None:
            modelId = modelId.text()
            print(modelId)
        name = self.ui.model_page_add_model_input.text()
        self.memberController.updateAModel(modelId, name)
        result = self.staffController.viewAvailableModels()
        self.loadModelTable(result)
        self.ui.model_page_add_model_input.clear()


    def manufacturerUpdate(self):
        row = self.ui.mamber_page_manufacturer_table.currentRow()
        manufacturerID = self.ui.mamber_page_manufacturer_table.item(row, 0)
        if manufacturerID != None:
            manufacturerID = manufacturerID.text()
        name = self.ui.model_page_add_manufacturer_input.text()
        self.memberController.updateAManufacturer(manufacturerID, name)
        result = self.staffController.viewAvailableManufacturers()
        self.loadManufacturerTable(result)
        self.ui.model_page_add_manufacturer_input.clear()


    def upgradeUpdate(self):
        row = self.ui.member_page_upgrade_table.currentRow()
        upgradeID = self.ui.member_page_upgrade_table.item(row, 0)
        if upgradeID != None:
            upgradeID = upgradeID.text()
        name = self.ui.upgrade_Page_add_upgrade_name_input.text()
        price = self.ui.upgrade_page_add_upgrade_price_input.text()

        if self.memberController.updateAnUpgrade(upgradeID, name, price):
            result = self.staffController.viewUpgrades()
            self.loadUpgradeTable(result)

            self.ui.upgrade_page_add_upgrade_price_input.clear()
            self.ui.upgrade_Page_add_upgrade_name_input.clear()
            self.ui.upgrade_price_error.setText('')
        else:
            self.ui.upgrade_price_error.setText("Price must be given in numbers only")




    def modelDelete(self):
        row = self.ui.mamber_page_model_table.currentRow()
        modelId = self.ui.mamber_page_model_table.item(row, 0)
        if modelId != None:
            modelId = modelId.text()
            print(modelId)
        s = self.memberController.removeAModel(modelId)
        print(s)
        if s:
            print("DELETEED")
            self.ui.model_error.clear()
            result = self.staffController.viewAvailableModels()
            self.loadModelTable(result)
        else:
            self.ui.model_error.setText("An undeleted car available with this model")


    def manufacturerDelete(self):
        row = self.ui.mamber_page_manufacturer_table.currentRow()
        manufacturerID = self.ui.mamber_page_manufacturer_table.item(row, 0)
        if manufacturerID != None:
            manufacturerID = manufacturerID.text()
        if self.memberController.removeAManufacturer(manufacturerID):
            self.ui.manufacturer_error.clear()
            result = self.staffController.viewAvailableManufacturers()
            self.loadManufacturerTable(result)
        else:
            self.ui.manufacturer_error.setText("An undeleted car available with this manufacturer")


    def deleteUpgrade(self):
        row = self.ui.member_page_upgrade_table.currentRow()
        upgradeID = self.ui.member_page_upgrade_table.item(row, 0)
        if upgradeID != None:
            upgradeID = upgradeID.text()

        self.memberController.deleteAnUpgrade(upgradeID)
        result = self.staffController.viewUpgrades()
        self.loadUpgradeTable(result)

    def deleteCar(self):
        print("delete car")
        row = self.ui.member_page_car_table.currentRow()
        carID = self.ui.member_page_car_table.item(row, 0)

        if carID != None:
            carID = carID.text()
            print("car ID", carID)
        self.memberController.removeACar(carID)
        self.memberCar()


    def addModel(self):
        text = self.ui.model_page_add_model_input.text().lower()
        if text.strip() != '':
            model = Model(text)
            self.memberController.addAModel(model)
            self.ui.model_page_add_model_input.clear()

        self.memberModel()


    def addManufacturer(self):
        print("Hello")
        text = self.ui.model_page_add_manufacturer_input.text().lower()
        if text.strip() != '':
            manufacturer = Manufacturer(text)
            self.memberController.addAManufacturer(manufacturer)
            self.ui.model_page_add_manufacturer_input.clear()

        self.memberManufacturer()

    def addUpgrade(self):
        name = self.ui.upgrade_Page_add_upgrade_name_input.text().lower()
        if name.strip() != '':
            price = self.ui.upgrade_page_add_upgrade_price_input.text()
            if self.memberController.addAnUpgrade(name.lower(), price):
                self.ui.upgrade_page_add_upgrade_price_input.clear()
                self.ui.upgrade_Page_add_upgrade_name_input.clear()
                self.ui.upgrade_price_error.setText('')
                self.memberUpgrade()
            else:
                self.ui.upgrade_price_error.setText("Price should be given in numbers")


    def addCar(self):
        regNo = self.ui.member_page_car_register_input.text().lower()
        if regNo.strip() != '':
            manufacturer = self.ui.member_page_manufacturer_combo_box.currentText().split(':')
            model = self.ui.member_page_model_combo_box.currentText().split(':')
            carName = self.ui.member_page_car_name_input.text().lower()
            numDoors = self.ui.member_page_num_doors_combo_box.currentText()
            price = self.ui.member_page_initial_price_input.text()
            color = self.ui.member_page_car_color_input.text()

            if carName.strip() == '':
                self.ui.car_name_error.setText("This field can not be empty")
            elif color.strip() == '':
                self.ui.car_color_error.setText("This field can not be empty")
            elif price.strip() == '':
                self.ui.car_price_error.setText("This field can not be empty")
            elif not price.isnumeric():
                self.ui.car_price_error.setText("This field must be in numbers")
            else:
                car = Car(regNo, carName, color, int(price), int(numDoors), int(model[0]), int(manufacturer[0]))
                print("addCR")
                print(self.email)
                if self.memberController.addACar(car, self.email):
                    self.ui.car_id_error.clear()

                    self.ui.member_page_car_register_input.clear()
                    self.ui.member_page_sold_car_initial_price.clear()
                    self.ui.member_page_car_color_input.clear()

                    self.ui.member_page_car_name_input.clear()
                    self.ui.member_page_initial_price_input.clear()

                    self.ui.member_page_sold_car_name.clear()

                    self.ui.memberStackedWidget.setCurrentWidget(self.ui.member_page_car)

                    result = self.memberController.viewAvailableCars()
                    self.loadCarTable(result)
                else:
                    self.ui.car_id_error.setText("Sorry this ID is already added")
        else:
            self.ui.car_id_error.setText("Registration number can not be empty")



    def availableCars(self):
        self.ui.car_title.setText("AVAILABLE CARS")
        result = self.memberController.viewAvailableCars()
        self.loadCarTable(result)


    def soldCars(self):
        self.ui.car_title.setText("SOLD CARS")
        result = self.memberController.viewSoldCars()
        self.loadCarTable(result)

    def errorBox(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)

        x = msg.exec_()



    def validateRegistration(self, email, name, password, passwordConfirm):
        if len(password) < 8:
            self.ui.registration_error.setText("Use 8 characters or more for your password")
            return False
        elif password != passwordConfirm:
            self.ui.registration_error.setText("Those passwords didn't match try again")
            return False
        elif len(name.strip())==0:
            self.ui.registration_error.setText("Name field can not be null")
            return False
        elif len(email.strip()) == 0:
            self.ui.registration_error.setText("Email field can not be null")
            return False
        else:
            return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Window()
    main_win.show()

    sys.exit(app.exec_())
