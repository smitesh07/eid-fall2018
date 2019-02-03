#Created by - Preshit Harlikar
#Date - 10/21/2018

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from SensorUI import Ui_SensorInterface
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #Import from AWS-IoT Library
import matplotlib.pyplot as plt
import Adafruit_DHT
import sqlite3
import time
import json

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        #integrating the UI
        self.ui = Ui_SensorInterface()      
        self.ui.setupUi(self)
        
        #MQTT setup
        self.mqttSetup()
        
        #global variables
        global unit, count, tempAvg, humAvg, samples, tempArr, humArr, timerflag, tempLimit, humLimit, tempHigh, tempLow, humHigh, humLow, temp, connection, crsr
        unit = 1
        count,tempAvg,humAvg,samples,timerflag,tempHigh,humHigh = 0,0,0,0,0,0,0
        tempLow, humLow = 500, 500
        tempArr = [None]*10  
        humArr = [None]*10 
        tempLimit = 100
        humLimit = 100
        
        #initialize database
        connection = sqlite3.connect("localdht.db")
        crsr = connection.cursor()
        
        #initializing timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.getTempHum)

        self.ui.refreshButton.clicked.connect(self.getTempHum)
        self.ui.celciusButton.clicked.connect(self.celciusTemp)
        self.ui.fahrenheitButton.clicked.connect(self.fahrenheitTemp)
        self.ui.timerButton.clicked.connect(self.timerStartStop)
        self.ui.resetButton.clicked.connect(self.resetAvg)
        self.ui.graphButton.clicked.connect(self.graphTempHum)
        self.ui.tempDial.valueChanged.connect(self.setTempLimit)
        self.ui.humDial.valueChanged.connect(self.setHumLimit)
        self.ui.cleardatabaseButton.clicked.connect(self.clearDB)
        
        #function to setup MQTT using REST API and private and root keys
    def mqttSetup(self):
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient("RaspberryPi")
        self.myAWSIoTMQTTClient.configureEndpoint("a1mtqpdqvd0l8h-ats.iot.us-east-1.amazonaws.com", 8883)
        self.myAWSIoTMQTTClient.configureCredentials("root-CA.crt", "pi-private.pem.key", "pi-certificate.pem.crt")
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        
        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()
        self.myAWSIoTMQTTClient.subscribe("DHT22", 1, None)
        
        #function to get temp and humidity from the sensor
    def getTempHum(self):
        global unit, count, tempAvg, humAvg, tempHigh, tempLow, humHigh, humLow, tempArr, humArr, samples, tempLimit, humLimit, temp, connection, crsr, timerflag
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        
        global temp3, temp4, hum3, hum4
        #create table
        crsr.execute("CREATE TABLE IF NOT EXISTS DHT_DATA(Timestamp TEXT,Temperature numeric(3,1),Unit TEXT,Average_Temperature numeric(3,1),High_Temperature numeric(3,1),Low_Temperature numeric(3,1),Humidity numeric(3,1),Average_Humidity numeric(3,1),High_Humidity numeric(3,1),Low_Humidity numeric(3,1))")

        #check if sensor is disconnected
        if humidity is None and temperature is None:
            self.ui.alertDisplay.setText(" SENSOR DISCONNECTED")
            self.ui.temperatureDisplay.display("")
            self.ui.humidityDisplay.display("")
            self.ui.temperatureAvgDisplay.display("")
            self.ui.humidityAvgDisplay.display("")
            self.ui.sensorStatus.setStyleSheet("background-color: rgb(255, 0, 0);")

            #update the time of request for tem and humidity values            
            newtime = time.strftime('%m-%d-%y  %H:%M:%S')
            self.ui.timeDisplay.setText(newtime)
            
            temp1,tempUnit,temp2,temp3,temp4,hum1,hum2,hum3,hum4time = 0,0,0,0,0,0,0,0,0
            #update database
            crsr.execute("INSERT INTO dht_data values(?,?,?,?,?,?,?,?,?,?)",(newtime,temp1,tempUnit,temp2,temp3,temp4,hum1,hum2,hum3,hum4))
            connection.commit()

        else:
            self.ui.sensorStatus.setStyleSheet("background-color: rgb(0, 255, 0);")
            count = count + 1
            tempA = '{0:.2f}'.format(temperature)            
            tempUnit = "°C"
            #conversion from cecius to fahrenheit
            if unit == 0:
                temperature = (temperature*1.8) + 32
                tempUnit = "°F"
            
            #display current temp and humidity value on LCD Display
            temp1 = '{0:.2f}'.format(temperature)
            self.ui.temperatureDisplay.display(temp1)
            hum1 = '{0:.2f}'.format(humidity)
            self.ui.humidityDisplay.display(hum1)
            
            
            #Set an alert for high temperautre
            if temperature > tempLimit:
                self.ui.alertDisplay.setText("    HIGH TEMPERATURE")
            elif humidity > humLimit:
                self.ui.alertDisplay.setText("        HIGH HUMIDITY")
            else:
                self.ui.alertDisplay.setText("")
                
            #calculating average temperature and humidity continuously for each sample    
            tempAvg=((tempAvg * (count-1)) + temperature) / count
            temp2 = '{0:.2f}'.format(tempAvg)
            self.ui.temperatureAvgDisplay.display(temp2)
            humAvg=((humAvg * (count-1)) + humidity) / count
            hum2 = '{0:.2f}'.format(humAvg)
            self.ui.humidityAvgDisplay.display(hum2)
            
            if temperature > tempHigh:
                tempHigh = temperature
                temp3 = '{0:.2f}'.format(tempHigh)
                self.ui.temperatureHighDisplay.display(temp3)
            
            if temperature < tempLow:
                tempLow = temperature
                temp4 = '{0:.2f}'.format(tempLow)
                self.ui.temperatureLowDisplay.display(temp4)
                
            if humidity > humHigh:
                humHigh = humidity
                hum3 = '{0:.2f}'.format(humHigh)
                self.ui.humidityHighDisplay.display(hum3)
            
            if humidity < humLow:
                humLow = humidity
                hum4 = '{0:.2f}'.format(humLow)
                self.ui.humidityLowDisplay.display(hum4)

            #update the time of request for tem and humidity values            
            newtime = time.strftime('%m-%d-%y  %H:%M:%S')
            self.ui.timeDisplay.setText(newtime)
                
            #update database
            crsr.execute("INSERT INTO dht_data values(?,?,?,?,?,?,?,?,?,?)",(newtime,temp1,tempUnit,temp2,temp3,temp4,hum1,hum2,hum3,hum4))
            connection.commit()
            
            #publish data to AWS IOT
            if timerflag == 1:
                payload ='"timestamp": "{}", "temperature": "{}", "humidity": "{}"'.format(newtime,tempA,hum1)
                payload = '{' +payload+ '}'
                self.myAWSIoTMQTTClient.publish("DHT22",(payload),1)


        #function to create a graph of last 10 temperature values
    def graphTempHum(self):
        global tempArr, humArr
        y = [1,2,3,4,5,6,7,8,9,10]
        
        plt.subplot(2,1,1)
        plt.title('Temperature and Humidity Plot of last 10 Readings')
        plt.plot(y, tempArr, label='Temperature')
        plt.ylabel('Degree Celcius')
        plt.legend()
                
        plt.subplot(2,1,2)        
        plt.plot(y, humArr, label='Humidity')
        plt.xlabel('Sample Number')
        plt.ylabel('Percent Humidity')
        plt.legend()
        plt.savefig('graph.jpg')
        plt.show()
        
        #function to switch from fahrenheit to celcius
    def celciusTemp(self):
        global unit, temp, tempAvg, tempHigh, tempLow, tempLimit
        if unit == 0:
            unit = 1
            tempAvg = (tempAvg-32) * 0.5556
            tempHigh = (tempHigh-32) * 0.5556
            temp = '{0:.2f}'.format(tempHigh)
            self.ui.temperatureHighDisplay.display(temp)
            tempLow = (tempLow-32) * 0.5556
            temp = '{0:.2f}'.format(tempLow)
            self.ui.temperatureLowDisplay.display(temp)
            tempLimit = (tempLimit-32) * 0.5556
            self.ui.tempThresholdDisplay.display(tempLimit);            
        self.getTempHum()

        #function to switch from celcius to fahrenheit
    def fahrenheitTemp(self):
        global unit, temp, tempAvg, tempHigh, tempLow, tempLimit
        if unit == 1:
            unit = 0
            tempAvg = (tempAvg*1.8) + 32
            tempHigh = (tempHigh*1.8) + 32
            temp = '{0:.2f}'.format(tempHigh)
            self.ui.temperatureHighDisplay.display(temp)            
            tempLow = (tempLow*1.8) + 32
            temp = '{0:.2f}'.format(tempLow)
            self.ui.temperatureLowDisplay.display(temp)
            tempLimit = (tempLimit*1.8) + 32
            self.ui.tempThresholdDisplay.display(tempLimit);
        self.getTempHum()      

        #function to start and stop the timer to continuously update values
    def timerStartStop(self):
        global timerflag
        if timerflag == 0:
            self.ui.timerStatus.setStyleSheet("background-color: rgb(0, 255, 0);");        
            self.timer.start()
            timerflag = 1
        elif timerflag == 1:
            self.ui.timerStatus.setStyleSheet("background-color: rgb(255, 0, 0);");
            self.timer.stop()
            timerflag = 0
            
        #function to set the high temperature threshold using dial
    def setTempLimit(self,value):
        global tempLimit, unit
        tempLimit = value
        if unit == 0:
            tempLimit = (tempLimit*1.8) + 32
        self.ui.tempThresholdDisplay.display(tempLimit);
        
        #function to set the high humidity threshold using dial
    def setHumLimit(self,value):
        global humLimit
        humLimit = value
        self.ui.humThresholdDisplay.display(humLimit);
        
        #function called when reset button is pressed to reset avg values
    def resetAvg(self):
        global tempAvg, tempHum, count
        tempAvg, tempHum, count = 0, 0, 0
        self.ui.temperatureAvgDisplay.display("")
        self.ui.humidityAvgDisplay.display("")
        
        #function to clear the local database
    def clearDB(self):
        global connection, crsr
        crsr.execute("DROP TABLE IF EXISTS dht_data")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())


