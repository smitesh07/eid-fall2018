# Python code to demonstrate SQL to fetch data. 
  
# importing the module 
import sqlite3 
  
# connect withe the myTable database 
connection = sqlite3.connect("localdht.db") 
  
# cursor object 
crsr = connection.cursor() 
  
# execute the command to fetch all the data from the table emp 
crsr.execute("SELECT * FROM dht_data")  
  
# store all the fetched data in the ans variable 
ans= crsr.fetchall()  

# loop to print all the data 
for i in ans: 
    print(i)


print()
print()

crsr.execute("SELECT * FROM dht_data ORDER BY Timestamp DESC LIMIT 1")
ans = crsr.fetchone()

Time,Temp,Unit,AvgTemp,HighTemp,LowTemp,Hum,AvgHum,HighHum,LowHum = ans

print(Unit)

connection.close()