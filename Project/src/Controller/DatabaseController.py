import sqlite3

conn = sqlite3.connect('../../database/database.db')
cur = conn.cursor()

#-----------------------------------------------------------------------------------
def insertModel(model):
    cur.execute("insert into model(name) values(?)",(model.getModelName(),))
    conn.commit()

def selectAllModels():
    cur.execute('select * from model')
    rows = cur.fetchall()
    return rows

def removeModel(modelID):
    conn.execute("PRAGMA foreign_keys = ON")
    cur.execute("delete from model where id=?",(modelID,))
    conn.commit()
def updateModel(modelID, name):
    try:
        cur.execute("update model set name=? where id=?",(name, modelID))
        conn.commit()
    except Exception as e:
        print(e)

def updateManufacturer(manufacturerID, name):
    try:
        cur.execute("update manufacturer set name=? where id=?", (name, manufacturerID))
        conn.commit()
    except Exception as e:
        print(e)
#------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
def insertManufacturer(manufacturer):
    cur.execute("insert into manufacturer(name) values(?)", (manufacturer.getManufacturerName(),))
    conn.commit()

def selectAllManufacturers():
    cur.execute('select * from manufacturer')
    rows = cur.fetchall()
    return rows

def removeManufacturer(manufacturerID):
    conn.execute("PRAGMA foreign_keys = ON")
    cur.execute("delete from manufacturer where id = ?", (manufacturerID,))
    conn.commit()

#-------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------
def insertCar(car,email):
    query = "insert into car values(?,?,?,?,?,?,?,?,?)"
    values=(car.getRegistrationNumber(), car.getCarName(),car.getColor(), car.getPrice(), car.getNumberOfDoors(), car.getStatus(),
            car.getCarModel(), car.getCarManufacturer(),email)

    cur.execute(query,values)
    conn.commit()

def selectAllCars():
    cur.execute('select * from car')
    rows = cur.fetchall()
    result = []

    #This for loop might make you confuse
    """
        All i am doing inside the for loop is,
            in the car table we only have the foriegn keys for the model and the manufacturer
            but for the end users, it is better if we can show them the names instead of just numbers
            what i am doing inside the for loop is that taking the ids and executing some other queries to take the names for those ids
            and finally I am assigning those names to the list and return it to the end user
        
    """
    for row in rows:
        out = list(row)

        cur.execute('select name from model where id=?', (row[-3],))
        modelName = cur.fetchone()
        cur.execute('select name from manufacturer where id=?', (row[-2],))
        manufacturerName=cur.fetchone()

        out[-3] = modelName[0]
        out[-2] = manufacturerName[0]
        result.append(out)

    return result

def removeCar(registration_number):
    try:
        cur.execute("delete from car where registration_number=?",(registration_number,))
        conn.commit()
        cur.execute("delete from orders where carID = ?",(registration_number,))
        conn.commit()
        cur.execute("delete from sells where carID = ?",(registration_number,))
        conn.commit()
    except Exception as e:
        print(e)

def sellCar(regNumber, upgrades, price,email, date, time):
    cur.execute("update car set status=1, price=? where registration_number=?",(price,regNumber))
    conn.commit()
    for u in upgrades:
        cur.execute("insert into orders(carID, upgradeID) values(?,?)",(regNumber, u))
        conn.commit()
    cur.execute("insert into sells(carID, seller, date, time) values(?,?,?,?)",(regNumber,email,date,time))
    conn.commit()

def selectSoldCar(regNumber):
    cur.execute('select * from orders where carID=?',(regNumber,))
    inter = cur.fetchall()
    order = []

    for o in inter:
        cur.execute('select * from upgrade where id=?',(o[2],))
        order.append(cur.fetchone())

    cur.execute('select * from sells where carID=?',(regNumber,))
    sells = cur.fetchone()

    out = [order, sells]
    return out
#--------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------
def selectAllUpgrades():
    cur.execute("select * from upgrade")
    rows = cur.fetchall()
    return rows

def insertUpgrade(name, price):
        cur.execute("insert into upgrade(name, price) values(?, ?)",(name, price))
        conn.commit()

def removeUpgrade(upgradeID):
    cur.execute("delete from upgrade where id=?",(upgradeID,))

def updateUpgrade(upgradeID, name, price):
    try:
        cur.execute("update upgrade set name=?,price=? where id=?", (name,price,upgradeID))
        conn.commit()
    except Exception as e:
        print(e)
#--------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------
def selectMember(email, password):
    cur.execute("select * from staff_member where email=? and password=?",(email, password))
    return cur.fetchone()

def selectSeller(email, password):
    cur.execute("select * from seller where email=? and password=?",(email, password))
    return cur.fetchone()
#---------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------

def registerMember(email, password, name):
    cur.execute("insert into staff_member values(?,?,?)",(email, password, name))
    conn.commit()


def registerSeller(email, password, name):
    cur.execute("insert into seller values(?,?,?)",(email, password, name))
    conn.commit()


#---------------------------------------------------------------------------------------
def searchCar(key):
    cur.execute("select id from model where name=?",(key,) )
    id = cur.fetchone()
    if id == None:
        cur.execute("select id from manufacturer where name=?",(key,))
        id = cur.fetchone()
    if id != None:
        cur.execute("select * from car where model = ? and status = 0 or manufacturer = ? and status = 0",(id[0], id[0]))
        result = []
        rows = cur.fetchall()

        for row in rows:
            out = list(row)

            cur.execute('select name from model where id=?', (row[-3],))
            modelName = cur.fetchone()
            cur.execute('select name from manufacturer where id=?', (row[-2],))
            manufacturerName = cur.fetchone()

            out[-3] = modelName[0]
            out[-2] = manufacturerName[0]
            result.append(out)

        if len(result) == 0:
            return None
        else:
            return result
    else:
        return None