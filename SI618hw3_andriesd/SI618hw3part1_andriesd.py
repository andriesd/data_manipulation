import sqlite3 as sqlite
import sys
import csv

file_input = open('vehicles.csv', 'rU')
csvfile = csv.reader(file_input)

cars = []
for line in csvfile:
    lst = []
    if line[22] == '' or line[22] == 'NA':
        continue
    elif line[23] == 'NA' or line[23] == '' or line[23] == '0':
        continue
    else:
        lst.append((line[63], line[46], line[47], line[62], line[22], line[23], line[57], line[4], line[34], line[15]))
        tup = lst[0]
        # print tup
        cars.append(tup)

del cars[0]
print len(cars)


con = None

try:
    con = sqlite.connect('vehicles.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Vehicles")
    cur.execute("CREATE TABLE Vehicles(Year TEXT, Make TEXT, Model TEXT, "
                "VClass TEXT, Cylinders INT, Displ FLOAT, Trany TEXT, City08 INT, Highway08 INT, Comb08 INT)")
    cur.executemany("INSERT INTO Vehicles VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cars)
    con.commit()

except sqlite.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    if con:
        con.close()