import sys
import Adafruit_DHT
import time
from PyQt5.QtWidgets import QWidget,QDialog,QApplication,QMessageBox,QInputDialog,QLineEdit
from PyQt5.QtCore import QTimer,QTime,QThread,QEventLoop
from Project1 import Ui_Form
import matplotlib.pyplot as plt

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        global threshold,deg,fah,temp_count,hum_count,temp_avg,hum_avg
        global temp_samples,hum_samples
        temp_samples=[]
        hum_samples=[]
        deg = 1           #default unit
        fah = 0
        threshold = 35    #default threshold
        temp_count=0
        hum_count=0
        temp_avg=0
        hum_avg=0
        self.show()
        self.check()

##      Functionality for Widgets
        self.threshold = QLineEdit()
        self.ui.get_hum.clicked.connect(self.getHum)
        self.ui.get_temp.clicked.connect(self.getTemp)
        self.ui.TempAndHumidity.clicked.connect(self.getTempHum)
        self.ui.threshold_button.clicked.connect(self.setThreshold)
        self.ui.degree_button.clicked.connect(self.degTemp)
        self.ui.fahrenheit_button.clicked.connect(self.fahTemp)
        self.ui.refresh.clicked.connect(self.startTimer)
        self.ui.stop_refresh.clicked.connect(self.stopTimer)
        self.ui.plotGraph.clicked.connect(self.plotGraphs)
        self.ui.exit.clicked.connect(self.close)

#   Timer function to start the timer
    def startTimer(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.getTempHum)
        self.timer.start(1000)
        self.ui.refresh_checkBox.setChecked(True)
        
#   Timer function to stop the timer
    def stopTimer(self):
        self.timer.stop()
        self.ui.refresh_checkBox.setChecked(False)
  
#   Function to check if sensor is connected or not
    def check(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

        if humidity is None or temperature is None:
            alert=QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
            self.ui.hum.display("")
        else:
            pass
        
#   Function to get temperature values in degree celsius and degree fahrenheit
#   Also populates the temperature samples list and calculates incremental average
    def getTemp(self):
        global threshold,deg,fah,temp_count,temp_avg
        global temp_samples,temp_count
        self.check()
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.temp_TOR.display(time)
        
        if humidity is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
        else:
            
            if deg == 1:
                temp = '{0:.2f}'.format(temperature)
                self.ui.temp.display(temp)
                temp_samples.append(temperature)
                deg = 0
                temp_count += 1
                temp_avg=temp_avg+(temperature-temp_avg)/temp_count
                temp_avg_display = '{0:.2f}'.format(temp_avg)
                self.ui.tempAvg.display(temp_avg_display)
            elif fah == 1:
                temperature = temperature*1.8 + 32
                temp = '{0:.2f}'.format(temperature)
                self.ui.temp.display(temp)
                fah = 0 
            else:
                temp = '{0:.2f}'.format(temperature)
                self.ui.temp.display(temp)
            
            #Check for high temperautre
            if threshold is None:
                pass
            elif temperature > threshold:
                alert=QMessageBox()
                alert.setIcon(QMessageBox.Warning)
                alert.setText("High Temperature!!!!!")
                alert.exec_()

#   Function to get %Humidity values
#   Also populates the Humidity samples list and calculates incremental average
    def getHum(self):
        global hum_samples,hum_count,hum_avg
        self.check()
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.hum_TOR.display(time)
        
        if humidity is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.hum.display("")
        else:
            hum = '{0:.2f}'.format(humidity)
            self.ui.hum.display(hum)
            hum_samples.append(humidity)
            hum_count +=1
            hum_avg=hum_avg+(humidity-hum_avg)/hum_count
            hum_avg_display = '{0:.2f}'.format(hum_avg)
            self.ui.humAvg.display(hum_avg_display)

#   Function to get temperature values in degree celsius and degree fahrenheit, and %Humidity values 
#   Also populates the temperature,humidity samples list and calculates incremental average
    def getTempHum(self):
        global threshold,temp_count,temp_avg,hum_count,hum_avg
        global hum_samples, temp_samples
        self.check()
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.temp_TOR.display(time)
        self.ui.hum_TOR.display(time)
        
        if humidity is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
            self.ui.hum.display("")
        else:
            hum = '{0:.2f}'.format(humidity)
            self.ui.hum.display(hum)
            hum_samples.append(humidity)
            temp = '{0:.2f}'.format(temperature)
            self.ui.temp.display(temp)
            temp_samples.append(temperature)
            temp_count += 1
            hum_count +=1
            temp_avg=temp_avg+(temperature-temp_avg)/temp_count
            hum_avg=hum_avg+(humidity-hum_avg)/hum_count
            hum_avg_display = '{0:.2f}'.format(hum_avg)
            self.ui.humAvg.display(hum_avg_display)
            temp_avg_display = '{0:.2f}'.format(temp_avg)
            self.ui.tempAvg.display(temp_avg_display)
            
            #Check for high temperautre
            if threshold is None:
                pass
            elif temperature > threshold:
                alert=QMessageBox()
                alert.setIcon(QMessageBox.Warning)
                alert.setText("High Temperature!!!!!")
                alert.exec_()

#   Function to set threshold based on user input
    def setThreshold(self):
        global threshold
        input, ok = QInputDialog.getInt(self, 'integer Input Dialog', 'Enter Threshold:')
        if ok:
            self.threshold.setText(str(input))
            threshold = input

#   Function to enable degree celsius mode
    def degTemp(self):
        global deg
        deg = 1
        self.getTemp()

#   Function to enable degree Fahrenheit mode
    def fahTemp(self):
        global fah
        fah = 1
        self.getTemp()

#   Function to plot graphs
    def plotGraphs(self):
        global temp_count,hum_count,temp_samples,hum_samples
        x_temp = [(i+1) for i in range(temp_count)]
        x_hum = [(i+1) for i in range(hum_count)]
        plt.subplot(211)
        plt.plot(x_temp, temp_samples)
        plt.xlabel('Sample Number')
        plt.ylabel('Degree Celcius')
        plt.title('Temperature Graph')
        plt.subplot(212)
        plt.plot(x_hum, hum_samples)
        plt.xlabel('Sample Number')
        plt.ylabel('% Humidity')
        plt.title('Humidity Graph')
        plt.subplots_adjust(left=0.2, bottom=None, right=None, top=None, wspace=None, hspace=1.0)
        plt.legend()
        plt.show()

#Function for exit
    def close(self):
        sys.exit(app.exec_())

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
